import Target

class TargetManager:

    def __init__(self, cmd_queue):
        self.targets = {}
        self.gui_queue = cmd_queue

    def add_target(self, target: Target) -> None:
        if target.addr not in self.targets:
            # Adding to dictionary
            self.targets[target.name] = target
            #Creating window
            self.gui_queue.put(f"create {target.name}")
    
    def remove_target(self, target: Target) -> None:
        if target.name in self.targets:
            #Removing from dictionary
            del self.targets[target.name]
            #Removing window
            self.gui_queue.put(f"remove {target.name}")

    def get_targets_by_address(self, addr: str) -> list:
        return [target for target in self.targets.values() if target.addr == addr]
    
    def contains_target(self, name: str) -> bool:
        return name in self.targets