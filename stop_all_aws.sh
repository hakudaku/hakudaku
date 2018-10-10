#!/bin/bash

for i in `aws ec2 describe-instances | grep InstanceId | awk -F\" '{print $4}'`;do aws ec2 stop-instances --instance-ids $i;done
