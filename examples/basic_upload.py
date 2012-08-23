from glacier import Connection, Vault, Archive

# == Basic file upload ==
# An easy example of how to store your data in Amazon's Glacier


# The access keys can be created and found in your AWS management console 
# under "Security Credentials".
access_key = "EXAMPLE_KEY"
secret_access_key = "EXAMPLE_SECRET_KEY"

# Establish a connection to the Glacier
my_glacier = Connection(access_key,secret_access_key,region="us-east-1")

# Create a new vault (not neccessary if you already have one!)
example_vault = my_glacier.create_vault("example")

# And finally upload a file called "example.txt"
my_archive = Archive("example.txt")
example_vault.upload(my_archive)

print "Success! The ID of your just uploaded file is " + my_archive.id
