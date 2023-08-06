#!/usr/bin/env python3
"""
Copyright (c) 2020, Francois Charih
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Tuple

def load_hsps(filename: str, id_to_index_map: dict) -> List[Tuple]:
    """Loads the HSPs from a file.

    Parameters
    ----------
    filename: str
    The path to the HSP file.

    id_to_index_map: Dict[str, int]
    A dictionary converting a protein name to an integer index.

    Returns
    -------
    List[Tuple[str, str, int, int, int]]
    A list of HSP tuples.
    """
    with open(filename) as hspfile:
        hsps = []
        for hsp in hspfile.read().splitlines():
            split = hsp.split()
            p1, p2 = [id_to_index_map[p] for p in split[:2]]
            s1, s2, l = [int(x) for x in split[2:]]
            hsps.append((p1, p2, s1, s2, l))
    return hsps

def dump_hsps(
    destination: str,
    hsps: List[Tuple],
    index_to_id_map: dict,
    binary: bool = False
):
    """Saves the HSPs from a file.

    Parameters
    ----------
    destination: str
    The path to the file where HSPs are to be saved.

    hsps: List[Tuple]
    List of HSPs of the form (int, int, int, int, int).

    index_to_id_map: Dict[int, str]
    A dictionary that can convert a protein index to a protein name.

    binary: bool
    Whether the file should be saved in binary format (default: False).
    """
    mode = "wb" if binary else "w"
    with open(destination, mode) as output_file:
        for hsp in hsps:
            string = f"{index_to_id_map[int(hsp[0])]} {index_to_id_map[int(hsp[1])]} {hsp[2]} {hsp[3]} {hsp[4]}\n"
            output_file.write(bytes(string, encoding="utf-8"))
