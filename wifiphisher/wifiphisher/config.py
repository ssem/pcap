import os
import ConfigParser

class Config:
    def __init__(self):
        self.http_port = '8080'
        self.ssl_port = '443'
        self.pem = 'wifiphisher.pem'
        self.phishing_page = 'access-point-pages/minimal'
        self.internet_iface = 'wlan0'
        self.monitor_iface = 'wlan1'
        self.ap_address = '172.16.5.1'
        self.ap_range = '172.16.5.2,172.16.5.100,12h'
        self.parse_conf()

    def parse_conf(self):
        conf = ConfigParser.ConfigParser()
        for f in ['wifiphisher.conf', '/etc/wifiphisher.conf']:
            if os.path.exists(f):
                conf.read(f)
                if conf.has_option('wifiphisher', 'http_port'):
                    self.http_port = conf.get('wifiphisher', 'http_port')
                if conf.has_option('wifiphisher', 'ssl_port'):
                    self.ssl_port = conf.get('wifiphisher', 'ssl_port')
                if conf.has_option('wifiphisher', 'pem'):
                    self.pem = conf.get('wifiphisher', 'pem')
                if conf.has_option('wifiphisher', 'phishing_page'):
                    self.phishing_page = conf.get('wifiphisher', 'phishing_page')
                if conf.has_option('wifiphisher', 'monitor_iface'):
                    self.monitor_iface = conf.get('wifiphisher', 'monitor_iface')
                if conf.has_option('wifiphisher', 'internet_iface'):
                    self.internet_iface = conf.get('wifiphisher', 'internet_iface')
                if conf.has_option('wifiphisher', 'ap_address'):
                    self.ap_address = conf.get('wifiphisher', 'ap_address')
                if conf.has_option('wifiphisher', 'ap_range'):
                    self.ap_range = conf.get('wifiphisher', 'ap_range')
