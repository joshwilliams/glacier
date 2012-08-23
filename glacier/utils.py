# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import hashlib, hmac, math
from time import strftime, gmtime

def sha256(value):
	if isinstance(value,str):
		# hash a single string
		return hashlib.sha256(value).hexdigest()
	elif isinstance(value,list) or isinstance(value,tuple):
		# hash a tuple/merge two hashes into one by hashing both of them glued together
		return hashlib.sha256("".join(value)).hexdigest()

def hmac_sha256(key,value):
       return hmac.new(key,value,hashlib.sha256).hexdigest()

def sign(key, value):
	return hmac.new(key, value.encode("utf-8"), hashlib.sha256).digest()

class sha256_tree:

	# thanks to pythonm :)
    
    def __init__(self):
        self.keys = []
        self.tree_hash = "" # only hash on command

    def add_chunk(self,data):
        self.keys.append(data)

    def build_tree(self,levels):
        if levels > 0:
            generator = self.build_tree(levels - 1)
            temp = None
            for firsthash, secondhash in generator:
                if not temp: temp = sha256((firsthash, secondhash))
                else: yield temp, sha256((firsthash, secondhash)); temp = None
            #If odd number of packets
            if temp: yield temp, None
        else:
            temp = None
            for chunk in self.keys:
                if not temp: temp = sha256(chunk)
                else: yield temp, sha256(chunk); temp = None
            if temp: yield temp, None

    def get_hash(self,levels):
        self.tree_hash = list(self.build_tree(levels))[0][0]
        return self.tree_hash

def levels(size,chunksize=1024):
	# calculate the hash "levels"
	chunks = math.ceil(float(size)/float(chunksize))
	divtwo = 0
	while chunks > 1.0:
		chunks /= 2.0
		divtwo += 1
	return divtwo

def time(format="%Y%m%d"):
	return strftime(format, gmtime())
