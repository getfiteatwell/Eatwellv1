from database import plannerdb, tasksdb, tasks_listdb, profiledb
from bson.objectid import ObjectId
import time
import math
error = []
return_code = []

class Planner:
    def __init__(self, _id):
        if (_id is not None) and (not plannerdb.find_one({"_id": ObjectId(_id)})) and (not profiledb.find_one({"_id": ObjectId(_id)})):
            raise SystemError(error)
        else:
            self._id = _id
            class Task:
                def __init__(self):
                    class activityTask:
                        def create(self, title, description, activity_id, blocks, append=False):
                            planner_id = _id
                            if planner_id is None:
                                raise SystemError(error)

                            if not set(blocks).isdisjoint(set(tasks_listdb.find_one({"_id": ObjectId(_id)})["blocks"])):
                                if not append:
                                    return error
                                task = tasksdb.insert_one({
                                    "title": title,
                                    "description": description,
                                    "type": "activity",
                                    "activity_id": activity_id,
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": time.time()
                                })
                                tasks_listdb.update_one({"point_id": ObjectId(_id)}, {"$push": {"tasks": str(task.inserted_id)}})
                                return return_code
                            else:
                                task = tasksdb.insert_one({
                                    "title": title,
                                    "description": description,
                                    "type": "activity",
                                    "activity_id": activity_id,
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": time.time()
                                })
                                tasks_listdb.insert_one({
                                    "point_id": _id,
                                    "tasks": [str(task.inserted_id)],
                                    "blocks": blocks,
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": time.time()
                                })
                                for i in blocks:
                                    plannerdb.update_one({"_id": ObjectId(_id)}, {"$set": {""}})
                                return return_code


                    class classTask:
                        def create(self, title, description, class_id, blocks, append=False):
                            planner_id = _id
                            if planner_id is None:
                                raise SystemError(error)

                            if not set(blocks).isdisjoint(set(tasks_listdb.find_one({"_id": ObjectId(_id)})["blocks"])):
                                if not append:
                                    return error
                                task = tasksdb.insert_one({
                                    "title": title,
                                    "description": description,
                                    "type": "class",
                                    "class_id": class_id,
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": time.time()
                                })
                                tasks_listdb.update_one({"point_id": ObjectId(_id)}, {"$push": {"tasks": str(task.inserted_id)}})
                                return return_code
                            else:
                                task = tasksdb.insert_one({
                                    "title": title,
                                    "description": description,
                                    "type": "class",
                                    "activity_id": class_id,
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": time.time()
                                })
                                tasks_listdb.insert_one({
                                    "point_id": _id,
                                    "tasks": [str(task.inserted_id)],
                                    "blocks": blocks,
                                    "status": "pending",
                                    "score": 0,
                                    "timestamp": time.time()
                                })
                                return return_code


                    self.activityTask = activityTask
                    self.classTask = classTask

                def create(self, title, description, blocks, append=False):
                    planner_id = _id
                    if planner_id is None:
                        raise SystemError(error)

                    if not set(blocks).isdisjoint(set(tasks_listdb.find_one({"_id": ObjectId(_id)})["blocks"])):
                        if not append:
                            return error
                        task = tasksdb.insert_one({
                            "title": title,
                            "description": description,
                            "type": "miscellaneous",
                            "status": "pending",
                            "score": 0,
                            "timestamp": time.time()
                        })
                        tasks_listdb.update_one({"point_id": ObjectId(_id)},
                                                {"$push": {"tasks": str(task.inserted_id)}})
                        return return_code
                    else:
                        task = tasksdb.insert_one({
                            "title": title,
                            "description": description,
                            "type": "miscellaneous",
                            "status": "pending",
                            "score": 0,
                            "timestamp": time.time()
                        })
                        tasks_listdb.insert_one({
                            "point_id": _id,
                            "tasks": [str(task.inserted_id)],
                            "blocks": blocks,
                            "status": "pending",
                            "score": 0,
                            "timestamp": time.time()
                        })
                        return return_code

                def update(self, _id):
                    if tasksdb.find_one({"_id": ObjectId(_id)}):
                        tasksdb.update_one({"_id": ObjectId(_id)}, {"$set": {"status": "completed"}})
                    else:
                        return error

                def remove(self, task_id):
                    if tasksdb.find_one({"_id": ObjectId(task_id)}):
                        tasksdb.delete_one({"_id": ObjectId(task_id)})
                        tasks_listdb.update({"tasks": task_id}, {"$pull": {"tasks": task_id}})
                        tasks_listdb.delete_many({"tasks": []})

            self.Task = Task

            class get:
                def __init__(self):
                    planner_id = _id

                    class week:
                        def get(self, index):
                            week = plannerdb.find_one({"_id": ObjectId(planner_id)})["planner"][index]
                            return week

                    self.week = week

                    class day:
                        def get(self, index):
                            week_index = math.floor(index/7)
                            relative_day_index = abs(7*math.floor(index/7) - index)
                            planner = plannerdb.find_one({"_id": ObjectId(planner_id)})["planner"][week_index][relative_day_index]
                            """code to display planner"""
                            return planner
                    self.day = day

            self.get = get

    def create(self, _id=None, append=False):
        if (self._id is not None and _id is not None) and (self._id != _id):
            _id = self._id
            raise UserWarning(error)
        if append:
            if _id is None:
                if plannerdb.find_one({"_id": ObjectId(self._id)}):
                    for i in range(6):
                        weeks = []
                        for j in range(7):
                            days = []
                            for k in range(48):
                                days.append(None)
                            weeks.append(days)
                        plannerdb.update_one({"_id": ObjectId(self._id)}, {"$push": {"planner": weeks}})
                else:
                    return error
            else:
                if plannerdb.find_one({"_id": ObjectId(_id)}):
                    for i in range(6):
                        weeks = []
                        for j in range(7):
                            days = []
                            for k in range(48):
                                days.append([])
                            weeks.append(days)
                        plannerdb.update_one({"_id": ObjectId(_id)}, {"$push": {"planner": weeks}})
                        self._id = _id
                else:
                    return error

        else:
            if (self._id is None) and (_id is None):
                return error
            else:
                planner = []
                for i in range(6):
                    weeks = []
                    for j in range(7):
                        days = []
                        for k in range(48):
                            days.append([])
                        weeks.append(days)
                    planner.append(weeks)

                plannerdb.insert_one({
                    "_id": ObjectId(_id),
                    "share": [],
                    "datetime": time.time(),
                    "timestamp": time.time(),
                    "planner": planner
                })
                self._id = _id

    def get(self, _id=None):
        if (self._id is not None and _id is not None) and (self._id != _id):
            _id = self._id
            raise UserWarning(error)

        if self._id is None:
            if _id is None:
                return error
            else:
                """return with _id"""
                return "planner"
        else:
            if _id is None:
                """return with self._id"""
                return "planner"
            else:
                return error



