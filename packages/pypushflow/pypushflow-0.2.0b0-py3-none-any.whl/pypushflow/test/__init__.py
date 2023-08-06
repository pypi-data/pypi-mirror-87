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

__authors__ = ["O. Svensson", "H.Payno"]
__license__ = "MIT"
__date__ = "02/04/2020"


import unittest
from .test_representation import suite as test_representation_suite
from .test_Actors import suite as test_actors_suite
from .test_UtilsMongoDb import suite as test_mongodb_suite
from .test_Workflows import suite as test_workflows_suite


def suite(loader=None):
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_actors_suite())
    test_suite.addTest(test_representation_suite())
    test_suite.addTest(test_mongodb_suite())
    test_suite.addTest(test_workflows_suite())
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
