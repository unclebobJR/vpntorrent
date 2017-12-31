# vpntorrent

Torrenting through a vpn tunnel requires sometimes a complete restart of torrent programme and tunnel. This was the original reason, but has been expanded as learning project for Ansible. Therefore, there are two ways of establishing this: 
* Via Ansible
* Via the original script. This one is deprecated in favour of the Ansible way.

# Ansible
Using ansible configuration the pi will be updated and upgraded and openvpn and qbittorrent wille be installed and configured.

## Pre-Requisites
* NAS with mount source
* Ansible > 2.\*
* VPN CA and CRT files
* Adjusted secrets and possibly vars files (examples can be found)
* Adjust the hosts file

## Usage
ansible-playbook playbook.yml -i hosts


# vpntorrent.py
DEPRECATED using a python script

## Pre-Requisites
* openVPN already setup and configured
* NAS with ability to wake on lan
* NAS mounts in fstab configured (so mount -a is enough)
* Linux commands on the path:
  * ping
  * mount
  * service
  * df
  * ps

## Running
Fill in the appropiate config items as found in config.py
Start the script as root
sudo ./vpntorrent.py

## Steps of scripts
1. The torrentproces is stopped (if not already stopped)
2. The NAS is waken up
3. All volumes are mounted
4. VPN tunnel is brought down, and then completely started
5. Start of torrentproces

Every step has some checks in it, and the script stops if these are not met.
In principle the script is idempotent: 

