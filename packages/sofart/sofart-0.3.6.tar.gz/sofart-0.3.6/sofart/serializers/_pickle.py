try:
	import cPickle as pickle
except:
	import pickle

class Serializer(object):
	def __init__(self, path):
		self.path = path

	def init(self, schema):
		with open(self.path, 'wb') as f:
			pickle.dump(schema, f)
		f.closed

	def dump(self, dump):
		with open(self.path, 'wb') as f:
			pickle.dump(dump, f)
		f.closed

	def load(self):
		with open(self.path, 'rb') as f:
			return pickle.load(f)
