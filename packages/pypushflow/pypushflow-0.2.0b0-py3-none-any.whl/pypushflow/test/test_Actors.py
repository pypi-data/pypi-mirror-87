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

import logging
import unittest

from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ErrorHandler import ErrorHandler
from pypushflow.ForkActor import ForkActor
from pypushflow.JoinActor import JoinActor
from pypushflow.RouterActor import RouterActor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("testPythonActor")


class TestPythonActor(unittest.TestCase):
    def test_PythonActor(self):
        script = "pypushflow.test.pythonActorTest.py"
        name = "Python Actor Test"
        actor = PythonActor(script=script, name=name)
        stopActor = StopActor()
        inData = {"name": "Ragnar"}
        actor.connect(stopActor)
        actor.trigger((None, inData))
        stopActor.join(timeout=10)
        out_channel, out_data = stopActor.out_data
        self.assertIsNotNone(out_data)
        self.assertEqual(out_data["reply"], "Hello Ragnar!")

    def test_ErrorHandler(self):
        script = "pypushflow.test.pythonErrorHandlerTest.py"
        name = "Python Error Handler Test"
        actor = PythonActor(script=script, name=name)
        errorHandler = ErrorHandler(name="Error handler")
        stopActor = StopActor()
        inData = {"name": "Ragnar"}
        actor.connect(stopActor)
        actor.connectOnError(errorHandler)
        errorHandler.connect(stopActor)
        actor.trigger((None, inData))
        stopActor.join(timeout=5)
        out_channel, out_data = stopActor.out_data
        self.assertIsNotNone(out_data)
        self.assertTrue("WorkflowException" in out_data)
        self.assertEqual(out_channel, None)

    def test_ForkAndJoinActors(self):
        start = StartActor()
        stop = StopActor()
        fork = ForkActor()
        joinActor = JoinActor()
        pythonActor1 = PythonActor(script="pypushflow.test.pythonActor1.py")
        pythonActor2 = PythonActor(script="pypushflow.test.pythonActor2.py")
        # Connections
        start.connect(fork)
        fork.connect(pythonActor1)
        fork.connect(pythonActor2)
        pythonActor1.connect(joinActor)
        joinActor.increaseNumberOfThreads()
        pythonActor2.connect(joinActor)
        joinActor.increaseNumberOfThreads()
        joinActor.connect(stop)
        # Run
        inData = {"a": 1}
        start.trigger((None, inData))
        stop.join(timeout=5)
        out_channel, out_data = stop.out_data
        self.assertIsNotNone(out_data)
        logger.info(out_data)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestPythonActor,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
