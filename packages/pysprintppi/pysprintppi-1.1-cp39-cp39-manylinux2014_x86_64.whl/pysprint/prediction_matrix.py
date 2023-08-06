#!/usr/bin/env python3
"""
Copyright (c) 2020, Francois Charih
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
import json
from typing import List, Tuple, Union

import numpy as np
from Bio import SeqIO

def get_row_start(index: int) -> int:
    return int(index * (index + 1) / 2)

class PredictionMatrix(object):

    def __init__(self, predictions: np.array, protein_ids: Union[List[str], dict, str]):
        self.predictions = predictions
        self.num_proteins = int((-1 + np.sqrt(8 * len(predictions) + 1))/2)

        if isinstance(protein_ids, str):
            self.id_to_index_map = json.load(open(protein_ids))
        elif isinstance(protein_ids, dict):
            self.id_to_index_map = protein_ids.copy()
        elif isinstance(id_to_index_map, list):
            self.id_to_index_map = { prot_id: i for i, prot_id in enumerate(protein_ids) }
        else:
            raise "Invalid format for protein ids provided to matrix. Must be a path to a .map.json file, a dict, or a list."

    @staticmethod
    def load(filename: str, protein_ids: Union[List[str], dict, str]) -> "PredictionMatrx":

        if isinstance(protein_ids, str):
            id_to_index_map = json.load(open(protein_ids))
        elif isinstance(protein_ids, dict):
            id_to_index_map = protein_ids.copy()
        elif isinstance(id_to_index_map, list):
            id_to_index_map = { prot_id: i for i, prot_id in enumerate(protein_ids) }
        else:
            raise "Invalid format for protein ids provided to matrix. Must be a path to a .map.json file, a dict, or a list."

        return PredictionMatrix(np.load(filename, allow_pickle=True), protein_ids)

    def _get_1d_index(self, i: int, j: int) -> int:
        assert i >= j
        return get_row_start(i) + j

    def get_score_for_pair(self, protein1_id: str, protein2_id: str) -> Tuple:
        index1 = self.id_to_index_map[protein1_id]
        index2 = self.id_to_index_map[protein2_id]
        index1, index2 = (max(index1, index2), min(index1, index2))
        pair_index = get_row_start(index1) + index2
        return self.predictions[pair_index]

    def get_scores_for_protein(self, protein_id: str) -> dict:
        protein_index = self.id_to_index_map[protein_id]
        row_start_index = get_row_start(protein_index)
        scores = self.predictions[row_start_index: row_start_index + protein_index]

        column_scores = []
        for i in range(protein_index + 1, self.num_proteins + 1):
            score = get_row_start(i)
            column_scores.append(self.predictions[self._get_1d_index(i - 1, protein_index)])

        return np.append(scores, np.array(column_scores))

    def save(self, filename: str):
        basename = filename.split(".")[0]
        
        with open(f"{basename}.map.json", "w") as map_file:
            map_file.write(json.dumps(self.id_to_index_map))

        with open(f"{basename}.mat", "wb") as matrix_file:
            np.save(matrix_file, self.predictions)

    def merge_with_matrix(self, other_matrix: 'PredictionMatrix', in_place=True):

        if set(self.id_to_index_map.keys()) != set(other_matrix.id_to_index_map.keys()):
            raise "To add a matrix, they must represent the same proteins, which is not the case."

        if not in_place:
            return PredictionMatrix(self.predictions + other_matrix.predictions, self.id_to_index_map)
        else:
            self.predictions = self.predictions + other_matrix.predictions
