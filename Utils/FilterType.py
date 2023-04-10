
# Description: This file contains the filter types that are used in the program.
filters = {
    "TCP": lambda pkt_info: pkt_info.transport_layer.protocol == "TCP",
    "UDP": lambda pkt_info: pkt_info.transport_layer.protocol == "UDP",
    "ICMP": lambda pkt_info: pkt_info.transport_layer.protocol == "ICMP",
    "ACK": lambda pkt_info: pkt_info.transport_layer.flags & 0x10 == 0x10,
    "SYN": lambda pkt_info: pkt_info.transport_layer.flags & 0x02 == 0x02,
    "FIN": lambda pkt_info: pkt_info.transport_layer.flags & 0x01 == 0x01,
} 

def validate_filter(filter_type: str, pkt_info) -> bool:
    return filters[filter_type](pkt_info)
