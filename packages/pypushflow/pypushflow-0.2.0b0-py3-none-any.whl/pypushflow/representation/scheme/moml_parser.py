__authors__ = ["Bioinformatics Laboratory, University of Ljubljana", "H.Payno"]
__license__ = "[GNU GPL v3+]: https://www.gnu.org/licenses/gpl-3.0.en.html"
__date__ = "29/05/2017"


from xml.etree.ElementTree import parse
from .parser import (
    _scheme,
    _node,
    _link,
    _nxNodeProperty,
    _nxRelation,
    _nxLink,
    _nxNode,
)
import logging
from .scheme import Node, Scheme
from .parser import Parser

logger = logging.getLogger(__name__)


class MomlParser(Parser):
    """This is a dictionnary to convert an OrangeWidget into a core process.
    """

    @staticmethod
    def scheme_load(file_, load_handlers=True):
        """

        :param file_: file containing the scheme definition
        :param bool load_handlers: try to load the handlers of each node. Used
                                   to make sure the process won't fail
        :return: :class:`Scheme`
        """
        desc = MomlParser.parse_moml_stream(file_)
        scheme = Scheme.from_desc(desc)
        if load_handlers is True:
            scheme.load_handlers()
        return scheme

    @staticmethod
    def parse_moml_stream(stream):
        doc = parse(stream)
        scheme = MomlParser.parse_moml_etree(doc)
        return scheme

    @staticmethod
    def parse_moml_etree(tree):
        def convertToOrangeLinks(nx_links, nx_relations):
            def getLink(_id):
                if _id not in links:
                    links[_id] = {"id": _id}
                return links[_id]

            links = {}
            # convert nx (.omlm) liks and relations to orange links
            for nx_link in nx_links:
                link = getLink(nx_link.relation)
                # TODO: for now some port / link type are not managed
                if nx_link.port in ("In", "Out", "No mesh defined"):
                    logger.warning(nx_link.port + " not managed yet")
                    continue
                else:
                    node_id, input_output = nx_link.port.split(".", -1)
                    if input_output.lower() in ("output", "other", "true"):
                        link["source_node_id"] = node_id
                    else:
                        link["sink_node_id"] = node_id

            for relation in nx_relations:
                assert relation.id in links
                links[relation.id]["source_channel"] = relation.class_
                links[relation.id]["sink_channel"] = relation.class_
                links[relation.id]["properties"] = relation.properties

            orangeLinks = []
            for linkid, link in links.items():
                # TODO: this condition is due from the case that some link are
                #  not managed yet.
                if "source_node_id" not in link or "sink_node_id" not in link:
                    continue
                l = _link(
                    id=link["id"],
                    source_node_id=link["source_node_id"],
                    sink_node_id=link["sink_node_id"],
                    source_channel=link["source_channel"],
                    sink_channel=link["sink_channel"],
                    enabled=True,
                )
                orangeLinks.append(l)

            return orangeLinks

        nodes, nx_links, nx_relations = [], [], []

        # Collect all nodes
        for node in tree.findall(".//entity"):
            node_id = node.get("name")
            node_class = node.get("class")
            node_properties = []
            for property in node.findall("property"):
                _property = _nxNodeProperty(
                    name=property.get("name"),
                    class_=property.get("class"),
                    value=property.get("value"),
                )
                node_properties.append(_property)
            nodes.append(
                _nxNode(
                    id=node_id,
                    class_=node_class,
                    properties=node_properties,
                    data=None,
                    qualified_name=node_class,
                )
            )

        # collect all nx links
        for link in tree.findall("link"):
            _my_link = _nxLink(port=link.get("port"), relation=link.get("relation"))
            nx_links.append(_my_link)

        # collect all nx relations
        for relation in tree.findall("relation"):
            relation_properties = []
            for property in relation.findall("property"):
                _property = _nxNodeProperty(
                    name=property.get("name"),
                    class_=property.get("class"),
                    value=property.get("value"),
                )
                relation_properties.append(_property)

            _relation = _nxRelation(
                id=relation.get("name"),
                class_=relation.get("class"),
                properties=relation_properties,
            )
            nx_relations.append(_relation)

        links = convertToOrangeLinks(nx_links=nx_links, nx_relations=nx_relations)

        return _scheme(
            version="nx 0.1",
            title=("undefined"),
            description=None,
            nodes=nodes,
            links=links,
            annotations=None,
        )
