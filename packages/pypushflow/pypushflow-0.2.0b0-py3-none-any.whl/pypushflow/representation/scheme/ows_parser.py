__authors__ = ["Bioinformatics Laboratory, University of Ljubljana", "H.Payno"]
__license__ = "[GNU GPL v3+]: https://www.gnu.org/licenses/gpl-3.0.en.html"
__date__ = "29/05/2017"


from xml.etree.ElementTree import parse
from .parser import (
    _scheme,
    _node,
    _link,
    _data,
    _annotation,
    _text_params,
    _arrow_params,
)
from ast import literal_eval
import ast
import logging
from .scheme import Scheme
from .parser import Parser

logger = logging.getLogger(__name__)


class OwsParser(Parser):
    """
    Parser managing the .ows (orange) files
    """

    @staticmethod
    def scheme_load(file_, load_handlers=True):
        """

        :param file_: file containing the scheme definition
        :param bool load_handlers: try to load the handlers of each node. Used
                                   to make sure the process won't fail
        :return: :class:`Scheme`
        """
        desc = OwsParser.parse_ows_stream(file_)
        scheme = Scheme.from_desc(desc)
        if load_handlers is True:
            scheme.load_handlers()
        return scheme

    @staticmethod
    def parse_ows_etree_v_2_0(tree):
        aliases = Parser.get_aliases()
        scheme = tree.getroot()
        nodes, links, annotations = [], [], []

        # First collect all properties
        properties = {}
        for property in tree.findall("node_properties/properties"):
            node_id = property.get("node_id")
            format = property.get("format")
            if "data" in property.attrib:
                data = property.get("data")
            else:
                data = property.text
            properties[node_id] = _data(format, data)

        # Collect all nodes
        for node in tree.findall("nodes/node"):
            node_id = node.get("id")
            qualified_name = node.get("qualified_name")
            if qualified_name in aliases:
                logger.info(
                    "replace"
                    + str(qualified_name)
                    + "by"
                    + str(aliases[qualified_name])
                )
                qualified_name = aliases[qualified_name]

            node = _node(
                id=node_id,
                title=node.get("title"),
                name=node.get("name"),
                position=tuple_eval(node.get("position", None)),
                project_name=node.get("project_name", None),
                qualified_name=qualified_name,
                version=node.get("version", ""),
                data=properties.get(node_id, None),
            )
            nodes.append(node)

        for link in tree.findall("links/link"):
            params = _link(
                id=link.get("id"),
                source_node_id=link.get("source_node_id"),
                sink_node_id=link.get("sink_node_id"),
                source_channel=link.get("source_channel"),
                sink_channel=link.get("sink_channel"),
                enabled=link.get("enabled") == "true",
            )
            links.append(params)

        for annot in tree.findall("annotations/*"):
            if annot.tag == "text":
                rect = tuple_eval(annot.get("rect", "(0.0, 0.0, 20.0, 20.0)"))

                font_family = annot.get("font-family", "").strip()
                font_size = annot.get("font-size", "").strip()

                font = {}
                if font_family:
                    font["family"] = font_family
                if font_size:
                    font["size"] = int(font_size)

                annotation = _annotation(
                    id=annot.get("id"),
                    type="text",
                    params=_text_params(rect, annot.text or "", font),
                )
            elif annot.tag == "arrow":
                start = tuple_eval(annot.get("start", "(0, 0)"))
                end = tuple_eval(annot.get("end", "(0, 0)"))
                color = annot.get("fill", "red")
                annotation = _annotation(
                    id=annot.get("id"),
                    type="arrow",
                    params=_arrow_params((start, end), color),
                )
            annotations.append(annotation)
        return _scheme(
            version=scheme.get("version"),
            title=scheme.get("title", ""),
            description=scheme.get("description"),
            nodes=nodes,
            links=links,
            annotations=annotations,
        )

    @staticmethod
    def parse_ows_stream(stream):
        doc = parse(stream)
        scheme_el = doc.getroot()
        version = scheme_el.get("version", None)
        if version is None:
            # Fallback: check for "widgets" tag.
            if scheme_el.find("widgets") is not None:
                version = "1.0"
            else:
                logger.warning("<scheme> tag does not have a 'version' attribute")
                version = "2.0"

        if version == "1.0":
            raise ValueError("old .ows version are not managed")
        elif version == "2.0":
            return OwsParser.parse_ows_etree_v_2_0(doc)
        else:
            raise ValueError("unrecognize scheme definition version")


# ---- TAKE back from Orange3 ---------


def tuple_eval(source):
    """
    Evaluate a python tuple literal `source` where the elements are
    constrained to be int, float or string. Raise ValueError if not
    a tuple literal.

    >>> tuple_eval("(1, 2, "3")")
    (1, 2, '3')

    """
    if source is None:
        return None
    node = ast.parse(source, "<source>", mode="eval")

    if not isinstance(node.body, ast.Tuple):
        raise ValueError("%r is not a tuple literal" % source)

    if not all(
        isinstance(el, (ast.Str, ast.Num)) or
        # allow signed number literals in Python3 (i.e. -1|+1|-1.0)
        (
            isinstance(el, ast.UnaryOp)
            and isinstance(el.op, (ast.UAdd, ast.USub))
            and isinstance(el.operand, ast.Num)
        )
        for el in node.body.elts
    ):
        raise ValueError("Can only contain numbers or strings")

    return literal_eval(source)


def resolve_replaced(scheme_desc, registry):
    widgets = registry.widgets()
    nodes_by_id = {}  # type: Dict[str, _node]
    replacements = {}
    replacements_channels = {}  # type: Dict[str, Tuple[dict, dict]]
    # collect all the replacement mappings
    for desc in widgets:  # type: WidgetDescription
        if desc.replaces:
            for repl_qname in desc.replaces:
                replacements[repl_qname] = desc.qualified_name

        input_repl = {}
        for idesc in desc.inputs or []:  # type: InputSignal
            for repl_qname in idesc.replaces or []:  # type: str
                input_repl[repl_qname] = idesc.name
        output_repl = {}
        for odesc in desc.outputs:  # type: OutputSignal
            for repl_qname in odesc.replaces or []:  # type: str
                output_repl[repl_qname] = odesc.name
        replacements_channels[desc.qualified_name] = (input_repl, output_repl)

    # replace the nodes
    nodes = scheme_desc.nodes
    for i, node in list(enumerate(nodes)):
        if (
            not registry.has_widget(node.qualified_name)
            and node.qualified_name in replacements
        ):
            qname = replacements[node.qualified_name]
            desc = registry.widget(qname)
            nodes[i] = node._replace(
                qualified_name=desc.qualified_name, project_name=desc.project_name
            )
        nodes_by_id[node.id] = nodes[i]

    # replace links
    links = scheme_desc.links
    for i, link in list(enumerate(links)):  # type: _link
        nsource = nodes_by_id[link.source_node_id]
        nsink = nodes_by_id[link.sink_node_id]

        _, source_rep = replacements_channels.get(nsource.qualified_name, ({}, {}))
        sink_rep, _ = replacements_channels.get(nsink.qualified_name, ({}, {}))

        if link.source_channel in source_rep:
            link = link._replace(source_channel=source_rep[link.source_channel])
        if link.sink_channel in sink_rep:
            link = link._replace(sink_channel=sink_rep[link.sink_channel])
        links[i] = link

    return scheme_desc._replace(nodes=nodes, links=links)
