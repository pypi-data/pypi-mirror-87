# Copyright 2020 University of Groningen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test that force field files are properly read.
"""

import textwrap
import pytest
import numpy as np
import networkx as nx
import vermouth.forcefield
import vermouth.molecule
from polyply import TEST_DATA
import polyply.src.meta_molecule
from polyply.src.meta_molecule import (MetaMolecule, Monomer)
from .example_fixtures import example_meta_molecule

class TestPolyply:
    @staticmethod
    def test_add_monomer():
        ff = vermouth.forcefield.ForceField(name='test_ff')
        meta_mol = MetaMolecule(name="test", force_field=ff)
        meta_mol.add_monomer(0,"PEO",[])
        meta_mol.add_monomer(1,"PEO",[(1, 0)])

        assert nx.get_node_attributes(meta_mol, "resname") == {0: 'PEO', 1: 'PEO'}
        assert list(meta_mol.nodes) == [0, 1]
        assert list(meta_mol.edges) == [(0, 1)]

    @staticmethod
    def test_add_monomer_fail():
        ff = vermouth.forcefield.ForceField(name='test_ff')
        meta_mol = MetaMolecule(name="test", force_field=ff)
        meta_mol.add_monomer(0,"PEO",[])
        with pytest.raises(IOError):
            meta_mol.add_monomer(1,"PEO",[(1, 8)])

    @staticmethod
    def test_get_edge_resname():
        ff = vermouth.forcefield.ForceField(name='test_ff')
        meta_mol = MetaMolecule(name="test", force_field=ff)
        meta_mol.add_monomer(0,"PEO",[])
        meta_mol.add_monomer(1,"PEO",[(1, 0)])
        name = meta_mol.get_edge_resname((1, 0))
        assert name == ["PEO", "PEO"]

    @staticmethod
    @pytest.mark.parametrize('monomers, edges, nodes, attrs', (
        # multiple blocks from single monomer
          ([Monomer(resname="PEO", n_blocks=2)],
           [(0,1)],
           [0,1],
           {0: 'PEO', 1: 'PEO'}
          ),
        # two blocks from two monomers
          ([Monomer(resname="PEO", n_blocks=1), Monomer(resname="PS",n_blocks=1)],
           [(0,1)],
           [0,1],
           {0: 'PEO', 1: 'PS'}
           ),
        # multiple blocks from two monomers
          ([Monomer(resname="PEO", n_blocks=2), Monomer(resname="PS",n_blocks=2)],
           [(0,1),(1,2),(2,3)],
           [0,1,2,3],
           {0: 'PEO', 1: 'PEO', 2: 'PS', 3: 'PS'}
         )))
    def test_from_monomer_seq_linear(monomers, edges, nodes, attrs):
        ff = vermouth.forcefield.ForceField(name='test_ff')
        name = "test"
        meta_mol = MetaMolecule.from_monomer_seq_linear(ff, monomers, name)

        assert nx.get_node_attributes(meta_mol, "resname") == attrs
        assert list(meta_mol.nodes) == nodes
        assert list(meta_mol.edges) == edges


    @staticmethod
    @pytest.mark.parametrize('file_name, edges, nodes, attrs', (
        # multiple blocks from single monomer
          (TEST_DATA + "/json/linear.json",
           [(0,1), (1,2)],
           [0,1,2],
           {0: 'PEO', 1: 'PEO', 2: 'PEO'}
          ),
       # two blocks from two monomers
         (TEST_DATA + "/json/single_branch.json",
          [(1,2),(2,3),(3,4),(2,5)],
          [1,2,3,4,5],
          {1: 'PEO', 2: 'PEO', 3: 'PS', 4: 'PS', 5:'PEO'}
          ),
       # two blocks from two monomers
         (TEST_DATA + "/json/double_branch.json",
          [(1,2),(2,3),(2,4),(4,5),(5,6),(5,8),(6,7)],
          [1,2,3,4,5,6,7,8],
          {1: 'PEO', 2: 'PEO', 3: 'PS', 4: 'PEO', 5:'PEO', 6: 'PS',
           7: 'PS', 8: 'PEO'}
          ),
       # Hyperbranched
         (TEST_DATA + "/json/hyperbranched.json",
          [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9),
           (4, 10), (4, 11), (5, 12), (5, 13)],
          [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
          {0: 'N1', 1: 'N2', 2: 'N3', 3: 'N3', 4: 'N2', 5: 'N3', 6: 'N3',
           7: 'N1', 8: 'N2', 9: 'N3', 10: 'N3', 11: 'N2', 12: 'N3', 13: 'N3'}
          ),
        # check that ordering is restored
          (TEST_DATA + "/json/linear_rev.json",
           [(0, 1), (1, 2)],
           [0, 1, 2],
           {0: 'PEO', 1: 'PEO', 2: 'PEO'}
          ),
           ))
    def test_from_json(file_name, edges, nodes, attrs):
        ff = vermouth.forcefield.ForceField(name='test_ff')
        name = "test"
        meta_mol = MetaMolecule.from_json(ff, file_name, name)

        #assert nx.get_node_attributes(meta_mol, "resname") == attrs
        print(meta_mol.edges)
        assert set(meta_mol.nodes) == set(nodes)
        assert set(meta_mol.edges) == set(edges)

    @staticmethod
    def test_from_itp():
       file_name = TEST_DATA + "/itp/PEO.itp"
       edges = [(0,1), (1,2)]
       nodes = [0, 1, 2]
       attrs = {0: 'PEO', 1: 'PEO', 2: 'PEO'}

       ff = vermouth.forcefield.ForceField(name='test_ff')
       name = "PEO"
       meta_mol = MetaMolecule.from_itp(ff, file_name, name)

       assert set(meta_mol.nodes) == set(nodes)
       assert set(meta_mol.edges) == set(edges)

@pytest.mark.parametrize('split_pattern, expct_high_res, expct_low_res, edges', (
    # split single residues of one type into two
    (
    ["B:B1-BB,BB1,BB2:B2-SC1,SC2"],
    {0: "A", 1: "A", 2: "A", 3: "A", 4: "B1", 5: "B1", 6: "B1", 7: "B2", 8: "B2",
     9: "A", 10: "A", 11: "A", 12: "A"},
    {0: "A", 1: "B1", 2: "B2", 3: "A"},
    [(0, 1), (1, 3), (1, 2)]
    ),
    # split two residues of one type into two
    (
    ["A:A1-BB,BB1:A2-SC1,SC2"],
    {0: "A1", 1: "A1", 2: "A2", 3: "A2", 4: "B", 5: "B", 6: "B", 7: "B", 8: "B",
     9: "A1", 10: "A1", 11: "A2", 12: "A2"},
    {0: "A1", 1: "A2", 2: "B", 3: "A1", 4: "A2"},
    [(0, 1), (0, 2), (2, 3), (3, 4)]
    ),
    # split all residues
    (
    ["A:A1-BB,BB1:A2-SC1,SC2", "B:B1-BB,BB1,BB2:B2-SC1,SC2"],
    {0: "A1", 1: "A1", 2: "A2", 3: "A2", 4: "B1", 5: "B1", 6: "B1", 7: "B2", 8: "B2",
     9: "A1", 10: "A1", 11: "A2", 12: "A2"},
    {0: "A1", 1: "A2", 2: "B1", 3: "B2", 4: "A1", 5: "A2"},
    [(0, 1), (0, 2), (2, 3), (2, 4), (4, 5)]
    ),
    ))
def test_split_residue(example_meta_molecule, split_pattern, expct_high_res, expct_low_res, edges):
    example_meta_molecule.split_residue(split_pattern)
    new_resnames_high = nx.get_node_attributes(example_meta_molecule.molecule, "resname")
    assert new_resnames_high == expct_high_res
    new_resnames_low = nx.get_node_attributes(example_meta_molecule, "resname")
    assert new_resnames_low == expct_low_res
    for node_a, node_b in edges:
        assert example_meta_molecule.has_edge(node_a, node_b)

def test_split_residue_err(example_meta_molecule):
    split_pattern = ["A:A1-BB,BB1:A2-BB1,SC1,SC2"]
    with pytest.raises(IOError):
         example_meta_molecule.split_residue(split_pattern)
