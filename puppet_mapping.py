#!/Users/vineetbhatia/ENV/bin/python -tt
import sys
import re
import os
from collections import defaultdict
import commands
import git
from pssh.clients import ParallelSSHClient
import time
import glob2


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    HEADER = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Script to display puppet configuration for a host


def find_puppetv2_config(host, hosts_yaml_path, hosts_yaml_regex, enforcer_path, puppet_search_module_path, puppet_repo, my_puppet_files_list):
    print bcolors.UNDERLINE
    print puppet_repo.git.checkout('master')
    print bcolors.ENDC
    print '\n'
    time.sleep(5)

    service = defaultdict(list)
    with open(os.path.abspath(hosts_yaml_path), 'r') as f:
        match = re.findall(hosts_yaml_regex, f.read(), re.DOTALL)
        f = open('tmp.txt', 'w')
        for t in match:
            f.write(' '.join(str(s) for s in t) + '\n') # For each tuple in the list, you convert all of its elements into strings, join them by spaces to form the string, and write the string with a new line to the file. Then you close the file.

    with open('tmp.txt', 'r') as f:
        service_match = re.findall(r'\s+-\s+(\S+)', f.read())
        print '{}{} has below services assigned in puppet:{}'.format(bcolors.HEADER, host, bcolors.ENDC)
        for x in service_match:
            service['a'].append(x)
        for k, dk in service.iteritems():
            for x in dk:
                print x

        for k, dk in service.iteritems():
            for x in dk:
                with open(enforcer_path, 'r') as f:
                    my_class_reg = r'^.+\("{}"\).+?include\s+(.+?)\n'.format(x)
                    class_match = re.findall(my_class_reg, f.read(), re.DOTALL)
                    print '{}\nService {} belongs to below classes:{}'.format(bcolors.HEADER, x, bcolors.ENDC)
                for c in class_match:
                    for filename in my_puppet_files_list:
                        with open(filename, 'r') as f:
                            my_regx = r'class\s+{}'.format(c)
                            match = re.findall(my_regx, f.read())
                            if match:
                                print c
                                print '{}\nPuppet manifest file where {} is defined:{}'.format(bcolors.HEADER, c, bcolors.ENDC)
                                print filename


def find_puppetv45_config(host, hosts_yaml_path, hosts_yaml_regex, service_manifest_path, infradb_search_module_path, infradb_repo, my_infradb_files_list):
    print bcolors.UNDERLINE
    print infradb_repo.git.checkout('rails4')
    print bcolors.ENDC
    print '\n'
    time.sleep(5)
    
    service = defaultdict(list)
    with open(os.path.abspath(hosts_yaml_path), 'r') as f:
        match = re.findall(hosts_yaml_regex, f.read(), re.DOTALL)
        f = open('tmp.txt', 'w')
        for t in match:
            f.write(' '.join(str(s) for s in t) + '\n')

    with open('tmp.txt', 'r') as f:
        service_match = re.findall(r'\s+-\s+(\S+)', f.read())
        print '{}{} has below services assigned in puppet:{}'.format(bcolors.HEADER, host, bcolors.ENDC)
        for x in service_match:
            service['a'].append(x)
        for k, dk in service.iteritems():
            for x in dk:
                print x

        for k, dk in service.iteritems():
            for x in dk:
                with open(service_manifest_path + x + '.pp', 'r') as f:
                    data = f.read()
                    my_class_reg = r'^.+.+?class\s+\{\s+\'(.+)\':'
                    my_class_reg_include = r'^.+.+?include\s+(.+?)\n'
                    class_match = re.findall(my_class_reg_include, data, re.DOTALL)
                    if not class_match:
                        class_match = re.findall(my_class_reg, data, re.DOTALL)
                    print '{}\nService {} belongs to below classes:{}'.format(bcolors.HEADER, x, bcolors.ENDC)
                    for c in class_match:
                        for filename in my_infradb_files_list:
                            with open(filename, 'r') as f:
                                my_regx = r'class\s+{}'.format(c)
                                match = re.findall(my_regx, f.read())
                                if match:
                                    print c
                                    print '{}\nPuppet manifest file where {} is defined:{}'.format(bcolors.HEADER, c, bcolors.ENDC)
                                    print filename


def main():
    args = sys.argv[1:]
    usage = ('puppet_mapping.py [host]\n'
             'Example: puppet_mapping.py lsv-1484')
    if not args or len(args) < 1:
        print usage
        sys.exit(1)
    hosts = [args[0]]

    # Global Vars
    home_dir = os.path.expanduser('~')
    hosts_yaml_path = '{}/git/operations/puppet/modules/puppet/files/hostinfo/hosts.yaml'.format(home_dir)
    enforcer_path = '{}/git/operations/puppet/modules/truth/manifests/enforcer.pp'.format(home_dir)
    service_manifest_path = '{}/git/operations/infradb/puppet/code/environments/production/modules/rfi/manifests/service/'.format(home_dir)
    puppet_repo_path = '{}/git/operations/puppet/'.format(home_dir)
    infradb_repo_path = '{}/git/operations/infradb/'.format(home_dir)
    puppet_search_module_path = '{}/git/operations/puppet/modules/**/*.pp'.format(home_dir)
    infradb_search_module_path = '{}/git/operations/infradb/puppet/code/environments/production/modules/**/*.pp'.format(home_dir)
    my_puppet_files_list = glob2.glob(puppet_search_module_path, recursive=True)
    my_infradb_files_list = glob2.glob(infradb_search_module_path, recursive=True)

    infradb_repo = git.Repo(infradb_repo_path)
    puppet_repo = git.Repo(puppet_repo_path)
    for host in hosts:
        hosts_yaml_regex = r'(%s):.*?services:(.*?)memory' % host

    # ssh to host to get puppet version
    client = ParallelSSHClient(hosts, timeout=5, user='vbhatia')
    output = client.run_command('puppet -V', stop_on_errors=False)
    for host, host_output in output.items():
        for line in host_output.stdout:
            host_puppet_version = line
    match = re.search(r'^2|^4|^5', host_puppet_version)
    if match.group() == '2':
        for host in hosts:
            print '{}{} is running puppet version 2.x...\n{}'.format(bcolors.HEADER, host, bcolors.ENDC)
            time.sleep(5)
            find_puppetv2_config(host, hosts_yaml_path, hosts_yaml_regex, enforcer_path, puppet_search_module_path, puppet_repo, my_puppet_files_list)
    elif match.group() == '4':
        print '{}{} is running puppet version 4.x...\n{}'.format(bcolors.HEADER, host, bcolors.ENDC)
        time.sleep(5)
        find_puppetv45_config(host, hosts_yaml_path, hosts_yaml_regex, service_manifest_path, infradb_search_module_path, my_infradb_files_list)
    elif match.group() == '5':
        print '{}{} is running puppet version 5.x...\n{}'.format(bcolors.HEADER, host, bcolors.ENDC)
        time.sleep(5)
        find_puppetv45_config(host, hosts_yaml_path, hosts_yaml_regex, service_manifest_path, infradb_search_module_path, infradb_repo, my_infradb_files_list)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
