import boto3

prefix = 't2s-test'
region = 'us-east-1'

ec2 = boto3.client('ec2', region_name=region)
elb = boto3.client('elbv2', region_name=region)
rds = boto3.client('rds', region_name=region)
s3 = boto3.resource('s3', region_name=region)

# Terminate EC2 instances
instances = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [f'{prefix}-ec2-*']}])
ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]
if ids:
    ec2.terminate_instances(InstanceIds=ids)

# Delete EBS volumes
vols = ec2.describe_volumes(Filters=[{'Name': 'tag:Name', 'Values': [f'{prefix}-ebs-*']}, {'Name': 'status', 'Values': ['available']}])
for v in vols['Volumes']:
    ec2.delete_volume(VolumeId=v['VolumeId'])

# Release Elastic IPs
eips = ec2.describe_addresses()
for e in eips['Addresses']:
    if 'AllocationId' in e and e.get('Tags') and any(prefix in t['Value'] for t in e['Tags']):
        ec2.release_address(AllocationId=e['AllocationId'])

# Delete S3 buckets
for bucket in s3.buckets.all():
    if prefix in bucket.name:
        try:
            bucket.objects.all().delete()
            bucket.delete()
        except Exception as e:
            print(f"Failed to delete {bucket.name}: {e}")

# Delete Load Balancers
lbs = elb.describe_load_balancers()
for lb in lbs['LoadBalancers']:
    if prefix in lb['LoadBalancerName']:
        elb.delete_load_balancer(LoadBalancerArn=lb['LoadBalancerArn'])

# Delete RDS instances
rds_instances = rds.describe_db_instances()
for db in rds_instances['DBInstances']:
    if prefix in db['DBInstanceIdentifier']:
        rds.delete_db_instance(DBInstanceIdentifier=db['DBInstanceIdentifier'], SkipFinalSnapshot=True)
