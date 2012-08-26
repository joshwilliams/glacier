# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import json
from request import Request
from vault import Vault

class Connection(object):
	""" Glacier API """

	def __init__(self, access_key, secret_access_key, region="us-east-1"):
		"""
            Creates a connection to a Glacier region
            
			:param access_key: Valid and activated access key
            :parm secret_access_key: Matching secret access key
        """
		self.access_key = access_key
		self.secret_access_key = secret_access_key
		self.region = region

	def get_vault(self, name):
		"""
            Returns a Vault instance
        """
		return Vault(name, self)

	def get_all_vaults(self):
		"""
            Requests a list of all vaults and returns all of them as
			initialized Vault instances.
        """
		req = self.make_request("GET", "/-/vaults")
		resp = req.send_request()

		vaults = []

		vdata = json.loads(resp.read())
		for vault in vdata["VaultList"]:
			vaults.append(self.get_vault(vault["VaultName"]))

		return vaults

	def make_request(self, method, path, header={}, signed=[], body=""):
		"""
            Returns a ready-to-use request.
        """
		return Request(	self, self.region, method, path,
						signed=signed, header=header,
						body=body)

	def create_vault(self, name):
		"""
            Requests the creation of a vault and returns upon creation
			the initialized Vault instance.
        """
		header = { "Content-Length":"0" }
		req = self.make_request("PUT", "/-/vaults/"+name, header=header)
		req.send_request()
		
		return self.get_vault(name)

	def delete_vault(self, name):
		"""
            Requests the deletion of a vault.
        """
		req = self.make_request("DELETE", "/-/vaults/"+name)
		req.send_request()
