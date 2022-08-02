# !/usr/bin/python3
from libs.arp import ARPdetect


arp_detector = ARPdetect('eth0')
arp_detector.detect()