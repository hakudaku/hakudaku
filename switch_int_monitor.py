#!/usr/bin/python

import commands
import re
import sys
import argparse
import os
from shutil import move
from tempfile import mkstemp
from os import fdopen, remove

EXIT_OK = 0
EXIT_WARN = 1
EXIT_CRITICAL = 2

def AdminStatus(switch_name, oid, int_dict):
    int_up = []
    int_down = []
    snmpwalk_cmd = 'snmpwalk -v 2c -c r0ck3tfu31# {0} {1}'.format(switch_name, oid)
    (status, output) = commands.getstatusoutput(snmpwalk_cmd)
    for key in int_dict.keys():
        my_dict = dict(re.findall('({0}).+:\s+(\w+)\('.format(key), output))
        for key in my_dict.keys():
            if my_dict[key] == 'down':
                int_down.append(int_dict[key])
            elif my_dict[key] == 'up':
                int_up.append(int_dict[key])

    if len(int_down) > 0:
        s = ', '.join(int_down)
        print 'CRITICAL: Interfaces {0} are down!'.format(s) 
        sys.exit(EXIT_CRITICAL)
    else:
        s = ', '.join(int_up)
        print 'OK: Interfaces {0} are up!'.format(s)
        sys.exit(EXIT_OK)

def int_errors(switch_name, oid, int_dict, mib):
    int_errors_yes = []
    int_errors_no = []    

    # Create file to store error count for each mib
    mib_file_count_path = '/tmp/{0}.{1}'.format(mib, switch_name)
    if not os.path.exists(mib_file_count_path):
        os.mknod(mib_file_count_path)
    # Run snmpwalk for oid and get output
    snmpwalk_cmd = 'snmpwalk -v 2c -c r0ck3tfu31# {0} {1}'.format(switch_name, oid)
    (status, output) = commands.getstatusoutput(snmpwalk_cmd)

    # create dict for int_id ---> error count mapping
    if os.path.getsize(mib_file_count_path) == 0:
        with open(mib_file_count_path, 'w') as f:
            for key in int_dict.keys():
                my_dict = dict(re.findall('({0}).+:\s+(\d+)'.format(key), output))
                f.write(int_dict[key] + ',' + my_dict[key] + '\n')
    elif os.path.getsize(mib_file_count_path) != 0:
        with open(mib_file_count_path, 'r') as f:
            for line in f:
                for key in int_dict.keys():
                    match = re.search(r'({0})\,(\d+)'.format(int_dict[key]), line)
                    if match:
                        my_dict = dict(re.findall('({0}).+:\s+(\d+)'.format(key), output))
                        int_id = match.group(1)
                        error_count = int(match.group(2))
                        if int(my_dict[key]) > int(error_count):
                            int_errors_yes.append(int_dict[key])
                            old_string = '{0},{1}\n'.format(int_dict[key], error_count)
                            new_string = '{0},{1}\n'.format(int_dict[key], my_dict[key])
                            tmp_path = '/tmp/tmp_file'
                            diff = int(my_dict[key]) - int(error_count)
                            fd, tmp_path = mkstemp()
                            with fdopen(fd, 'w') as new_file:
                                with open(mib_file_count_path) as old_file:
                                    for line in old_file:
                                        new_file.write(line.replace(old_string, new_string))

                            remove(mib_file_count_path)
                            move(tmp_path, mib_file_count_path)

                        elif int(my_dict[key]) == int(error_count):
                            int_errors_no.append(int_dict[key])
    
    if len(int_errors_yes) > 0:
        s = ', '.join(int_errors_yes)
        print 'WARNING: Interfaces {0} have an increase in {1} errors since last check!'.format(s, mib) 
        sys.exit(EXIT_WARN)
    else:
        s = ', '.join(int_errors_no)
        print 'OK: Interfaces {0} have 0 {1} errors incremented since last check.'.format(s, mib) 
        sys.exit(EXIT_OK)


def main():
    parser = argparse.ArgumentParser(description="Switch interface monitoring")
    parser.add_argument("-H", "--hostname", help="switch name")
    parser.add_argument("-M", "--module", help="SNMP MIB object")
    args = parser.parse_args()

    ifAdminStatus = '.1.3.6.1.2.1.2.2.1.7'
    ifAlias = '1.3.6.1.2.1.31.1.1.1.18'
    InDiscards = '.1.3.6.1.2.1.2.2.1.13'
    ifInErrors = '.1.3.6.1.2.1.2.2.1.14'
    ifOutDiscards = '.1.3.6.1.2.1.2.2.1.19'
    ifOutErrors = '.1.3.6.1.2.1.2.2.1.20'
    dot3StatsAlignmentErrors = '1.3.6.1.2.1.10.7.2.1.2'
    dot3StatsFCSErrors = '1.3.6.1.2.1.10.7.2.1.3'
    dot3StatsSingleCollisionFrames = '1.3.6.1.2.1.10.7.2.1.4'
    dot3StatsMultipleCollisionFrames = '1.3.6.1.2.1.10.7.2.1.5'
    dot3StatsSQETestErrors = '1.3.6.1.2.1.10.7.2.1.6'
    dot3StatsDeferredTransmissions = '1.3.6.1.2.1.10.7.2.1.7'
    dot3StatsLateCollisions = '1.3.6.1.2.1.10.7.2.1.8'
    dot3StatsExcessiveCollisions = '1.3.6.1.2.1.10.7.2.1.9'
    dot3StatsInternalMacTransmitErrors = '1.3.6.1.2.1.10.7.2.1.10'
    dot3StatsCarrierSenseErrors = '1.3.6.1.2.1.10.7.2.1.11'
    dot3StatsFrameTooLongs = '1.3.6.1.2.1.10.7.2.1.13'
    dot3StatsInternalMacReceiveErrors = '1.3.6.1.2.1.10.7.2.1.16'
    dot3StatsSymbolErrors = '1.3.6.1.2.1.10.7.2.1.18'
    dot3InPauseFrames = '1.3.6.1.2.1.10.7.10.1.3'
    dot3OutPauseFrames = '1.3.6.1.2.1.10.7.10.1.4'
    dot3HCInPauseFrames = '1.3.6.1.2.1.10.7.10.1.5'
    dot3HCOutPauseFrames = '1.3.6.1.2.1.10.7.10.1.6'
    dot3HCStatsAlignmentErrors = '1.3.6.1.2.1.10.7.11.1.1'
    dot3HCStatsFCSErrors = '1.3.6.1.2.1.10.7.11.1.2'
    dot3HCStatsInternalMacTransmitErrors = '1.3.6.1.2.1.10.7.11.1.3'
    dot3HCStatsFrameTooLongs = '1.3.6.1.2.1.10.7.11.1.4'
    dot3HCStatsInternalMacReceiveErrors = '1.3.6.1.2.1.10.7.11.1.5'
    dot3HCStatsSymbolErrors = '1.3.6.1.2.1.10.7.11.1.6'

    snmpwalk_ifalias_cmd = 'snmpwalk -v 2c -c r0ck3tfu31# {0} {1}'.format(args.hostname, ifAlias)

    (status, output) = commands.getstatusoutput(snmpwalk_ifalias_cmd)

    # Open template file to grab switch name and interface
    with open("switch_int.txt", 'r') as f:
        match = re.findall 

    if args.module == 'ifAdminStatus':
        AdminStatus(args.hostname, ifAdminStatus, int_dict)
    elif args.module == 'InDiscards':
        int_errors(args.hostname, InDiscards, int_dict, 'InDiscards')
    elif args.module == 'ifInErrors':
        int_errors(args.hostname, ifInErrors, int_dict, 'ifInErrors')
    elif args.module == 'ifOutDiscards':
        int_errors(args.hostname, ifOutDiscards, int_dict, 'ifOutDiscards')
    elif args.module == 'ifOutErrors':
        int_errors(args.hostname, ifOutErrors, int_dict, 'ifOutErrors')
    elif args.module == 'dot3StatsAlignmentErrors':
        int_errors(args.hostname, dot3StatsAlignmentErrors, int_dict, 'dot3StatsAlignmentErrors')
    elif args.module == 'dot3StatsFCSErrors':
        int_errors(args.hostname, dot3StatsFCSErrors, int_dict, 'dot3StatsFCSErrors')
    elif args.module == 'dot3StatsSingleCollisionFrames':
        int_errors(args.hostname, dot3StatsSingleCollisionFrames, int_dict, 'dot3StatsSingleCollisionFrames')
    elif args.module == 'dot3StatsMultipleCollisionFrames':
        int_errors(args.hostname, dot3StatsMultipleCollisionFrames, int_dict, 'dot3StatsMultipleCollisionFrames')
    elif args.module == 'dot3StatsSQETestErrors':
        int_errors(args.hostname, dot3StatsSQETestErrors, int_dict, 'dot3StatsSQETestErrors')
    elif args.module == 'dot3StatsDeferredTransmissions':
        int_errors(args.hostname, dot3StatsDeferredTransmissions, int_dict, 'dot3StatsDeferredTransmissions')
    elif args.module == 'dot3StatsLateCollisions':
        int_errors(args.hostname, dot3StatsLateCollisions, int_dict, 'dot3StatsLateCollisions')
    elif args.module == 'dot3StatsExcessiveCollisions':
        int_errors(args.hostname, dot3StatsExcessiveCollisions, int_dict, 'dot3StatsExcessiveCollisions')
    elif args.module == 'dot3StatsInternalMacTransmitErrors':
        int_errors(args.hostname, dot3StatsInternalMacTransmitErrors, int_dict, 'dot3StatsInternalMacTransmitErrors')
    elif args.module == 'dot3StatsCarrierSenseErrors':
        int_errors(args.hostname, dot3StatsCarrierSenseErrors, int_dict, 'dot3StatsCarrierSenseErrors')
    elif args.module == 'dot3StatsFrameTooLongs':
        int_errors(args.hostname, dot3StatsFrameTooLongs, int_dict, 'dot3StatsFrameTooLongs')
    elif args.module == 'dot3StatsInternalMacReceiveErrors':
        int_errors(args.hostname, dot3StatsInternalMacReceiveErrors, int_dict, 'dot3StatsInternalMacReceiveErrors')
    elif args.module == 'dot3StatsSymbolErrors':
        int_errors(args.hostname, dot3StatsSymbolErrors, int_dict, 'dot3StatsSymbolErrors')
    elif args.module == 'dot3InPauseFrames':
        int_errors(args.hostname, dot3InPauseFrames, int_dict, 'dot3InPauseFrames')
    elif args.module == 'dot3OutPauseFrames':
        int_errors(args.hostname, dot3OutPauseFrames, int_dict, 'dot3OutPauseFrames')
    elif args.module == 'dot3HCInPauseFrames':
        int_errors(args.hostname, dot3HCInPauseFrames, int_dict, 'dot3HCInPauseFrames')
    elif args.module == 'dot3HCOutPauseFrames':
        int_errors(args.hostname, dot3HCOutPauseFrames, int_dict, 'dot3HCOutPauseFrames')
    elif args.module == 'dot3HCStatsAlignmentErrors':
        int_errors(args.hostname, dot3HCStatsAlignmentErrors, int_dict, 'dot3HCStatsAlignmentErrors')
    elif args.module == 'dot3HCStatsFCSErrors':
        int_errors(args.hostname, dot3HCStatsFCSErrors, int_dict, 'dot3HCStatsFCSErrors')
    elif args.module == 'dot3HCStatsInternalMacTransmitErrors':
        int_errors(args.hostname, dot3HCStatsInternalMacTransmitErrors, int_dict, 'dot3HCStatsInternalMacTransmitErrors')
    elif args.module == 'dot3HCStatsFrameTooLongs':
        int_errors(args.hostname, dot3HCStatsFrameTooLongs, int_dict, 'dot3HCStatsFrameTooLongs')
    elif args.module == 'dot3HCStatsInternalMacReceiveErrors':
        int_errors(args.hostname, dot3HCStatsInternalMacReceiveErrors, int_dict, 'dot3HCStatsInternalMacReceiveErrors')
    elif args.module == 'dot3HCStatsSymbolErrors':
        int_errors(args.hostname, dot3HCStatsSymbolErrors, int_dict, 'dot3HCStatsSymbolErrors')


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
