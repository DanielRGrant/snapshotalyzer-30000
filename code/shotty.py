import boto3
import click

def FilterInstances(project):
	if project:
		filters = [{'Name':'tag:project', 'Values':[project]}] #not clear in boto3 docs. may need to google
		return ec2.instances.filter(Filters=filters)
	else:
		return ec2.instances.all()

session= boto3.Session(profile_name='Shotty')
ec2 = session.resource('ec2')

@click.group()
def instances():
	'''Commands for instances'''


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



if __name__ == "__main__":
	instances()