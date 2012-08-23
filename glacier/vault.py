# Glacier
# Copyright 2012 Paul Engstler
# See LICENSE for details.

import json
from request import Request

class Vault(object):
	""" Vault API """
	
	def __init__(self,name,connection):
		self.connection = connection
		self.name = name
		self.region = self.connection.region

	def describe(self):
		req = Request(self.connection,self.region,"GET","/-/vaults/"+self.name)
		resp = req.send_request()
		return json.loads(resp.read())

	def upload(self,archive,description=""):
		header = 	{ 	
							"Content-Length":str(archive.size), 
							"x-amz-sha256-tree-hash":archive.treehash, 
							"x-amz-content-sha256":archive.hash
					}

		if description:
			header["x-amz-archive-description"] = description

		req = self.connection.make_request(	"POST",
											"/-/vaults/"+self.name+"/archives",
											signed=["x-amz-content-sha256"],
											header=header,
											body=archive.file)
											
		resp = req.send_request()

		if resp.status != 201:
			raise Exception("archive could not be created",resp)

		# assign the id to the archive
		archive.id = resp.getheader("x-amz-archive-id")

		return archive

	def delete(self,archive):
		req = self.connection.make_request(	"DELETE",
											"/-/vaults/"+self.name+"/archives/"+archive.id)
		resp = req.send_request()

		if resp.status != 204:
			raise Exception("could not delete " + archive.id,resp)

	# Notifications

	def set_notifications(self,snstopic,events):
		config = { "SNSTopic":snstopic,"Events":events }
		req = self.connection.make_request(	"PUT",
											"/-/vaults/"+self.name+"/notification-configuration",
											body=json.dumps(config))
		resp = req.send_request()

		if resp.status != 204:
			raise Exception("could not set notifications",resp)

	def get_notifications(self):
		req = self.connection.make_request(	"GET",
											"/-/vaults/"+self.name+"/notification-configuration")
		resp = req.send_request()
	
		if resp.status != 200:
			raise Exception("could not get notifications",resp)

		return resp.read()

	def delete_notifications(self):
		req = self.connection.make_request(	"DELETE",
											"/-/vaults/"+self.name+"/notification-configuration")
		resp = req.send_request()

		if resp.status != 204:
			raise Exception("could not delete notifications",resp)

	# Jobs 

	def initiate_job(self,type,description="",archive=None,format="",snstopic=""):
		if type == "archive-retrieval" and not archive:
			raise Exception("no archive passed for job type 'archive-retrieval'")
		
		jobr = { "Type":type }
		if description:
			jobr["Description"] = description
		if format:
			jobr["Format"] = format
		if snstopic:
			jobr["SNSTopic"] = snstopic
		if type == "archive-retrieval":
			jobr["ArchiveId"] = archive.id

		req = self.connection.make_request(	"POST",
											"/-/vaults/"+self.name+"/jobs",
											body=json.dumps(jobr))
		resp = req.send_request()

		if resp.status != 202:
			raise Exception("could not initiate job",resp)

		return resp.getheader("x-amz-job-id")
			
	def describe_job(self,jid):
		req = self.connection.make_request(	"GET",
											"/-/vaults/"+self.name+"/jobs/"+jid,
											body=json.dumps(jobr))
		resp = req.send_request()

		if resp.status != 201:
			raise Exception("could not describe job",resp)

		return json.dumps(resp.read())

	def get_job_output(self,jid,byte_range=-1):
		header = {}
		if byte_range != -1:
			header["Range"] = byte_range

		req = self.connection.make_request(	"GET",
											"/-/vaults/"+self.name+"/jobs/"+jid+"/output",
											header=header)
		resp = req.send_request()

		if resp.status != 200:
			raise Exception("could not get job output",resp)

		return json.dumps(resp.read())

	def list_jobs(self):
		req = self.connection.make_request(	"GET",
											"/-/vaults/"+self.name+"/jobs")
		resp = req.send_request()

		if resp.status != 200:
			raise Exception("could not get list jobs",resp)

		return json.dumps(resp.read())
