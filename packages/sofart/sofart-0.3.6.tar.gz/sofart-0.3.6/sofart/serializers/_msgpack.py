import msgpack

class Serializer(object):
    def __init__(self, path):
        self.path = path
        self.unpacker = msgpack.Unpacker(use_list=True, encoding='utf-8')
        self.packer = msgpack.Packer(encoding='utf-8')

    def init(self, schema):
        self.dump(schema)

    def dump(self, dump):
        with open(self.path, 'wb') as f:
            f.write(self.packer.pack(dump))
        f.closed

    def load(self):
        with open(self.path, 'rb') as f:
            self.unpacker.feed(f.read())
        f.closed
        return self.unpacker.unpack()
