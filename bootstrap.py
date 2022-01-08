#!/usr/bin/env python

import argparse
import commands
import re
import os
import time
from shutil import copy 
import glob
import base64

def add_fw_rules(hostname, region, ticket, env, decoded_password):
    get_ip_cmd = 'dig a {} +short'.format(hostname)
    (status, output) = commands.getstatusoutput(get_ip_cmd)
    ip_list = output.split()
    ip = ip_list[0]
    iptables_cmd = 'echo {} | sudo -S iptables -A INPUT -s "{}/32" -p tcp -m multiport --dports 443 -m comment --comment "allow_{}_32_to_443" -j ACCEPT && sudo iptables -L -n |egrep {}'.format(decoded_password, ip, ip, ip)
    knife_ssh_cmd = 'knife ssh -t 15 "role:chef-server" "{}"'.format(iptables_cmd)
    os.system(knife_ssh_cmd)
    get_vault_items(hostname, region, ticket, env, decoded_password)

def get_vault_items(hostname, region, ticket, env, decoded_password):
    get_runlist_cmd = 'knife node show {}'.format(hostname)
    (status, output) = commands.getstatusoutput(get_runlist_cmd)
    match = re.search(r'Run List:\s+(.+])', output)
    app_runlist = match.group(1) 
    my_chef_dir = os.path.expanduser('~') + '/git_repos/work/OPERATIONS/chef'
    os.chdir(my_chef_dir)
    vault_item_cmd = './scripts/vault_items {} "{}"'.format(env, app_runlist)
    (status, output) = commands.getstatusoutput(vault_item_cmd)
    vault_item_list = output.split()
    vault_item_str = ' '.join(vault_item_list)
    delete_from_chef(hostname, vault_item_str, app_runlist, region, ticket, env, decoded_password)

def delete_from_chef(hostname, vault_item_str, app_runlist, region, ticket, env, decoded_password):
    chef_file_backup_path = os.path.expanduser('~') + '/decoms/decom_host_backup_files'
    backup_chef_node_cmd = 'knife node show -F json {} > {}.json'.format(hostname, hostname)
    backup_client_key_cmd = 'knife client key show -F json {} default > {}.pub'.format(hostname, hostname)
    delete_node_from_chef_cmd = 'knife node delete {} -y'.format(hostname)
    delete_client_from_chef_cmd = 'knife client delete {} -y'.format(hostname)

    # Run commands
    os.system(backup_chef_node_cmd)
    os.system(backup_client_key_cmd)
    os.system(delete_node_from_chef_cmd)
    os.system(delete_client_from_chef_cmd)

    # Copy chef backup files to backup location
    chef_node_backup_file = glob.glob('*.json')
    chef_client_key_backup_file = glob.glob('*.pub')
    for f in chef_node_backup_file:
        copy(f, chef_file_backup_path)
    for f in chef_client_key_backup_file:
        copy(f, chef_file_backup_path)
    
    bootstrap(hostname, vault_item_str, app_runlist, region, ticket, env, decoded_password)

def bootstrap(hostname, vault_item_str, app_runlist, region, ticket, env, decoded_password):
    gce_bootstrap_key_path = os.path.expanduser('~') + '/.ssh/gce_bootstrap'
    bootstrap_cmd = 'knife bootstrap -y -x chef -i {} -E {} -N {} --json-attributes \'{{"authentic8":{{"use_apt_mirrors": false}}}}\' --bootstrap-version 12 -r role[common] --sudo {} {}'.format(gce_bootstrap_key_path, env, hostname, vault_item_str, hostname)
    print bootstrap_cmd
    os.system(bootstrap_cmd)
    if 'qs' in hostname:
        knife_exec_cmd = 'knife exec -E "nodes.transform(\'fqdn:{}\') {{|n| n.normal[\'etc_environment\'][\'XRDP_ENCODE_PREFER_H264_HW\']=\'QUICKSYNC\'; n.save}}"'.format(hostname)
        os.system(knife_exec_cmd)
    add_to_runlist_cmd = 'knife node run_list add {} \'{}\''.format(hostname, app_runlist)
    os.system(add_to_runlist_cmd)
    run_chef_cmd = 'knife ssh -m {} "echo {} | sudo -Si chef-client" -t 15 --no-host-key-verify'.format(hostname, decoded_password)
    os.system(run_chef_cmd)
    apply_updates_and_reboot_cmd = 'knife ssh -m {} "echo {} | sudo -S apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::=--force-confnew --with-new-pkgs upgrade && echo {} | sudo -S systemctl reboot --force"'.format(hostname, decoded_password, decoded_password)
    os.system(apply_updates_and_reboot_cmd)
    time.sleep(300)
    os.system(run_chef_cmd)
    down_tag_it_cmd = 'knife tag create {} {} down nomon-{}'.format(hostname, region, ticket)
    os.system(down_tag_it_cmd)
    print "Bootstrap complete. Remember to remove down and nomon tags once ready to take traffic"

def main():
    parser = argparse.ArgumentParser(description="Bootstrap servers")
    parser.add_argument("hostname", help="FQDN of host being bootstrapped")
    parser.add_argument("region", help="Region tag of host being bootstrapped")
    parser.add_argument("ticket", help="Jira ticket")
    parser.add_argument("env", help="Environment of the host being Bootstrap")

    args = parser.parse_args()
    hostname = args.hostname
    region = args.region
    ticket = args.ticket
    env = args.env

    sudo_password = raw_input("sudo password:\n")
    encoded_password = base64.b64encode(sudo_password.encode("utf-8"))
    decoded_password = base64.b64decode(encoded_password).decode("utf-8")
    
    add_fw_rules(hostname, region, ticket, env, decoded_password)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
