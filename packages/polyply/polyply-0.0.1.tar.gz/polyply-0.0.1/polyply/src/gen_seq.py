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

import random
import json
import networkx as nx
from networkx.readwrite import json_graph
from vermouth.graph_utils import make_residue_graph
from .load_library import load_library
from .generate_templates import find_atoms


def _branched_graph(resname, branching_f, n_levels):
    """
    Generate a tree graph of branching factor `branching_f`
    and number of generations as `n_levels` - 1. Each node
    gets the attribute resname.

    Parameters
    ----------
    resname:  str
    branching_f: int
    n_levels: int

    Returns
    -------
    `:class:networkx.Graph`
    """
    graph = nx.balanced_tree(r=branching_f, h=n_levels-1)
    resnames = {idx: resname for idx in graph.nodes}
    nx.set_node_attributes(graph, resnames, "resname")
    return graph


def _random_replace_nodes_attribute(graph, residues, weights, attribute, seed=None):
    """
    Randomly replace resname attribute of `graph`
    based on the names in `residues` taking into
    account `weights` provided.

    Parameters
    ----------
    graph: `:class:networkx.Graph`
    residues: list[str]
    weights: list[float]
    attribute: str
        the attribute to be replaced
    seed: float

    Returns:
    --------
    `:class:networkx.Graph`
    """
    random.seed(seed)
    for node in graph.nodes:
        resname = random.choices(residues, weights=weights)
        graph.nodes[node][attribute] = resname[0]

    return graph


class MacroString():
    """
    Define a (random) tree graph based on a string.
    The graph is generated each time the `gen_graph`
    attribute is run. For random graph they will be
    independent.
    """

    def __init__(self, string):
        """
        Convert string into definitions of the
        random tree graph.

        Parameters:
        -----------
        string: str
           the input string containing all definitions
        """
        input_params = string.split(":")
        self.name = input_params[0]
        self.levels = int(input_params[1])
        self.bfact = int(input_params[2])
        self.res_probs = input_params[3].split(',')

        self.residues = []
        self.weights = []
        for res_prob in self.res_probs:
            name, prob = res_prob.split("-")
            self.residues.append(name)
            self.weights.append(float(prob))

    def gen_graph(self, seed=None):
        """
        Generate a graph from the definitions stored in this
        instance a random seed can be provided.
        """
        graph = _branched_graph("dum", self.bfact, self.levels)
        graph = _random_replace_nodes_attribute(graph, self.residues,
                                                self.weights, "resname", seed)
        return graph

class MacroFile():
    """
    Define a macro as residue graph of a
    vermouth molecule.
    """

    def __init__(self, name, force_field):
        """
        Select the appropiate molecule from
        the force_field.

        Parameters:
        -----------
        name: str
        force_field: `:class:vermouth.froce_field.ForceField`
        """
        self.molecule = force_field.blocks[name]

    def gen_graph(self, seed=None):
        """
        Generate a graph from the definitions stored in this
        instance by converting a molecule to a residue graph
        and setting the resname attribute.
        """
        block = make_residue_graph(self.molecule, attrs=('resid', 'resname'))
        resnames = nx.get_node_attributes(block, 'resname')
        graph = nx.Graph()
        graph.add_nodes_from(block.nodes)
        graph.add_edges_from(block.edges)
        nx.set_node_attributes(graph, resnames, "resname")
        return graph


def _add_edges(graph, edges, idx, jdx):
    """
    Add edges to a graph using the edge format
    'node_1,node_2', where the node keys refer
    to the node relative to the nodes with the same
    attribute `seqid`. The sequence ids are provided by
    `idx` and `jdx`.

    Parameters
    ----------
    graph: `:class:networkx.Graph`
    edges:  list[str]
        str has the format `node_keyA-node_keyB,node_keyC-node_keyD`,
        where edges will be added between nodes A and B, and C and D
    idx: int
    jdx: int

    Returns
    --------
    `:class:networkx.Graph`
    """
    for edge in edges.split(","):
        node_idx, node_jdx = map(str.strip, edge.split('-'))
        idx_nodes = find_atoms(graph, "seqid", idx)
        jdx_nodes = find_atoms(graph, "seqid", jdx)

        if not idx_nodes:
            msg = ("Trying to add connect between block with seqid {} and block with"
                   "seqid {}. However, cannot find block with seqid {}.")
            raise IOError(msg.format(idx, jdx, idx))
        elif not jdx_nodes:
            msg = ("Trying to add connect between block with seqid {} and block with"
                   "seqid {}. However, cannot find block with seqid {}.")
            raise IOError(msg.format(idx, jdx, jdx))

        try:
            node_i = idx_nodes[int(node_idx)]
        except IndexError:
            msg = ("Trying to add connect between block with seqid {} and block with"
                   "seqid {}. However, cannot find resid {} in block with seqid {}.")
            raise IOError(msg.format(idx, jdx, node_idx, idx))

        try:
            node_j = jdx_nodes[int(node_jdx)]
        except IndexError:
            msg = ("Trying to add connect between block with seqid {} and block with"
                   "seqid {}. However, cannot find resid {} in block with seqid {}.")
            raise IOError(msg.format(idx, jdx, node_idx, idx))

        graph.add_edge(node_i, node_j)

    return graph


def generate_seq_graph(sequence, macros, connects):
    """
    Given a sequence definition in terms of blocks in macros
    generate a graph and add the edges provided in connects.

    Parameters:
    ----------
    sequence: list
      a list of blocks defining a sequence
    macros: dict[str, networkx.graph]
      a dictionary of graphs defining a macro block
    connects: list[str]
      a list of connects

    Returns:
    -------
    `:class:networkx.graph`
    """
    seq_graph = nx.Graph()
    for idx, macro_name in enumerate(sequence):
        sub_graph = macros[macro_name].gen_graph()

        nx.set_node_attributes(
            sub_graph, {node: idx for node in sub_graph.nodes}, "seqid")
        seq_graph = nx.disjoint_union(seq_graph, sub_graph)

    for connect in connects:
        idx, jdx, edges = connect.split(":")
        _add_edges(seq_graph, edges, int(idx), int(jdx))

    return seq_graph


def _find_terminal_nodes(graph):
    """
    Find all termini of a graph and return the node key.
    A termini is defined as a node with degree of 1. Note
    that graph is assumed to be undirected.
    """
    termini = []
    for node in graph.nodes:
        if graph.degree(node) == 1:
            termini.append(node)

    return termini

def _apply_termini_modifications(graph, modifications):
    """
    Given a `graph` change the resname attribute of the end
    nodes as specified in modifications.

    Parameters:
    -----------
    graph: nx.Graph
    modifications: list[str:str]
        list of seq_ID:resname, where resname is the name
        to be applied to all terminal nodes part of block
        with seq_ID
    """
    terminal_nodes = _find_terminal_nodes(graph)
    for modification in modifications:
        seq_ID, resname = modification.split(':')
        idx_nodes = find_atoms(graph, "seqid", int(seq_ID))
        for node in idx_nodes:
            if node in terminal_nodes:
                graph.nodes[node]["resname"] = resname


def gen_seq(args):
    """
    Given a sequence definition and macros defining smaller
    building blocks of the sequence, create a residue graph
    and write it to a .json file to be used with gen_itp.
    """
    macros = {}

    if args.from_file:
        force_field = load_library("seq", None, args.inpath)
        for tag_name in args.from_file:
            tag, name = tag_name.split(":")
            macros[tag] = MacroFile(name, force_field)

    for macro_string in args.macros:
        macro = MacroString(macro_string)
        macros[macro.name] = macro

    seq_graph = generate_seq_graph(args.seq, macros, args.connects)

    _apply_termini_modifications(seq_graph, args.modifications)

    g_json = json_graph.node_link_data(seq_graph)
    with open(args.outpath, "w") as file_handle:
        json.dump(g_json, file_handle, indent=2)
