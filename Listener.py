from threading import Thread
from queue import Queue
import socket


class Listener(Thread):
    def __init__(self, pkt_queue: Queue):
        super().__init__()
        self.pkt_queue = pkt_queue

    def run(self):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        while True:
            raw_data, _ = s.recvfrom((65565))
            self.pkt_queue.put_nowait(raw_data)