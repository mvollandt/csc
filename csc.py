'''
File name       : csc.py
Description     : check Cisco Nexus configs for security settings (using nxapi)
Created         : 07/03/2018
Last Modified   : 26/04/2018
Version         : 0.2
Copyright 2018 M. Vollandt (github863027@s245050704.online.de) All rights reserved.

This script will read Cisco Nexus configuration and check predefined security settings.

Changelog:
0.1 -   first working version (no checks yet)
0.2 -   added local config file support
'''

import argparse
import re
import requests
import json
import time
import datetime
from threading import Thread
from csc_devices import *
from csc_checks import *

# cli input parsing
parser = argparse.ArgumentParser(prog='csc.py')
parser.add_argument('-s', '--scope', help='defines the scope of the test [ALL, TEST, UAT] or a config file to read (def: file "switch.conf" )',
                    default='switch.conf')
parser.add_argument('-U', '--username', help='args.username (def: admin )',
                    default='admin')
parser.add_argument('-P', '--password', help='args.password (def: password )',
                    default='password')
parser.add_argument('-B', '--basedir', help='directory to store data',
                    default='DATA/')
parser.parse_args()
args = parser.parse_args()

configs = {}
connect = 1
now = datetime.datetime.now()
clicommand_nxos = 'show run ntp'
device_counter = 0

check_list = [csc1_1, csc1_2, csc1_3]

requests.packages.urllib3.disable_warnings()


if args.scope == 'ALL':
    device_list = [switch_014, switch_024]
elif args.scope == 'TEST':
    device_list = [switch_034, ]
elif args.scope == 'UAT':
    device_list = [switch_044, ]
else:
    connect = 0
    device_list = [args.scope, ]
    with open(args.scope, "r") as inputfile:
        configs.setdefault(args.scope, [])
        for line in inputfile:
            configs[args.scope].append(line)


def fetch_show_command_data(device, **kwargs):
    net_connect = ConnectHandler(
        device_type=device['device_type'],
        ip=device['ip'],
        username=args.username,
        password=args.password,
        port=device['port'],
        secret=device['secret'],
        verbose=device['verbose']
    )
    net_connect.enable()
    output = net_connect.send_command_expect(kwargs['showCommand'])
    net_connect.disconnect()
    return output


def get_data(hostname, username, password, show_command, qtype="cli_show", timeout=30):
    if not show_command.startswith("show "):
        msg = str("\"" + show_command + "\" is not a valid show command")
        raise Exception(msg)

    payload = [
        {
            "ins_api": {
                "version": "1.2",
                "type": qtype,
                "chunk": "0",
                "sid": "1",
                "input": show_command,
                "output_format": "json"
            }
        }
    ]

    headers = {'content-type': 'application/json'}

    response = requests.post("http://%s/ins" % (hostname),
                             auth=(username, password),
                             headers=headers,
                             data=json.dumps(payload),
                             verify=False,
                             timeout=timeout)
    if response.status_code == 200:
        return response.json()['ins_api']['outputs']['output']
    else:
        msg = 'call to {hostname} failed, status code {sc} ({rc})'.format(
            hostname=hostname, sc=response.status_code, rc=response.content)
        print(msg)
        raise Exception(msg)


def get_configs(**kwargs):
    global device_counter
    print('connecting to ' + kwargs['device_name'] + '...', end='\n')
    #print("---------> " + str(kwargs))
    if kwargs['device_type'] == 'cisco_nxos':
        data = get_data(
            kwargs["ip"],
            args.username,
            args.password,
            # kwargs["username"],
            # kwargs["password"],
            clicommand_nxos,
            "cli_show_ascii",
            120
        )
        configs.setdefault(kwargs['device_name'], data['body'])

    device_counter += 1


def check_in_simple(**kwargs):
    data = kwargs['data']
    print('simple check')
    print(data)
    print(data['match'])


def check_not_in_simple(**kwargs):
    data = kwargs['data']
    print('simple check - not in')


def check_parameter(**kwargs):
    data = kwargs['data']
    print('parameter check')


def check_configs():
    configdata = []

    for check in check_list:
        if check['check_type'] == 'check_in_simple':
            check_in_simple(data=check)
        elif check['check_type'] == 'check_not_in_simple':
            check_not_in_simple(data=check)
        else:
            check_parameter(data=check)

    if connect == 1:
        with open(args.basedir + "device_config_" + timestamp + ".conf", "a") as output:
            for line in configdata:
                output.write(line + '\n')


def print_result(result, text):
    if result == 'ok':
        print('+ {} : {}'.format(result, text))
    elif result == 'failed':
        print('- {} : {}'.format(result, text))
    else:
        print('o {} : {}'.format(result, text))


if __name__ == "__main__":
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    timestamp = now.strftime("%Y%m%d_%H%M")
    if connect == 1:
        for a_device in device_list:
            print(a_device)
            t = Thread(target=get_configs, kwargs=a_device)
            time.sleep(0.1)
            t.start()

        while len(device_list) - device_counter > 0:
            if (len(device_list) - device_counter > 1):
                print('waiting for {} devices...'.format(
                    str(len(device_list) - device_counter)))
            else:
                print('waiting for {} device...'.format(
                    str(len(device_list) - device_counter)))
            time.sleep(2)

    # if connect == 1:
    #    write_configs()

    check_configs()
    print('DONE.')
