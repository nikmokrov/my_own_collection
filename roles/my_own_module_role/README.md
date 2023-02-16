my_own_module_role
=========

This role run my_own_module module for ansible

Role Variables
--------------

_my_own_module_path_ - where to write file </br>
_my_own_module_content_ - single-line string file content </br>
_my_own_module_append_ - append content to file or overwrite, default true </br>

Example Playbook
----------------

You can use this role simple like this:

    - hosts: servers
      roles:
         - { role: my_own_module_role, my_own_module_path: "./test123.txt", my_own_module_content: "test123"  }

License
-------

MIT

Author Information
------------------

Nikolay Mokrov
