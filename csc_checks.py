# filename    : csc_checks.py
# description : check definitions (security best practices and CVEs)
# create date : 2018-05-02 13:20:48.485834

csc1_1 = {'check_name': 'csc1_1',
		'check_type': 'check_in_simple',
		'match1': 'banner motd',
		'match2': 'n/a',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Some additional information.',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_2 = {'check_name': 'csc1_2',
		'check_type': 'check_in_simple',
		'match1': 'no cdp enable',
		'match2': 'n/a',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Some additional information.',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_3 = {'check_name': 'csc1_3',
		'check_type': 'check_in_simple',
		'match1': 'snmpv1',
		'match2': 'n/a',
		'required': 'no',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Some additional information.',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_4 = {'check_name': 'csc1_4',
		'check_type': 'check_in_simple',
		'match1': 'xxxx',
		'match2': 'n/a',
		'required': 'no',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Some additional information.',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_5 = {'check_name': 'csc1_5',
		'check_type': 'check_parameter',
		'match1': 'ssh key rsa',
		'match2': '2048',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'RSA key length [2048]',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_6 = {'check_name': 'csc1_6',
		'check_type': 'check_parameter',
		'match1': 'snmp-server source-interface traps',
		'match2': 'mgmt0',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'SNMP source interface [mgmt0]',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_7 = {'check_name': 'csc1_7',
		'check_type': 'check_parameter',
		'match1': 'snmp-server location',
		'match2': 'FR.*',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'SNMP location string',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_8 = {'check_name': 'csc1_8',
		'check_type': 'check_parameter',
		'match1': 'snmp-server host',
		'match2': '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'SNMP destination server',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_9 = {'check_name': 'csc1_9',
		'check_type': 'check_parameter',
		'match1': 'snmp-server community',
		'match2': 'your_community_string_here',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'SNMP community string',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_10 = {'check_name': 'csc1_10',
		'check_type': 'check_parameter',
		'match1': 'ntp server',
		'match2': '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'NTP server',
		'url': 'n/a',
		'fix': 'Command to fix',}

csc1_11 = {'check_name': 'csc1_11',
		'check_type': 'check_parameter',
		'match1': 'ntp source-interface',
		'match2': 'mgmt0',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'NTP source interface [mgmt0]',
		'url': 'n/a',
		'fix': 'Command to fix',}

CVE_2018_0102 = {'check_name': 'CVE_2018_0102',
		'check_type': 'check_two_parameters',
		'match1': 'feature pong',
		'match2': 'feature-set fabricpath',
		'required': 'no',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Affected versions: 7.2(2)d1(1), 7.2(2)d1(2), 7.2(1)d(1)',
		'url': 'https://www.cvedetails.com/cve/CVE-2018-0102/',
		'fix': 'Command to fix',}

CVE_2018_0090 = {'check_name': 'CVE_2018_0090',
		'check_type': 'check_two_parameters',
		'match1': 'cisco Nexus(20|30|55|56|60|70|77)00',
		'match2': 'access-list',
		'required': 'no',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Affected versions: 7.3(2)n1(0.6), 8.3(0)kms(0.31),  8.8(3.5)s0',
		'url': 'https://www.cvedetails.com/cve/CVE-2018-0090/',
		'fix': 'Command to fix',}

CVE_2018_0092 = {'check_name': 'CVE_2018_0092',
		'check_type': 'check_two_parameters',
		'match1': 'cisco Nexus(30|36|90|95)00',
		'match2': 'role network-operator',
		'required': 'yes',
		'result_ok': 'This test has been successful.',
		'result_failed': 'Test failed.',
		'info': 'Affected versions:  7.0(3)i5(2),  7.0(3)i6(1), 7.0(3)i7(1)',
		'url': 'https://www.cvedetails.com/cve/CVE-2018-0092/',
		'fix': 'Command to fix',}

