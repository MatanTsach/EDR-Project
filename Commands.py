from Exceptions.CommandException import CommandException
from Utils.AddressUtils import *
from TargetManager import TargetManager
from Target import Target
import Utils.FilterType as FilterType

class CommandHandler:
    def __init__(self, target_manager: TargetManager):
        self.target_manager = target_manager
        self.cli_commands = {
            "add": self.add_target,
            "remove": self.remove_target,
            "add_filter": self.add_filter,
            "remove_filter": self.remove_filter,
            "list_targets": self.list_targets,
            "list_target_filters": self.list_target_filters,
            "help": self.help
        }

    def add_target(self, args):
        if len(args) != 3:
            raise CommandException("Invalid number of arguments")

        addr = args[0]
        addr_type = args[1]
        name = args[2]

        if addr_type not in ["ipv4", "mac"]:
            raise CommandException("Invalid address type")

        if addr_type == "ipv4":
            if not is_valid_ipv4_address(addr):
                raise CommandException("Invalid IPv4 address")
        else:
            if not is_valid_mac_address(addr):
                raise CommandException("Invalid MAC address")

        if not name.isalnum():
            raise CommandException("Name needs to be alphanumeric.")

        if self.target_manager.contains_target(name):
            raise CommandException("A target with this name already exists.")

        self.target_manager.add_target(Target(addr, addr_type, name))
        return f"Target {name} added."

    def remove_target(self, args):
        if len(args) != 1:
            raise CommandException("Invalid number of arguments")

        name = args[0]

        target = self.target_manager.get_target_by_name(name)

        if target is None:
            raise CommandException("Target does not exist.")

        self.target_manager.remove_target(target)
        return f"Target {name} removed."

    def add_filter(self, args):
        name = args[0]
        target_filter = args[1]

        target = self.target_manager.get_target_by_name(name)
        if target is None:
            raise CommandException("Target does not exist.")
        
        if not target_filter in FilterType.filters:
            raise CommandException("Invalid filter type.")
        
        if target.has_filter(target_filter):
            raise CommandException("Target already has this filter.")
        
        target.add_filter(target_filter)
        return f"Filter {target_filter} added to target {name}."

    def remove_filter(self, args):
        name = args[0]
        target_filter = args[1]

        target = self.target_manager.get_target_by_name(name)
        if target is None:
            raise CommandException("Target does not exist.")
        
        if not target_filter in FilterType.filters:
            raise CommandException("Invalid filter type.")
        
        if not target.has_filter(target_filter):
            raise CommandException("Target does not have this filter.")
        
        target.remove_filter(target_filter)
        return f"Filter {target_filter} removed from target {name}."

    def list_targets(self, args):
        targets = self.target_manager.targets.values()
        
        return_val = "Active Targets:\n"
        for target in targets:
            return_val += f"\t{target.name} {target.addr} {target.addr_type}\n"
        return return_val

    def list_target_filters(self, args):
        target_name = args[0]
        target = self.target_manager.get_target_by_name(target_name)

        if not target:
            raise CommandException("Target does not exist.")
        
        return_val = f"Filters for target {target_name}:\n"
        for pkt_filter in target.filters:
            return_val += f"\t{pkt_filter}\n"
        return return_val
    
    def help(self, args):
        return_val = "Available commands:\n"
        
        return_val += "\tadd <address> <address_type> <name>\n"
        return_val += "\t\tAdds a target to the list of targets.\n"
        return_val += "\t\t<address_type> can be either ipv4 or mac.\n"
        return_val += "\tremove <name>\n"
        return_val += "\t\tRemoves a target from the list of targets.\n"
        return_val += "\tadd_filter <name> <filter>\n"
        return_val += "\t\tAdds a filter to a target.\n"
        return_val += "\t\t<filter> is the filter to add to the target.\n"
        return_val += "\tremove_filter <name> <filter>\n"
        return_val += "\t\tRemoves a filter from a target.\n"
        return_val += "\t\t<filter> is the filter to remove from the target.\n"
        return_val += "\tlist_targets\n"
        return_val += "\t\tLists all active targets.\n"
        return_val += "\tlist_target_filters <name>\n"
        return_val += "\t\tLists all filters for a target.\n"
        return return_val

    def execute_command(self, command: str, args: str):
        if command in self.cli_commands:
            return self.cli_commands[command](args)
        else:
            raise CommandException("Unknown command")
