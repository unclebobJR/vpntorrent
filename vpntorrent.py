#!/usr/bin/python

import config
from utils import service, wake_up, mount_all, new_vpn_tunnel

service('stop', config.torrentproces)

wake_up(config.nas_ip, config.nas_mac)

mount_all(config.target_dir)

new_vpn_tunnel(config.vpn_tunnel, config.home_ip)

service('start', config.torrentproces)
