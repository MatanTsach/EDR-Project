from threading import Thread
from queue import Queue
from queue import Empty
from TargetManager import TargetManager
from Target import Target
from Utils.PacketInfo import PacketInfo
import Utils.FilterType as FilterType


class Dispacher(Thread):
    def __init__(self, manager: TargetManager, pkt_queue: Queue, cmd_queue: Queue):
        super().__init__()
        self.pkt_queue = pkt_queue
        self.cmd_queue = cmd_queue
        self.manager = manager

    def run(self):
        while True:
            try:
                # Receive packet from queue
                packet = self.pkt_queue.get_nowait()
                pkt = PacketInfo(packet)

                # Check if packet is valid
                if not pkt.transport_layer:
                    continue

                # Get targets by address
                mac_targets = self.manager.get_targets_by_address(
                    pkt.eth_layer['source_mac'])
                ip_targets = self.manager.get_targets_by_address(
                    pkt.ip_layer['source_ip'])

                # Attempt send packet to targets
                self.send_packet(mac_targets + ip_targets, pkt)
            except Empty:
                pass

    def send_packet(self, targets: list, pkt: PacketInfo):
        for target in targets:
            if self.validate_filters(target, pkt):
                self.cmd_queue.put(
                    f"update {target.name} {target.addr} {pkt.transport_layer['source_port']} {pkt.transport_layer_type} {pkt.transport_layer['payload']}")

    def validate_filters(self, target: Target, pkt: PacketInfo):
        for pkt_filter in target.filters:
            if not FilterType.validate_filter(pkt_filter, pkt):
                return False
        return True
