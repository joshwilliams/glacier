# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import hashlib, hmac
from time import strftime, gmtime

def sha256(value):
	"""
		Returns the hexdigested SHA256 hash of the object.

		:type value: string or file
	"""
	if isinstance(value, str):
		return hashlib.sha256(value).hexdigest()
	elif isinstance(value, file):
		return sha256_file(value)

def sha256_digest(value):
	"""
		Returns the digested SHA256 hash of the object.

		:type value: string
	"""
	return hashlib.sha256(value).digest()

def sha256_file(file_to_hash):
	"""
		Returns the hexdigested SHA256 hash of the given file.

		:type file_to_hash: file
	"""
	# Only read small portions and return the hash
	# Again, to keep the memory footprint small
	sha256 = hashlib.sha256()
	file_to_hash.seek(0)
	while True:
		data = file_to_hash.read(256)
		if not data:
			break
		sha256.update(data)
	return sha256.hexdigest()

def hmac_sha256(key, value):
	"""
		Returns the hexdigested HMAC-SHA256 hash of the value.
	"""
	return hmac.new(key, value, hashlib.sha256).hexdigest()

def sign(key, value):
	"""
		Returns the digested HMAC-SHA256 hash of the value.
	"""
	return hmac.new(key, value.encode("utf-8"), hashlib.sha256).digest()

def get_tree_hash(chunk_hashes):
	"""
		Returns the hexdigested SHA256 tree hash of the chunks.
		
		:type chunk_hashes: list, tuple
	"""
	# shout-out to hareevs for this elegant method!

	hashes = chunk_hashes[:]

	while len(hashes) > 1:
		hashes = [sha256_digest("".join(hashes[i:i+2]))
		for i in xrange(0, len(hashes), 2)]

	return hashes[0].encode("hex")

def time(format="%Y%m%d"):
	return strftime(format, gmtime())
