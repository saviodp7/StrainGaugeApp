import tkinter as tk
from tkinter import ttk
from channels import ChannelsFrame


class WorkPage(ttk.Frame):

    def __init__(self, container, com_port, number_of_channels, tempo_di_misura, smp_time):
        super().__init__(container)

        # Frame canali
        self.channels = ChannelsFrame(self, com_port, number_of_channels, tempo_di_misura, smp_time)
        self.channels.pack(side="left", fill="both", expand=True)

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
