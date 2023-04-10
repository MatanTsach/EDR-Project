
class Target:
    def __init__(self, addr, addr_type: str, name: str):
        self.addr = addr
        self.name = name
        self.addr_type = addr_type
        self.filters = []

    def add_filter(self, pkt_filter) -> None:
        if pkt_filter not in self.filters:
            self.filters.append(pkt_filter)
    
    def remove_filter(self, pkt_filter) -> None:
        if pkt_filter in self.filters:
            self.filters.remove(pkt_filter)

    def has_filter(self, pkt_filter) -> bool:
        return pkt_filter in self.filters

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    
    
    
    