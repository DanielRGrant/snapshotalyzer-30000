import boto3
import click

def FilterInstances(project):
	if project:
		filters = [{'Name':'tag:project', 'Values':[project]}] #not clear in boto3 docs. may need to google
		return ec2.instances.filter(Filters=filters)
	else:
		return ec2.instances.all()

## Initialise session
session= boto3.Session(profile_name='shotty')
#get resources
ec2 = session.resource('ec2')



@click.group()
def cli():
	'''Shotty manages snapshots'''

@cli.group()
def instances():
	'''Commands for instances'''

@cli.group()
def volumes():
	'''Commands for volumes'''

@cli.group()
def snapshots():
	'''Commands for snapshots'''




## list instances
@instances.command('list')
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")
def ListInstances(project):
	'''List ec2 instances'''
	instances= []
	instances = FilterInstances(project)

	for i in instances:
		tags = { t['Key'] : t['Value'] for t in i.tags or [] }

		print(", ".join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'],
			i.state['Name'],
			i.public_dns_name,
			str(tags)
			)))
	return

## stop instances
@instances.command('stop')
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")

def StopInstances(project):
	'''Stop ec2 instances'''
	instances= []
	instances = FilterInstances(project)

	for i in instances:
		i.stop()

	return


## start instances
@instances.command('start')
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")

def StartInstances(project):
	'''Stop ec2 instances'''
	instances= []
	instances = FilterInstances(project)

	for i in instances:
		i.start()

	return





## list volumes
@volumes.command('list')
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")
def ListVolumes(project):
	'''List ec2 instances'''
	instances= []
	instances = FilterInstances(project)

	for i in instances:
		for v in i.volumes.all():
			print(", ".join((
			i.id,
			v.id,
			v.state,
			str(v.size)+ "GiB"
			)))
	return



## list snapshots
@snapshots.command('list')
@click.option('--project', default=None,
	help="Only instances for project (tag project:<name>)")
def ListSnapshots(project):
	'''List ec2 instances'''

	instances = []
	instances = FilterInstances(project)

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(", ".join((
					i.id,
					v.id,
					s.id,
					s.start_time.strftime("%c"),
					str(s.volume_size)+"GiB",
					s.state,
					s.progress
					)))
	return


if __name__ == "__main__":
	cli()