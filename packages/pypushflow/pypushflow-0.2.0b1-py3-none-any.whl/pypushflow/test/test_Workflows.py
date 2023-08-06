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
import logging
import unittest
from pypushflow.test.TestWorkflow import Workflow1
from pypushflow.test.TestWorkflow import Workflow2
from pypushflow.test.TestWorkflow import Workflow3

try:
    import pymongo
except ImportError:
    _has_pymongo = False
else:
    _has_pymongo = True


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("testWorkflow")


@unittest.skipUnless(_has_pymongo, "need pymongo install")
class TestWorkflows(unittest.TestCase):
    def setUp(self):
        os.environ[
            "PYPUSHFLOW_MONGOURL"
        ] = "mongodb://pybes:pybes@linsvensson.esrf.fr:27017/pybes"
        os.environ["PYPUSHFLOW_INITIATOR"] = "TestWorkflows"

    def test_Workflow1(self):
        testWorkflow1 = Workflow1("Test workflow 1")
        inData = {"name": "Jerry"}
        out_data = testWorkflow1.run(inData)
        self.assertIsNotNone(out_data)
        self.assertEqual(out_data["reply"], "Hello Jerry!")

    def test_Workflow2(self):
        testWorkflow2 = Workflow2("Test workflow 2")
        inData = {"name": "Tom"}
        out_data = testWorkflow2.run(inData)
        self.assertIsNotNone(out_data)
        self.assertTrue("WorkflowException" in out_data)

    def test_Workflow3(self):
        testWorkflow3 = Workflow3("Test workflow 3")
        inData = {"name": "Cat"}
        out_data = testWorkflow3.run(inData)
        self.assertIsNotNone(out_data)
        self.assertEqual(out_data["reply"], "Hello Cat!")

    def test_Workflow4(self):
        testWorkflow4 = Workflow2("Test workflow 4")
        inData = {"name": "Dog"}
        out_data = testWorkflow4.run(inData)
        self.assertIsNotNone(out_data)
        self.assertTrue("WorkflowException" in out_data)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestWorkflows,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
