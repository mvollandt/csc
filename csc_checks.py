# name: csc_checks.py
# desc: check definitions (security best practices and CVEs)

CVE_2018_0102 = {'check_name' : 'CVE_2018_0102',
          'check_type': 'check_two_parameters',
          'match1': 'feature pong',
          'match2': 'feature-set fabricpath',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Affected versions: 7.2(2)d1(1), 7.2(2)d1(2), 7.2(1)d(1) \nhttps://www.cvedetails.com/cve/CVE-2018-0102/',
          'fix': 'Command to fix'}

CVE_2018_0090 = {'check_name' : 'CVE_2018_0090',
          'check_type': 'check_two_parameters',
          'match1': 'cisco Nexus(20|30|55|56|60|70|77)00',
          'match2': 'access-list',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Affected versions: 7.3(2)n1(0.6), 8.3(0)kms(0.31),  8.8(3.5)s0 \nhttps://www.cvedetails.com/cve/CVE-2018-0090/',
          'fix': 'Command to fix'}

CVE_2018_0092 = {'check_name' : 'CVE_2018_0092',
          'check_type': 'check_two_parameters',
          'match1': 'cisco Nexus(30|36|90|95)00',
          'match2': 'role network-operator',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Affected versions:  7.0(3)i5(2),  7.0(3)i6(1), 7.0(3)i7(1) \nhttps://www.cvedetails.com/cve/CVE-2018-0092/',
          'fix': 'Command to fix'}

csc1_1 = {'check_name' : 'csc1_1',
          'check_type': 'check_in_simple',
          'match': 'banner motd',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
csc1_2 = {'check_name' : 'csc1_2',
          'check_type': 'check_in_simple',
          'match': 'no cdp enable',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
csc1_3 = {'check_name' : 'csc1_3',
          'check_type': 'check_in_simple',
          'match': 'snmpv1',
          'required' : 'no',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
csc1_4 = {'check_name' : 'csc1_4',
          'check_type': 'check_in_simple',
          'match': 'xxxx',
          'required' : 'no',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}

csc1_5 = {'check_name' : 'csc1_5',
          'check_type': 'check_parameter',
          'parameter': 'ssh key rsa',
          'match': '2048',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}

csc1_6 = {'check_name' : 'csc1_6',
          'check_type': 'check_parameter',
          'parameter': 'snmp-server source-interface traps',
          'match': 'mgmt0',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Check for snmp source interface = mgmt0',
          'fix': 'Command to fix'}

csc1_7 = {'check_name' : 'csc1_7',
          'check_type': 'check_parameter',
          'parameter': 'snmp-server location',
          'match': 'FR.*',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Check for snmp location string',
          'fix': 'Command to fix'}

csc1_8 = {'check_name' : 'csc1_8',
          'check_type': 'check_parameter',
          'parameter': 'snmp-server location',
          'match': 'FR.*',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Check for snmp location string',
          'fix': 'Command to fix'}



csc1_9 = {'check_name' : 'csc1_9',
          'check_type': 'check_parameter',
          'parameter': 'snmp-server location',
          'match': 'FR.*',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Check for snmp location string',
          'fix': 'Command to fix'}


csc1_10 = {'check_name' : 'csc1_10',
          'check_type': 'check_parameter',
          'parameter': 'snmp-server location',
          'match': 'FR.*',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Check for snmp location string',
          'fix': 'Command to fix'}


csc1_11 = {'check_name' : 'csc1_11',
          'check_type': 'check_parameter',
          'parameter': 'snmp-server location',
          'match': 'FR.*',
          'required' : 'yes',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Check for snmp location string',
          'fix': 'Command to fix'}

