# name: csc_checks.py
# desc: check definitions


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


