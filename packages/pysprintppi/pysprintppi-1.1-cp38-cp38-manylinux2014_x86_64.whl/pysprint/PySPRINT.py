#!/usr/bin/env python3
"""
Copyright (c) 2020, Francois Charih
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from typing import List, Optional, Tuple, Union

import numpy as np
from Bio import SeqIO
from mpi4py import MPI
import pysprint

from .prediction_matrix import PredictionMatrix

class PySPRINT(object):
    """Python wrapper for the rSPRINT protein-protein interaction predictor.

    This class wraps rSPRINT, which is a Rust-based implementation of SPRINT,
    which is described in:

    [1] Y. Li, L. Ilie, SPRINT: Ultrafast protein-protein interaction prediction
    of the entire human interactome, BMC Bioinformatics 18 (2017) 485.
    """

    def __init__(self,
        sequences_file: str,
        hsp_file: str,
        training_pairs_file: str,
        min_hsp_length: int = 20,
        smer_sim_threshold: int = 15,
        hsp_threshold: int = 35,
        count_threshold: int = 40,
        preprocess_hsps: bool = False,
        verbose: bool = False
    ) -> "rSPRINT":
        """Instantiates the rSPRINT object.

        Parameters
        ----------
        sequences_file
        Path to the file containing all the sequences (in FASTA format) that
        are used to extract High-Scoring Segment Pairs (HSPs).

        hsp_file
        File containing the HSPs; one per line in the following format:
        <protein 1> <protein 2> <position 1> <position 2> <length>. If the
        file does not exist, PySPRINT will create it and save it to the
        path specified.

        min_hsp_length
        Minimum length of an HSP in amino acids (default: 20).

        smer_sim_threshold
        Minimum score that anchors extracted with the seeds must achieve
        in the "care" positions in order to investigate the sites of the
        s-mers a potential HSPs (default: 15).

        hsp_threshold
        Minimum score that must be achieved for a region to be considered
        a HSP, as assessed with the PAM120 matrix (default: 35). 

        count_threshold
        Maximum number of occurences of a specific amino acid in a given
        protein in HSPs above which this position is discarded from HSPs due
        to the fact that the regions that encompass it are likely to be
        highly non-specific (default: 40).

        preprocess_hsps
        Whether the HSPs extracted should be processed or unprocessed to account
        for frequency of residues within HSPs, as this can be done later
        (default: False).

        verbose
        Whether the HSP extraction and/or PPI scoring should log information
        to the console.

        Raises
        -------
        FileNotFoundException
        Raised if the file containing the sequences or HSPs is not found.
        """
        # MPI stuff
        self.comm = MPI.COMM_WORLD
        self.process_rank = self.comm.Get_rank()
        self.world_size = self.comm.Get_size()

        # Training stuff
        self.sequences = [(protein.id, str(protein.seq)) for protein in list(SeqIO.parse(sequences_file, "fasta"))]
        self.index_to_id_map = { index: protein[0] for index, protein in enumerate(self.sequences) }
        self.id_to_index_map = { protein[0]: index for index, protein in enumerate(self.sequences) }

        # Scoring stuff
        self.peptide_hsps = []
        self.training_pairs = self._load_training_pairs(training_pairs_file)

        # Extraction settings
        self.min_hsp_length = min_hsp_length
        self.smer_sim_threshold = smer_sim_threshold
        self.hsp_threshold = hsp_threshold
        self.preprocess_hsps = preprocess_hsps
        self.count_threshold = count_threshold
        self.verbose = verbose

        # Load the HSPs
        try:
            self._load_hsps(hsp_file)
        except FileNotFoundError:
            print(f"File {hsp_file} not found, extracting the HSPs from scratch.")
            self.hsps = self.extract_hsps(hsp_file)


    def _load_hsps(self, filename: str):
        """Loads the HSPs into the PySPRINT object.

        Parameters
        ----------
        output_file
        File where the HSPs are located.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError

        print(f"Loading HSPs from: {filename}...")
        hsps = []
        for line in open(filename).read().splitlines():
            split = line.split()
            protein1, protein2 = split[0:2] # TODO, check that they are in the sequences
            start1, start2, length = [int(x) for x in split[2:]]
            hsps.append((
                self.id_to_index_map[protein1],
                self.id_to_index_map[protein2],
                start1,
                start2,
                length
            ))
        self.hsps = hsps

    def _load_training_pairs(self, training_pairs_file: str):
        """Returns the training pairs used to score interactions.

        Parameters
        ----------
        output_file
        File where the HSPs are located.

        Raises
        -------
        FileNotFoundError
        Raised if the file with the training pairs specified is
        not found.
        """
        pairs = []
        for pair in open(training_pairs_file).read().splitlines():
            pairs.append(tuple(pair.split()))
        return pairs

    def extract_hsps(self, output_file: str) -> List[Tuple[int, int, int, int, int]]:
        """Using the sequences provided to the rSPRINT object, this
        method extracts all the high-scoring segment pairs (HSPs) using
        the parameters provided to the object.

        Parameters
        ----------
        output_file
        File where the HSPs are to be saved.

        Returns
        -------
        A list of HSPs as tuples of the form
        List[(protein1_index, protein2_index, position1, position2, length)].
        """
        hsps = pysprint.extraction.extract_all_hsps(
            self.sequences,
            [], # no peptides
            output_file,
            self.min_hsp_length,
            self.smer_sim_threshold,
            self.hsp_threshold,
            self.process_rank,
            self.world_size,
            self.verbose
        )
        return hsps

    def score_proteins(self) -> PredictionMatrix:
        """Generates the comprehensive prediction matrix for all sequences
        in the PySPRINT set of sequences.

        Returns
        ---------
        PredictionMatrix
        An object representing the prediction matrix.
        """
        matrix = pysprint.prediction.score_all_interactions(
            self.sequences,
            [], # no peptides
            self.hsps,
            self.training_pairs,
            self.min_hsp_length,
            self.process_rank,
            self.world_size,
            self.verbose
        )
        return PredictionMatrix(np.array(matrix, dtype="float32"), self.id_to_index_map)

    def extract_peptide_hsps(
        self,
        peptides: List[Tuple]
    ) -> List[Tuple]:
        """Extracts and returns the HSPs ONLY FOR THE PEPTIDES with the sequences
        in the object's attribute `self.sequences`.

        Returns
        ---------
        List[Tuple[int, int, int, int, int]]
        A list of HSPs in the form of tuples of the form
        List[(protein1_index, protein2_index, position1, position2, length)].
        """
        peptide_hsps = pysprint.extraction.extract_all_hsps(
            self.sequences,
            peptides,
            None, # not saved in peptide scoring mode
            self.min_hsp_length,
            self.smer_sim_threshold,
            self.hsp_threshold,
            self.process_rank,
            self.world_size,
            self.verbose
        )
        return peptide_hsps

    def score_peptides(
        self,
        peptides: List[Tuple],
        peptide_hsps: List[Tuple]
    ) -> PredictionMatrix:
        """Generates the prediction matrix including the peptides and
        the proteins in `self.sequences`.

        Returns
        ---------
        PredictionMatrix
        An object representing the peptide prediction matrix.
        """
        matrix = pysprint.prediction.score_all_interactions(
            self.sequences,
            peptides,
            self.hsps + peptide_hsps,
            self.training_pairs,
            self.min_hsp_length,
            self.process_rank,
            self.world_size,
            self.verbose
        )

        peptide_indices = {x[0]: i + len(self.sequences) for i, x in enumerate(peptides) }
        new_map = {**self.id_to_index_map.copy(), **peptide_indices}

        return PredictionMatrix(np.array(matrix, dtype="float32"), new_map)

    def get_name_to_index_map(self) -> dict:
        """Returns the conversion map from protein/peptide name to an index
        for use in a PredictionMatrix object.

        Returns
        -------
        Dict[str, int]
        A dictionary mapping the protein name to an index.
        """
        return self.id_to_index_map.copy()
