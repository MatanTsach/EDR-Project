from tkinter import *
from tkinter import ttk
from threading import Thread
from queue import Queue
from queue import Empty


class Gui(Thread):
    def __init__(self, cmd_queue: Queue):
        super().__init__()
        self.cmd_queue = cmd_queue
        self.windows = {}
        self.headers = ['Source', 'Port', 'Protocol', 'Info']

    def run(self):
        root = Tk()
        root.withdraw()
        while True:
            try:
                cmd = self.cmd_queue.get_nowait().split(" ")

                if cmd[0] == "create":
                    self.windows[cmd[1]] = self.create_window(root, cmd[1])
                elif cmd[0] == "delete":
                    self.delete_window(cmd[1])
                elif cmd[0] == "update":
                    self.update_window(
                        cmd[1], cmd[2], cmd[3], cmd[4], ' '.join(cmd[5:]))

            except Empty:
                pass

            root.update()

    def create_window(self, master, title: str):
        window = Toplevel(master)
        window.title(title)
        window.geometry("1000x400")
        window.configure(background='white')

        tree = ttk.Treeview(window, columns=self.headers, show='headings')
        for i, header in enumerate(self.headers):
            tree.heading(i, text=header)
            tree.column(i, width=0, anchor='center', stretch=True)

        tree.grid(row=0, column=0, sticky='nsew')

        '''configure grid weights so the tree will expand to fill the window'''
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        return window

    def delete_window(self, name):
        self.windows[name].destroy()
        del self.windows[name]

    def update_window(self, name, addr, port, protocol, data):
        window = self.windows[name]

        """insert the data to the treeview"""
        tree = window.children['!treeview']
        tree.insert('', 'end', values=(addr, port, protocol, data))
