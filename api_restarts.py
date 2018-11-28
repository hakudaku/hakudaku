#!/Users/vineetbhatia/ENV/bin/python -tt
import sys
from pssh.clients import ParallelSSHClient
import logging

def run(cluster, cmd):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(cluster, user='vbhatia')
  output = client.run_command(cmd, stop_on_errors=True)
  for host in output:
    for line in output[host]['stdout']:
      print host, line

def main():
  args = sys.argv[1:]
  usage = ('api_restarts.py [cluster]\n'
           'Example: api_restarts.py fuel')
  if not args or len(args) < 1:
    print usage
    sys.exit(1)

  #####host assignments###
  nginx = ['lsv-1484.rfiserve.net', 'lsv-1485.rfiserve.net']
  analytics = ['lsv-1480.rfiserve.net', 'lsv-1481.rfiserve.net', 'inw-1246.rfiserve.net']
  fuel = ['lsv-1482.rfiserve.net', 'lsv-1483.rfiserve.net', 'inw-1245.rfiserve.net']
  apollo = ['inw-1231.rfiserve.net', 'lsv-1503.rfiserve.net']
  
  if args[0] == 'nginx':
    cmd = 'sudo svc -t /service/ui.orion.production/;sleep 5;sudo svstat /service/ui.orion.production/'
    run(nginx, cmd)
  elif args[0] == 'analytics':
    cmd = 'sudo svc -t /service/api.analytics.production/;sleep 5;sudo svstat /service/api.analytics.production/'
    run(analytics, cmd) 
  elif args[0] == 'fuel':
    cmd = 'sudo svc -t /service/api.fuel.production/;sleep 5;sudo svstat /service/api.fuel.production/'
    run(fuel, cmd) 
  elif args[0] == 'apollo':
    cmd = 'cd /srv/app/ui.apollo/production/current;sudo -u apache touch tmp/restart.txt;sleep 30;ps -ef | grep Rails | grep -i production | grep -v grep'
    run(apollo, cmd)
  else:
    print usage

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
