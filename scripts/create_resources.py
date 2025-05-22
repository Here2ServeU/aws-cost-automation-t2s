import boto3
import time
import string
import random

region = "us-east-1"
ec2 = boto3.client('ec2', region_name=region)
elb = boto3.client('elbv2', region_name=region)
rds = boto3.client('rds', region_name=region)
s3 = boto3.client('s3', region_name=region)

def random_suffix():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

suffix = random_suffix()

# 1. Create EC2 instance
ec2_response = ec2.run_instances(
    ImageId='ami-0c02fb55956c7d316',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': f't2s-test-ec2-{suffix}'}]
    }]
)
instance_id = ec2_response['Instances'][0]['InstanceId']

# 2. Create EBS volume
az = ec2_response['Instances'][0]['Placement']['AvailabilityZone']
volume = ec2.create_volume(
    AvailabilityZone=az,
    Size=1,
    VolumeType='gp2',
    TagSpecifications=[{
        'ResourceType': 'volume',
        'Tags': [{'Key': 'Name', 'Value': f't2s-test-ebs-{suffix}'}]
    }]
)

# 3. Allocate Elastic IP
eip = ec2.allocate_address(Domain='vpc')
ec2.create_tags(Resources=[eip['AllocationId']], Tags=[{'Key': 'Name', 'Value': f't2s-test-eip-{suffix}'}])

# 4. Create S3 bucket
bucket_name = f't2s-test-s3-{suffix}'
s3.create_bucket(Bucket=bucket_name)

# 5. Create Load Balancer
subnets = ec2.describe_subnets()['Subnets'][:2]
subnet_ids = [s['SubnetId'] for s in subnets]

elb.create_load_balancer(
    Name=f't2s-test-lb-{suffix}',
    Subnets=subnet_ids,
    Scheme='internet-facing',
    Type='application',
    IpAddressType='ipv4'
)

# 6. Create RDS instance
rds.create_db_instance(
    DBInstanceIdentifier=f't2s-test-rds-{suffix}',
    AllocatedStorage=20,
    DBName='t2stestdb',
    Engine='mysql',
    MasterUsername='admin',
    MasterUserPassword='Admin123456!',
    DBInstanceClass='db.t3.micro',
    PubliclyAccessible=True
)

print("Provisioning complete.")
