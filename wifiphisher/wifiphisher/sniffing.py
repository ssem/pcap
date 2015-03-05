import os
import sys
import time
import random
import threading
import subprocess
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
import scapy
from scapy.all import sniff

def _channel_hop(iface, interval, stop):
    while not stop.is_set():
        try:
            channel = str(random.choice([1,1,1,2,3,4,5,6,6,6,7,8,9,10,11,11,11]))
            subprocess.call(['iw', 'dev', iface, 'set', 'channel', channel],
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:pass
        time.sleep(interval)

access_points = []
def targeting_cb(pkt):
    if pkt.haslayer(scapy.all.Dot11Beacon) or pkt.haslayer(scapy.all.Dot11ProbeResp):
        ap_channel = str(ord(pkt[scapy.all.Dot11Elt:3].info))
        essid = pkt[scapy.all.Dot11Elt].info
        mac = pkt[scapy.all.Dot11].addr2
        for ap in access_points:
            if essid == ap[1]:
                return
        access_points.append([ap_channel, essid, mac])
        os.system('clear')
        sys.stdout.write('[+] Ctrl-C at any time to copy an access point from below\n')
        sys.stdout.write('num       ch        ESSID\n')
        sys.stdout.write('-------------------------\n')
        for ap in access_points:
            sys.stdout.write('\033[32m{:<10}\033[0m{:<10}\033[93m{:20}\033[0m\n'.format(
                access_points.index(ap), ap[0], ap[1]))

class Sniffing:
    def __init__(self):
        self.events = {}

    def find_target_ap(self, iface, interval=1):
        try:
            sys.stdout.write('[\033[32m+\033[0m] Setting Up Interface %s\n' % iface)
            self._reset_interface(iface)
            self._start_channel_hoping(iface, interval)
            sniff(iface=iface, prn=targeting_cb, store=0) # scapy sniff
        except: exit('Not able to monitor on %s' % iface)
        while True:
            try:
                num = raw_input('[+] Choose the [\033[32mnum\033[0m] of the AP you wish to copy: ')
                results = access_points[int(num)]
                self._stop_channel_hoping(iface)
                os.system('clear')
                return results
            except KeyboardInterrupt:
                sys.exit(-1)

    def _reset_interface(self, iface):
        #sys.stdout.write('[\033[32m+\033[0m] %s Killing Processes\n' % iface)
        subprocess.call(['airmon-ng', 'stop', iface],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] %s Down\n' % iface)
        subprocess.call(['ifconfig', iface, 'down'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] %s Monitor Mode\n' % iface)
        subprocess.call(['iwconfig', iface, 'mode', 'monitor'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #sys.stdout.write('[\033[32m+\033[0m] %s Up\n' % iface)
        subprocess.call(['ifconfig', iface, 'up'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def _start_channel_hoping(self, iface, interval):
        stop = threading.Event()
        self.events[iface] = stop
        hop = threading.Thread(target=_channel_hop, args=(iface, interval, stop))
        hop.daemon = True
        hop.start()

    def _stop_channel_hoping(self, iface):
        try:self.events[iface].set()
        except:pass
