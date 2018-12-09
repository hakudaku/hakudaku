#!/Users/vineetbhatia/ENV/bin/python -tt
import sys
from pssh.clients import ParallelSSHClient
import paramiko, base64
import logging
import os
import re

def ssh(cluster, cmd, web_svc_port_dict):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(cluster, user='vbhatia')
  for key in web_svc_port_dict.keys():
    output = client.run_command(cmd + ' ' + web_svc_port_dict[key], stop_on_errors=True)
    for host in output:
      for line in output[host]['stdout']:
        if 'succeeded' in line:
          print '%s %s %s connect successful' % (host, key, web_svc_port_dict[key])
        else:
          print '%s %s %s connect failed' % (host, key, web_svc_port_dict[key])

def scp(host, iws_config_path_remote, iws_config_path_local):
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host, username='vbhatia')

  sftp = client.open_sftp()
  sftp.get(iws_config_path_remote, iws_config_path_local)
  sftp.close()

def get_service_port_mapping_from_cfg_file(iws_config_path_local, cluster, cmd):
  web_svc_port_dict = {}
  f = open(os.path.abspath(iws_config_path_local), 'r')
  match = re.findall(r'^frontend\s+(\S+)\s+\S+:(\d+)', f.read(), re.M)
  if match:
    for x in match:
      iws_name =  x[0]
      iws_port =  x[1]
      web_svc_port_dict[iws_name] = iws_port 
  ssh(cluster, cmd, web_svc_port_dict) 
            

def main():
  args = sys.argv[1:]
  usage = ('web_svcs_check.py [cluster]\n'
           'Example: web_svcs_check.py fuel')
  if not args or len(args) < 1:
    print usage
    sys.exit(1)
  iws_config_path_remote = '/srv/etc/haproxy/iwsclient.cfg'
  iws_config_path_local = '/tmp/iwsclient.cfg' 
  
  #####host assignments###
  analytics = ['lsv-1480.rfiserve.net', 'lsv-1481.rfiserve.net', 'inw-1246.rfiserve.net']
  fuel = ['lsv-1482.rfiserve.net', 'lsv-1483.rfiserve.net', 'inw-1245.rfiserve.net']
  apollo = ['inw-1231.rfiserve.net', 'lsv-1503.rfiserve.net']
  cmd = 'nc -zv 127.0.0.1'

  if args[0] == 'fuel':
    scp(fuel[0], iws_config_path_remote, iws_config_path_local)
    get_service_port_mapping_from_cfg_file(iws_config_path_local, fuel, cmd)
    
  if args[0] == 'analytics':
    scp(analytics[0], iws_config_path_remote, iws_config_path_local)
    get_service_port_mapping_from_cfg_file(iws_config_path_local, analytics, cmd)

  if args[0] == 'apollo':
    scp(apollo[0], iws_config_path_remote, iws_config_path_local)
    get_service_port_mapping_from_cfg_file(iws_config_path_local, apollo, cmd)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
