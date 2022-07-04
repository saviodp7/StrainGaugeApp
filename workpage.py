import tkinter as tk
from tkinter import ttk
from channels import ChannelsFrame
import serial


class WorkPage(ttk.Frame):

    def __init__(self, master, container, **kwargs):
        super().__init__(container)

        self.master = master

        # Frame canali
        self.channels = ChannelsFrame(self, kwargs['com_port'], kwargs['number_of_channels'], kwargs['tempo_di_misura'], kwargs['smp_time'])
        self.channels.pack(side="left", fill="both", expand=True)
        self.master.geometry("1400x" + str(int(kwargs['number_of_channels']) * 300))

        # Frame comandi
        self.commands_frame = ttk.Frame(self)
        self.commands_frame.pack(side="right", fill="y")
        # Start
        self.start_button = tk.Button(self.commands_frame, text="START/STOP", bg="black",
                                      fg="white", command=self.channels.start_stop)
        self.start_button.pack(padx=10, pady=10, ipadx=20, ipady=12, fill="both")
        # Reset
        self.reset_button = tk.Button(self.commands_frame, text="RESET", bg="black",
                                      fg="white", command=self.channels.reset)
        self.reset_button.pack(padx=10, pady=10, ipadx=20, ipady=12, fill="both")
        # Tara
        self.tara_button = tk.Button(self.commands_frame, text="TARA", bg="black",
                                     fg="white", command=self.channels.tara)
        self.tara_button.pack(padx=10, pady=10, ipadx=20, ipady=12, fill="both")
        # Export
        self.export_button = tk.Button(self.commands_frame, text="EXPORT", bg="black",
                                       fg="white", command=self.channels.export_to_csv)
        self.export_button.pack(side="bottom", padx=10, pady=10, ipadx=20, ipady=12, fill="both")
