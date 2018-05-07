'''
File name       : csc.py
Description     : check Cisco Nexus configs for security settings (using nxapi)
Created         : 07/03/2018
Last Modified   : 07/05/2018
Version         : 0.8
Copyright 2018 M. Vollandt (github863027@s245050704.online.de) All rights reserved.

This script will read Cisco Nexus configuration and check predefined security settings.

Changelog:
0.1 -   first working version (no checks yet)
0.2 -   added local config file support
0.3 -   simple tests are working (more have to be defined)
0.4 -   add two parameter support, check info, and check export as csv
0.5 -   convert checks (from cvs file) to .py file, fix username/password behavior
0.6 -   colored output for better readability
0.7 -   write results as reports ("DATA/csc_report_<devicename>.txt")
0.8 -   added new checks

Planned:
- write readme (add some examples how to use csc.py)
- add more CVE checks
- add more basic checks
'''

import argparse
import re
import requests
import json
import time
import datetime
from colorama import Fore, Back, Style, init
from threading import Thread
from csc_devices import *
from csc_checks import *

# cli input parsing
parser = argparse.ArgumentParser(prog='csc.py')
parser.add_argument('-s', '--scope', help='defines the scope of the test [ALL, TEST, UAT] or a config file to read (def: file switch.conf)',
                    default='switch.conf')
parser.add_argument('-U', '--username', help='args.username (def: admin )',
                    default='admin')
parser.add_argument('-P', '--password', help='args.password (def: password )',
                    default='password')
parser.add_argument('-B', '--basedir', help='directory to store data',
                    default='DATA/')
parser.add_argument('-v', '--verbose', help='increase output verbosity',
                    action='store_true')
parser.add_argument('-i', '--info', help='show detail for check id')
parser.add_argument('-c', '--convert',
                    help='convert all check ids from csv to csc_checks.py')
parser.add_argument(
    '-e', '--export', help='export all check ids as csv', action='store_true')
parser.parse_args()
args = parser.parse_args()

configs = {}
connect = 1
now = datetime.datetime.now()
# clicommand_nxos = ['show version', 'show run ntp']  # for testing
clicommand_nxos = ['show version', 'show run all']
device_counter = 0

check_list = [csc1_1, csc1_2, csc1_3, csc1_4, csc1_5, csc1_6, csc1_7, csc1_8, csc1_9,
              csc1_10, csc1_11, csc1_12, csc1_13, csc1_14, csc1_15, csc1_16, csc1_17, csc1_18, csc1_19,
              csc1_20,
              CVE_2018_0102,
              CVE_2018_0090,
              CVE_2018_0092,
              CVE_2018_009x, ]

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
    if kwargs['device_type'] == 'cisco_nxos':
        if kwargs["username"] == 'dummy_username':
            username = args.username
        else:
            username = kwargs["username"]
        if kwargs["password"] == 'dummy_password':
            password = args.password
        else:
            password = kwargs["password"]
        data = get_data(
            kwargs["ip"],
            username,
            password,
            clicommand_nxos[0],
            "cli_show_ascii",
            120
        )
        configs.setdefault(kwargs['device_name'], data['body'])
        if clicommand_nxos[1]:
            data2 = get_data(
                kwargs["ip"],
                username,
                password,
                clicommand_nxos[1],
                "cli_show_ascii",
                120
            )
            configs[kwargs['device_name']
                    ] = configs[kwargs['device_name']] + data2['body']
    device_counter += 1


def check_in_simple(report, configdata, **kwargs):
    found = 0
    data = kwargs['data']
    print('{} - simple check - {}'.format(data['check_name'], data['info']))
    report.write(
        '{} - simple check - {}\n'.format(data['check_name'], data['info']))
    for line in configdata:
        match = re.compile(data['match1']).search(line)
        if match:
            found = found + 1
            if args.verbose:
                print(
                    '\033[36m' + '# found this: {} '.format(match.group(0)) + '\033[37m')
    if found > 0 and data['required'] == 'yes':
        print_result(report, 'ok', data['result_ok'])
    elif found == 0 and data['required'] == 'no':
        print_result(report, 'ok', data['result_ok'])
    else:
        print_result(report, 'failed', data['result_failed'])


def check_parameter(report, configdata, **kwargs):
    data = kwargs['data']
    found = 0
    print('{} - parameter check - {}'.format(data['check_name'], data['info']))
    report.write(
        '{} - parameter check - {}\n'.format(data['check_name'], data['info']))
    parameter = re.compile(data['match1'])
    value = re.compile(data['match2'])

    for line in configdata:
        match = parameter.search(line)
        if match:
            match_value = value.search(line)
            if match_value:
                found = found + 1
                if args.verbose:
                    print('\033[36m' + '# found this: {} {}'.format(
                        match.group(0), match_value.group(0)) + '\033[37m')
    if found > 0 and data['required'] == 'yes':
        print_result(report, 'ok', data['result_ok'])
    elif found == 0 and data['required'] == 'no':
        print_result(report, 'ok', data['result_ok'])
    else:
        print_result(report, 'failed', data['result_failed'])


def check_two_parameters(report, configdata, **kwargs):
    data = kwargs['data']
    found_first = 0
    found_second = 0
    print(
        '{} - two parameters check - {}'.format(data['check_name'], data['info']))
    report.write(
        '{} - two parameters check - {}\n'.format(data['check_name'], data['info']))
    match1 = re.compile(data['match1'])
    match2 = re.compile(data['match2'])

    for line in configdata:
        match_first = match1.search(line)
        match_second = match2.search(line)
        if match_first:
            found_first = found_first + 1
            if args.verbose:
                print(
                    '\033[36m' + '# found first: {}'.format(match_first.group(0)) + '\033[37m')
        if match_second:
            found_second = found_second + 1
            if args.verbose:
                print(
                    '\033[36m' + '# found second: {}'.format(match_second.group(0)) + '\033[37m')

    if found_first > 0 and data['required'] == 'yes':
        if found_second > 0:
            print_result(report, 'ok', data['result_ok'])
    elif found_first == 0 and data['required'] == 'no':
        if found_second == 0:
            print_result(report, 'ok', data['result_ok'])
    else:
        print_result(report, 'failed', data['result_failed'])


def check_configs(report, configdata):
    for check in check_list:
        if check['check_type'] == 'check_in_simple':
            check_in_simple(report, configdata, data=check)
        elif check['check_type'] == 'check_two_parameters':
            check_two_parameters(report, configdata, data=check)
        else:
            check_parameter(report, configdata, data=check)

    if connect == 1:
        with open(args.basedir + "device_config_" + timestamp + ".conf", "a") as output:
            for line in configdata:
                output.write(line + '\n')


def print_result(report, result, text):
    if result == 'ok':
        #print('\033[31m' + 'some red text')
        print('\033[32m' + '\t+ {} : {}'.format(result, text) + '\033[37m')
        report.write('\t+ {} : {}\n'.format(result, text))
    elif result == 'failed':
        print('\033[31m' + '\t- {} : {}'.format(result, text) + '\033[37m')
        report.write('\t- {} : {}\n'.format(result, text))
    else:
        print('\033[33m' + '\to {} : {}'.format(result, text) + '\033[37m')
        report.write('\to {} : {}\n'.format(result, text))


def load_config_from_device(devicename):
    configdata = []
    print(devicename)
    if args.verbose:
        print(
            '\033[36m' + '# loading device config: {}'.format(devicename) + '\033[37m')

    configdata.append('!***' + devicename)
    for line in configs[devicename].split("\n"):
        configdata.append(line)

    with open(args.basedir + "device_config_" + timestamp + ".conf", "a") as output:
        for line in configdata:
            # print(line)
            output.write(line + '\n')
    return configdata


def load_config_from_file(filename):
    configdata = []
    with open(filename, "r") as input:
        for line in input:
            configdata.append(line.replace('\n', ''))
    return configdata


def show_check_id_details(checkid):
    for check in check_list:
        if check['check_name'] == checkid:
            for x in check.items():
                print('{:10}\t: {}'.format(x[0], x[1]))


def export_check_id_details():
    with open(args.basedir + "csc_checks_export.csv", "w") as output:
        for check in check_list:
            line = ''
            for x in check.items():
                    #print('{:10}\t: {}'.format(x[0],x[1]))
                print('{};'.format(x[1].rstrip()), end='')
                line += '{};'.format(x[1].rstrip())
            output.write(line + '\n')
            print(line)


def convert_check_ids_from_file(filename):
    with open(filename, 'r') as infile:
        with open("csc_checks.py", "w") as outputfile:
            outputfile.write('# filename    : csc_checks.py\n')
            outputfile.write(
                '# description : check definitions (security best practices and CVEs)\n')
            outputfile.write('# create date : {}\n\n'.format(now))
            for line in infile.readlines():
                if not line.startswith('#'):
                    line_values = line.split(';')
                    output = ('{check_name} = {{\'check_name\': \'{check_name}\','.format(
                        check_name=line_values[0]))
                    output += ('\n\t\t\'check_type\': \'{check_type}\','.format(
                        check_type=line_values[1]))
                    output += ('\n\t\t\'match1\': \'{match1}\','.format(
                        match1=line_values[2]))
                    output += ('\n\t\t\'match2\': \'{match2}\','.format(
                        match2=line_values[3]))
                    output += ('\n\t\t\'required\': \'{required}\','.format(
                        required=line_values[4]))
                    output += ('\n\t\t\'result_ok\': \'{result_ok}\','.format(
                        result_ok=line_values[5]))
                    output += ('\n\t\t\'result_failed\': \'{result_failed}\','.format(
                        result_failed=line_values[6]))
                    output += ('\n\t\t\'info\': \'{info}\','.format(
                        info=line_values[7]))
                    output += ('\n\t\t\'url\': \'{url}\','.format(
                        url=line_values[8]))
                    output += ('\n\t\t\'fix\': \'{fix}\','.format(
                        fix=line_values[9].rstrip()))
                    output += ('}\n')
                    print(output)
                    outputfile.write(output + '\n')


if __name__ == "__main__":
    init()  # init colorama
    print('\033[37m' + now.strftime("%Y-%m-%d %H:%M:%S"))
    timestamp = now.strftime("%Y%m%d_%H%M")

    if args.info:
        show_check_id_details(args.info)
    elif args.export:
        export_check_id_details()
    elif args.convert:
        convert_source = args.convert
        convert_check_ids_from_file(convert_source)
    else:
        if connect == 1:
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

        if connect == 1:
            for device in device_list:
                devicename = device['device_name']
                configdata = load_config_from_device(devicename)
                reportfile = args.basedir + "csc_report_" + devicename + ".txt"
                with open(reportfile, "w") as report:
                    report.write(
                        '# {} report (written at {})\n'.format(devicename, now))
                    check_configs(report, configdata)
        else:
            configdata = load_config_from_file(args.scope)
            reportfile = args.basedir + "csc_report_" + args.scope + ".txt"
            with open(reportfile, "w") as report:
                report.write(
                    '# {} report (written at {})\n'.format(args.scope, now))
                check_configs(report, configdata)

    print('DONE.')
