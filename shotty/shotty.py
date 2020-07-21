import boto3
import botocore
import click
from datetime import datetime, timedelta, timezone





@click.option('--profile', default=None, type = str
	help="Set which user profile to run commands from")
@click.option('--region', default=None, type = str
	help="Set which user region to run commands from")
@click.group()
def cli(profile, region):
	'''Shotty manages snapshots'''
	global ec2
	try:
		if profile:
			session= boto3.Session(profile_name=profile)
		else:
			session= boto3.Session(profile_name='shotty')
		if region:
			ec2 = session.resource(service_name='ec2', region_name=region)
			list(ec2.instances.all())
		else:
			ec2 = session.resource('ec2')

	except botocore.exceptions.ProfileNotFound as e:
		raise
	except botocore.exceptions.EndpointConnectionError as e:
		raise Exception("Error: CHECK REGION TAG. {0}".format(str(e)))

	return


def FilterInstances(project):
	if project:
		filters = [{'Name':'tag:project', 'Values':[project]}] #not clear in boto3 docs. may need to google
		return ec2.instances.filter(Filters=filters)
	else:
		return ec2.instances.all()

def HasPendingSnapshots(volume):
	snapshots = list(volume.snapshots.all())
	return snapshots and snapshots[0].state == 'pending'



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
@click.option('--project', default=None, type = str,
	help="Only instances for project (tag project:<name>)")
@click.option('--force', 'force_all_instances', default=False, is_flag=True,
	help="DANGER! This flag applies the tag to ever accessible to user.")
@click.option('--instance_ids', default=[], multiple=True, type = str,
	help='''Specify instances, by instance id, to snapshot. For multiple instances 
	use the option multiple times.''')

def StopInstances(project, instance_ids, force_all_instances):
	'''Stop ec2 instances'''

	if not project and not force_all_instances:
		print("Error: Missing --project parameter. To apply command to all instances accessible to user, use --force flag")
		return
	instances= []
	instances = FilterInstances(project)

	for i in instances:

		#if user provides instance ids, skip if current id not provided
		if instance_ids and i.id not in instance_ids:
			continue

		print("Stopping instance: {0}".format(i.id))
		try:
			i.stop()
			print("Instance stopped: {0}".format(i.id))
		except botocore.exceptions.ClientError as e:
			print("Could not stop {0}: ".format(i.id), str(e))

	return


## start instances
@instances.command('start')
@click.option('--project', default=None, type = str,
	help="Only instances for project (tag project:<name>)")
@click.option('--force', 'force_all_instances', default=False, is_flag=True,
	help="DANGER! This flag applies the tag to ever accessible to user.")
@click.option('--instance_ids', default=[], multiple=True, type = str,
	help='''Specify instances, by instance id, to snapshot. For multiple instances 
	use the option multiple times.''')

def StartInstances(project, instance_ids, force_all_instances):
	'''Start ec2 instances'''

	if not project and not force_all_instances:
		print("Error: Missing --project parameter. To apply command to all instances accessible to user, use --force flag")
		return
	instances= []
	instances = FilterInstances(project)

	for i in instances:
		#if user provides instance ids, skip if current id not provided
		if instance_ids and i.id not in instance_ids:
			continue

		print("Starting instance: {0}".format(i.id))
		try:
			i.start()
			print("Instance started: {0}".format(i.id))
		except botocore.exceptions.ClientError as e:
			print("Could not start {0}: ".format(i.id), str(e))

	return


## reboot instances
@instances.command('reboot')
@click.option('--project', default=None, type = str,
	help="Only instances for project (tag project:<name>)")
@click.option('--force', 'force_all_instances', default=False, is_flag=True,
	help="DANGER! This flag applies the tag to ever accessible to user.")
@click.option('--instance_ids', default=[], multiple=True, type = str,
	help='''Specify instances, by instance id, to snapshot. For multiple instances 
	use the option multiple times.''')

def RebootInstances(project, instance_ids, force_all_instances):
	'''Reboot ec2 instances'''

	if not project and not force_all_instances:
		print("Error: Missing --project parameter. To apply command to all instances accessible to user, use --force flag")
		return
	instances= []
	instances = FilterInstances(project)

	for i in instances:

		#if user provides instance ids, skip if current id not provided
		if instance_ids and i.id not in instance_ids:
			continue

		print("Rebooting instance: {0}".format(i.id))
		try:
			i.stop()
			i.wait_until_stopped()
			i.start()
			print("Instance rebooted: {0}".format(i.id))
		except botocore.exceptions.ClientError as e:
			print("Could not rebooted {0}: ".format(i.id), str(e))

	return


## Create snapshots
@instances.command('snapshot')
@click.option('--project', default=None, type= str,
	help="Only instances for project (tag project:<name>)")
@click.option('--instance_ids', default=[], multiple=True, type = str,
	help='''Specify instances, by instance id, to snapshot. For multiple instances 
	use the option multiple times.''')
@click.option('--force', 'force_all_instances', default=False, is_flag=True,
	help="DANGER! This flag applies the tag to ever accessible to user.")
@click.option('--age', default=None, type = int,
	help="Snapshot if last snapshot of volume is older than <int> days")
def CreateSnapshots(project, instance_ids, force_all_instances, age):
	'''Stop ec2 instances'''

	if not project and not force_all_instances:
		print('''Error: Missing --project parameter. To apply command to all instances 
			accessible to user, use --force flag.''')
		return

	instances= []
	instances = FilterInstances(project) #filter users instances by project parameter


	for i in instances:

		#if user provides instance ids, skip if current id not provided
		if instance_ids and i.id not in instance_ids:
			continue

		restart=True
		if i.state["Name"]=="stopped":
			restart=False


		for v in i.volumes.all():
			if HasPendingSnapshots(v):
				print("Skipping volume {0}. Snapshot already in progress.".format(v.id))
				continue

			#check if last snapshot is older than the one set for --age option
			last_snapshot_too_recent = None
			for s in v.snapshots.all():
				if s.start_time > datetime.now(timezone.utc)-timedelta(days= int(age) ):
					last_snapshot_too_recent = True
					print("No snapshot created for instance volume {0} of instance {1}. Last snapshot created {2}".format(v.id, i.id, s.start_time.strftime("%c")))

					break
			if last_snapshot_too_recent:
				continue

			#stop instance to create snapshot
			print("Stopping instance: "+i.id)
			i.stop()
			i.wait_until_stopped()

			#create snapshot
			try:
				print("Creating snapshot of: "+v.id)
				v.create_snapshot(Description= "Snapshot created by snapshotalyzer 30000")
			except botocore.exceptions.ClientError as e:
				print("Error: Could not create snapshot. Request rate exceeded. {0}".format(str(e)))

		#restart instance
		if restart:
			print("Instance starting: "+i.id)
			i.start()

	print("Snapshotting completed!")

## list volumes
@volumes.command('list')
@click.option('--project', default=None, type = str,
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
@click.option('--project', default=None, type = str
	help="Only instances for project (tag project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True,
	help="List all snapshots for each volume, not just most recent")
def ListSnapshots(project, list_all):
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
				if s.state== "completed" and not list_all:
					break

	return


if __name__ == "__main__":
	cli()