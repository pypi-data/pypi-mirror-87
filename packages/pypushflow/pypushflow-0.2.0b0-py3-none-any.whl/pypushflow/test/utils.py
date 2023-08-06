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
"""utils for the tests"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "02/04/2020"


class ProcessingClass1:
    """Class to test the workflow. Simply add one to input"""

    def process(self, input):
        input["data"] += 4
        return input

    __call__ = process


class ProcessingClass2:
    """Class to test the workflow. Simply add self.value to input"""

    # define handler has name, type, and handler
    inputs = [["data", dict, "process"]]

    def __init__(self):
        self.value = 1

    def process(self, input):
        input["data"] += self.value
        return input

    def setConfiguration(self, config):
        self.value = config["value"]

    __call__ = process


def test_function(input):
    """Class to test the workflow. Simply add self.value to input"""
    input["data"] += 2
    return input
