#!/Users/vineetbhatia/ENV/bin/python -tt

import argparse
import glob
import os
import commands
import shutil
import re


def add_service_check_existing_service(svc_template_file, mod_nrpe_cfg_file, nrpe_content_svc_check,
                                       git_co_rails4, git_co_master, infradb_repo):
    os.chdir(infradb_repo)
    output = commands.getoutput(git_co_rails4)
    print output

    with open(mod_nrpe_cfg_file, 'w') as fo:
        fo.write(nrpe_content_svc_check)

    output = commands.getoutput('git stash')
    print output
    output = commands.getoutput(git_co_master)
    print output

    with open('/Users/vbhatia/bin/test_space/svc_erb_content', 'rU') as f:
        data = f.read()

    with open(svc_template_file, 'rU') as in_file:
        buf = in_file.read()
        match = re.search(r'<% end -%>', buf)
        if match:
            with open(svc_template_file, 'w') as out_file:
                s = match.group()
                buf = buf.replace(s, data + s)
                out_file.write(buf)

def add_new_check_script_existing_service(script_file, mod_files_dir, mod_nrpe_cfg_file, nrpe_content,
                                          svc_manifest_file, svc_template_file, sudoers_template_file,
                                          git_co_rails4, git_co_master, infradb_repo, sudoers_content):

    os.chdir(infradb_repo)
    output = commands.getoutput(git_co_rails4)
    print output
    shutil.copy(script_file, mod_files_dir )

    with open(mod_nrpe_cfg_file, 'w') as fo:
        fo.write(nrpe_content)

    with open('/Users/vbhatia/bin/test_space/init_content', 'rU') as f:
        data = f.read()

    with open(svc_manifest_file, 'rU') as in_file:
        buf = in_file.read()
        match = re.search(r'mode.+;\s+}', buf)
        if match:
            with open(svc_manifest_file, 'w') as out_file:
                s = match.group()
                buf = buf.replace(s, s[:-1] + data + '  ' + '}')
                out_file.write(buf)
    output = commands.getoutput('git stash')
    print output
    output = commands.getoutput(git_co_master)
    print output

    with open('/Users/vbhatia/bin/test_space/svc_erb_content', 'rU') as f:
        data = f.read()

    with open(svc_template_file, 'rU') as in_file:
        buf = in_file.read()
        match = re.search(r'<% end -%>', buf)
        if match:
            with open(svc_template_file, 'w') as out_file:
                s = match.group()
                buf = buf.replace(s, data + s)
                out_file.write(buf)


    with open(sudoers_template_file, 'rU') as in_file:
        buf = in_file.read()
        match = re.search(r'(nagios ALL.*)(\s+%.*)', buf)
        if match:
            buf = buf.replace(match.group(),
                              match.group(1) + '\n' + sudoers_content + match.group(2))
            with open(sudoers_template_file, 'w') as out_file:
                out_file.write(buf)


def main():

    parser = argparse.ArgumentParser(description="setup nagios client side check")
    parser.add_argument("svc", help="Service for which alert is being added")
    parser.add_argument("--script", help="Path to the monitoring script")
    parser.add_argument("-s", "--service_check", help="add a simple service up/down check", action="store_true")
    args = parser.parse_args()
    svc_name = args.svc
    script_file = os.path.expanduser('~') + '/{}'.format(args.script)
    home_dir = os.path.expanduser('~')
    infradb_repo = glob.glob(home_dir + '/*/operations/infradb')[0]
    mod_files_dir = '{}/puppet/code/environments/production/modules/{}/files'.format(infradb_repo, svc_name)
    mod_nrpe_cfg_file = '{}/checks/check-{}-new-nrpe.cfg'.format(mod_files_dir, svc_name)
    nrpe_content = 'command[check_{}_log]=/usr/bin/sudo /usr/local/bin/{}'.format(svc_name, script_file)
    nrpe_content_svc_check = 'command[check_{}_svc]=/usr/bin/sudo /usr/local/bin/check_svc {}'.format(svc_name, svc_name)
    svc_manifest_file = '{}/puppet/code/environments/production/modules/{}/manifests/init.pp'.format(infradb_repo,
                         svc_name)
    svc_template_file = '{}/app/views/api/nagios_modular/_services_{}.erb'.format(infradb_repo, svc_name)
    sudoers_template_file = '{}/app/views/api/sudo/_sudoers.erb'.format(infradb_repo)
    sudoers_content = 'nagios ALL=(root) /usr/local/bin/{}'.format(script_file)

    git_co_rails4 = 'git checkout rails4'
    git_co_master = 'git checkout master'

    if args.service_check:
        add_service_check_existing_service(svc_template_file, mod_nrpe_cfg_file,
                                           nrpe_content_svc_check, git_co_rails4, git_co_master, infradb_repo)

    else:
        add_new_check_script_existing_service(script_file, mod_files_dir, mod_nrpe_cfg_file, nrpe_content,
                                     svc_manifest_file, svc_template_file, sudoers_template_file,
                                     git_co_rails4, git_co_master, infradb_repo, sudoers_content)




# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
