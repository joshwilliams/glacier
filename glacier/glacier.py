# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import httplib, time, os, utils, json
from urllib import urlencode, quote_plus
from httplib import HTTPSConnection
from utils import sha256, hmac_sha256, levels, sha256_tree
from request import Request
from vault import Vault

class Connection(object):
	""" Glacier API """

	def __init__(self,access_key,secret_access_key,region="us-east-1"):
		self.access_key = access_key
		self.secret_access_key = secret_access_key
		self.region = region

	def get_vault(self,name):
		return Vault(name,self)

	def get_all_vaults(self):

		req = self.make_request("GET","/-/vaults")
		resp = req.send_request()

		vaults = []

		vdata = json.loads(resp.read())
		for vault in vdata:
			vaults.append(self.get_vault(vault["VaultName"]))

		return vaults

	def make_request(self,method,path,header={},signed=[],body=""):
		return Request(	self,self.region,method,path,
						signed=signed,header=header,
						body=body)

	def create_vault(self,name):
		header = { "Content-Length":"0" }
		req = self.make_request("PUT","/-/vaults/"+name,header=header)
		resp = req.send_request()
		
		return self.get_vault(name)

	def delete_vault(self,name):
		req = self.make_request("DELETE","/-/vaults/"+name)
		resp = req.send_request()
