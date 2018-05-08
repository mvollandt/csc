# csc
Configuration Security Check

csc checks Cisco Nexus configuration for given security settings

csc is able to connect to a given list of Nexus devices or check a given switch configuration.
All checks can be simply extended in "csc_checks.csv".
This file can be converted to "csc_checks.py" and will then by used by csc.py.

A report will be written every time csc.py is excuted.
All reports are stored in "DATA/csc_report_<switchname>.txt".

Please start by entering "py csc.py -h" to display helpful information.

C:\Users\Python\py csc.py -h

usage: csc.py [-h] [-s SCOPE] [-U USERNAME] [-P PASSWORD] [-B BASEDIR] [-v]
              [-i INFO] [-c CONVERT] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -s SCOPE, --scope SCOPE
                        defines the scope of the test [ALL, TEST, UAT] or a
                        config file to read (def: file switch.conf)
  -U USERNAME, --username USERNAME
                        args.username (def: admin )
  -P PASSWORD, --password PASSWORD
                        args.password (def: password )
  -B BASEDIR, --basedir BASEDIR
                        directory to store data
  -v, --verbose         increase output verbosity
  -i INFO, --info INFO  show detail for check id
  -c CONVERT, --convert CONVERT
                        convert all check ids from csv to csc_checks.py
  -e, --export          export all check ids as csv


Expample:

C:\Users\Python\py csc.py

2018-05-08 09:34:50
csc1_1 - simple check - A banner shoud be set
        + ok : Test successful.
csc1_2 - simple check - CDP should not be enabled globally
        + ok : Test successful.
csc1_3 - simple check - SNMP version 1 should not be configured
        + ok : Test successful.
csc1_4 - simple check - SNMP version 2c
        + ok : Test successful.
csc1_5 - parameter check - RSA key length [2048]
        + ok : Test successful.
csc1_6 - simple check - SNMP source interface [mgmt0]
        - failed : Test failed.
csc1_7 - parameter check - SNMP source interface [mgmt0]
        + ok : Test successful.
csc1_8 - parameter check - SNMP location string
        + ok : Test successful.
csc1_9 - parameter check - SNMP destination server
        + ok : Test successful.
csc1_10 - parameter check - SNMP community string
        - failed : Test failed.
csc1_11 - parameter check - NTP server have to be configured
        + ok : Test successful.
csc1_12 - parameter check - NTP source interface [mgmt0]
        + ok : Test successful.
csc1_13 - simple check - no feature telnet
        + ok : Test successful.
csc1_14 - simple check - password strength-check
        + ok : Test successful.
csc1_15 - simple check - password secure-mode
        - failed : Test failed.
csc1_16 - simple check - no ssh key dsa
        - failed : Test failed.
csc1_17 - simple check - aaa authentication login default group
        + ok : Test successful.
csc1_18 - simple check - aaa authentication login console group
        + ok : Test successful.
csc1_19 - simple check - no ip source-route
        + ok : Test successful.
csc1_20 - simple check - no ip igmp snooping
        - failed : Test failed.
CVE_2018_0102 - two parameters check - Affected versions: 7.2(2)d1(1), 7.2(2)d1(2), 7.2(1)d(1)
        + ok : Test successful.
CVE_2018_0090 - two parameters check - Affected versions: 7.3(2)n1(0.6), 8.3(0)kms(0.31),  8.8(3.5)s0
        - failed : Test failed.
CVE_2018_0092 - two parameters check - Affected versions:  7.0(3)i5(2),  7.0(3)i6(1), 7.0(3)i7(1)
        - failed : Test failed.
CVE_2017_12341 - simple check - Affected versions:  8.1(1),  8.2(1), 8.1(0.59)s0
        + ok : Test successful.
DONE.
