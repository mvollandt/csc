'''
File name       : csc.py
Description     : check Cisco Nexus configs for security settings (using nxapi)
Created         : 07/03/2018
Last Modified   : 25/04/2018
Version         : 0.1
Copyright 2018 M. Vollandt (github863027@s245050704.online.de) All rights reserved.

This script will read Cisco Nexus configuration and check predefined security settings.

Changelog:
0.1 -   first working version (no checks yet)
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
parser.add_argument('-s', '--scope', help='defines the scope of the test [ALL, TEST, UAT] or a config file to read - this is required! (def: file "switch.conf" )',
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

if args.scope == 'ALL':
    device_list = [switch_014, switch_024]
elif args.scope == 'TEST':
    device_list = [switch_034, ]
elif args.scope == 'UAT':
    device_list = [switch_044, ]
else:
    with open(args.scope, "r") as output:



now = datetime.datetime.now()
clicommand_nxos = 'show run ntp'
device_counter = 0

requests.packages.urllib3.disable_warnings()


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


def check_configs():
    configdata = []

    for device in device_list:
        device_name = device['device_name']
        print(device_name)
        configdata.append('!***' + device_name)
        for line in configs[device_name].split("\n"):
            if 'mgmt0' in line:
                print('TEST OK ' + line)

    with open(args.basedir + "device_config_" + timestamp + ".conf", "a") as output:
        for line in configdata:
            # print(line)
            output.write(line + '\n')


def write_configs():
    configdata = []

    for device in device_list:
        device_name = device['device_name']
        print(device_name)
        configdata.append('!***' + device_name)
        for line in configs[device_name].split("\n"):
            configdata.append(line)

    with open(args.basedir + "device_config_" + timestamp + ".conf", "a") as output:
        for line in configdata:
            # print(line)
            output.write(line + '\n')


if __name__ == "__main__":
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    timestamp = now.strftime("%Y%m%d_%H%M")
    for a_device in device_list:
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

    check_configs()
    write_configs()
