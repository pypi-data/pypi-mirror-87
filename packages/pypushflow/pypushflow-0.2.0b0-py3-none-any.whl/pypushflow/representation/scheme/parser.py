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
__date__ = "19/08/2019"

from collections import namedtuple
import importlib
import logging

_logger = logging.getLogger(__name__)


class Parser(object):
    @staticmethod
    def scheme_load(file_, load_handlers=True):
        """

        :param file_: file containing the scheme definition
        :param bool load_handlers: try to load the handlers of each node. Used
                                   to make sure the process won't fail
        :return: :class:`Scheme`
        """
        raise NotImplementedError()

    @staticmethod
    def get_aliases():
        """

        :return: the list of aliases for a processing_pt (module.class or
                 module.function name)
        :rtype: dict
        """
        aliases = {}
        try:
            import ppfaddon
        except ImportError:
            return aliases
        else:
            import pkgutil

            for importer, modname, ispkg in pkgutil.iter_modules(ppfaddon.__path__):
                try:
                    mod_name = ".".join((ppfaddon.__name__, modname, "aliases"))
                    module = importlib.import_module(mod_name)
                except ImportError:
                    _logger.warning(
                        modname + " does not fit the add-on design, skip it"
                    )
                else:
                    if hasattr(module, "aliases"):
                        new_aliases = getattr(module, "aliases")
                        if not isinstance(new_aliases, dict):
                            raise TypeError("aliases should be an instance of dict")
                        else:
                            aliases.update(new_aliases)
        return aliases

    __main__ = scheme_load


_scheme = namedtuple(
    "_scheme", ["title", "version", "description", "nodes", "links", "annotations"]
)

_node = namedtuple(
    "_node",
    [
        "id",
        "title",
        "name",
        "position",
        "project_name",
        "qualified_name",
        "version",
        "data",
    ],
)

_data = namedtuple("_data", ["format", "data"])

_link = namedtuple(
    "_link",
    [
        "id",
        "source_node_id",
        "sink_node_id",
        "source_channel",
        "sink_channel",
        "enabled",
    ],
)

_annotation = namedtuple("_annotation", ["id", "type", "params"])

_text_params = namedtuple("_text_params", ["geometry", "text", "font"])

_arrow_params = namedtuple("_arrow_params", ["geometry", "color"])

_nxNode = namedtuple("_node", ["id", "class_", "properties", "data", "qualified_name"])

_nxNodeProperty = namedtuple("_property", ["name", "class_", "value"])

_nxLink = namedtuple("_nxLink", ["port", "relation"])

_nxRelation = namedtuple("_relation", ["id", "class_", "properties"])
