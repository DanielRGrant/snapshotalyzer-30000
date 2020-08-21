# snapshotalyzer-30000


## Configuring

shotty uses configuration created by the AWS cli. e.g.

`aws configure --profile shotty`


## Running

from ./code:
`pipenv run shotty.py <options1><group><command><options2>`

*options1*
-profile (specify config profile)
-region (override config region)

*group*
instances, volumes, snapshots 

*command*
for instances:
-list (list instances)
	*options2*
	--project (instances must have tag project:<name>)

-stop (stop instances)
	*options2*
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)
-start (start instances)
	*options2*
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)
-reboot (reboot instances)
	*options2*
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--force (don't raise exception if project not specified)
-snapshot (snapshot all volumes attached to instances)
	*options*
	--instance_ids (specify instance ids to stop. to specify multiple ids, use option multiple times.)
	--age (only take snapshot if this amount of days has passed since last snapshot was taken.)
	--force (don't raise exception if project not specified)

for volumes:
-list
	*options2*
	--project (instances must have tag project:<name>)

for snapshots:
-list
	*options2*
	--project (instances must have tag project:<name>)






to do:
-exception handling for option inputs
