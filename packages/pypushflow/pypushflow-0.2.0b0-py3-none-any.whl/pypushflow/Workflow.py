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

__authors__ = ["O. Svensson", "H. Payno"]
__license__ = "MIT"
__date__ = "28/05/2019"


import pprint
import logging
from pypushflow.representation import Scheme
from pypushflow.PythonActor import PythonActor as ActorFactory
from pypushflow.StartActor import StartActor
from pypushflow.StopActor import StopActor
from pypushflow.JoinActor import JoinUntilStopSignal
from pypushflow.addon import utils
from pypushflow.addon.classes import BaseWorkflowAddOn


logger = logging.getLogger("pypushflow")


class _BaseWorkflow:
    def __init__(self, configuration):
        self._configuration = configuration or {}
        self._add_ons = []
        for add_on_class in self._getAddOnsClasses():
            self._add_ons.append(
                add_on_class(workflow=self, configuration=self._configuration)
            )

    def _getAddOnsClasses(self):
        add_ons = []
        for _, classes in utils.get_registered_add_ons_classes().items():
            for class_ in classes:
                import inspect

                if BaseWorkflowAddOn in (inspect.getmro(class_)):
                    add_ons.append(class_)
        return add_ons


class Workflow(_BaseWorkflow):
    """TODO"""

    def __init__(self, name):
        super(Workflow, self).__init__()
        self.name = name
        self.listOnErrorActor = []

    def connectOnError(self, actor):
        logger.debug(
            "In connectOnError in subModule {0}, actor name {1}".format(
                self.name, actor.name
            )
        )
        self.listOnErrorActor.append(actor)

    def triggerOnError(self, inData):
        logger.debug(pprint.pformat(inData))
        for onErrorActor in self.listOnErrorActor:
            logger.debug(onErrorActor.trigger)
            onErrorActor.trigger(inData)

    def getActorPath(self):
        return "/" + self.name


class ProcessableWorkflow(_BaseWorkflow):
    """Define a workflow that can be executed

    :param scheme: the workflow scheme
    :param configuration: some configuration / settings that can be pass to
                          the add-on.
    """

    def __init__(self, scheme, configuration=None):
        super(ProcessableWorkflow, self).__init__(configuration=configuration)
        assert isinstance(scheme, Scheme)
        self._representation = scheme
        # first load node handlers if any
        scheme.load_handlers()

        self._actor_factory = {}
        for node in self._representation.nodes:
            name = "-".join((str(node.id), node._process_pt))
            self._actor_factory[node] = ActorFactory(
                parent=None, name=name, node=node, errorHandler=None
            )

        # deal with connect
        for node in self._representation.nodes:
            actor_factory = self._actor_factory[node]
            for downstream_node in node.downstream_nodes:
                downstream_actor_factory = self._actor_factory[downstream_node]
                actor_factory.connect(downstream_actor_factory)

        # add start actor
        self._start_actor = StartActor()
        for node in self._representation.start_nodes():
            actor_factory = self._actor_factory[node]
            self._start_actor.connect(actor_factory)

        def connect_finals_nodes(actor):
            # add end actor
            for node in self._representation.final_nodes():
                actor_factory = self._actor_factory[node]
                actor_factory.connect(actor)

        self._end_actor = StopActor()

        if self.has_final_join():
            self._join_actor = JoinUntilStopSignal("stop join")
            connect_finals_nodes(self._join_actor)
            self._join_actor.connect(self._end_actor)
        else:
            connect_finals_nodes(self._end_actor)

    def has_final_join(self):
        """True if we need to send a 'end' signal before closing the workflow
        This is needed for DataList and DataWatcher
        """
        for node in self._representation.nodes:
            if node.need_stop_join:
                return True
        return False


class Converter:
    """
    Write a Workflow to a python file which can be executed later
    """

    def __init__(self, workflow, output_file):
        if not isinstance(workflow, _BaseWorkflow):
            raise TypeError("workflow should be an instance of `_BaseWorkflow`")
        self.workflow = workflow
        self.output_file = output_file

    def process(self):
        self._write_import()
        self._write_util_functions()
        self._write_main_section()
        self._write_processes_creation()
        self._write_processing()
        self._close_main_section()

    def _write_main_section(self):
        with open(self.output_file, "a") as file_:
            file_.write("\n\n")
            file_.write("def main(input_data, channel):\n")

    def _close_main_section(self):
        with open(self.output_file, "a") as file_:
            file_.write("\n\n")

    def _write_import(self):
        with open(self.output_file, "a") as file_:
            file_.write("\n")
            for node in self.workflow._representation.nodes:
                class_name, mod_name = node.get_class_name_and_module_name()
                file_.write("import {}\n".format(mod_name))
            # create logger
            file_.write(
                "{}\n{}\n".format(
                    "import logging", "_logger = logging.getLogger(__name__)"
                )
            )

    def _write_processes_creation(self):
        with open(self.output_file, "a") as file_:
            file_.write("\n")
            for node in self.workflow._representation.nodes:
                class_name, mod_name = node.get_class_name_and_module_name()
                file_.write(
                    "    process_{} = {}.{}()\n".format(node.id, mod_name, class_name)
                )
                if hasattr(node.class_instance, "set_properties"):
                    # filter some orange properties
                    properties = node.properties
                    for param in (
                        "controlAreaVisible",
                        "savedWidgetGeometry",
                        "__version__",
                        "libraryListSource",
                    ):
                        if param in properties:
                            del properties[param]
                    file_.write(
                        "    process_{}.set_properties({})\n".format(
                            node.id, properties
                        )
                    )

    def _write_processing(self):
        for _, link in self.workflow._representation.links.items():
            print(link)
            self._write_connection(
                sink_channel=link.sink_channel,
                source_channel=link.source_channel,
                sink_node_id=link.sink_node_id,
                source_node_id=link.source_node_id,
            )

        with open(self.output_file, "a") as file_:
            file_.write("\n# start processing\n")
            for node in self.workflow._representation.start_nodes():
                self._write_starter(node)

    def _write_starter(self, node):
        with open(self.output_file, "a") as file_:
            file_.write("    trigger(process_{}, input_data, channel)".format(node.id))

    def _write_connection(
        self, sink_channel, source_channel, sink_node_id, source_node_id
    ):
        with open(self.output_file, "a") as file_:
            file_.write(
                '    connect(process_{}, "{}", process_{}, '
                '"{}")\n'.format(
                    source_node_id, source_channel, sink_node_id, sink_channel
                )
            )

    def _write_util_functions(self):
        with open(self.output_file, "a") as file_:
            file_.write(self._get_utils_functions())

    def _get_utils_functions(self):
        return """
connections = {}


def get_output_channel_name(class_inst, output):
    assert hasattr(class_inst, 'outputs')
    for output_ in class_inst.outputs:
            output_name, output_type_, output_handler = output_[:3]
            if isinstance(output, output_type_):
                return output_name
    return None

def get_handler(class_inst, channel_name):
    '''Find the associate handler for channel `channel_name`'''
    if hasattr(class_inst, 'inputs'):
        for input_ in class_inst.inputs:
            input_name, input_type, input_handler = input_[:3]
            if input_name == channel_name:
                return input_handler
        return None
    return None


def connect(source_process, source_channel, sink_process, sink_channel):
    if (source_process, source_channel) not in connections:
        connections[(source_process, source_channel)] = []
    handler = get_handler(sink_process, channel_name=sink_channel)
    if handler is None:
        return TypeError('{} channel is not managed by {}'.format(sink_channel,
                                                                  sink_process))
    connections[source_process, source_channel].append((sink_process, handler))
    '''Register for each cuple process / outputtype the process and handler
    to launch when processes end'''


def trigger(process, input_data, channel_name):
    _logger.info('{} has been trigger on channel {} with input {}'
                 ''.format(process, channel_name, input_data))
    if isinstance(process, IgnoreProcess):
        output_data = input_data
        output_channel_name = channel_name
    else:
        handler = get_handler(class_inst=process, channel_name=channel_name)
        if handler is None:
            raise ValueError('Fail to find handler for {} on channel {}'
                             ''.format(process, channel_name))
        assert hasattr(process, handler)
        output_data = getattr(process, handler)(input_data)
        output_channel_name = get_output_channel_name(process, output_data)

    if (process, output_channel_name) in connections:
        for downstream in connections[(process, output_channel_name)]:
            sink_process, handler = downstream
            trigger(sink_process, output_data, output_channel_name)
        """
