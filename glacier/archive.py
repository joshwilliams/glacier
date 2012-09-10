# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import os, utils, math

class Archive(object):
	""" Archive API """

	def __init__(self, inp):
		"""
            Creates an archive instance
            
            Archives can either represent a local file instance or
			a remote id. As soon as the archive gets uploaded the 
			instance will transform.
            
			:param inp: local file name or archive id
            :type inp: string

		"""

		# Within Amazon Glacier files use their names and get ID labels.
		# If you want to keep the interface the same it should take
		# either a file name or an ID within Glacier.
		# That's why the input is undefinied at first.

		# As stated here (http://docs.amazonwebservices.com/amazonglacier/
		# latest/dev/working-with-archives.html) archive IDs are 138 bytes long.
		# If there is the coincidence that the file name is 138 bytes long
		# the result will still be interpreted as file if it exists.
	
		# If you run into trouble opening files on Mac: If you drag and drop
		# files into the editor/terminal the escaped strings wil look like
		# this: "\ ". This doesn't work for Python. Remove each backslash
		# and you will running again.

		self.partsize = 1024 * 1024 * 64 # 64M parts, because why not

		if len(inp) == 138 and not os.path.isfile(inp):
			self.id = inp
		else:
			try:
				self.file = open(inp,"r")
			except IOError:
				raise IOError("file " + inp + " does not exist.")

			self.path = inp
			self.size = os.fstat(self.file.fileno()).st_size
			self.partcount = int(math.ceil(float(self.size)/float(self.partsize)))
			self.hash = None
			self.treehash = None

	def get_hash(self):
		if not self._hash:
			self._hash = utils.sha256(self.file)
		return self._hash

	def set_hash(self, hashvalue):
		self._hash = hashvalue

	hash = property(get_hash, set_hash)

	def get_treehash(self):
		if not self._treehash:
			self._treehash = self.calculate_tree_hash()
		return self._treehash

	def set_treehash(self, hashvalue):
		self._treehash = hashvalue

	treehash = property(get_treehash, set_treehash)

	def calculate_tree_hash(self, part=None):
		"""
		Returns the tree hash of the archive, the entire file
		if the part number is not given, or just the part if so

		.. note:: only works with a local archive

		:param part: The part number if hashing just one part
		:type inp: integer
		"""
		# This process takes some time for bigger files, please be patient
		# "The progress bar is moving but the remaining time is going up!"
		# - CollegeHumor, Matrix runs on WinXP

		chunk_hashes = []
        
		chunk_size = 1024*1024 # 1 MB chunks
		if part != None:
			chunk_count = int(math.ceil(float(self.part_size(part))/float(chunk_size)))
			self.file.seek(self.partsize * part)
		else:
			chunk_count = int(math.ceil(float(self.size)/float(chunk_size)))
			self.file.seek(0)

		for _ in range(chunk_count):
			# Read and immediately hash the chunk portion, we just need
			# 32 bytes stored for each 1 MB chunk. Now that's reducing
			# the memory footprint!
			chunk_hashes.append(utils.sha256_digest(self.file.read(chunk_size)))
    
		return utils.get_tree_hash(chunk_hashes)
	
	def read_part(self, part):
		"""
            Returns the actual bytes of the requested part
		"""
		self.file.seek(self.partsize * part)
		return self.file.read(self.part_size(part))

	def part_hash(self, part):
		"""
            Returns the sha256 hashof the requested part
		"""
		return utils.sha256(self.read_part(part))

	def part_size(self, part):
		"""
            Returns the size in bytes of the requested part

			.. note:: This could use a better, less ambiguous name ... TODO

			:param part: The part number
            :type inp: integer
        """
		if part > self.partcount - 1:
			raise IndexError("archive does not contain part")

		# The last part may be smaller than partsize, naturally...
		if part == self.partcount - 1:
			return self.size - (self.partsize * part)
		else:
			return self.partsize
	
	def content_range(self, part):
		"""
            Returns the byte content range for the requested part

			:param part: The part number
            :type inp: integer
        """
		return "bytes " + str(part * self.partsize) + "-" + str((part * self.partsize) + self.part_size(part) - 1) + "/*"

