#!/usr/bin/env python3
"""
Copyright (c) 2020, Francois Charih
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
import gzip
import io
import os

from bs4 import BeautifulSoup

import requests
from Bio import SeqIO

UNIPROT_FTP_URL = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/"
KINGDOM_BASE_URL = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/{}/"
KINGDOMS = ["Archaea", "Bacteria", "Eukaryota", "Viruses"]

def download_swissprot(fasta_file: dict, destination: str):
    print(f"Downloading the sequences from {fasta_file['url']}...")
    response = requests.get(fasta_file["url"])
    print("Successfully retrieved!")
    sequences_fasta = response.content
    output_file = io.StringIO(sequences_fasta.decode("utf-8"))
    sequences = list(SeqIO.parse(output_file, "fasta"))

    print(f"Writing {len(sequences)} sequences to {destination}...")
    with open(os.path.join(destination, fasta_file["filename"]), "w") as destination_file:
        content = [f">{p.id.split('|')[1]}\n{str(p.seq)}" for p in sequences]
        destination_file.write("\n".join(content))
    print("Done!")

def download_fasta_files(organism_ids, destination):
    organisms_of_interest = set([int(org_id) for org_id in organism_ids])
    all_files = []
    for kingdom in KINGDOMS:
        print(f"Parsing the {kingdom} directory...")
        kingdom_root_url = KINGDOM_BASE_URL.format(kingdom)

        # Get the directory contents and parse
        page_content = requests.get(kingdom_root_url).content
        soup = BeautifulSoup(page_content, 'html.parser')
        links = soup.find_all("a")

        # Get all the FASTA file urls
        files = [link.get("href") for link in links if "fasta" in link.get("href")]

        # Add all of these files to the list of all FASTA files
        # on the server
        files = [{ 
            "organism_id": int(f.split("_")[1].split(".")[0]),
            "filename": f.rstrip(".gz"),
            "url": kingdom_root_url + f
        } for f in files]
        all_files += files

    files_of_interest = [f for f in all_files if f["organism_id"] in organisms_of_interest]
    
    for f in files_of_interest:
        download_swissprot(f, destination)
