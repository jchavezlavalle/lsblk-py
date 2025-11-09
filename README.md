# LSBLK_PY
<img width="256" height="256" alt="ChatGPT Image 9 nov 2025, 14_56_01" src="https://github.com/user-attachments/assets/1d29cde2-54f2-4a1a-b33d-25e1349839aa" />

CLI tool in Python to parse output from lsblk into JSON format.

## The issue with LSBLK 
The tool lsblk when run inside a container you can only see the following output that lists all devices:
```
$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0    7:0    0   576K  1 loop /snap/snapd-desktop-integration/315
loop1    7:1    0 346,3M  1 loop /snap/gnome-3-38-2004/119
loop2    7:2    0 249,2M  1 loop /snap/firefox/7084
loop3    7:3    0 349,7M  1 loop /snap/gnome-3-38-2004/143
loop4    7:4    0 165,1M  1 loop /snap/mysql-workbench-community/13
loop5    7:5    0  73,9M  1 loop /snap/core22/2133
loop7    7:7    0  12,2M  1 loop /snap/snap-store/1216
loop8    7:8    0     4K  1 loop /snap/bare/5
loop9    7:9    0  50,9M  1 loop /snap/snapd/25577
loop10   7:10   0  91,7M  1 loop /snap/gtk-common-themes/1535
loop11   7:11   0  50,8M  1 loop /snap/snapd/25202
loop12   7:12   0  73,9M  1 loop /snap/core22/2139
loop13   7:13   0  12,9M  1 loop /snap/snap-store/1113
loop14   7:14   0   568K  1 loop /snap/snapd-desktop-integration/253
loop15   7:15   0 516,2M  1 loop /snap/gnome-42-2204/226
loop16   7:16   0  63,8M  1 loop /snap/core20/2669
loop17   7:17   0   516M  1 loop /snap/gnome-42-2204/202
loop18   7:18   0 249,1M  1 loop /snap/firefox/7177
loop19   7:19   0  63,8M  1 loop /snap/core20/2682
sda      8:0    0 931,5G  0 disk 
├─sda1   8:1    0   512M  0 part /boot/efi
├─sda2   8:2    0     1M  0 part 
└─sda3   8:3    0   931G  0 part /var/snap/firefox/common/host-hunspell
```
So what happens when you just need to list one of those devices? Giving the option to the side won't work, lets say we need to list only device loop4

```
$ lsblk loop4
lsblk: loop4: not a block device
```
But it is a block device, only that it is not recognized since we are inside a container. So to solve this issue, I have developed this cli tool.

## Run the cli tool

Let's check for the same device as before loop4:
```
$ python3 lsblk_py.py loop4
         '{'name': 'loop4', 'size': '165,1M', 'type': 'loop', 'mountpoint': '/snap/mysql-workbench-community/13'}'
```
Okay, now let's check for an interesting use case, a device with children in the branch, like for example sda:

```
$ python3 lsblk_py.py sda
         '{'name': 'sda', 'size': '931,5G', 'type': 'disk', 'mountpoint': None, 'children': [{'name': 'sda1', 'size': '512M', 'type': 'part', 'mountpoint': '/boot/efi'}, {'name': 'sda2', 'size': '1M', 'type': 'part', 'mountpoint': None}, {'name': 'sda3', 'size': '931G', 'type': 'part', 'mountpoint': '/'}]}'
```

Yay! now we can see the expected output in a JSON format only for the needed device 😄🚀
