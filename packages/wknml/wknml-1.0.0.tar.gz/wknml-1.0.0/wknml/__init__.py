import xml.etree.ElementTree as ET
from loxun import XmlWriter
from typing import BinaryIO, NamedTuple, List, Tuple, Optional

Vector3 = Tuple[float, float, float]
Vector4 = Tuple[float, float, float, float]
IntVector6 = Tuple[int, int, int, int, int, int]


class NMLParameters(NamedTuple):
    """
    Contains common metadata for NML files

    Attributes:
        name: str
        scale: Vector3
        offset: Optional[Vector3]
        time: Optional[int]
        editPosition: Optional[Vector3]
        editRotation: Optional[Vector3]
        zoomLevel: Optional[float]
        taskBoundingBox: Optional[IntVector6]
        userBoundingBox: Optional[IntVector6]
    """

    name: str
    scale: Vector3
    offset: Optional[Vector3]
    time: Optional[int]
    editPosition: Optional[Vector3]
    editRotation: Optional[Vector3]
    zoomLevel: Optional[float]
    taskBoundingBox: Optional[IntVector6]
    userBoundingBox: Optional[IntVector6]


class Node(NamedTuple):
    """
    A webKnossos skeleton node annotation object.

    Attributes:
        id: int
        position: Vector3
        radius: Optional[float]
        rotation: Optional[Vector3]
        inVp: Optional[int]
        inMag: Optional[int]
        bitDepth: Optional[int]
        interpolation: Optional[bool]
        time: Optional[int]
    """

    id: int
    position: Vector3
    radius: Optional[float]
    rotation: Optional[Vector3]
    inVp: Optional[int]
    inMag: Optional[int]
    bitDepth: Optional[int]
    interpolation: Optional[bool]
    time: Optional[int]


class Edge(NamedTuple):
    """
    A webKnossos skeleton edge.

    Attributes:
        source (int): node id reference
        target (int): node id reference
    """

    source: int
    target: int


class Tree(NamedTuple):
    """
    A webKnossos skeleton (tree) object. A graph structure consisting of nodes and edges.

    Attributes:
        id: int
        color (Vector4): RGBA
        name: str
        nodes: List[Node]
        edges: List[Edge]
        groupId (Optional[int]): group id reference
    """

    id: int
    color: Vector4
    name: str
    nodes: List[Node]
    edges: List[Edge]
    groupId: Optional[int]


class Branchpoint(NamedTuple):
    """
    A webKnossos branchpoint, i.e. a skeleton node with more than one outgoing edge.

    Attributes:
        id (int): node id reference
        time (int): Unix timestamp
    """

    id: int
    time: int


class Group(NamedTuple):
    """
    A container to group several skeletons (trees) together. Mostly for cosmetic or organizational purposes.

    Attributes:
        id: int
        name: str
        children: List[Group]
    """

    id: int
    name: str
    children: List["Group"]


class Comment(NamedTuple):
    """
    A single comment belonging to a skeleton node.

    Attributes:
        node (int): node id reference
        content (str): supports Markdown
    """

    node: int
    content: str


class NML(NamedTuple):
    """
    A complete webKnossos skeleton annotation object contain one or more skeletons (trees).

    Attributes:
        parameters: NMLParameters
        trees: List[Tree]
        branchpoints: List[Branchpoint]
        comments: List[Comment]
        groups: List[Group]
    """

    parameters: NMLParameters
    trees: List[Tree]
    branchpoints: List[Branchpoint]
    comments: List[Comment]
    groups: List[Group]


def __parse_bounding_box(nml_parameters, prefix):
    boundingBox = None
    bboxName = prefix + "BoundingBox"
    if nml_parameters.find(bboxName) is not None:
        boundingBox = (
            int(nml_parameters.find(bboxName).get("topLeftX")),
            int(nml_parameters.find(bboxName).get("topLeftY")),
            int(nml_parameters.find(bboxName).get("topLeftZ")),
            int(nml_parameters.find(bboxName).get("width")),
            int(nml_parameters.find(bboxName).get("height")),
            int(nml_parameters.find(bboxName).get("depth")),
        )
    return boundingBox


def __parse_parameters(nml_parameters):
    offset = None
    if nml_parameters.find("offset") is not None:
        offset = (
            float(nml_parameters.find("offset").get("x")),
            float(nml_parameters.find("offset").get("y")),
            float(nml_parameters.find("offset").get("z")),
        )

    editRotation = None
    if nml_parameters.find("editRotation") is not None:
        editRotation = (
            float(nml_parameters.find("editRotation").get("xRot")),
            float(nml_parameters.find("editRotation").get("yRot")),
            float(nml_parameters.find("editRotation").get("zRot")),
        )

    editPosition = None
    if nml_parameters.find("editPosition") is not None:
        editPosition = (
            float(nml_parameters.find("editPosition").get("x")),
            float(nml_parameters.find("editPosition").get("y")),
            float(nml_parameters.find("editPosition").get("z")),
        )

    time = None
    if nml_parameters.find("time") is not None:
        time = int(nml_parameters.find("time").get("ms"))

    zoomLevel = None
    if nml_parameters.find("zoomLevel") is not None:
        zoomLevel = nml_parameters.find("zoomLevel").get("zoom")

    taskBoundingBox = __parse_bounding_box(nml_parameters, "task")
    userBoundingBox = __parse_bounding_box(nml_parameters, "user")

    return NMLParameters(
        name=nml_parameters.find("experiment").get("name"),
        scale=(
            float(nml_parameters.find("scale").get("x")),
            float(nml_parameters.find("scale").get("y")),
            float(nml_parameters.find("scale").get("z")),
        ),
        offset=offset,
        time=time,
        editPosition=editPosition,
        editRotation=editRotation,
        zoomLevel=zoomLevel,
        taskBoundingBox=taskBoundingBox,
        userBoundingBox=userBoundingBox,
    )


def __parse_node(nml_node):
    rotation = None
    if nml_node.get("rotX") is not None:
        rotation = (
            float(nml_node.get("rotX")),
            float(nml_node.get("rotY")),
            float(nml_node.get("rotZ")),
        )

    return Node(
        id=int(nml_node.get("id")),
        radius=float(nml_node.get("radius"))
        if nml_node.get("radius") is not None
        else None,
        position=(
            float(nml_node.get("x")),
            float(nml_node.get("y")),
            float(nml_node.get("z")),
        ),
        rotation=rotation,
        inVp=int(nml_node.get("inVp")) if nml_node.get("inVp") is not None else None,
        inMag=int(nml_node.get("inMag")) if nml_node.get("inMag") is not None else None,
        bitDepth=int(nml_node.get("bitDepth"))
        if nml_node.get("bitDepth") is not None
        else None,
        interpolation=bool(nml_node.get("interpolation"))
        if nml_node.get("interpolation") is not None
        else None,
        time=int(nml_node.get("time")) if nml_node.get("time") is not None else None,
    )


def __parse_edge(nml_edge):
    return Edge(source=int(nml_edge.get("source")), target=int(nml_edge.get("target")))


def __parse_tree(nml_tree):
    name = None
    if "comment" in nml_tree.attrib:
        name = nml_tree.get("comment")
    if "name" in nml_tree.attrib:
        name = nml_tree.get("name")

    color = None
    if "color.r" in nml_tree.attrib:
        color = (
            float(nml_tree.get("color.r")),
            float(nml_tree.get("color.g")),
            float(nml_tree.get("color.b")),
            float(nml_tree.get("color.a")),
        )
    if "colorr" in nml_tree.attrib:
        color = (
            float(nml_tree.get("colorr")),
            float(nml_tree.get("colorg")),
            float(nml_tree.get("colorb")),
            float(nml_tree.get("colora")),
        )
    try:
        groupId = int(nml_tree.get("groupId", default=-1))
    except ValueError:
        groupId = -1

    return Tree(
        nodes=[],
        edges=[],
        id=int(nml_tree.get("id")),
        name=name,
        groupId=groupId if groupId >= 0 else None,
        color=color,
    )


def __parse_branchpoint(nml_branchpoint):
    return Branchpoint(
        int(nml_branchpoint.get("id")),
        int(nml_branchpoint.get("time"))
        if nml_branchpoint.get("time") is not None
        else None,
    )


def __parse_comment(nml_comment):
    return Comment(
        int(nml_comment.get("node")), nml_comment.get("content", default=None)
    )


def __parse_group(nml_group):
    return Group(int(nml_group.get("id")), nml_group.get("name", default=None), [])


def parse_nml(file: BinaryIO) -> NML:
    """
    Reads a webKnossos NML skeleton file from disk, parses it and returns an NML Python object

    Attributes:
        file (BinaryIO): A Python file handle

    Return:
        NML: A webKnossos skeleton annotation as Python NML object

    Example:
        ```
        with open("input.nml", "rb") as f:
            nml = wknml.parse_nml(f, nml)
        ```
    """

    parameters = None
    trees = []
    branchpoints = []
    comments = []
    current_tree = None
    root_group = Group(-1, "", [])
    group_stack = [root_group]
    element_stack = []

    for event, elem in ET.iterparse(file, events=("start", "end")):
        if event == "start":
            element_stack.append(elem)
            if elem.tag == "thing":
                current_tree = __parse_tree(elem)
                trees.append(current_tree)
            elif elem.tag == "node":
                assert (
                    current_tree is not None
                ), "<node ...> tag needs to be child of a <thing ...> tag."
                current_tree.nodes.append(__parse_node(elem))
            elif elem.tag == "edge":
                assert (
                    current_tree is not None
                ), "<edge ...> tag needs to be child of a <thing ...> tag."
                current_tree.edges.append(__parse_edge(elem))
            elif elem.tag == "branchpoint":
                branchpoints.append(__parse_branchpoint(elem))
            elif elem.tag == "comment":
                comments.append(__parse_comment(elem))
            elif elem.tag == "group":
                group = __parse_group(elem)
                group_stack[-1].children.append(group)
                group_stack.append(group)
        elif event == "end":
            if elem.tag == "parameters":
                parameters = __parse_parameters(elem)
            elif elem.tag == "thing":
                current_tree = None
            elif elem.tag == "group":
                group_stack.pop()

            element_stack.pop()
            # Do not clear the elements of the parameters tag as we want to parse those all at once
            # when the closing parameters tag is parsed
            if len(element_stack) and element_stack[-1].tag != "parameters":
                # Discard the element to save memory
                elem.clear()

    return NML(
        parameters=parameters,
        trees=trees,
        branchpoints=branchpoints,
        comments=comments,
        groups=root_group.children,
    )


def __dump_bounding_box(xf, parameters, prefix):
    bboxName = prefix + "BoundingBox"
    parametersBox = getattr(parameters, bboxName)

    if parametersBox is not None:
        xf.tag(
            bboxName,
            {
                "topLeftX": str(parametersBox[0]),
                "topLeftY": str(parametersBox[1]),
                "topLeftZ": str(parametersBox[2]),
                "width": str(parametersBox[3]),
                "height": str(parametersBox[4]),
                "depth": str(parametersBox[5]),
            },
        )


def __dump_parameters(xf, parameters):
    xf.startTag("parameters")
    xf.tag("experiment", {"name": parameters.name})
    xf.tag(
        "scale",
        {
            "x": str(parameters.scale[0]),
            "y": str(parameters.scale[1]),
            "z": str(parameters.scale[2]),
        },
    )

    if parameters.offset is not None:
        xf.tag(
            "offset",
            {
                "x": str(parameters.offset[0]),
                "y": str(parameters.offset[1]),
                "z": str(parameters.offset[2]),
            },
        )

    if parameters.time is not None:
        xf.tag("time", {"ms": str(parameters.time)})
    if parameters.editPosition is not None:
        xf.tag(
            "editPosition",
            {
                "x": str(parameters.editPosition[0]),
                "y": str(parameters.editPosition[1]),
                "z": str(parameters.editPosition[2]),
            },
        )
    if parameters.editRotation is not None:
        xf.tag(
            "editRotation",
            {
                "xRot": str(parameters.editRotation[0]),
                "yRot": str(parameters.editRotation[1]),
                "zRot": str(parameters.editRotation[2]),
            },
        )
    if parameters.zoomLevel is not None:
        xf.tag("zoomLevel", {"zoom": str(parameters.zoomLevel)})

    __dump_bounding_box(xf, parameters, "task")
    __dump_bounding_box(xf, parameters, "user")

    xf.endTag()  # parameters


def __dump_node(xf, node):

    attributes = {
        "id": str(node.id),
        "x": str(node.position[0]),
        "y": str(node.position[1]),
        "z": str(node.position[2]),
    }

    if node.radius is not None:
        attributes["radius"] = str(node.radius)

    if node.rotation is not None:
        attributes["rotX"] = str(node.rotation[0])
        attributes["rotY"] = str(node.rotation[1])
        attributes["rotZ"] = str(node.rotation[2])

    if node.inVp is not None:
        attributes["inVp"] = str(node.inVp)

    if node.inMag is not None:
        attributes["inMag"] = str(node.inMag)

    if node.bitDepth is not None:
        attributes["bitDepth"] = str(node.bitDepth)

    if node.interpolation is not None:
        attributes["interpolation"] = str(node.interpolation)

    if node.time is not None:
        attributes["time"] = str(node.time)

    xf.tag("node", attributes)


def __dump_edge(xf, edge):
    xf.tag("edge", {"source": str(edge.source), "target": str(edge.target)})


def __dump_tree(xf, tree):
    attributes = {
        "id": str(tree.id),
        "color.r": str(tree.color[0]),
        "color.g": str(tree.color[1]),
        "color.b": str(tree.color[2]),
        "color.a": str(tree.color[3]),
        "name": tree.name,
    }

    if tree.groupId is not None:
        attributes["groupId"] = str(tree.groupId)

    xf.startTag("thing", attributes)
    xf.startTag("nodes")
    for n in tree.nodes:
        __dump_node(xf, n)
    xf.endTag()  # nodes
    xf.startTag("edges")
    for e in tree.edges:
        __dump_edge(xf, e)
    xf.endTag()  # edges
    xf.endTag()  # thing


def __dump_branchpoint(xf, branchpoint):
    if branchpoint.time is not None:
        xf.tag(
            "branchpoint", {"id": str(branchpoint.id), "time": str(branchpoint.time)}
        )
    else:
        xf.tag("branchpoint", {"id": str(branchpoint.id)})


def __dump_comment(xf, comment):
    if comment.content is not None:
        xf.tag("comment", {"node": str(comment.node), "content": comment.content})
    else:
        xf.tag("comment", {"node": str(comment.node)})


def __dump_group(xf, group):
    xf.startTag("group", {"id": str(group.id), "name": group.name})
    for g in group.children:
        __dump_group(xf, g)
    xf.endTag()  # group


def __dump_nml(xf, nml: NML):
    xf.startTag("things")
    __dump_parameters(xf, nml.parameters)
    for t in nml.trees:
        __dump_tree(xf, t)

    xf.startTag("branchpoints")
    for b in nml.branchpoints:
        __dump_branchpoint(xf, b)
    xf.endTag()  # branchpoints

    xf.startTag("comments")
    for c in nml.comments:
        __dump_comment(xf, c)
    xf.endTag()  # comments

    xf.startTag("groups")
    for g in nml.groups:
        __dump_group(xf, g)
    xf.endTag()  # groups
    xf.endTag()  # things


def write_nml(file: BinaryIO, nml: NML):
    """
    Writes an NML object to a file on disk.

        Arguments:
            file (BinaryIO): A Python file handle
            nml (NML): A NML object that should be persisted to disk

    Example:
        ```
        with open("out.nml", "wb") as f:
            wknml.write_nml(f, nml)
        ```
    """
    with XmlWriter(file) as xf:
        __dump_nml(xf, nml)
