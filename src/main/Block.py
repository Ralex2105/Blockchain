import json
import random
import string
from hashlib import sha256


class Block:
    def __init__(self, index, prev_hash, nonce, host):
        self.index = index
        self.prev_hash = prev_hash
        self.hash = None
        self.data = None
        self.nonce = nonce
        self.host = host,
        self.generate_random_data(256)
        self.generate_hash()

    def generate_random_data(self, length):
        self.data = ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def generate_hash(self):
        current_string = str(self.index) + self.prev_hash + self.data + str(self.nonce)
        c_hash = sha256(current_string.encode('utf-8'))
        while c_hash.hexdigest()[-4:] != "0000":
            self.nonce += random.randint(1, 30)
            current_string = str(self.index) + self.prev_hash + self.data + str(self.nonce)
            c_hash = sha256(current_string.encode('utf-8'))
        self.hash = c_hash.hexdigest()

    def block_to_json(self):
        jsondict = {
            'This block generated by Node ': self.host,
            'index': self.index,
            'hash': self.hash,
            'prev_hash': self.prev_hash,
            'data': self.data,
            'nonce': self.nonce
        }
        return json.dumps(jsondict)


def create_genesis():
    return create_new_block(0, 'GENESIS', 1, -1).block_to_json()


def create_new_block(index, prev_hash, nonce_type, host):
    return Block(index, prev_hash, nonce_type, host)
