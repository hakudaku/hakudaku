#!/usr/bin/env python

import argparse
import commands
import sys
import re
import os
from datetime import date
from datetime import timedelta

def delete_from_chef_only(hostname):
    backup_chef_node_cmd = 'knife node show -F json {} > {}.json'.format(hostname, hostname)
    backup_client_key_cmd = 'knife client key show -F json {} default > {}.pub'.format(hostname, hostname)
    delete_node_from_chef_cmd = 'knife node delete {} -y'.format(hostname)
    delete_client_from_chef_cmd = 'knife client delete {} -y'.format(hostname)
    
    # Run commands
    os.system(backup_chef_node_cmd)
    os.system(backup_client_key_cmd)
    os.system(delete_node_from_chef_cmd)
    os.system(delete_client_from_chef_cmd)

def stop_instance(hostname, gcp_hostname, ticket, zone, project):
    decom_date = date.today() + timedelta(7)
    print 'Stopping instance {}!!'.format(hostname)
    create_tags_cmd = 'knife tag create {} down nomon-{} decom-{}'.format(hostname, ticket, decom_date)
    shutdown_gcp_instance_cmd = 'gcloud compute instances stop {} --zone {} --project {} --quiet'.format(gcp_hostname, zone, project)
    create_snapshot_cmd = 'gcloud compute disks snapshot {} --zone {} --project {}'.format(gcp_hostname, zone, project)
    
    # Run commands
    os.system(create_tags_cmd)
    os.system(shutdown_gcp_instance_cmd)
    os.system(create_snapshot_cmd)

def delete_instance(hostname, gcp_hostname, aws_hostname, region, zone, project):
    print 'Deleting instance {}!!'.format(hostname)
    delete_gcp_instance_cmd = 'gcloud compute instances delete {} --zone {} --project {} --quiet'.format(gcp_hostname, zone, project)
    backup_chef_node_cmd = 'knife node show -F json {} > {}.json'.format(hostname, hostname)
    backup_client_key_cmd = 'knife client key show -F json {} default > {}.pub'.format(hostname, hostname)
    delete_node_from_chef_cmd = 'knife node delete {} -y'.format(hostname)
    delete_client_from_chef_cmd = 'knife client delete {} -y'.format(hostname)
    delete_route53_rr_cmd = 'cli53 rrdelete authentic8.com {} A'.format(aws_hostname)
 
    # Check if ip is static
    is_static = 'gcloud compute --project "{}" addresses list --filter="name:({}) region:({})"'.format(project, gcp_hostname, region)
    (status, output) = commands.getstatusoutput(is_static)
    if "Listed 0 items" in output:
        print 'Host {} does not have static ip assigned'.format(hostname)
    else:
        delete_static_ip_cmd = 'gcloud compute addresses delete {} --region {} --project {} --quiet'.format(gcp_hostname, region, project)
        os.system(delete_static_ip_cmd)
    
    # Run commands
    os.system(delete_gcp_instance_cmd)
    os.system(backup_chef_node_cmd)
    os.system(backup_client_key_cmd)
    os.system(delete_node_from_chef_cmd)
    os.system(delete_client_from_chef_cmd)
    os.system(delete_route53_rr_cmd)
    
def main():
    parser = argparse.ArgumentParser(description="Decom of GCP hosted VM instances")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("hostname", help="FQDN of host being decom'd")
    parser.add_argument("ticket", help="Jira ticket number associated with decom")
    parser.add_argument("zone", help="GCP zone: e.g. us-central1-f")
    group.add_argument("-s", "--stop", help="Stop instance", action="store_true")
    group.add_argument("-d", "--delete", help="Delete instance", action="store_true")
    group.add_argument("-c", "--chef_removal_only", help="Delete from chef only", action="store_true")

    args = parser.parse_args()
    hostname = args.hostname
    ticket = args.ticket
    zone = args.zone
    region = zone[:-2]
    gcp_hostname = hostname.replace('.', '-')
    aws_hostname = hostname.replace('.authentic8.com', '')

    if 'eng' in hostname:
        project = 'a8eng-1'
    elif 'qa' in hostname:
        project = 'a8qa-1'
    else:
        project = 'a8prod-1'    

    if args.stop:
        stop_instance(hostname, gcp_hostname, ticket, zone, project)
    elif args.delete:
        delete_instance(hostname, gcp_hostname, aws_hostname, region, zone, project)
    elif args.chef_removal_only:
        delete_from_chef_only(hostname)
   


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
