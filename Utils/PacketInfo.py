from Utils.PacketHandler import *
import socket

class PacketInfo:
    def __init__(self, packet):
        self.eth_layer = unpack_ethernet(packet)
        self.ip_layer = unpack_ipv4(packet)

        transport_protocol = self.ip_layer['protocol']
        if transport_protocol == socket.IPPROTO_TCP:
            self.transport_layer = unpack_tcp(packet, self.ip_layer['header_length'])
            self.transport_layer_type = 'TCP'
        elif transport_protocol == socket.IPPROTO_UDP:
            self.transport_layer = unpack_udp(packet, self.ip_layer['header_length'])
            self.transport_layer_type = 'UDP'
        elif transport_protocol == socket.IPPROTO_ICMP:
            self.transport_layer = unpack_icmp(packet, self.ip_layer['header_length'])
            self.transport_layer_type = 'ICMP'
        else:
            self.transport_layer = None
            self.transport_layer_type = 'Not suported'
        