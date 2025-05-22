#!/bin/bash
SUFFIX=$(date +%s | sha256sum | base64 | head -c 6)
REGION="us-east-1"

EC2_ID=$(aws ec2 run-instances --image-id ami-0c02fb55956c7d316 --count 1 --instance-type t2.micro   --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=t2s-test-ec2-$SUFFIX}]"   --query 'Instances[0].InstanceId' --output text)

AZ=$(aws ec2 describe-instances --instance-ids $EC2_ID --query "Reservations[0].Instances[0].Placement.AvailabilityZone" --output text)
aws ec2 create-volume --availability-zone $AZ --size 1 --volume-type gp2   --tag-specifications "ResourceType=volume,Tags=[{Key=Name,Value=t2s-test-ebs-$SUFFIX}]"

EIP_ALLOC=$(aws ec2 allocate-address --domain vpc --query "AllocationId" --output text)
aws ec2 create-tags --resources $EIP_ALLOC --tags Key=Name,Value=t2s-test-eip-$SUFFIX

aws s3api create-bucket --bucket t2s-test-s3-$SUFFIX --region $REGION

SUBNETS=$(aws ec2 describe-subnets --query "Subnets[:2].SubnetId" --output text)
aws elbv2 create-load-balancer --name t2s-test-lb-$SUFFIX --subnets $SUBNETS --scheme internet-facing   --type application --ip-address-type ipv4

aws rds create-db-instance --db-instance-identifier t2s-test-rds-$SUFFIX --db-instance-class db.t3.micro   --engine mysql --master-username admin --master-user-password Admin123456!   --allocated-storage 20 --publicly-accessible --db-name t2stestdb
