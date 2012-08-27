import unittest
from glacier import Connection, Vault, Archive
import glacier.utils

"""

	Test classes to verify that everything is working as expected.
	Before sending a pull request be sure that your fork passes
	all tests!

	(No data is being sent to/received from Amazon Glacier)

	.. note: run this script in the folder /tests/ not from outside!

"""

class TestArchive(unittest.TestCase):

	def setUp(self):
		self.archive = Archive("5KB.bin")
		self.rarchive = Archive("a"*138)
	
	def test_local_init(self):
		# Local archive
		self.assertIsInstance(self.archive.file,file)
		self.assertEqual(self.archive.path,"5KB.bin")
		self.assertEqual(self.archive.size,5120)
		eh = "a11937f356a9b0ba592c82f5290bac8016cb33a3f9bc68d3490147c158ebb10d"
		self.assertEqual(self.archive.hash,eh)
		# this has to be the same due to the size < 1 MB
		self.assertEqual(self.archive.hash,self.archive.treehash)
		self.assertFalse(hasattr(self.archive,"id"))

	def test_remote_init(self):
		# Remote archive
		self.assertEqual(self.rarchive.id,"a"*138)
		self.assertFalse(hasattr(self.rarchive,"file"))

class TestUtils(unittest.TestCase):

	def setUp(self):
		self.even_chunks = ("abc", "def")
		self.even_hashes = []

		self.odd_chunks = ("abc","def","ghi")
		self.odd_hashes = []

		for chunk in self.even_chunks:
			self.even_hashes.append(glacier.utils.sha256_digest(chunk))
	
		for chunk in self.odd_chunks:
			self.odd_hashes.append(glacier.utils.sha256_digest(chunk))

	def test_simple_hashing(self):
		self.assertEqual(	glacier.utils.sha256("a"),
							glacier.utils.sha256_digest("a").encode("hex"))

		a_hash =	 "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
		self.assertEqual(glacier.utils.sha256("a"),a_hash)

		eh = "a11937f356a9b0ba592c82f5290bac8016cb33a3f9bc68d3490147c158ebb10d"
		self.assertEqual(glacier.utils.sha256_file(open("5KB.bin","r")),eh)

	def test_tree_hashing(self):

		# Interesting side note here: In tree hashing you must not work
		# internally with hexdigested hashes! Only digested hashes
		# will work properly. That's why the hash below is the way it is
		# and not the hexdigested one:
		# c4e66df524678be2ce0ac784f9cd63c1f9f888f802808b4881114855783812a5
		# (the output has to be hexdigested, of course)

		computed_even_tree_hash = glacier.utils.get_tree_hash(self.even_hashes)
		real_even_hash = "9c04d30057b754af1b2d2d4f5675782dd61a5a659c34ee6c2af47526b66cafa6"

		self.assertEqual(computed_even_tree_hash,real_even_hash)

		computed_odd_tree_hash = glacier.utils.get_tree_hash(self.odd_hashes)
		real_odd_hash = "97fe840328e0f6eca8769ab936b29b549196a04f65ac67ed4ae41ce4d6e0bfda"

		self.assertEqual(computed_odd_tree_hash,real_odd_hash)

	def test_signing(self):
		# key = "key", value = "value"
		key_value = "90fbfcf15e74a36b89dbdb2a721d9aecffdfdddc5c83e27f7592594f71932481"
		self.assertEqual(glacier.utils.sign("key","value").encode("hex"),key_value)

class TestConnection(unittest.TestCase):

	def setUp(self):
		self.connection = Connection("abc","def")
		self.vault = self.connection.get_vault("name")
	
	def test_vault(self):
		self.assertEqual(self.vault.name,"name")
		self.assertEqual(self.vault.region,self.connection.region)
		self.assertEqual(self.vault.connection,self.connection)

	# TODO: Request integrity is not being checked yet

	def test_request(self):
		# check if errors occur while creating a request
		self.assertNotEqual(self.connection.make_request("GET","/glacier"),"")
		

if __name__ == '__main__':
	unittest.main()
