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

# Create an archive for a file called "example.txt"
my_archive = Archive("example.txt")

upload_id = example_vault.initiate_multipart_upload(my_archive)
print "Multi-part upload started, id is ... " + upload_id

# That ID can be set here, to continue an upload, instead of initiating a new one above
#my_archive.multi_part_id = "example_multi_part_id"

# Upload each part
for part in range(0, my_archive.partcount):
   print "Sending part %d of %d..." % (part, my_archive.partcount)
   example_vault.upload_part(my_archive, part)

# Finally, send the complete archive command
example_vault.complete_multipart_upload(my_archive)

print "Success! The ID of your just uploaded file is " + my_archive.id
