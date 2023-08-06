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

from pypushflow.Workflow import Workflow
from pypushflow.Submodel import Submodel
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
import unittest


class Workflow1(Workflow):
    """
    Workflow containing one start actor,
    one python actor and one stop actor.
    """

    def __init__(self, name):
        Workflow.__init__(self, name)
        self.startActor = StartActor(parent=self)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.test.pythonActorTest.py",
            name="Python Actor Test",
        )
        self.stopActor = StopActor(parent=self)
        self.startActor.connect(self.pythonActor)
        self.pythonActor.connect(self.stopActor)

    def run(self, inData):
        self.startActor.trigger(inData)
        self.stopActor.join(timeout=15)
        return self.stopActor.outData


class Workflow2(Workflow):
    """
    Workflow with error handling, containing one start actor,
    one python actor and one stop actor.

    The python actor throws an exception.
    """

    def __init__(self, name):
        Workflow.__init__(self, name)
        self.startActor = StartActor(parent=self)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.test.pythonErrorHandlerTest.py",
            name="Python Error Handler Test",
            errorHandler=self,
        )
        self.stopActor = StopActor(parent=self)
        self.startActor.connect(self.pythonActor)
        self.pythonActor.connect(self.stopActor)
        self.connectOnError(self.stopActor)

    def run(self, inData):
        self.startActor.trigger(inData)
        self.stopActor.join(timeout=5)
        return self.stopActor.outData


class Submodel1(Submodel):
    """
    Submodel containing one python actor.
    """

    def __init__(self, parent, name):
        Submodel.__init__(self, parent, name=name)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.test.pythonActorTest.py",
            name="Python Actor Test",
        )
        self.getPort("In").connect(self.pythonActor)
        self.pythonActor.connect(self.getPort("Out"))


class Workflow3(Workflow):
    """
    Workflow containing one start actor,
    one submodel and one stop actor.
    """

    def __init__(self, name):
        Workflow.__init__(self, name)
        self.startActor = StartActor(parent=self)
        self.submodel1 = Submodel1(parent=self, name="Submodel 1")
        self.stopActor = StopActor(parent=self)
        self.startActor.connect(self.submodel1.getPort("In"))
        self.submodel1.getPort("Out").connect(self.stopActor)

    def run(self, inData):
        self.startActor.trigger(inData)
        self.stopActor.join(timeout=15)
        return self.stopActor.outData


class Submodel2(Submodel):
    """
    Submodel containing one python actor which throws an exception.
    """

    def __init__(self, parent, name):
        Submodel.__init__(self, parent, name=name)
        self.pythonActor = PythonActor(
            parent=self,
            script="pypushflow.test.pythonErrorHandlerTest.py",
            name="Python Error Handler Test",
            errorHandler=self,
        )
        self.getPort("In").connect(self.pythonActor)
        self.pythonActor.connect(self.getPort("Out"))


class Workflow4(Workflow):
    """
    Workflow containing one start actor,
    one submodel which throws an exception and one stop actor.
    """

    def __init__(self, name):
        Workflow.__init__(self, name)
        self.startActor = StartActor()
        self.submodel2 = Submodel2("Submodel 2")
        self.stopActor = StopActor()
        self.startActor.connect(self.submodel2.getPort("In"))
        self.submodel2.getPort("Out").connect(self.stopActor)

    def run(self, inData):
        self.startActor.trigger(inData)
        self.stopActor.join(timeout=5)
        return self.stopActor.outData


def suite():
    test_suite = unittest.TestSuite()
    for ui in ():
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
