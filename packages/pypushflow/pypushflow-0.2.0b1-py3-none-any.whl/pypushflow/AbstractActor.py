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
from pypushflow.addon import utils
from pypushflow.addon.classes import BaseActorAddOn


logger = logging.getLogger("pypushflow")


class AbstractActor(object):
    """
    TODO
    """

    def __init__(self, parent=None, name=None):
        if name is None:
            raise RuntimeError("Actor name is None!")
        self.name = name
        self.listDownStreamActor = []
        self.parent = parent
        self.actorId = None

        self._add_ons = []
        for add_on_class in self._getAddOnsClasses():
            self._add_ons.append(add_on_class())

    def connect(self, actor):
        logger.debug(
            'Connecting actor "{0}" to actor "{1}"'.format(self.name, actor.name)
        )
        self.listDownStreamActor.append(actor)

    def trigger(self, inData):
        for actor in self.listDownStreamActor:
            logger.debug(
                'In actor "{0}", triggering actor "{1}"'.format(self.name, actor.name)
            )
            self._process_pre_trigger_add_on(inData)
            actor.trigger(inData)
            self._process_post_trigger_add_on()

    def getActorPath(self):
        return self.parent.getActorPath()

    def get_addons(self):
        """Return the list of add-on that will be apply to this actor"""
        raise NotImplementedError()

    def _process_post_trigger_add_on(self):
        for add_on in self._add_ons:
            add_on.post_trigger_action(actor=self)

    def _process_pre_trigger_add_on(self, in_data):
        for add_on in self._add_ons:
            add_on.pre_trigger_action(actor=self, in_data=in_data)

    def _getAddOnsClasses(self):
        add_ons = []
        for _, classes in utils.get_registered_add_ons_classes().items():
            for class_ in classes:
                import inspect

                if BaseActorAddOn in (inspect.getmro(class_)):
                    add_ons.append(class_)
        return add_ons
