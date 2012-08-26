from glacier import Connection, Vault, Archive

# == Basic job creation ==
# Another easy example of how to get an inventory of your stored
# data in Amazon's Glacier.


# The access keys can be created and found in your AWS management console 
# under "Security Credentials".
access_key = "EXAMPLE_KEY"
secret_access_key = "EXAMPLE_SECRET_KEY"

# Establish a connection to the Glacier
my_glacier = Connection(access_key,secret_access_key,region="us-east-1")

# Get the "example" vault (has to exist)
example_vault = my_glacier.get_vault("example")

# Order the inventory
job_id = example_vault.initiate_job("inventory-retrieval")

# Wait until the job is finished (that will take at least some hours)
# You can check the progress at any time with the following snippet:
# 
# if example_vault.describe_job(job_id)["Completed"]:
#	print "The job is done :-)"
#
# However, each time you call the command you send a request which
# can potentially cost you (more) money.
#
# The more cost-efficient way is to wait until a notification arrives
# in your SNS topic.

inventory = example_vault.get_job_output(job_id)
