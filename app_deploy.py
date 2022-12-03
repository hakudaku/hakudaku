#!/usr/bin/env python

import commands
import os
import requests
import re
from find_lb import get_lb

def app_server_deploy(regions):
    for region in regions:
        knife_search_cmd = 'knife search "roles:app-prod AND tags:{} AND NOT (tags:down OR tags:standby OR tags:nomon-asg)" -i'.format(region)
        (status, output) = commands.getstatusoutput(knife_search_cmd)
        all_app_servers_for_region = re.findall(r'app.+', output) # all_app_servers_for_region will be a list/array of app server names for the region
        sample_app_server = all_app_servers_for_region[0] # use this to get the LBs for QA to test
        lbs_for_region = get_lb(sample_app_server, 'prod')
        lb_match = re.search(r'app.+', lbs_for_region, re.DOTALL) # lbs_for_region variable has \n and other strings. Just want the app server names. DOTALL, so it matches \n.
        if len(all_app_servers_for_region) < 10:
            concurrency = len(all_app_servers_for_region)/2 # If we have less than 10 app servers in a region, we only want to run chef on half of them concurrently
        else:
            concurrency = 10
        webhook_url = 'https://hooks.slack.com/services/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'
        payload_start = {"channel": "#prod-deploy-team", "username": "Deploy_status", "text": "Deploy to" + " " + region + " " + "started..."}
        payload_complete = {"channel": "#prod-deploy-team", "username": "Deploy_status", "text": region + " " + "complete!!!"}
        payload_lb_list = {"channel": "#prod-deploy-team", "username": "Deploy_status", "text": "LBs for " + region + ':' + '\n' + lb_match.group()}
        knife_ssh_cmd = 'knife ssh "roles:app-prod AND tags:{} AND NOT (tags:down OR tags:standby OR tags:nomon-asg)" "sudo -i chef-client" -t 5 -C {}'.format(region, concurrency)
        knife_status_cmd = 'knife search "role:app-prod AND tags:{} AND NOT (ohai_time:[$(date --date=\'5 hours ago\' \'+%s\') TO $(date \'+%s\')] OR tags:down OR tags:standby OR tags:nomon-asg)" -i'.format(region)
        requests.post(webhook_url, json = payload_start) # Post to #prod-deploy-team that deploy for region is starting
        os.system(knife_ssh_cmd)
        (status, output) = commands.getstatusoutput(knife_status_cmd)
        app_servers_pending_chef_run = re.findall(r'app.+', output) # app_servers_pending_chef_run will be a list/array of app server names without a chef run within last 5 hours for the region
        if len(app_servers_pending_chef_run) == 0: # All app servers in the region had a recent successful chef run
            with open('completed_regions', 'a') as f:
                f.write(region + ' ' + 'is complete!\n')
                requests.post(webhook_url, json = payload_complete) # Post to #prod-deploy-team that deploy for region is complete
                requests.post(webhook_url, json = payload_lb_list) # Post to #prod-deploy-team the LBs for region
        elif len(app_servers_pending_chef_run) > 0: # Some app servers in the region did not have a successful chef run within last 5 hours
            list_of_app_completed_ok = []
            for app in all_app_servers_for_region:
                if app not in app_servers_pending_chef_run:
                    list_of_app_completed_ok.append(app) # Create list/array of app servers in region that had a successful chef run within last 5 hours. QA can test on one of them even though region is not complete
            payload_incomplete = {"channel": "#prod-deploy-team", "username": "Deploy_status", "text": region + " " + "completed but some app servers do NOT have latest code. QA can still perform verification on" + " " + list_of_app_completed_ok[0]}
            requests.post(webhook_url, json = payload_incomplete) # Post to #prod-deploy-team a successfully completed app server that can be QA verified
            requests.post(webhook_url, json = payload_lb_list) # Post to #prod-deploy-team the LBs for region
            with open('completed_regions', 'a') as f:
                f.write(region + ' ' + 'is incomplete!\n')


def main():
    #regions = ['eu-west-1', 'eu-west-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'app-kr', 'eu-de-1', 'us-atl-1', 'us-east-1', 'us-east-cogent', 'us-east-mixed', 'us-east-np', 'us-west-2', 'us-las-1', 'us-west-fs', 'us-east-fs', 'alvin-asia-se1', 'alvin-eu-west4', 'alvin-us-east4', 'alvin-us-west4']
    regions = ['alvin-asia-se1', 'alvin-eu-west4', 'alvin-us-east4', 'alvin-us-west4']
    app_server_deploy(regions)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
