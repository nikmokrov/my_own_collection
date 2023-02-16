#!/usr/bin/python

# Nikolay Mokrov for Netology DEVOPS-22
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This is my own module which can save file with given content

version_added: "1.0.0"

description: This is my own module which can save file with given content

options:
    path:
        description: Path to file
        required: true
        type: str
    content:
        description: File content as one-line string
        required: true
        type: str
    append:
        description: If true, content will be added to the end of file, else file will be overwritten
        required: false
        default: false
        type: bool

extends_documentation_fragment:
    - nikmokrov.my_collection.my_doc_fragment_name

author:
    - Nikolay Mokrov (https://github.com/nikmokrov)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  nikmokrov.my_collection.my_own_module:
    path: /home/user/test123.txt
    content: test123
    append: False

# pass in a message and have changed true
- name: Test with a message and changed output
  nikmokrov.my_collection.my_own_module:
    path: test123.txt
    content: test123
    append: True

# fail the module
- name: Test failure of the module
  nikmokrov.my_collection.my_own_module:
    path: 'one*two.txt'
    content: one*two
'''

RETURN = r'''
# These are examples of possible return values.
original_message:
    description: The original path and rewrite params that was passed in.
    type: str
    returned: always
    sample: 'Requested file test123.txt. Content must be overwritten.'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'File was written successfully.'
'''

from ansible.module_utils.basic import AnsibleModule
import os


def is_path_valid(path):
    forbidden_chars = '<>:"|?*'
    for c in path:
        if c in forbidden_chars:
            return False
    return True


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
                       path=dict(type='str', required=True),
                       content=dict(type='str', required=True),
                       append=dict(type='bool', required=False, default=False)
                      )
    
    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = f"Requested file {module.params['path']}. Content must be {'added' if module.params['append'] else 'overwritten'}."

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    something_wrong = False
    if len(module.params['path']) == 0:
        something_wrong = True
        result['message'] = 'Path is empty string'
    elif not is_path_valid(module.params['path']):
        something_wrong = True
        result['message'] = 'Path is not valid, forbidden chars'
    elif (len(os.path.dirname(module.params['path'])) > 0) and not os.path.isdir(os.path.dirname(module.params['path'])):
        something_wrong = True
        result['message'] = 'Dir is not exists'
    elif len(module.params['content']) == 0:
        something_wrong = True
        result['message'] = 'Nothing to write. Content is empty'
    else:
        need_write = True
        mode = 'a' if module.params.get('append', False) else 'w'
        if mode == 'w':
            try:
                with open(module.params['path'], mode='r', encoding='utf8') as file:
                    data = file.read()
                    if data == module.params['content']:
                        result['message'] = 'Content is the same. File was NOT touched.'
                        need_write = False
            except:
                pass

        # write file
        if need_write:
            try:
                with open(module.params['path'], mode=mode, encoding='utf8') as file:
                    file.write(module.params['content'])
                    result['message'] = 'File was written successfully.'
                    result['changed'] = True
            except:
                something_wrong = True 
                result['message'] = 'There was exception.'

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if something_wrong:
        module.fail_json(msg='File was not written.', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()