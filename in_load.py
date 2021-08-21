#!/usr/bin/env python

import commands
import sys
import os
import re






def check_for_hosts_added_to_load(dns_hostnames_list_new): # compare current cli53 export hosts with previous export to check if any new records were added
    hosts_added_to_load = []
    with open('dns_hostnames_file', 'r') as f:
        dns_hostnames_old = f.read() # read the whole file into a single string. dns_hostnames is string which contains output of previous cli53 export
        for host in dns_hostnames_list_new: # dns_hostnames_list_new is output of current cli53 export
            if host in dns_hostnames_old: # host was there during last check, host is there now (no change).
                pass
            elif host not in dns_hostnames_old: # current cli53 export has host which was not in previous cli53 export
                hosts_added_to_load.append(host)
    check_chef(hosts_added_to_load)

def check_for_hosts_removed_from_load(dns_hostnames_list_new): # compare previous cli53 export hosts with current export to check if any new records were removed 
    host_list_previous_cli53_export = []
    hosts_removed_from_load = []
    dns_hostnames_str_new = ''.join(dns_hostnames_list_new) # convert current cli53 export list to str for easier comparision 
    with open('dns_hostnames_file', 'r') as f: # convert previous cli53 export host file to list for easier comparision
        for line in f:
            host_list_previous_cli53_export.append(line)
    for host in host_list_previous_cli53_export:
        if host in dns_hostnames_str_new: # host was there during last check, host is there now (no change).
            pass
        elif host not in dns_hostnames_str_new: # previous cli53 export has host which is not in current cli53 export 
            hosts_removed_from_load.append(host)
    
def check_chef(hosts_added_to_load):
    get_chef_record_cmd = "knife search 'chef_environment:eng AND (tags:down OR tags:nomon OR tags:standby OR tags:decom)' -i"
    (status, output) = commands.getstatusoutput(get_chef_record_cmd)
    if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(status)
    chef_hostnames_list = re.findall(r'(\S+m)\s+', output)
    chef_hostnames_list_str = ''.join(chef_hostnames_list) # convert chef host list to str for easier comparision
    for host in hosts_added_to_load:
        if host in chef_hostnames_list_str:
            hosts_added_to_load.remove(host)
    
    
    


def main():
    get_rr_cmd = 'cli53 export ahttps.com'
    (status, output) = commands.getstatusoutput(get_rr_cmd)
    if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(status)
    if os.path.exists('dns_hostnames_file'): # previously generated cli53 export list 
        dns_hostnames_list_new = re.findall(r'(\S+).+A\s+', output) # generate new cli53 export list
        check_for_hosts_added_to_load(dns_hostnames_list_new)
        check_for_hosts_removed_from_load(dns_hostnames_list_new)
    else: # initial script run. No cli53 export list exists yet.
        with open('dns_hostnames_file', 'w') as f:
            for host in dns_hostnames_list_new:
                f.write(host + '\n')
    
        

    #get_chef_record_cmd = "knife search 'chef_environment:eng AND NOT (tags:down OR tags:nomon OR tags:standby OR tags:decom)' -i"
    #(status, output) = commands.getstatusoutput(get_chef_record_cmd)
    #if status:    ## Error case, print the command's output to stderr and exit
    #    sys.stderr.write(output)
    #    sys.exit(status)
    #chef_hostnames_list = re.findall(r'(\S+m)\s+', output)

    
   

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
