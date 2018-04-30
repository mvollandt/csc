# name: csc_checks.py
# desc: check definitions (security best practices and CVEs)

CVE_2018_0102 = {'check_type': 'check_two_parameters',
          'match1': 'feature pong',
          'match2': 'feature-set fabricpath',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Affected versions: 7.2(2)d1(1), 7.2(2)d1(2), 7.2(1)d(1) \nhttps://www.cvedetails.com/cve/CVE-2018-0102/',
          'fix': 'Command to fix'}

CVE_2018_0090 = {'check_type': 'check_two_parameters',
          'match1': 'cisco Nexus(20|30|55|56|60|70|77)00',
          'match2': 'access-list',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Affected versions: 7.3(2)n1(0.6), 8.3(0)kms(0.31),  8.8(3.5)s0 \nhttps://www.cvedetails.com/cve/CVE-2018-0090/',
          'fix': 'Command to fix'}

CVE_2018_0092 = {'check_type': 'check_two_parameters',
          'match1': 'cisco Nexus(30|36|90|95)00',
          'match2': 'role network-operator',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Affected versions:  7.0(3)i5(2),  7.0(3)i6(1), 7.0(3)i7(1) \nhttps://www.cvedetails.com/cve/CVE-2018-0092/',
          'fix': 'Command to fix'}

csc1_1 = {'check_type': 'check_in_simple',
          'match': 'banner motd',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
csc1_2 = {'check_type': 'check_in_simple',
          'match': 'no cdp enable',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
csc1_3 = {'check_type': 'check_not_in_simple',
          'match': 'snmpv1',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
csc1_4 = {'check_type': 'check_not_in_simple',
          'match': 'xxxx',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}

csc1_5 = {'check_type': 'check_parameter',
          'match': 'xxxx',
          'result_ok': 'This test has been successful.',
          'result_failed': 'Test failed.',
          'info': 'Some additional information.',
          'fix': 'Command to fix'}
