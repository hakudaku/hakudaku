#!/Users/vineetbhatia/ENV/bin/python -tt

import commands
import re
import argparse
import os
from pssh.clients import ParallelSSHClient
import logging
from socket import timeout
import time
import sys


def aws_start(instance_id, my_aws_user, my_aws_key, update_dns_zone_cmd):
    my_aws_start_cmd = 'aws ec2 start-instances --instance-ids {}'.format(instance_id)
    os.system(my_aws_start_cmd)
    # Wait 30 sec after start cmd. The public DNS name will not be available until instance is fully started
    time.sleep(30)
    # get the new hostname/ip after aws start
    my_cmd = 'aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicDnsName" --output=text'
    (status, out) = commands.getstatusoutput(my_cmd)
    # convert hostname to list since ParallelSSHClient needs hostname in list data structure
    new_aws_hostname = out.split()
    update_dns_zone(new_aws_hostname, my_aws_user, my_aws_key, update_dns_zone_cmd)


def update_dns_zone(new_aws_hostname, my_aws_user, my_aws_key, update_dns_zone_cmd):
    print 'Updating DNS zone file...'
    print update_dns_zone_cmd
    client = ParallelSSHClient(new_aws_hostname, timeout=5, user=my_aws_user, pkey=my_aws_key)
    client.run_command(update_dns_zone_cmd, sudo=True)
    # convert new_aws_hostname back to string before passing to update_bash
    new_aws_hostname_str = ''.join(new_aws_hostname)
    update_bash(new_aws_hostname_str)

def update_bash(new_aws_hostname_str):
    my_bash = os.path.expanduser('~') + '/.bashrc'
    my_out_file = 'out.txt'
    # if line in .bashrc matches the regexs, do the replace operation (only if ip has changed), else copy line as is
    with open(my_bash, 'r') as fin:
        with open(os.path.expanduser('~') + '/' + my_out_file, 'w') as fout:
            for line in fin:
                match = re.search(r'(ec2.+)"', line)
                if match:
                    if match.group(1) == new_aws_hostname_str:
                        print 'IP has not changed. Nothing to do.'
                        sys.exit(1)
                    if match.group(1) != new_aws_hostname_str:
                        string_to_replace = match.group(1)
                        fout.write(line.replace(string_to_replace, 'ubuntu@' + new_aws_hostname_str))
                else:
                    fout.write(line)
# Rename out file to .bashrc
    os.rename(os.path.expanduser('~') + '/' + my_out_file, my_bash)


def aws_stop(instance_id):
    my_aws_stop_cmd = 'aws ec2 stop-instances --instance-ids {}'.format(instance_id)
    os.system(my_aws_stop_cmd)


def main():
    parser = argparse.ArgumentParser(description="Start/stop aws instances")
    parser.add_argument("-start", help="Start instance", action="store_true")
    parser.add_argument("-stop", help="Stop instance", action="store_true")
    args = parser.parse_args()

    my_home_dir = os.path.expanduser('~')
    my_aws_user = 'ubuntu'
    my_aws_key = '{}/.ssh/aws.pem'.format(my_home_dir)
    update_dns_zone_cmd = '/usr/bin/python3 /home/ubuntu/bin/zone_update.py'
    
    my_aws_get_instance_cmd = 'aws ec2 describe-instances | grep InstanceId'
    (status, output) = commands.getstatusoutput(my_aws_get_instance_cmd)

    match = re.search(r'\".*(\w\-\S+)\"', output)

    if match:
        instance_id = match.group(1)

    if args.start:
        aws_start(instance_id, my_aws_user, my_aws_key, update_dns_zone_cmd)
    if args.stop:
        aws_stop(instance_id)


    
if __name__ == '__main__':
    main()

