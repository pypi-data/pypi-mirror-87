from wknml import NMLParameters, Group, Edge, Node, Tree, NML, Branchpoint, Comment
import networkx as nx
import numpy as np

import logging
import colorsys
from typing import Tuple, List, Dict, Union, Any
from copy import deepcopy


logger = logging.getLogger(__name__)


def random_color_rgba():
    # https://stackoverflow.com/a/43437435/783758

    h, s, l = (
        np.random.random(),
        0.5 + np.random.random() / 2.0,
        0.4 + np.random.random() / 5.0,
    )
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (r, g, b, 1)


def discard_children_hierarchy(groups: List[Group]) -> List[Group]:
    groups_without_hierarchy = []
    for group in groups:
        children = discard_children_hierarchy(group.children)
        groups_without_hierarchy.append(
            Group(id=group.id, name=group.name, children=[])
        )
        groups_without_hierarchy.extend(children)
    return groups_without_hierarchy


def globalize_tree_ids(group_dict: Dict[str, List[nx.Graph]]):
    current_id = 1
    for tree_group in group_dict.values():
        for tree in tree_group:
            tree.graph["id"] = current_id
            current_id += 1


def globalize_node_ids(group_dict: Dict[str, List[nx.Graph]]):
    current_id = 1
    for tree_group in group_dict.values():
        for tree_index in range(len(tree_group)):
            tree = tree_group[tree_index]
            new_tree = nx.Graph(**tree.graph)
            edge_mapping_dict = {}
            for old_id in tree.nodes:
                tree.nodes[old_id]["id"] = current_id
                edge_mapping_dict[old_id] = current_id
                new_tree.add_node(current_id, **tree.nodes[old_id])

                current_id += 1
            new_edges = []
            for edge in tree.edges:
                new_edges.append(
                    (edge_mapping_dict[edge[0]], edge_mapping_dict[edge[1]])
                )

            new_tree.add_edges_from(new_edges)
            tree_group[tree_index] = new_tree


def generate_nml(
    tree_dict: Union[List[nx.Graph], Dict[str, List[nx.Graph]]],
    parameters: Dict[str, Any] = {},
    globalize_ids=True,
) -> NML:
    no_group_provided = False
    if not isinstance(tree_dict, dict):
        tree_dict = {"main_group": tree_dict}
        no_group_provided = True

    if globalize_ids:
        globalize_tree_ids(tree_dict)
        globalize_node_ids(tree_dict)

    nmlParameters = NMLParameters(
        name=parameters.get("name", "dataset"),
        scale=parameters.get("scale", [11.24, 11.24, 25]),
        offset=parameters.get("offset", None),
        time=parameters.get("time", None),
        editPosition=parameters.get("editPosition", None),
        editRotation=parameters.get("editRotation", None),
        zoomLevel=parameters.get("zoomLevel", None),
        taskBoundingBox=parameters.get("taskBoundingBox", None),
        userBoundingBox=parameters.get("userBoundingBox", None),
    )

    comments = [
        Comment(node, tree.nodes[node]["comment"])
        for group in tree_dict.values()
        for tree in group
        for node in tree.nodes
        if "comment" in tree.nodes[node]
    ]

    branchpoints = [
        Branchpoint(tree.nodes[node]["id"], 0)
        for group in tree_dict.values()
        for tree in group
        for node in tree.nodes
        if "branchpoint" in tree.nodes[node]
    ]

    if no_group_provided:
        groups = []
    else:
        groups = [
            Group(id=group_id, name=group_name, children=[])
            for group_id, group_name in enumerate(tree_dict, 1)
        ]

    trees = []

    for group_id, group_name in enumerate(tree_dict, 1):
        for tree in tree_dict[group_name]:
            nodes, edges = extract_nodes_and_edges_from_graph(tree)
            color = tree.graph.get("color", random_color_rgba())
            name = tree.graph.get("name", f"tree{tree.graph['id']}")

            trees.append(
                Tree(
                    nodes=nodes,
                    edges=edges,
                    id=tree.graph["id"],
                    name=name,
                    groupId=None if no_group_provided else group_id,
                    color=color,
                )
            )

    nml = NML(
        parameters=nmlParameters,
        trees=trees,
        branchpoints=branchpoints,
        comments=comments,
        groups=groups,
    )

    return nml


def generate_graph(nml: NML) -> Tuple[Dict[str, List[nx.Graph]], Dict]:
    nml = deepcopy(nml)._replace(groups=discard_children_hierarchy(nml.groups))
    group_dict = {}
    for group in nml.groups:
        graphs_in_current_group = []
        for tree in nml.trees:
            if tree.groupId == group.id:
                graphs_in_current_group.append(nml_tree_to_graph(tree))
        group_dict[group.name] = graphs_in_current_group

    nml_parameters = nml.parameters
    parameter_dict = {}

    parameter_list = [
        "name",
        "scale",
        "offset",
        "time",
        "editPosition",
        "editRotation",
        "zoomLevel",
        "taskBoundingBox",
        "userBoundingBox",
    ]

    for parameter in parameter_list:
        if getattr(nml_parameters, parameter) is not None:
            parameter_dict[parameter] = getattr(nml_parameters, parameter)

    for comment in nml.comments:
        for group in group_dict.values():
            for tree in group:
                if comment.node in tree.nodes:
                    tree.nodes[comment.node]["comment"] = comment.content

    for branchpoint in nml.branchpoints:
        for group in group_dict.values():
            for tree in group:
                if branchpoint.id in tree.nodes:
                    tree.nodes[branchpoint.id]["branchpoint"] = branchpoint.time

    return group_dict, parameter_dict


def nml_tree_to_graph(tree: Tree) -> nx.Graph:
    optional_attribute_list = ["rotation", "inVp", "inMag", "bitDepth", "interpolation"]

    graph = nx.Graph(id=tree.id, color=tree.color, name=tree.name, groupId=tree.groupId)
    for node in tree.nodes:
        node_id = node.id
        graph.add_node(node_id, id=node_id, radius=node.radius, position=node.position)
        for optional_attribute in optional_attribute_list:
            if getattr(node, optional_attribute) is not None:
                graph.nodes[node_id][optional_attribute] = getattr(
                    node, optional_attribute
                )

    graph.add_edges_from([(edge.source, edge.target) for edge in tree.edges])

    return graph


def extract_nodes_and_edges_from_graph(
    graph: nx.Graph,
) -> Tuple[List[Node], List[Edge]]:
    node_nml = [
        Node(
            id=graph.nodes[node]["id"],
            position=graph.nodes[node]["position"],
            radius=graph.nodes[node].get("radius", 1.0),
            rotation=graph.nodes[node].get("rotation", None),
            inVp=graph.nodes[node].get("inVp", None),
            inMag=graph.nodes[node].get("inMag", None),
            bitDepth=graph.nodes[node].get("bitDepth", None),
            interpolation=graph.nodes[node].get("interpolation", None),
            time=graph.nodes[node].get("time", None),
        )
        for node in graph.nodes
    ]

    edge_nml = [Edge(source=edge[0], target=edge[1]) for edge in graph.edges]

    return node_nml, edge_nml
