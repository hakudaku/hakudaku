#!/usr/bin/python

import sys
import re
import os

EXIT_OK = 0
EXIT_WARN = 1
EXIT_CRITICAL = 2


def log_error_check(log_path, offset_path, timestamp_path, pattern):
    offset = 0
    if not os.path.exists(offset_path):
        with open(offset_path, 'w') as fo:
            fo.write(str(offset))
            fo.close()
    if not os.path.exists(timestamp_path):
        with open(timestamp_path, 'w') as fo:
            fo.write('')
            fo.close()

    count = 0
    with open(offset_path, 'r') as fo_offset:
        pos = fo_offset.readline()
        pos = int(pos)
        fo_offset.close()

    '''
    If timestamp in the beginning of file has not changed,
    follow the offset in "offset" file,
    otherwise (log rotation has occured), start from pos 0
    '''
    with open(log_path, 'rU') as fo:
        line = fo.readline()
        first_index = line.split()
        my_timestamp = first_index[0]
        with open(timestamp_path, 'r') as fo_read_timestamp:
            my_timestamp_list = fo_read_timestamp.readline()
            fo_read_timestamp.close()
            if my_timestamp == my_timestamp_list:
                fo.seek(pos)
            elif my_timestamp != my_timestamp_list:
                fo.seek(0)
                with open(timestamp_path, 'w') as fo_write_timestamp:
                    fo_write_timestamp.write(my_timestamp)
                    fo_write_timestamp.close()
        for line in fo:
            error_match = re.search(pattern, line, re.IGNORECASE)
            if error_match:
                count = count + 1
                pos = fo.tell()
    with open(offset_path, 'w+') as fw:
        fw.write(str(pos))

    if count > 0:
        print 'CRITICAL: error condition has occurred'
        sys.exit(EXIT_CRITICAL)
    else:
        print 'OK: Normal'
        sys.exit(EXIT_OK)


def main():
    dbz_log_dir = '/service/debezium/log/main'
    log_path = os.path.join(dbz_log_dir, 'current')
    offset_path = os.path.join(dbz_log_dir, 'offset')
    timestamp_path = os.path.join(dbz_log_dir, 'timestamp')
    error_pattern = r'.+error\s+while\s+.+\n|.+error\s+failed\s+.+\n'

    log_error_check(log_path, offset_path, timestamp_path, error_pattern)


if __name__ == '__main__':
    main()
