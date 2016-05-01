import binascii
import os
from Crypto.Hash import SHA256

BLOCK_SIZE = 1024

def read_file(file_name):
	statinfo = os.stat(file_name)
	last_block_size = statinfo.st_size % BLOCK_SIZE
	with open(file_name, 'rb') as f:
		current_pos = -last_block_size
		digest = hash_last_block(f, current_pos, last_block_size)
		while current_pos > -statinfo.st_size:
			current_pos -= BLOCK_SIZE
			digest = hash_block(f, current_pos, BLOCK_SIZE, digest)			
		#print(current_pos)
		print(binascii.hexlify(digest))


def hash_last_block(f, current_pos, last_block_size):
	f.seek(current_pos,2)
	block = f.read(last_block_size)
	digest = SHA256.new(block).digest()
	return digest


def hash_block(f, current_pos, block_size, digest):
	f.seek(current_pos,2)
	block = f.read(BLOCK_SIZE)
	block += digest
	digest = SHA256.new(block).digest()
	return digest


read_file('test.mp4')
read_file('task.mp4')

