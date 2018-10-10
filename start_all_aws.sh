#!/bin/bash

for i in `aws ec2 describe-instances | grep InstanceId | awk -F\" '{print $4}'`;do aws ec2 start-instances --instance-ids $i;done
