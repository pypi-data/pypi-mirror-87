# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "17/12/2018"


from xml.etree.ElementTree import TreeBuilder, Element, ElementTree
from collections import defaultdict
from itertools import count, chain
from typing import Union
import json
import pprint
import base64
import pickle
import logging
import typing
from .node import Node
from .link import Link
from ast import literal_eval

_logger = logging.getLogger(__name__)


class Scheme(object):
    """
    class to define a workflow scheme from nodes and links

    :param typing.Iterable nodes: set of Node contained in this scheme.
                                  note: subschemes are considered as Node.
                                  So if any defined it should be given as a
                                  Node
    :param typing.Iterable links: set of Link
    :type: typing.Iterable

    """

    _JSON_DESCRIPTION = "description"
    _JSON_TITLE = "title"
    _JSON_NODES = "nodes"
    _JSON_LINKS = "links"

    def __init__(
        self,
        nodes: typing.Iterable = None,
        links: typing.Iterable = None,
        description: str = None,
        title: str = None,
    ):
        self.__rnodes = None
        self.__rlinks = None
        self.__rsub_schemes = None

        self._reset(nodes=nodes, links=links, description=description, title=title)

    @property
    def rnodes(self) -> Union[None, list]:
        """All the nodes recursively. So this mean contained in this scheme or
        in a subscheme"""
        if self.__rnodes is None:
            self.__rnodes = list(self.nodes)
            for subscheme in self.sub_schemes:
                self.__rnodes.extend(subscheme.rnodes)
        return self.__rnodes

    @property
    def rlinks(self) -> Union[None, dict]:
        """all the links recursively. So this mean contained in this scheme or
        in a subscheme"""
        if self.__rlinks is None:
            self.__rlinks = self.links
            for subscheme in self.sub_schemes:
                self.__rlinks.update(subscheme.rlinks)
        return self.__rlinks

    @property
    def sub_schemes(self) -> Union[None, list]:
        """list of sub schemes contained by this scheme"""
        return self.__sub_schemes

    @property
    def rsub_schemes(self) -> Union[None, list]:
        """list of all sub schemes contained in this scheme recursively
        """
        if self.__rsub_schemes is None:
            self.__rsub_schemes = self.sub_schemes
            for sub_scheme in self.sub_schemes:
                self.__rsub_schemes.extend(sub_scheme.rsub_schemes)
        return self.__rsub_schemes

    def _reset(self, nodes, links, description, title) -> None:
        self.title = title or ""
        self.description = description or ""
        # clear structure
        self.links = {}  # keys are link ID, values are Link
        self.__sub_schemes = []
        self.__rnodes = None
        self.__rlinks = None

        if links is not None:
            for link in links:
                self.links[link.id] = link
        self.nodes = nodes or []
        """list of nodes"""
        self.nodes_dict = {}
        """dict with node id as key and node as value"""

        # register all sub scheme
        for node in self.nodes:
            if isinstance(node, SubScheme):
                self.__sub_schemes.append(node)
                self.nodes_dict[node.id] = node
        # update nodes for sub_schemes
        for node in self.rnodes:
            self.nodes_dict[node.id] = node

        if links is not None:
            self._update_nodes_from_links()

    def final_nodes(self) -> list:
        """

        :return: list of final nodes (with no output) and which hasn't any
                 control node upstream
        """
        res = []
        for node in self.rnodes:
            assert isinstance(node, Node)
            if node.isfinal():
                res.append(node)
        return res

    def start_nodes(self) -> list:
        """

        :return: list of nodes starting the workflow. Those does not require
                 any input_data.
        :rtype: list
        """
        res = []
        for node in self.rnodes:
            assert isinstance(node, Node)
            if node.isstart():
                res.append(node)
        return res

    def endlessNodes(self) -> list:
        """

        :return: list of final nodes.
        :rtype: list
        """
        res = []
        for node in self.rnodes:
            assert isinstance(node, Node)
            if node.endless is True:
                res.append(node)
        return res

    def save_to(self, output_file: str) -> None:
        """
        Save the scheme as an xml formated file to `stream`

        :param output_file: name of the output file.
        :type: str
        """
        if output_file.lower().endswith(".json"):
            self.save_as_json(output_file)
        else:
            self.save_as_xml(output_file)

    def save_as_xml(self, output_file: str) -> None:
        """
        save current scheme to a default xml format

        :param str output_file: file path
        """
        tree = self.scheme_to_etree(data_format="literal")
        indent(tree.getroot(), 0)

        tree.write(output_file)

    def save_as_json(self, output_file: str) -> None:
        """
        save current scheme to a default json format

        :param str output_file: file path
        """
        with open(output_file, "w") as json_file:
            json.dump(self.to_json(), json_file)

    def nodes_to_json(self) -> list:
        """

        :return: nodes to json compatible format
        :rtype: list
        """
        res = []
        for node in self.nodes:
            res.append(node.to_json())
        return res

    @staticmethod
    def nodes_from_json(json_data: dict) -> tuple:
        """

        :param json_data: data containing the json definition
        :return: nodes, sub_schemes
        :rtype: tuple
        :raises: ValueError if the json is not a valid Node description
        """
        nodes = []
        sub_schemes = []
        for node_json_data in json_data:
            # if contains a node description then this is a subscheme
            if Scheme._JSON_NODES in node_json_data:
                sub_scheme = SubScheme.load_from_json(node_json_data)
                sub_schemes.append(sub_scheme)
            else:
                nodes.append(Node.from_json(node_json_data))
        return nodes, sub_schemes

    def links_to_json(self) -> list:
        """

        :return: links to json compatible format
        :rtype: list
        """
        res = []
        for link in self.links.values():
            res.append(link.to_json())
        return res

    @staticmethod
    def links_from_json(json_data: dict) -> list:
        """

        :param json_data: data containing the json definition
        :return: list of Link defined by the json data
        :rtype: list
        """
        links = []
        for link_json_data in json_data:
            links.append(Link.from_json(link_json_data))
        return links

    def to_json(self) -> dict:
        """
        Convert scheme to json

        :return: json dict
        :rtype: dict
        """
        return {
            self._JSON_DESCRIPTION: self.description,
            self._JSON_TITLE: self.title,
            self._JSON_NODES: self.nodes_to_json(),
            self._JSON_LINKS: self.links_to_json(),
        }

    @staticmethod
    def from_json_file(json_file_path: str):
        """
        Create and load Scheme from a json file

        :param str json_file_path: json file
        :return: Scheme fitting the json description
        :rtype: Scheme
        :raises: ValueError if file not found or invalid
        """
        scheme = Scheme()
        try:
            scheme.load_from_json_file(json_file_path)
        except ValueError as e:
            _logger.error(e)
            return None
        else:
            return scheme

    def load_from_json_file(self, json_file_path: str):
        """

        :param str json_file_path: path to the json file containing the scheme
                                   description

        :return: Scheme fitting the json description contains if the file.
                 If description is incomplete, return None
        :rtype: Union[Scheme, None]
        """
        try:
            with open(json_file_path, "r") as json_file:
                json_data = json.load(json_file)
        except IOError as e:
            _logger.error("fail to read json file", str(e))
        else:
            self.load_from_json(json_data=json_data)

    @staticmethod
    def load_scheme_info_from_json(json_data: dict) -> tuple:
        """
        load fom json stream the Scheme Information

        :param json_data: scheme description
        :return: nodes, links, sub-schemes, title, description
        :rtype: tuple
        """
        # load title
        if Scheme._JSON_TITLE not in json_data:
            _logger.warning("no title found in the json")
            title = None
        else:
            title = json_data[Scheme._JSON_TITLE]
        # load description
        if Scheme._JSON_DESCRIPTION not in json_data:
            _logger.warning("no description found in the json")
            description = None
        else:
            description = json_data[Scheme._JSON_DESCRIPTION]
        # load links
        if Scheme._JSON_LINKS not in json_data:
            _logger.error("no link found in the json")
            links = None
        else:
            try:
                links = Scheme.links_from_json(json_data=json_data[Scheme._JSON_LINKS])
            except ValueError as e:
                _logger.error(e)
                links = None
        # load nodes
        nodes, sub_schemes = None, None
        if Scheme._JSON_NODES not in json_data:
            _logger.error("no nodes found in the json")
        else:
            try:
                nodes, sub_schemes = Scheme.nodes_from_json(
                    json_data=json_data[Scheme._JSON_NODES]
                )
            except ValueError as e:
                _logger.error(e)
                nodes = None
        return nodes, links, sub_schemes, title, description

    def load_from_json(self, json_data: dict):
        """

        :param json_data: scheme description
        :raise ValueError: if sink or source channel missing or if link id
                           missing or if sink or source node missing
        """
        nodes, links, sub_schemes, title, description = self.load_scheme_info_from_json(
            json_data
        )
        # create scheme if possible
        if nodes is None or links is None:
            raise ValueError(
                "unable to load scheme from json description." "Information missing"
            )
        else:
            if sub_schemes is not None:
                nodes.extend(sub_schemes)
            self._reset(nodes=nodes, links=links, description=description, title=title)

    def scheme_to_etree(
        self, data_format: str = "literal", pickle_fallback: bool = False
    ):
        """
        Return an 'xml.etree.ElementTree' representation of the scheme.
        """
        builder = TreeBuilder(element_factory=Element)
        builder.start(
            "scheme",
            {
                "version": "2.0",
                "title": self.title or "",
                "description": self.description or "",
            },
        )

        # Nodes
        node_ids = defaultdict(count().__next__)
        builder.start("nodes", {})
        for node in self.nodes:  # type: SchemeNode
            attrs = {"id": node.id, "qualified_name": node._qualified_name}

            if type(node) is not Node:
                attrs["scheme_node_type"] = "%s.%s" % (
                    type(node).__name__,
                    type(node).__module__,
                )
            builder.start("node", attrs)
            builder.end("node")

        builder.end("nodes")

        # Links
        link_ids = defaultdict(count().__next__)
        builder.start("links", {})
        for link in self.links:  # type: SchemeLink
            source = link.source_node_id
            sink = link.sink_node_id
            source_id = node_ids[source]
            sink_id = node_ids[sink]
            attrs = {
                "id": str(link_ids[link]),
                "source_node_id": str(source_id),
                "sink_node_id": str(sink_id),
                "source_channel": link.source_channel,
                "sink_channel": link.sink_channel,
                "enabled": "true" if link.enabled else "false",
            }
            builder.start("link", attrs)
            builder.end("link")

        builder.end("links")

        # Annotations
        annotation_ids = defaultdict(count().__next__)
        builder.start("thumbnail", {})
        builder.end("thumbnail")

        # Node properties/settings
        builder.start("node_properties", {})
        for node in self.nodes:
            data = None
            if node.properties:
                try:
                    data, format = dumps(
                        node.properties,
                        format=data_format,
                        pickle_fallback=pickle_fallback,
                    )
                except Exception:
                    _logger.error(
                        "Error serializing properties for node %r",
                        node.title,
                        exc_info=True,
                    )
                if data is not None:
                    builder.start(
                        "properties", {"node_id": str(node_ids[node]), "format": format}
                    )
                    builder.data(data)
                    builder.end("properties")

        builder.end("node_properties")

        builder.end("scheme")
        root = builder.close()
        tree = ElementTree(root)
        return tree

    def _update_nodes_from_links(self):
        """
        Update upstream and downstream nodes from links definition
        """
        self._clear_nodes_connections()
        for link_id, link in self.links.items():
            source_node = self.nodes_dict[link.source_node_id]
            sink_node = self.nodes_dict[link.sink_node_id]
            source_node.downstream_nodes.add(self.nodes_dict[link.sink_node_id])
            sink_node.upstream_nodes.add(self.nodes_dict[link.source_node_id])

    def _clear_nodes_connections(self):
        """
        clear for all nodes downstream and upstream nodes
        """
        for node in self.nodes:
            assert isinstance(node, Node)
            node.downstream_nodes = set()
            node.upstream_nodes = set()

    def has_final_join(self):
        """
        :return: True if we need to send a 'end' signal before closing the
                 workflow. This is needed in the 'acquisition workflow' like
                 tomwer and the DataWatcher process for example.
        :rtype: bool
        """
        for node in self.nodes:
            if node.need_stop_join:
                return True
        return False

    @staticmethod
    def from_desc(desc):
        """

        :param desc:
        :return: instance of Scheme from it description.
        :rtype: :class:`Scheme`
        """
        nodes = []
        nodes_dict = {}

        for node_d in desc.nodes:
            node = Node(id=node_d.id, processing_pt=node_d.qualified_name)
            nodes.append(node)
            nodes_dict[node.id] = node
            data = node_d.data
            if data:
                properties = loads(data.data, data.format)
                node.properties = properties
            else:
                node.properties = {}
            node.qualified_name = node_d.qualified_name

        for link_d in desc.links:
            upstream_node = nodes_dict[link_d.source_node_id]
            assert isinstance(upstream_node, Node)
            downstream_node = nodes_dict[link_d.sink_node_id]
            upstream_node.downstream_nodes.add(downstream_node)
            downstream_node.upstream_nodes.add(upstream_node)

        scheme = Scheme(nodes=nodes, links=desc.links)
        scheme.title = desc.title
        scheme.description = desc.description

        return scheme

    def load_handlers(self):
        """
        load all nodes handlers.
        """
        for node in self.nodes:
            node.load_handlers()


class SubScheme(Scheme, Node):
    """
    Define a sub-scheme of the workflow (or subworkflow). SubScheme are
    as Scheme expect that they are not 'root'.

    :param nodes: set of Node
    :type: typing.Iterable
    :param links: set of Node
    :type: typing.Iterable
    :param description: description of the subscheme
    :type: str
    :param error_handler: ErrorHandler
    """

    def __init__(
        self,
        nodes: typing.Iterable,
        links: typing.Iterable,
        description: str = None,
        error_handler=None,
        title="",
        id=None,
    ):
        Node.__init__(self, processing_pt=None, error_handler=error_handler, id=id)
        Scheme.__init__(
            self, nodes=nodes, links=links, title=title, description=description
        )

    def to_json(self):
        """
        Convert sub scheme to json

        :return: json dict
        :rtype: dict
        """
        desc = Scheme.to_json(self)
        desc.update(Node.to_json(self))
        return desc

    @staticmethod
    def load_from_json(json_data: dict):
        """

        :param json_data: scheme description.

        :raise ValueError: if sink or source channel missing or if link id
                           missing or if sink or source node missing.
        """
        (
            nodes,
            links,
            sub_schemes,
            title,
            description,
        ) = Scheme.load_scheme_info_from_json(json_data)
        _id, _properties, _process_pt = Node.load_node_info_from_json(json_data)
        if _properties is not None:
            _logger.warning("SubScheme properties are not managed")
        if _process_pt is not None:
            _logger.warning("SubScheme pointer to ptocess is not managed")
        # create scheme if possible
        if nodes is None or links is None:
            raise ValueError(
                "unable to load scheme from json description." "Information missing"
            )
        sub_scheme = SubScheme(
            nodes=nodes, links=links, description=description, title=title, id=_id
        )
        return sub_scheme


def contains_control_nodes(nodes_list: typing.Iterable):
    """
    Return the list of the 'control' nodes.

    :param typing.Iterable nodes_list:
    :return:
    """
    for _node in nodes_list:
        if _node.endless or contains_control_nodes(_node.upstream_nodes):
            return True
    return False


def loads(string: str, format: str) -> object:
    """load stream from the given format.

    :param str string: stream to load
    :param str format: format
    :return: object contained in the stream
    :rtype: object
    """
    if format == "literal":
        return literal_eval(string)
    elif format == "json":
        return json.loads(string)
    elif format == "pickle":
        return pickle.loads(base64.decodebytes(string.encode("ascii")))
    else:
        raise ValueError("Unknown format")


def indent(element, level=0, indent="\t"):
    """
    Indent an instance of a :class:`Element`. Based on
    (http://effbot.org/zone/element-lib.htm#prettyprint).

    """

    def empty(text):
        return not text or not text.strip()

    def indent_(element, level, last):
        child_count = len(element)

        if child_count:
            if empty(element.text):
                element.text = "\n" + indent * (level + 1)

            if empty(element.tail):
                element.tail = "\n" + indent * (level + (-1 if last else 0))

            for i, child in enumerate(element):
                indent_(child, level + 1, i == child_count - 1)

        else:
            if empty(element.tail):
                element.tail = "\n" + indent * (level + (-1 if last else 0))

    return indent_(element, level, True)


def dumps(obj, format="literal", prettyprint=False, pickle_fallback=False):
    """
    Serialize `obj` using `format` ('json' or 'literal') and return its
    string representation and the used serialization format ('literal',
    'json' or 'pickle').

    If `pickle_fallback` is True and the serialization with `format`
    fails object's pickle representation will be returned

    """
    if format == "literal":
        try:
            return (literal_dumps(obj, prettyprint=prettyprint, indent=1), "literal")
        except (ValueError, TypeError) as ex:
            if not pickle_fallback:
                raise

            _logger.debug("Could not serialize to a literal string")

    elif format == "json":
        try:
            return (json.dumps(obj, indent=1 if prettyprint else None), "json")
        except (ValueError, TypeError):
            if not pickle_fallback:
                raise

            _logger.debug("Could not serialize to a json string")

    elif format == "pickle":
        return base64.encodebytes(pickle.dumps(obj)).decode("ascii"), "pickle"

    else:
        raise ValueError("Unsupported format %r" % format)

    if pickle_fallback:
        _logger.warning("Using pickle fallback")
        return base64.encodebytes(pickle.dumps(obj)).decode("ascii"), "pickle"
    else:
        raise Exception("Something strange happened.")


# This is a subset of PyON serialization.
def literal_dumps(obj, prettyprint=False, indent=4):
    """
    Write obj into a string as a python literal.
    """
    memo = {}
    NoneType = type(None)

    def check(obj):
        if type(obj) in [int, float, bool, NoneType, str, bytes]:
            return True

        if id(obj) in memo:
            raise ValueError("{0} is a recursive structure".format(obj))

        memo[id(obj)] = obj

        if type(obj) in [list, tuple]:
            return all(map(check, obj))
        elif type(obj) is dict:
            return all(map(check, chain(iter(obj.keys()), iter(obj.values()))))
        else:
            raise TypeError(
                "{0} can not be serialized as a python " "literal".format(type(obj))
            )

    check(obj)

    if prettyprint:
        return pprint.pformat(obj, indent=indent)
    else:
        return repr(obj)
