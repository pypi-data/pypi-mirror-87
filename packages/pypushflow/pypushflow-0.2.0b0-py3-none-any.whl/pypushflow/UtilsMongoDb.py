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
__date__ = "16/10/2019"

import os
import bson
import datetime
import pymongo

from bson.objectid import ObjectId


def getDateTimeString():
    return datetime.datetime.now()


def getMongoUrl():
    return os.environ.get("PYPUSHFLOW_MONGOURL", None)


def initMongo(name):
    workflowId = None
    mongoUrl = getMongoUrl()
    if mongoUrl is not None:
        initiator = os.environ.get("PYPUSHFLOW_INITIATOR", "Unknown")
        host = os.environ.get("PYPUSHFLOW_HOST", "Unknown")
        port = os.environ.get("PYPUSHFLOW_PORT", "Unknown")
        objectId = os.environ.get("PYPUSHFLOW_OBJECTID", str(bson.objectid.ObjectId()))
        collection = pymongo.MongoClient(mongoUrl).pybes.pybes
        workflowData = {
            "_id": bson.objectid.ObjectId(objectId),
            "Request ID": objectId,
            "startTime": getDateTimeString(),
            "initiator": initiator,
            "host": host,
            "port": port,
            "name": name,
            "status": "started",
            "actors": [],
        }
        insertOneResult = collection.insert_one(workflowData)
        workflowId = insertOneResult.inserted_id
    return workflowId


def setMongoStatus(workflowId, status):
    mongoUrl = getMongoUrl()
    if mongoUrl is not None:
        collection = pymongo.MongoClient(mongoUrl).pybes.pybes
        dictWorkflow = collection.find_one({"_id": workflowId})
        dictWorkflow["status"] = status
        collection.update_one({"_id": workflowId}, {"$set": dictWorkflow}, upsert=False)


def closeMongo(workflowId):
    mongoUrl = getMongoUrl()
    if mongoUrl is not None:
        collection = pymongo.MongoClient(mongoUrl).pybes.pybes
        dictWorkflow = collection.find_one({"_id": workflowId})
        if dictWorkflow["status"] != "error":
            dictWorkflow["status"] = "finished"
        dictWorkflow["stopTime"] = getDateTimeString()
        collection.update_one({"_id": workflowId}, {"$set": dictWorkflow}, upsert=False)


def initActor(name, workflowId, actorData={}, script=None):
    actorId = None
    mongoUrl = getMongoUrl()
    if mongoUrl is not None:
        collection = pymongo.MongoClient(mongoUrl).pybes.pybes
        actorId = ObjectId()
        actor = {
            "_id": actorId,
            "startTime": getDateTimeString(),
            "name": name,
            "status": "started",
            "script": script,
        }
        actor.update(actorData)
        collection.update({"_id": workflowId}, {"$push": {"actors": actor}})
    return actorId


def addDataToActor(workflowId, actorId, actorData={}):
    mongoUrl = getMongoUrl()
    if mongoUrl is not None:
        collection = pymongo.MongoClient(mongoUrl).pybes.pybes
        dictWorkflow = collection.find_one({"_id": workflowId})
        for actor in dictWorkflow["actors"]:
            if actor["_id"] == actorId:
                actor.update(actorData)
                break
        collection.update_one({"_id": workflowId}, {"$set": dictWorkflow}, upsert=False)
