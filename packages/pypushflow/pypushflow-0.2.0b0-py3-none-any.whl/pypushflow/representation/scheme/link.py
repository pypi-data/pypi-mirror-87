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


from typing import Union
import logging

_logger = logging.getLogger(__name__)


# TODO: next lines should be removed
global next_link_free_id
next_link_free_id = 0


def get_next_link_free_id():
    global next_link_free_id
    _id = next_link_free_id
    next_link_free_id += 1
    return _id


class Link(object):
    """
    Define a link between two node with an execution order. Sink_node will be
    executed after source_node.

    :param  source_node: upstream node
    :type: Union[`.Node`,int]
    :param sink_node: downstream node
    :type: Union[`.Node`,int]
    :param str source_channel: channel name used for connection
    :param str sink_channel: channel name used for connection
    """

    _JSON_SOURCE_CHANNEL = "source_channel"
    _JSON_SINK_CHANNEL = "sink_channel"
    _JSON_SOURCE_NODE_ID = "source_node_id"
    _JSON_SINK_NODE_ID = "sink_node_id"
    _JSON_LINK_ID = "link_id"

    def __init__(
        self,
        source_node,
        sink_node,
        source_channel: str = "default",
        sink_channel: str = "default",
        id=None,
    ):
        self.id = get_next_link_free_id() if id is None else id
        if isinstance(source_node, int):
            self.source_node_id = source_node
        else:
            self.source_node_id = source_node.id

        if isinstance(sink_node, int):
            self.sink_node_id = sink_node
        else:
            self.sink_node_id = sink_node.id

        self.source_channel = source_channel
        self.sink_channel = sink_channel

    def to_json(self) -> dict:
        """

        :return: Link description to the json format
        :rtype: dict
        """
        return {
            self._JSON_LINK_ID: self.id,
            self._JSON_SOURCE_CHANNEL: self.source_channel,
            self._JSON_SINK_CHANNEL: self.sink_channel,
            self._JSON_SOURCE_NODE_ID: self.source_node_id,
            self._JSON_SINK_NODE_ID: self.sink_node_id,
        }

    @staticmethod
    def from_json(json_data: dict):
        """

        :param json_data: link description
        :return: New Link created from the json description
        :rtype: Link
        :raise ValueError: if sink or source channel missing or if link id
                           missing or if sink or source node missing
        """
        # load link id
        if Link._JSON_LINK_ID not in json_data:
            _id = None
            _logger.error("Missing link id information")
        else:
            _id = json_data[Link._JSON_LINK_ID]
        # load sink channel
        if Link._JSON_SINK_CHANNEL not in json_data:
            sink_channel = None
            _logger.error("Missing sink channel information")
        else:
            sink_channel = json_data[Link._JSON_SINK_CHANNEL]
        # load source channel
        if Link._JSON_SOURCE_CHANNEL not in json_data:
            source_channel = None
            _logger.error("Missing source channel information")
        else:
            source_channel = json_data[Link._JSON_SOURCE_CHANNEL]
        # load sink node id
        if Link._JSON_SINK_NODE_ID not in json_data:
            sink_node_id = None
            _logger.error("Missing source node id information")
        else:
            sink_node_id = json_data[Link._JSON_SINK_NODE_ID]
        # load source node id
        if Link._JSON_SOURCE_NODE_ID not in json_data:
            source_node_id = None
            _logger.error("Missing source node id information")
        else:
            source_node_id = json_data[Link._JSON_SOURCE_NODE_ID]

        if (
            sink_channel is None
            or source_channel is None
            or _id is None
            or source_node_id is None
            or sink_node_id is None
        ):
            raise ValueError("Missing core information for creating a Link")
        else:
            return Link(
                id=_id,
                sink_channel=sink_channel,
                source_channel=source_channel,
                source_node=source_node_id,
                sink_node=sink_node_id,
            )

    def __str__(self):
        return "node %s: source:(%s, %s), sink:(%s, %s)" % (
            self.id,
            self.source_node_id,
            self.source_channel,
            self.sink_node_id,
            self.sink_channel,
        )
