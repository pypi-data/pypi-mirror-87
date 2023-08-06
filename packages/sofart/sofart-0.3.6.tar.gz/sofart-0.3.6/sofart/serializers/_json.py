import json

class Serializer(object):
	def __init__(self, path):
		self.path = path

	def init(self, schema):
		self.dump(schema)

	def dump(self, dump):
		with open(self.path, 'w') as f:
			json.dump(dump, f)
		f.closed

	def load(self):
		with open(self.path, 'r') as f:
			return json.load(f)
