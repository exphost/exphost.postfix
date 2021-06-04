#!/bin/bash
result=0
trap 'result=1' ERR

chmod 400 ssh_config
py.test --hosts='ansible://test' --ansible-inventory=./libvirt-inventory.py --ssh-config ssh_config --color=yes verify.d
py.test --hosts='ansible://client' --ansible-inventory=./libvirt-inventory.py --ssh-config ssh_config --color=yes verify_client.d
exit $result

