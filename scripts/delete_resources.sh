#!/bin/bash
PREFIX="t2s-test"

for id in $(aws ec2 describe-instances --filters "Name=tag:Name,Values=$PREFIX-ec2-*"     --query "Reservations[].Instances[].InstanceId" --output text); do
  aws ec2 terminate-instances --instance-ids $id
done

for vol in $(aws ec2 describe-volumes --filters "Name=tag:Name,Values=$PREFIX-ebs-*"     "Name=status,Values=available" --query "Volumes[].VolumeId" --output text); do
  aws ec2 delete-volume --volume-id $vol
done

for bucket in $(aws s3api list-buckets --query "Buckets[].Name" --output text | grep $PREFIX); do
  aws s3 rm s3://$bucket --recursive
  aws s3api delete-bucket --bucket $bucket
done

for lb in $(aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(LoadBalancerName, '$PREFIX')].LoadBalancerArn" --output text); do
  aws elbv2 delete-load-balancer --load-balancer-arn $lb
done

for db in $(aws rds describe-db-instances     --query "DBInstances[?starts_with(DBInstanceIdentifier, '$PREFIX')].DBInstanceIdentifier" --output text); do
  aws rds delete-db-instance --db-instance-identifier $db --skip-final-snapshot
done
