#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

DOCUMENTATION = r'''
---
module: sasluser

short_description: Create users in sasldb

'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
    )


    result = dict(
        changed=False,
        original_message='',
        message='',
        my_useful_info={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    re_user = re.compile("^%s:"%module.params['username'])
    existing_users = module.run_command("sasldblistusers2")
    user_found = False
    for line in existing_users[1].split("\n"):
        if re_user.match(line):
            user_found = True
            break

    if not user_found:
        result['changed'] = True
        if not module.check_mode:
            create_result = module.run_command("""sh -c "echo '{password}' | saslpasswd2 -p -c {username}" """.format(password=module.params['password'], username=module.params['username']))
            result['original_message'] = create_result[1]
        result['message'] = 'user created'

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
