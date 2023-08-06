#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import sys
import isit
import re
import collections

from copy import copy
from itertools import tee

from sofart.operators import isadvancedquery
from sofart.operators import computequery
from sofart.logger import get_logger
from sofart.exceptions import CollectionException

REGEXP = type(re.compile('sofart'))
logger = get_logger()

#####################################################################
# String helpers
if isit.py2:
  import codecs
  def isstring(x):
    if isinstance(x, str) or isinstance(x, unicode):
      return True
    return False
else:
  def isstring(x):
    if isinstance(x, str):
      return True
    return False

if sys.version < '3':
  import codecs
  def u(x):
    return codecs.unicode_escape_decode(x)[0]
else:
  def u(x):
    return x
#####################################################################

class Collection(object):
  def __init__(self, name, path, db):
    self.name = name
    self.path = path
    self.db = db

    if not name in db.collection_names():
      self.entries = []
      self.empty = True
    else:
      self.entries = db.db[self.name]
      self.empty = False

  def __repr__(self):
      return "%s(%s)" % (self.name, self.db)

  def count(self):
    return len(self.entries)

  def rename(self, name):
    if name in self.db.collection_names():
      raise CollectionException('Collection name already taken')
    if self.db.mode == "multi":
      tmp = self.db.db
      tmp[name] = tmp.pop(self.name)
      self.db._update(tmp)
      del tmp
    elif self.db.mode == "single":
      self.db.db[name] = self.db.db.pop(self.name)
    self.name = name

  def _update(self, new_collection):
    if not isinstance(new_collection, list):
      raise CollectionException("Collection update can't be empty")
    try:
      if self.db.mode == "multi":
        tmp = self.db.db
        tmp[self.name] = new_collection
        self.db.serializer.dump(tmp)
        del tmp
      elif self.db.mode == "single":
        self.db.db[self.name] == new_collection
    except Exception as err:
      raise CollectionException('Seems to be invalid (%s)' % err)

  def save(self, record):
    if not isinstance(record, dict):
      raise CollectionException('Save is not valid')

    if self.empty:
      self.db.create_collection(self.name)
      self.entries = self.db.db[self.name]
      self.empty = False

    record = copy(record)
    if not record.get('_id', False):
      record_id = u(str(uuid.uuid4()))
      record['_id'] = record_id
    else:
      if [rec['_id'] for rec in self.entries if rec['_id'] == record['_id']]:
        raise CollectionException('Id already taken')
      else:
        record_id = u(record['_id'])
    if self.db.mode == "single":
      self.entries.append(record)
      self.db._add_id(record_id)
    elif self.db.mode == "multi":
      tmp = self.entries
      tmp.append(record)
      self._update(tmp)
      self.db._add_id(record_id)
      del tmp
    del record
    return record_id

  def remove(self, enreg_id):
    if self.db.mode == "multi":
      tmp = self.entries
      tmp[:] = [d for d in tmp if d.get('_id') != enreg_id]
      self._update(tmp)
      self.db._del_id(enreg_id)
    elif self.db.mode == "single":
      self.entries[:] = [d for d in self.entries if u(d.get('_id')) != u(enreg_id)]
      self.db._del_id(enreg_id)

  def find_one(self, spec_or_id=None):
    if spec_or_id is not None and not isinstance(spec_or_id, dict):
      spec_or_id = {"_id": spec_or_id}

    for result in self.find(spec_or_id, limit=1):
      return result

  def find(self, spec_or_id=None, limit=0):
    if spec_or_id is not None and not isinstance(spec_or_id, dict):
      spec_or_id = {"_id": spec_or_id}

    # If empty
    if spec_or_id is None:
      spec_or_id = {}

    # If not dict
    if not isinstance(spec_or_id, dict):
      raise CollectionException('Query must be dict or an id')

    current_item = 0
    tmp_entries = copy(self.entries)
    for enreg in tmp_entries:
      if current_item >= limit and limit != 0:
        break
      counter = True
      for key, value in spec_or_id.items():
        # Detect advanced query
        if isadvancedquery(enreg.get(key, None), value):
          logger.debug('!! Advanced query detected')
          if not computequery(enreg.get(key, None), value):
            counter = False
            break
        # Simple query
        elif key in enreg.keys():
        #elif enreg.get(key, True):
          if isinstance(value, REGEXP):
            logger.debug('!! Regexp detected')
            if value.match(enreg[key]) is None:
              counter = False
              break
          else:
            if not enreg[key] == value:
              counter = False
              break
        else:
          counter = False
      if counter:
        current_item += 1
        yield copy(enreg)

  def drop(self):
    self.db.drop_collection(self.name)

  def sync(self):
    self.db.sync()
