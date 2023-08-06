# -*- coding: utf-8 -*-

class DatabaseException(RuntimeError):
	""" Database Error """

class DatabaseError(DatabaseException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class CollectionException(RuntimeError):
	""" Collection Error """

class CollectionError(CollectionException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

class QueryException(RuntimeError):
	""" Query Error """

class QueryError(QueryException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)
