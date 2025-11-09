"""CLI tool to parse `lsblk` output and convert it to JSON format."""

import subprocess
import shlex
import json


# create a function that runs suprocess and returns the output
def run_command(command):
    """Run a shell command and return its output."""
    if not command:
        return {}
    cmd = shlex.split(command)
    output = subprocess.check_output(cmd)
    return output

def run_lsblk(device):
    """
    Runs lsblk command and parses it into a JSON output format:

    lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT
    {
    "blockdevices": [
        {"name": "vda", "size": "59.6G", "type": "disk", "mountpoint": null,
            "children": [
                {"name": "vda1", "size": "59.6G", "type": "part", "mountpoint": "/etc/hosts"}
            ]
        }
    ]
    }
    """
    command = 'lsblk -J -o NAME,SIZE,TYPE,MOUNTPOINT'
    output = run_command(command)
    devices = json.loads(output)['blockdevices']
    for parent in devices:
        if parent['name'] == device:
            return parent
        for child in parent.get('children', []):
            if child['name'] == device:
                return child
    return {}

def main(device):
    """Main execution of the program: runs lsblk and prints formatted output."""

    output = run_lsblk(device)
    print(f"{output}")

if __name__ == '__main__':
    import sys
    main(sys.argv[-1])
