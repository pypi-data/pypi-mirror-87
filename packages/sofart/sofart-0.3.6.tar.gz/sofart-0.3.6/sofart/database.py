# -*- coding: utf-8 -*-
import uuid
import os
import sys
import datetime

from sofart.exceptions import DatabaseError
from sofart.collection import Collection

class Database(object):
    def __init__(self, path = None, mode = "single", serializer = "json"):
        self.init_schema = {"_infos": { "creation_date": datetime.datetime.now().isoformat(),
                                        "serializer": serializer,
                                        "total_entries": 0}}

        self.mode = mode
        self.path = path
        self.serializer_name = serializer
        self.serializer = None

        if self.mode not in ['single','multi']:
            raise DatabaseError('Invalid database mode')
        self._initialize()

    def __getattr__(self, collection):
        try:
            return self._get(collection)
        except DatabaseError:
            #self.create_collection(collection)
            return self._get(collection)

    def __getitem__(self, collection):
        return self.__getattr__(collection)

    def __repr__(self):
        return 'Database(path="%s", mode="%s")' % (self.path, self.mode)

    def _load_serializer(self):
        serializer = __import__("sofart.serializers._%s" % self.serializer_name)
        serializer = sys.modules["sofart.serializers._%s" % self.serializer_name]
        if serializer is None:
            raise DatabaseError('Failed to load %s serializer' % self.serializer_name)
        self.serializer = serializer.Serializer(self.path)

    def _load_existing_db(self):
        if self.serializer is None:
            self._load_serializer()
        if not os.path.exists(self.path):
            self.serializer.init(self.init_schema)
        try:
            self.db = self.serializer.load()
            if not isinstance(self.db , dict):
                raise DatabaseError('Seems to be corrupt or not %s object' % self.serializer)
        except:
            raise DatabaseError('Seems to be corrupt or not %s object' % self.serializer)

    def _initialize(self):
        if self.mode == "multi":
            self._load_serializer()
            self._load_existing_db()
        elif self.mode == "single":
            if self.path:
                self._load_serializer()
                self._load_existing_db()
            else:
                self.db = {}
                self.db['_infos'] = self.init_schema['_infos']

    def _update(self, new_db):
        if not isinstance(new_db, dict):
            raise DatabaseError("Database update can't be empty")
        try:
            if self.mode == "multi":
                self.serializer.dump(self.db)
            elif self.mode == "single":
                self.db = new_db
        except:
            raise DatabaseError('Update problem')

    def _add_id(self, new_id):
        if self.mode == "multi":
            tmp = self.db
            tmp['_infos']['total_entries'] += 1
            self._update(tmp)
        elif self.mode == "single":
            self.db['_infos']['total_entries'] += 1

    def _del_id(self, old_id):
        try:
            if self.mode == "multi":
                tmp = self.db
                tmp['_infos']['total_entries'] -= 1
                self._update(tmp)
            elif self.mode == "single":
                self.db['_infos']['total_entries'] -= 1
        except:
            raise DatabaseError('Id is not in database')

    def _get(self, collection_name):
        return Collection(collection_name, self.path, self)

    def rename(self, old_name, new_name):
        if not old_name in self.collection_names():
            raise DatabaseError('Collection not exist')
        if new_name in self.collection_names():
            raise DatabaseError('Collection name already taken')

        if self.mode == "multi":
            tmp = self.db
            tmp[new_name] = tmp.pop(old_name)
            self._update(tmp)
            del tmp
        elif self.mode == "single":
            self.db[new_name] = self.db.pop(old_name)

    def create_collection(self, name):
        if not name in self.collection_names():
            if self.mode == "multi":
                tmp = self.db
                tmp[name] = []
                self._update(tmp)
                del tmp
            elif self.mode == "single":
                self.db[name] = []

    def drop_collection(self, name):
        if name == "_infos":
            raise DatabaseError("Can't remove \"_infos\" database")
        try:
            if self.mode == "multi":
                tmp = self.db
                tmp['_infos']['total_entries'] -= len(tmp[name])
                del tmp[name]
                self._update(tmp)
                del tmp
            elif self.mode == "single":
                self.db['_infos']['total_entries'] -= len(self.db[name])
                del self.db[name]
        except KeyError as err:
            pass

    def collection_names(self):
        return [c for c in self.db.keys() if c != '_infos']

    def sync(self):
        if not self.path:
            raise DatabaseError('Need path')
        if self.serializer is None:
            self._load_serializer()
        self.serializer.dump(self.db)
