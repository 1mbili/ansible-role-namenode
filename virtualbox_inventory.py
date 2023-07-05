"""
Creates dynamic inventory of virtualbox VMs related to Hadoop cluster
"""

import subprocess
import re
from ansible.module_utils._text import to_text

START = """
[all:children]
namenodes
datanodes

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
ansible_port=22
ansible_user='vagrant'
ansible_ssh_private_key_file="{{ lookup('env','ansible_ssh_key') }}"

[namenodes]
"""
def get_vms():
    """
    Returns a Dict of VMs that are running
    """
    cmd = "vagrant global-status --prune"
    boxes = {"namenodes": [], "datanodes": []}

    vms = subprocess.check_output(cmd, shell=True)
    vms = vms.decode("utf-8")
    vms = vms.split("\n")
    vms = vms[2:-9]
    for vm in vms:
        vm = re.split(r"\s+", vm)
        if "running" not in vm[3]:
            continue
        if "dn" in vm[1]:
            boxes["datanodes"].append(vm[1])
        elif "nn" in vm[1]:
            boxes["namenodes"].append(vm[1])
    return boxes


def main():
    vms = get_vms()
    global START
    for namenode in vms["namenodes"]:
        START += namenode + " ansible_host=192.168.58.2\n"
    START += "\n[datanodes]\n"
    for i, datanode in enumerate(vms["datanodes"]):
        START += datanode + " ansible_host=192.168.58." + str(i + 3) + "\n"
    return START

if __name__ == "__main__":
    print(main())