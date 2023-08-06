#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"

import os
import pprint
import logging
import traceback
import functools
import multiprocessing
from multiprocessing.pool import Pool as _Pool
from pypushflow.AbstractActor import AbstractActor
from pypushflow.representation.scheme.node import Node


logger = logging.getLogger(__name__)


class WorkflowException(Exception):
    def __init__(self, errorMessage="", traceBack="", data={}, msg=None):
        super(WorkflowException, self).__init__(msg)
        self.errorMessage = errorMessage
        if data is None:
            data = {}
        self.data = data
        self.traceBack = traceBack


def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            out_data = func(*args, **kwargs)
        except Exception as e:
            errorMessage = "{0}".format(e)
            logger.exception(errorMessage)
            traceBack = traceback.format_exc()
            return WorkflowException(
                errorMessage=errorMessage, traceBack=traceBack, data=args[1]
            )
        return out_data

    return wrapped_func


#############################################################################
# Create no daemon processes
# See : https://stackoverflow.com/a/8963618
#


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.


class Pool(_Pool):
    Process = NoDaemonProcess


#
#
#############################################################################


@trace_unhandled_exceptions
def _exec_node(name: str, channel_name: str, data: dict, properties: dict):
    """
    Execute a node from the name of the process, input of the process and
    properties of the process

    :param str name: full name of the process to execute
    :param data: data to process
    :param properties: process properties / settings
    :return: result of Node.execute
    """
    logger.debug(
        "processing {0} on channel {1} with input {2} and {3} as "
        "properties".format(str(name), str(channel_name), str(data), str(properties))
    )
    return Node.execute(
        process_pt=name, properties=properties, input_data=data, input_name=channel_name
    )


class AsyncFactory:
    """
    TODO
    """

    def __init__(self, node, callback=None, errorCallback=None):
        self.node = node
        self.callback = callback
        self.errorCallback = errorCallback
        self.pool = Pool(1)

    def call(self, *args, **kwargs):
        logger.debug(
            "Before apply_async, func={0}, callback={1}, errorCallback={2}".format(
                self.node, self.callback, self.errorCallback
            )
        )
        logger.debug("args={0}, kwargs={1}".format(args, kwargs))
        if self.callback is None:
            self.pool.apply_async(_exec_node, args, kwargs)
        elif self.errorCallback is None:
            self.pool.apply_async(_exec_node, args, kwargs, self.callback)
        else:
            self.pool.apply_async(
                _exec_node, args, kwargs, self.callback, self.errorCallback
            )
        logger.debug("After apply_async")

    def wait(self):
        self.pool.close()
        self.pool.join()


class ActorWrapper(object):
    """
    TODO
    """

    def __init__(self, node):
        self.node = node

    @trace_unhandled_exceptions
    def run(self, in_data):
        logger.debug("In actor wrapper for {node}".format(node=self.node))
        output_channel_name, out_data = self.node.execute(in_data)
        if isinstance(out_data, WorkflowException):
            return output_channel_name, out_data
        else:
            in_data.update(out_data)
            return output_channel_name, out_data


class PythonActor(AbstractActor):
    """
    TODO

    * find a way to avoid 'duplication' of input 'script/process_pt'
      (should be done upstream)
    * I don't think script should have a default value.

    :param parent:
    :param name:
    :param errorHandler:
    :param script: script originally used
    :param node: Node from representation

    """

    def __init__(
        self,
        parent=None,
        name="Python Actor",
        errorHandler=None,
        script=None,
        node=None,
    ):
        if node is not None:
            if script is not None:
                raise ValueError(
                    "if a process pointer is provided, you "
                    "shouldn't provide a script"
                )
        elif script is None:
            raise ValueError("no script provide to the python actor")

        AbstractActor.__init__(self, parent=parent, name=name)
        self.error_handler = errorHandler
        self.list_error_handler = []
        # Import script
        self.script = script
        if script is not None:
            # module = importlib.import_module(os.path.splitext(script)[0])
            if script.endswith(".py"):
                script = "".join(os.path.splitext(script)[:-1])
            node = Node(".".join((script, "run")))
            self.actor_wrapper = ActorWrapper(node=node)
        else:
            self.actor_wrapper = ActorWrapper(node=node)

        self.in_data = None
        self.out_data = None
        self.async_factory = None

    def get_input_channel_name(self, type_):
        return self.actor_wrapper.node.get_input_channel_name(type_)

    def get_output_channel_name(self, type_):
        return self.actor_wrapper.node.get_output_channel_name(type_)

    def connectOnError(self, errorHandler):
        self.list_error_handler.append(errorHandler)

    def trigger(self, in_data):
        """
        'callback' function when this function is triggered.

        :param data: input data
        """
        channel, in_data = in_data
        logging.info("On trigger channel is " + str(channel))
        # cast data to dict if necessary
        if hasattr(in_data, "to_dict"):
            in_data = in_data.to_dict()

        self.in_data = in_data
        logger.debug(
            "In trigger {0}, inData = {1}".format(self.name, pprint.pformat(in_data))
        )
        if isinstance(in_data, WorkflowException):
            logger.error(
                "Error from previous actor! Not running actor {0}".format(self.name)
            )
            if self.error_handler is not None:
                workflowException = in_data
                oldInData = workflowException.data
                exceptionDict = {
                    "errorMessage": workflowException.errorMessage,
                    "traceBack": workflowException.traceBack.split("\n"),
                }
                oldInData["WorkflowException"] = exceptionDict
                self.triggerOnError(oldInData)

        self.async_factory = AsyncFactory(
            self.actor_wrapper.run,
            callback=self.triggerDownStreamActor,
            errorCallback=self.error_handler,
        )
        self.async_factory.call(
            self.actor_wrapper.node.process_pt,
            channel,
            in_data,
            self.actor_wrapper.node.properties,
        )

    def errorHandler(self, exception):
        logger.error("Error when running actor {0}!".format(self.name))
        workflowException = WorkflowException(
            errorMessage=exception, traceBack=None, data=None
        )
        inData = {"WorkflowException": workflowException}
        logger.error(exception)
        for errorHandler in self.list_error_handler:
            errorHandler.trigger(inData)
        if self.error_handler is not None:
            self.error_handler.triggerOnError(inData)

    def triggerDownStreamActor(self, output_last_processing=(None, {})):
        logging.warning("---------------------")
        logging.warning(output_last_processing)
        logging.warning("---------------------")
        try:
            output_channel, inData = output_last_processing
        except TypeError:
            output_channel, inData = None, output_last_processing
        logger.info(
            "In triggerDownStreamActor for {0}, Output channel is {1}, "
            "inData is {2}".format(self.name, output_channel, inData)
        )
        if isinstance(inData, WorkflowException):
            logger.error(
                "Error from previous actor! Not running down stream actors {0}".format(
                    [actor.name for actor in self.listDownStreamActor]
                )
            )
            workflowException = inData
            oldInData = workflowException.data
            exceptionDict = {
                "errorMessage": workflowException.errorMessage,
                "traceBack": workflowException.traceBack.split("\n"),
            }
            logger.warning(
                "oldInData type: {}, value: {}".format(type(oldInData), oldInData)
            )
            oldInData["WorkflowException"] = exceptionDict
            for errorHandler in self.list_error_handler:
                errorHandler.trigger((None, oldInData))
            if self.error_handler is not None:
                logger.error(
                    'Trigger on error on errorHandler "{0}"'.format(
                        self.error_handler.name
                    )
                )
                self.error_handler.triggerOnError(inData=(None, oldInData))
        else:
            out_data = {}
            if inData is not None:
                for key, value in inData.items():
                    if key in self.in_data:
                        if self.in_data[key] != value:
                            out_data[key] = value
                    else:
                        out_data[key] = value

            for downStreamActor in self.listDownStreamActor:
                downStreamActor.trigger((output_channel, inData))
