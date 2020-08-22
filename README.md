# snapshotalyzer-30000


## Configuring

Download and pip install snapshotalyzer-0.1-py3-none-any.whl
Ensure you have an AWS CLI profile configured

## Running

Command format:
`shotty <options1><group><command><options2>`

Examples:

`shotty --profile=ExampleProfile instances create_image --project=ExampleProject`

`shotty --profile=ExampleProfile volumes --project=ExampleProject`

`shotty --profile=ExampleProfile instances stop --force`



*options1*
--profile (specify config profile)
--region (override config region)

*group*

instances, volumes, snapshots 

*command*

for instances:

list (list instances)

	*options2*
	--project (instances must have tag project:<name>)

stop (stop instances)

	*options2*
	--project (specify the value for a tag project:<name>. REQUIRED unless force tag specified)
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)
	
start (start instances)

	*options2*
	--project (specify the value for a tag project:<name>. REQUIRED unless force tag specified)
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)
	
reboot (reboot instances)

	*options2*
	--project (specify the value for a tag project:<name>. REQUIRED unless force tag specified)
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)
	
snapshot (snapshot all volumes attached to instances)

	*options*
	--project (specify the value for a tag project:<name>. REQUIRED unless force tag specified)
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--age (only take snapshot if this amount of days has passed since last snapshot was taken.)
	--force (don't raise exception if project not specified)
	
create_image (create images of all instances)

	*options*
	--project (specify the value for a tag project:<name>. REQUIRED unless force tag specified)
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)	



for volumes:

list

	*options2*
	--project (instances must have tag project:<name>)

for snapshots:

list

	*options2*
	--project (instances must have tag project:<name>)




