import socket
import struct
import textwrap


def unpack_ethernet(packet):
    # ! = big endian s = char[](char=1byte), H = short(2bytes)
    # htons convert from computer encoding to network(big endian)
    ethernet_header = packet[:14] # Get the Ethernet header bytes from the packet
    dest_mac, src_mac, ethertype = struct.unpack("!6s6sH", ethernet_header)
    return {
        "destination_mac": dest_mac.hex(':'),
        "source_mac": src_mac.hex(':'),
        "ethertype": hex(ethertype)
    }


def unpack_ipv4(packet):
    ipv4_header = packet[14:34] # Get the IPv4 header bytes from the packet
    version_header_length, dscp_ecn, total_length, identification, flags_fragment_offset, ttl, protocol, header_checksum, source_ip, dest_ip = struct.unpack('!BBHHHBBH4s4s', ipv4_header)
    version = version_header_length >> 4 # Get the version from the version-header length field
    header_length = (version_header_length & 0xF) * 4 # Get the header length from the version-header length field
    df = bool(flags_fragment_offset & (1 << 14)) # Get the DF (Don't Fragment) flag from the flags-fragment offset field
    mf = bool(flags_fragment_offset & (1 << 13)) # Get the MF (More Fragments) flag from the flags-fragment offset field
    reserved = bool(flags_fragment_offset & 0x1FFF) # Get the Reserved field from the flags-fragment offset field
    fragment_offset = flags_fragment_offset & 0x1FFF # Get the fragment offset from the flags-fragment offset field
    return {
        "version": version,
        "header_length": header_length,
        "dscp_ecn": dscp_ecn,
        "total_length": total_length,
        "identification": identification,
        "df": df,
        "mf": mf,
        "reserved": reserved,
        "fragment_offset": fragment_offset,
        "ttl": ttl,
        "protocol": protocol,
        "header_checksum": header_checksum,
        "source_ip": socket.inet_ntoa(source_ip),
        "dest_ip": socket.inet_ntoa(dest_ip)
    }

def unpack_tcp(packet, ip_header_length=20):
        tcp_header = struct.unpack('!HHLLBBHHH', packet[14+ip_header_length:14+ip_header_length+20])
        
        # Extracting fields from the header
        source_port = tcp_header[0]
        destination_port = tcp_header[1]
        sequence_number = tcp_header[2]
        acknowledgement_number = tcp_header[3]
        data_offset = (tcp_header[4] >> 4) * 4
        flags = tcp_header[5]
        window_size = tcp_header[6]
        checksum = tcp_header[7]
        urgent_pointer = tcp_header[8]
        
        # TCP flags bit masks
        urg = flags & 0x20
        ack = flags & 0x10
        psh = flags & 0x08
        rst = flags & 0x04
        syn = flags & 0x02
        fin = flags & 0x01

        payload = packet[14+ip_header_length+data_offset:]
        # Return a dictionary of the extracted fields
        return {
            'source_port': source_port,
            'destination_port': destination_port,
            'sequence_number': sequence_number,
            'acknowledgement_number': acknowledgement_number,
            'data_offset': data_offset,
            'flags': {
                'urg': bool(urg),
                'ack': bool(ack),
                'psh': bool(psh),
                'rst': bool(rst),
                'syn': bool(syn),
                'fin': bool(fin),
            },
            'window_size': window_size,
            'checksum': checksum,
            'urgent_pointer': urgent_pointer,
            'payload': format_payload(payload)
        }

def unpack_udp(packet, ip_header_length=20):
    udp_header = struct.unpack('!HHHH', packet[14+ip_header_length:14+ip_header_length+8])   
    # Extracting fields from the header
    source_port = udp_header[0]
    destination_port = udp_header[1]
    length = udp_header[2]
    checksum = udp_header[3]
    payload = packet[14+ip_header_length+8:]
    # Return a dictionary of the extracted fields
    return {
        'source_port': source_port,
        'destination_port': destination_port,
        'length': length,
        'checksum': checksum,
        'payload': format_payload(payload)
    }

    

def unpack_icmp(packet, ip_header_length=20):
    icmp_header = struct.unpack('!BBH', packet[14+ip_header_length:14+ip_header_length+4])
            
    # Extracting fields from the header
    icmp_type = icmp_header[0]
    icmp_code = icmp_header[1]
    icmp_checksum = icmp_header[2]
    
    # Extract the payload
    payload = packet[14+ip_header_length+4:]
    
    # Return a dictionary of the extracted fields and payload
    return {
        'source_port': '-',
        'type': icmp_type,
        'code': icmp_code,
        'checksum': icmp_checksum,
        'payload': format_payload(payload)
    }


def getip(ip_data):
    return '.'.join(map(str, ip_data))


def convert_mac_addr(data):
    mac = map('{:02x}'.format, data)
    return ':'.join(mac).upper()


def format_payload(payload):
    hexed_payload = ' '.join(format(n, '02X') for n in payload)
    return hexed_payload
