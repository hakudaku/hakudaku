#!/usr/bin/python

while True:
    with open('/var/log/messages', 'r') as f:
        my_list = f.readlines()
        print my_list[-1]
