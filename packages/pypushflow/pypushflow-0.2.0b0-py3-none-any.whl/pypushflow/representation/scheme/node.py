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
__date__ = "29/05/2017"

import functools
import logging
import traceback
import inspect
import importlib
from typing import Union
from importlib.machinery import SourceFileLoader

_logger = logging.getLogger(__name__)

global next_node_free_idF
next_node_free_id = 0


def get_next_node_free_id() -> int:
    global next_node_free_id
    _id = next_node_free_id
    next_node_free_id += 1
    return _id


def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            out_data = func(*args, **kwargs)
        except Exception as e:
            _logger.exception(e)
            errorMessage = "{0}".format(e)
            traceBack = traceback.format_exc()
            return WorkflowException(
                msg=errorMessage, traceBack=traceBack, data=args[1]
            )
        return out_data

    return wrapped_func


class Node(object):
    """
    Node in the `.Scheme`. Will be associated to a core process.

    :param processing_pt: pointer to a class or a function or str defining the
                          callback. If the callback is a class then the handler
                          should be defined or the class should have a default
                          'process' function that will be called by default.
    :param int id: unique id of the node.
    :param dict properties: properties of the node
    :param str luigi_task: luigi task associate to this node
    """

    need_stop_join = False
    """flag to stop the node only when receive the 'stop' signal"""

    _JSON_PROCESS_PT = "process_pt"
    _JSON_ID = "id"
    _JSON_PROPERTIES = "properties"
    _JSON_ERROR_HANDLER = "error_handler"

    def __init__(
        self,
        processing_pt,
        id: Union[None, int] = None,
        properties: Union[None, dict] = None,
        error_handler=None,
    ):
        self.id = get_next_node_free_id() if id is None else id
        """int of the node id"""
        self.properties = properties or {}
        """dict of the node properties"""
        self.upstream_nodes = set()
        """Set of upstream nodes"""
        self.downstream_nodes = set()
        """Set of downstream nodes"""
        self.__process_instance = None
        """"""
        self._process_pt = processing_pt
        """process instance"""
        self._handlers = {}
        """handlers with link name as key and callback as value.
        The default handler is store under the 'None' value"""
        self._input_type_to_name = {}
        """link input type to a signal name"""
        self._output_type_to_name = {}
        """link output type to a signal name"""
        self._error_handler = error_handler
        self.out_data = None

    def get_input_channel_name(self, data_object):
        for dtype, channel_name in self._input_type_to_name.items():
            if isinstance(data_object, dtype):
                return channel_name
        return None

    def get_output_channel_name(self, data_object):
        for dtype, channel_name in self._output_type_to_name.items():
            if isinstance(data_object, dtype):
                return channel_name
        return None

    @property
    def handlers(self) -> dict:
        return self._handlers

    @property
    def process_pt(self):
        return self._process_pt

    @property
    def class_instance(self):
        return self.__process_instance

    def isfinal(self) -> bool:
        """

        :return: True if the node is at the end of a branch.
        :rtype: bool
        """
        return len(self.downstream_nodes) is 0

    def isstart(self) -> bool:
        """

        :return: True if the node does not requires any input
        :rtype: bool
        """
        return len(self.upstream_nodes) is 0

    def get_class_name_and_module_name(self) -> tuple:
        """
        :retruns: (class name, module name)
        """
        sname = self._process_pt.rsplit(".")
        if not (len(sname) > 1):
            raise ValueError(self._process_pt + " is not recognized as a valid name")
        class_name = sname[-1]
        del sname[-1]
        mod_name = ".".join(sname)
        return class_name, mod_name

    def load_handlers(self) -> None:
        """
        load handlers from the `processing_pt` defined.
        For callable it will always be `processing_pt`.
        But for not-callable class it will be class function defined in the
        `inputs` variable.

        :raises: ValueError if unable to find sme handlers in the classes
                 definition
        """
        self._handlers.clear()
        self._input_type_to_name.clear()
        self._output_type_to_name.clear()

        assert self._process_pt is not None
        if callable(self._process_pt):
            self.__process_instance = self._process_pt
            self._handlers[None] = self._process_pt
        else:
            if not type(self._process_pt) is str:
                raise ValueError(
                    "process_pt should be a callable or path to a class or function"
                )
            else:
                class_name, module_name = self.get_class_name_and_module_name()
                if module_name.endswith(".py"):
                    # warning: in this case the file should not have any relative
                    module = SourceFileLoader(module_name, module_name).load_module()
                else:
                    module = importlib.import_module(module_name)

                class_or_fct = getattr(module, class_name)
                if inspect.isclass(class_or_fct):
                    _logger.debug("instanciate " + str(class_or_fct))
                    self.__process_instance = class_or_fct()
                else:
                    self.__process_instance = class_or_fct
                if callable(self.__process_instance):
                    self._handlers[None] = self.__process_instance
                # manage the case where a class has several input handler
                if hasattr(self.__process_instance, "inputs"):
                    for input_ in self.__process_instance.inputs:
                        input_name, input_type, input_handler = input_[:3]
                        _logger.debug(
                            "[node: %s] add input_name: %s, "
                            "input_type: %s, input_handler: %s"
                            % (self._process_pt, input_name, input_type, input_handler)
                        )
                        if str(input_type) in self._input_type_to_name:
                            raise ValueError(
                                "Several input name found for the "
                                "same input type. This case is not managed."
                            )
                        self._input_type_to_name[input_type] = input_name
                        self._handlers[input_name] = input_handler
                        # self._handlers[input_name] = getattr(self.__process_instance, input_handler)
                if hasattr(self.__process_instance, "outputs"):
                    for output_ in self.__process_instance.outputs:
                        output_name, output_type, output_handler = output_[:3]
                        _logger.debug(
                            "[node: %s] add output_name: %s, "
                            "output_type: %s, output_handler: %s"
                            % (self._process_pt, input_name, input_type, input_handler)
                        )
                        if output_type in self._output_type_to_name:
                            raise ValueError(
                                "Several output name found for the "
                                "same output type. This case is not managed."
                            )
                        self._output_type_to_name[output_type] = output_name

        if len(self._handlers) == 0:
            raise ValueError(
                "Fail to init handlers, none defined for " + str(self._process_pt)
            )

    @staticmethod
    def execute(
        process_pt, properties: dict, input_name: str, input_data: object
    ) -> tuple:
        """
        Create an instance of a node with 'process_pt' and execute it with the
        given input_name, properties and input_data.

        :param str process_pt: name of the process to execute
         (can be a module.class name, or a module.function)
        :param dict properties: process properties
        :param str input_name: name of the input data
        :param input_data: input data :warning: Should be serializable

        :return: (output data type, output data)
                 :warning: Should be serializable
        """
        node = Node(processing_pt=process_pt, properties=properties)
        node.load_handlers()
        logging.info(
            "start execution of {0} with {1} through channel {2}"
            "".format(str(process_pt), input_data, input_name)
        )
        if hasattr(node.__process_instance, "set_properties"):
            node.__process_instance.set_properties(properties)

        if input_name in node.handlers:
            if type(node.handlers[input_name]) is str:
                out = getattr(node.__process_instance, node.handlers[input_name])(
                    input_data
                )
            else:
                out = node.handlers[input_name](input_data)
        elif None in node.handlers:
            if type(node.handlers[None]) is str:
                out = getattr(node.__process_instance, node.handlers[None])(input_data)
            else:
                out = node.__process_instance(input_data)
        else:
            err = '"{0}" channel is not managed by {1}'.format(
                input_name, node._process_pt
            )
            raise KeyError(err)

        # retrieve output channel
        if out is None:
            output_channel = None
        else:
            output_channel = node.get_output_channel_name(out)

        if hasattr(out, "to_dict"):
            return output_channel, out.to_dict()
        else:
            return output_channel, out

    def to_json(self) -> dict:
        """

        :return: json description of the node
        :rtype: dict
        """
        res = {
            self._JSON_PROCESS_PT: self.process_pt,
            self._JSON_ID: self.id,
            self._JSON_PROPERTIES: self.properties,
        }
        res.update(self._get_error_handler_json())
        return res

    def _get_error_handler_json(self):
        error_handler_json = (
            self._error_handler.to_json() if self._error_handler else {}
        )
        return {self._JSON_ERROR_HANDLER: error_handler_json}

    @staticmethod
    def load_node_info_from_json(json_data: dict) -> tuple:
        """
        load fom json stream the Node Information

        :param json_data: node description
        :return: node id, properties, pointer to the process to run
        :rtype: tuple
        """
        # load properties
        if Node._JSON_PROPERTIES not in json_data:
            _logger.error("Missing node properties in json description")
            _properties = None
        else:
            _properties = json_data[Node._JSON_PROPERTIES]
            assert type(_properties) is dict
        # load id
        if Node._JSON_ID not in json_data:
            _logger.error("Missing node id in json description")
            _id = None
        else:
            _id = json_data[Node._JSON_ID]
            assert type(_id) is int
        # load process_pt
        if Node._JSON_PROCESS_PT not in json_data:
            _logger.error("Missing node process_pt in json description")
            _process_pt = None
        else:
            _process_pt = json_data[Node._JSON_PROCESS_PT]
        return _id, _properties, _process_pt

    @staticmethod
    def from_json(json_data: dict):
        """

        :param json_data: node description
        :return: New node created from the json description
        :rtype: Node
        :raise ValueError: if properties or id or processing_pt missing
        """
        _id, _properties, _process_pt = Node.load_node_info_from_json(json_data)
        if _properties is None or _id is None or _process_pt is None:
            raise ValueError(
                "Unable to create Node from json, core information " "are missing"
            )
        else:
            return Node(id=_id, properties=_properties, processing_pt=_process_pt)

    def __str__(self):
        return "node %s - %s" % (self.id, self._process_pt)


class WorkflowException(Exception):
    def __init__(self, traceBack="", data=None, msg=None):
        if data is None:
            data = {}
        super(WorkflowException, self).__init__(msg)
        self.errorMessage = msg
        self.data = data
        self.traceBack = traceBack


class ErrorHandler(Node):
    """
    TODO
    """

    def __init__(self, processing_pt, id=None, properties=None):
        super(ErrorHandler, self).__init__(
            processing_pt=processing_pt,
            id=id,
            properties=properties,
            error_handler=None,
        )

    def _get_error_handler_json(self):
        return {}
