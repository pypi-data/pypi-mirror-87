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

from pypushflow.AbstractActor import AbstractActor


class JoinActor(AbstractActor):
    def __init__(self, parent=None, name="Join actor"):
        AbstractActor.__init__(self, parent=parent, name=name)
        self.numberOfThreads = 0
        self.listInData = []

    def increaseNumberOfThreads(self):
        self.numberOfThreads += 1

    def trigger(self, in_data):
        if in_data is None:
            channel = data = None
        else:
            channel, data = in_data
        self.listInData.append(data)
        if len(self.listInData) == self.numberOfThreads:
            newInData = {}
            for data in self.listInData:
                newInData.update(data)
            for actor in self.listDownStreamActor:
                actor.trigger((channel, data))


class JoinUntilStopSignal(AbstractActor):
    def __init__(self, name):
        self.name = name
        self.listInData = []
        self.listDownStreamActor = []
        self._nprocess_received = 0
        self._nprocess_waited = 0
        self._can_stop = False

    def connect(self, actor):
        self.listDownStreamActor.append(actor)

    def trigger(self, inData):
        if (
            type(inData) is dict
            and "sig_type" in inData
            and inData["sig_type"] == "stop"
        ):
            self._can_stop = True
            self._nprocess_waited = inData["n_process"]
        else:
            self._nprocess_received += 1

        self.listInData.append(inData)
        if self._can_stop and self._nprocess_waited <= self._nprocess_received:
            newInData = {}
            for data in self.listInData:
                newInData.update(data)
            for actor in self.listDownStreamActor:
                actor.trigger(newInData)
