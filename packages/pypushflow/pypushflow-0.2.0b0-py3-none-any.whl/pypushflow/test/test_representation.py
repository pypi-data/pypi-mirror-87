# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2019 European Synchrotron Radiation Facility
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
"""test representation is well taken into account"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/04/2020"


import unittest
from pypushflow.representation import Scheme, Node, Link
from pypushflow.Workflow import ProcessableWorkflow


def exec_(scheme, input_=None):
    """
    Simple execution procedure of a workflow.

    :param Scheme scheme:
    :param input_: workflow input if any
    """
    assert isinstance(scheme, ProcessableWorkflow)
    scheme._start_actor.trigger(input_)
    scheme._end_actor.join()
    return scheme._end_actor.out_data


class TestScheme(unittest.TestCase):
    """Test the Scheme class"""

    def setUp(self):
        self.node1 = Node(processing_pt="pypushflow.test.utils.test_function")
        self.node2 = Node(processing_pt="pypushflow.test.utils.ProcessingClass1")
        self.node3 = Node(processing_pt="pypushflow.test.utils.ProcessingClass2")
        self.link1 = Link(self.node1, self.node2, "data", "data")
        self.link2 = Link(self.node2, self.node3, "data", "data")

        self.scheme = Scheme(
            nodes=(self.node1, self.node2, self.node3), links=(self.link1, self.link2)
        )

    def testSchemeDefinition(self):
        """simple test of scheme definition"""
        self.assertEqual(len(self.scheme.nodes), 3)
        self.assertEqual(len(self.scheme.links), 2)
        self.assertTrue(self.scheme.start_nodes() == [self.node1])
        self.assertTrue(self.scheme.final_nodes() == [self.node3])

    def testProcessing(self):
        processable_workflow = ProcessableWorkflow(scheme=self.scheme)
        channel_out, out_ = exec_(
            scheme=processable_workflow, input_=(None, {"data": 0})
        )
        self.assertEqual(out_["data"], 7)


class TestNodeExecution(unittest.TestCase):
    """Insure Node.execute works"""

    def testCase1(self):
        "test that a specific function from her name can be executed"
        node = Node(processing_pt="pypushflow.test.utils.test_function")
        res = node.execute(
            node.process_pt, properties={}, input_name="data", input_data={"data": 0}
        )
        self.assertEqual(res, (None, {"data": 2}))

    def testCase2(self):
        "test that an callable class can be executed from her name"
        node = Node(processing_pt="pypushflow.test.utils.ProcessingClass1")
        res = node.execute(
            node.process_pt, properties={}, input_name="data", input_data={"data": 0}
        )
        self.assertEqual(res, (None, {"data": 4}))

    def testCase3(self):
        """Test that a class with handler can be executed"""
        node = Node(processing_pt="pypushflow.test.utils.ProcessingClass2")
        res = node.execute(
            node.process_pt, properties={}, input_name="data", input_data={"data": 0}
        )
        self.assertEqual(res, (None, {"data": 1}))

    def testCase4(self):
        script = "pypushflow.test.pythonActorTest.run"
        node = Node(processing_pt=script)
        res = node.execute(
            node.process_pt,
            properties={},
            input_name="data",
            input_data={"name": "pythonActorTest"},
        )
        self.assertEqual(res, (None, {"reply": "Hello pythonActorTest!"}))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestScheme, TestNodeExecution):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
