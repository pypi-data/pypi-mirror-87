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
from collections import (namedtuple, OrderedDict)
import json
import networkx as nx
from networkx.readwrite import json_graph
from vermouth.graph_utils import make_residue_graph
from .polyply_parser import read_polyply
from .graph_utils import find_nodes_with_attributes

Monomer = namedtuple('Monomer', 'resname, n_blocks')

def _make_edges(force_field):
    for block in force_field.blocks.values():
        inter_types = list(block.interactions.keys())
        for inter_type in inter_types:
            if inter_type not in ["pairs", "exclusions"]:
               block.make_edges_from_interaction_type(type_=inter_type)

    for link in force_field.links:
        inter_types = list(link.interactions.keys())
        for inter_type in inter_types:
            link.make_edges_from_interaction_type(type_=inter_type)

def _interpret_residue_mapping(graph, resname, new_residues):
    """
    Find all nodes corresponding to resname in graph
    and generate a corrspondance dict of these nodes
    to new resnames as defined by new_residues string
    which has the format <resname-atom1,atom2 ...>.

    Parameters:
    -----------
    graph: networkx.graph
    resname: str
    new_residues:  list[str]

    Returns:
    --------
    dict
        mapping of nodes to new residue name
    """
    atom_name_to_resname = {}
    had_atoms = []

    for new_res in new_residues:
        new_name, atoms = new_res.split("-")
        names = atoms.split(",")

        for name in names:
            if name in had_atoms:
                msg = ("You are trying to split residue {} into {} residues. "
                       "However, atom {} is mentioned more than once. This is not "
                       "allowed. ")
                raise IOError(msg.format(resname, len(new_residues), name))
            nodes = find_nodes_with_attributes(graph, resname=resname, atomname=name)
            had_atoms.append(name)

            for node in nodes:
                atom_name_to_resname[node] = new_name

    return atom_name_to_resname

class MetaMolecule(nx.Graph):
    """
    Graph that describes molecules at the residue level.
    """

    node_dict_factory = OrderedDict

    def __init__(self, *args, **kwargs):
        self.force_field = kwargs.pop('force_field', None)
        self.mol_name = kwargs.pop('mol_name', None)
        super().__init__(*args, **kwargs)
        self.molecule = None
        nx.set_node_attributes(self, True, "build")

    def add_monomer(self, current, resname, connections):
        """
        This method adds a single node and an unlimeted number
        of edges to an instance of :class::`MetaMolecule`. Note
        that matches may only refer to already existing nodes.
        But connections can be an empty list.
        """
        resids = nx.get_node_attributes(self, "resid")

        if resids:
           resid = max(resids.values()) + 1
        else:
           resid = 1

        self.add_node(current, resname=resname, resid=resid, build=True)
        for edge in connections:
            if self.has_node(edge[0]) and self.has_node(edge[1]):
                self.add_edge(edge[0], edge[1])
            else:
                msg = ("Edge {} referes to nodes that currently do"
                       "not exist. Cannot add edge to unkown nodes.")
                raise IOError(msg.format(edge))

    def get_edge_resname(self, edge):
        return [self.nodes[edge[0]]["resname"], self.nodes[edge[1]]["resname"]]

    def relabel_and_redo_res_graph(self, mapping):
        """
        Relable the nodes of `self.molecule` using `mapping`
        and regenerate the meta_molecule (i.e. residue graph).

        Parameters:
        -----------
        mapping: dict
            mapping of node-key to new residue name
        """
        # find the maximum resiude id
        max_resid = max(nx.get_node_attributes(self.molecule, "resid").values())
        # resname the residues and increase with pseudo-resid
        for node, resname in mapping.items():
            self.molecule.nodes[node]["resname"] = resname
            old_resid = self.molecule.nodes[node]["resid"]
            self.molecule.nodes[node]["resid"] = old_resid + max_resid + 1

        # make a new residue graph and overwrite the old one
        new_meta_graph = make_residue_graph(self.molecule, attrs=('resid', 'resname'))
        self.clear()
        self.add_nodes_from(new_meta_graph.nodes(data=True))
        self.add_edges_from(new_meta_graph.edges)

    def split_residue(self, split_strings):
        """
        Split all residues defind by the in `split_strings`, which is a list
        of strings with format <resname>:<new_resname>-<atom1>,<atom2><etc>
        into new residues and also update the underlying molecule with these
        new residues.

        Parameters:
        -----------
        split_strings:  list[str]
             list of split strings

        Returns:
        dict
            mapping of the nodes to the new resnames
        """
        mapping = {}
        for split_string in split_strings:
            # split resname and new resiude definitions
            resname, *new_residues = split_string.split(":")
            # find out which atoms map to which new residues
            mapping.update(_interpret_residue_mapping(self.molecule, resname, new_residues))
        # relabel graph and redo residue graph
        self.relabel_and_redo_res_graph(mapping)
        return mapping

    @staticmethod
    def _block_graph_to_res_graph(block):
        """
        generate a residue graph from the nodes of `block`.

        Parameters
        -----------
        block: `:class:vermouth.molecule.Block`

        Returns
        -------
        :class:`nx.Graph`
        """
        res_graph = make_residue_graph(block, attrs=('resid', 'resname'))
        return res_graph

    @classmethod
    def from_monomer_seq_linear(cls, force_field, monomers, mol_name):
        """
        Constructs a meta graph for a linear molecule
        which is the default assumption from
        """

        meta_mol_graph = cls(force_field=force_field, mol_name=mol_name)
        res_count = 0

        for monomer in monomers:
            trans = 0
            while trans < monomer.n_blocks:

                if res_count != 0:
                    connect = [(res_count-1, res_count)]
                else:
                    connect = []
                trans += 1

                meta_mol_graph.add_monomer(res_count, monomer.resname, connect)
                res_count += 1
        return meta_mol_graph

    @classmethod
    def from_json(cls, force_field, json_file, mol_name):
        """
        Constructs a :class::`MetaMolecule` from a json file
        using the networkx json package.
        """
        with open(json_file) as file_:
            data = json.load(file_)

        init_graph = nx.Graph(json_graph.node_link_graph(data))
        graph = nx.Graph(node_dict_factory=OrderedDict)
        nodes = list(init_graph.nodes)
        nodes.sort()

        for node in nodes:
            attrs = init_graph.nodes[node]
            graph.add_node(node, **attrs)

        graph.add_edges_from(init_graph.edges)
        meta_mol = cls(graph, force_field=force_field, mol_name=mol_name)
        return meta_mol

    @classmethod
    def from_itp(cls, force_field, itp_file, mol_name):
        """
        Constructs a :class::`MetaMolecule` from an itp file.
        """
        with open(itp_file) as file_:
            lines = file_.readlines()
            read_polyply(lines, force_field)

        graph = MetaMolecule._block_graph_to_res_graph(force_field.blocks[mol_name])
        meta_mol = cls(graph, force_field=force_field, mol_name=mol_name)
        meta_mol.molecule = force_field.blocks[mol_name].to_molecule()
        return meta_mol

    @classmethod
    def from_block(cls, force_field, mol_name):
        """
        Constructs a :class::`MetaMolecule` from an vermouth.molecule.
        """
        _make_edges(force_field)
        block = force_field[mol_name]
        graph = MetaMolecule._block_graph_to_res_graph(block)
        meta_mol = cls(graph, force_field=force_field, mol_name=mol_name)
        meta_mol.molecule = force_field.blocks[mol_name].to_molecule()
        return meta_mol
