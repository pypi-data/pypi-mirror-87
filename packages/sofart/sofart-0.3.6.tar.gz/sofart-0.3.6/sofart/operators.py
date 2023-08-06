# -*- coding: utf-8 -*-

from sofart.exceptions import QueryError

_01 = ['gt','lt','gte','lte']
_02 = ['all','exists','mod','ne']
_03 = ['in','nin']

_ops = _01 + _02 + _03

def isadvancedquery(value, query):
	if isinstance(query, dict):
		for key in query.keys():
			if isinstance(key, str) or isinstance(key, unicode):
				if key[0] == "$":
					if key[1:] in _ops:
						return True
	return False

def computequery(value, query):
	counter = True

	for key in query.keys():
		_key = key[1:]

		# Check exists
		if value is not None:
			if _key == "exists":
				if query[key] == False:
					return False
				break
		else:
			if _key == "exists":
				if query[key] == True:
					return False
				break
			return False

		# And check every operand

		# $gt
		if _key == "gt":
			if not (value > query[key]):
				return False
		# $lt
		elif _key == "lt":
			if not (value < query[key]):
				return False
		# $gte
		elif _key == "gte":
			if not (value >= query[key]):
				return False
		# $lte
		elif _key == "lte":
			if not (value <= query[key]):
				return False
		# $all
		elif _key == "all":
			for i in query[key]:
				if not i in value:
					return False
		# $mod
		elif _key == "mod":
			if len(query[key]) != 2:
				raise QueryError('Modulo take a list of two elements')
			if value % query[key][0] != query[key][1]:
				return False
		# $ne
		elif _key == "ne":
			if query[key] == value:
				return False
		# $in
		elif _key == "in":
			_i = False
			if not isinstance(value, list):
				value = [value]
			for i in value:
				if i in query[key]:
					_i = True
					break
			if not _i:
				return False
		# $nin
		elif _key == "nin":
			_i = True
			if not isinstance(value, list):
				value = [value]

			for i in value:
				if i in query[key]:
					_i = False
					break
			if not _i:
				return False	

	# Finally
	if counter:
		return True
	return False
