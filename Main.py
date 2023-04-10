import queue
from Exceptions.CommandException import CommandException
from Listener import Listener
from TargetManager import TargetManager
from Dispacher import Dispacher
from Gui import Gui
from Commands import CommandHandler

if __name__ == "__main__":
    pkt_queue = queue.Queue()
    cmd_queue = queue.Queue()

    manager = TargetManager(cmd_queue)
    listener = Listener(pkt_queue)
    dispacher = Dispacher(manager, pkt_queue, cmd_queue)
    command_handler = CommandHandler(manager)
    gui = Gui(cmd_queue)

    listener.start()
    dispacher.start()
    gui.start()

    ''' Todo add CLI ALL ELSE IS ADDED'''
    while True:
        cmd = input("> ")
        cmd = cmd.split(" ")
        try:
            result = command_handler.execute_command(cmd[0], cmd[1:])
            print(result)
        except CommandException as e:
            print(e)
