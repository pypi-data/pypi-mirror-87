# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2019-2020 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "22/04/2020"


import logging
import pkgutil
import inspect
import importlib

_logger = logging.getLogger(__name__)


def get_registered_add_ons():
    """Return the list of registered add-on"""
    try:
        import ppfaddon
    except ImportError:
        _logger.info("no add on found")
        return []
    else:
        modules = []
        for importer, modname, ispkg in pkgutil.iter_modules(ppfaddon.__path__):
            if ispkg:
                modules.append(modname)
        return modules


def _check_module_for_class(module, depth=0):
    classes = []
    for m in inspect.getmembers(module):

        if inspect.isclass(m[1]):
            if m[1].__module__ != "pypushflow.addon.classes":
                classes.append(m[1])

        if inspect.ismodule(m[1]):
            if inspect.isclass(m[1]):
                classes.append(m[1])
            elif hasattr(m[1], "__path__"):
                for importer, modname, ispkg in pkgutil.iter_modules(m[1].__path__):
                    module_name = module.__name__
                    submod_name = ".".join((module_name, m[0], modname))
                    try:
                        mod = importlib.import_module(submod_name)
                    except Exception:
                        pass
                    else:
                        classes.extend(
                            _check_module_for_class(module=mod, depth=depth + 1)
                        )
    return classes


def get_registered_add_ons_classes():
    """Return a dictionary with the list of registered add-on classes for each
    add-on"""
    classes = {}

    add_on_modules = get_registered_add_ons()
    for module_name in add_on_modules:
        package_name = ".".join(("ppfaddon", module_name))
        try:
            module = __import__(package_name)
        except:
            _logger.error("fail to import {}".format(package_name))
            return []

        classes[module_name] = _check_module_for_class(module=module)
    return classes


def is_add_on_class_relative_to(add_on_class, myclass):
    """Return the list of registered add-on classes"""
    return isinstance(myclass, add_on_class.target)
