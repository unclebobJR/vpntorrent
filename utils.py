import subprocess
import time
from wakeonlan import wol


def wake_up(nas_ip, nas_mac):
    wol.send_magic_packet(nas_mac)

    i = 0
    while i < 36 and not is_up(nas_ip):
        time.sleep(5)
        i += 1

    if i == 36:
        print "Timeout waking up" + nas_ip
        exit(1)


def is_up(host):
    ping = subprocess.Popen(
        ["ping", "-c", "1", host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = ping.communicate()
    if "Unreachable" in out:
        return False
    else:
        return True


def mount_all(mount_dir):
    mount = subprocess.Popen(
        ["mount", "-a"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = mount.communicate()
    if out != "" or error != "":
        print "Fail mounting: " + out + error
        exit(1)
    else:
        df = subprocess.Popen(
            ["df", "-h"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, error = df.communicate()
        if mount_dir not in out:
            print 'volume not found: ' + mount_dir
            exit(1)


def service(cmd, name):
    svc = subprocess.Popen(
        ["service", name, cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = svc.communicate()
    if out != "" or error != "":
        print "Fail service " + cmd + " for " + name
        exit(1)
    ps = subprocess.Popen(
        ["ps", "ax"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = ps.communicate()
    if name in out:
        if cmd == 'start':
            print "Service started: " + name
        else:
            print "Service not stopped: " + name
            exit(1)
    else:
        if cmd == 'start':
            print "Service not started: " + name
            exit(1)
        else:
            print "Service stopped: " + name


def external_ip():
    curl = subprocess.Popen(
        ["curl", "ifconfig.io"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = curl.communicate()
    out = out.strip()
    return out


def kill_all(ps_name):
    kill = subprocess.Popen(
        ["killall", "-9", ps_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = kill.communicate()
    if out != "":
        print "killall failed: " + out + error
        exit(1)
    else:
        if error != "":
            if "no process found" not in error:
                print "killall failed" + out + error
                exit(1)


def new_vpn_tunnel(config, home_ip):
    if external_ip() != home_ip:
        kill_all('openvpn')

    vpn = subprocess.Popen(
        ["openvpn", "--config", config],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, error = vpn.communicate()
    if out != "" or error != "":
        print out + error
        exit(1)

    time.sleep(5)

    exit_ip = external_ip()
    if exit_ip == home_ip:
        print "tunnel failed: " + exit_ip
        exit(1)
    else:
        print "tunnel successful " + exit_ip
