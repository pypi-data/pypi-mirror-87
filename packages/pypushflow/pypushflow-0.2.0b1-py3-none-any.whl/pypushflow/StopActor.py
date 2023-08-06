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
import multiprocessing

# from pypushflow import UtilsMongoDb

logger = logging.getLogger("pypushflow")


class StopActor(object):
    def __init__(self, parent=None, errorHandler=None, name="Stop actor"):
        self.errorHandler = errorHandler
        self.name = name
        self.lock = multiprocessing.Lock()
        self.lock.acquire()
        self.out_data = None
        self.parent = parent

    def trigger(self, inData):
        logger.debug(
            "In trigger {0}, errorHandler = {1}".format(self.name, self.errorHandler)
        )
        # if self.parent is not None and hasattr(self.parent, 'mongoId'):
        #     UtilsMongoDb.closeMongo(self.parent.mongoId)
        if self.errorHandler is not None:
            self.errorHandler.errorHandler.stopActor.trigger(inData)
        else:
            self.out_data = inData
            self.lock.release()

    def join(self, timeout=7200):
        self.lock.acquire(timeout=timeout)
