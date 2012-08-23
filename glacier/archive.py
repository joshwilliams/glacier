# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import os, utils

class Archive(object):
	""" Archive API """

	def __init__(self,inp):
		# Within Amazon Glacier files use their names and get ID labels.
		# If you want to keep the interface the same it should take
		# either a file name or an ID within Glacier.
		# That's why the input is undefinied at first.

		# As stated here (http://docs.amazonwebservices.com/amazonglacier/
		# latest/dev/working-with-archives.html) archive IDs are 138 bytes long.
		# If there is the coincidence that the file name is 138 bytes long
		# the result will still be interpreted as file if it exists.
		if len(inp) == 138 and not os.path.isfile(inp):
			self.id = inp
		else:
			try:
				self.file = open(inp,"r").read()
				self.path = inp
				self.size = len(self.file)
				self.hash = utils.sha256(self.file)
				self.treehash = self.get_tree_hash()
			except IOError:
				raise IOError("file " + inp + " does not exist.")

	def get_tree_hash(self):
        # this process takes some time for bigger files, trust me
        
		chunksize = 1024*1024 # 1 MB chunks
		bytepos = 0
        
		tree = utils.sha256_tree()

		while (bytepos < self.size):
			# read the chunk portion
			tree.add_chunk(self.file[bytepos:bytepos+chunksize])

 			bytepos += chunksize  
    
		return tree.get_hash(utils.levels(self.size,chunksize))
