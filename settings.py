import tkinter as tk
from tkinter import ttk
from PIL import ImageTk


class SettingsPage(ttk.Frame):
    def __init__(self, container, master):
        super().__init__(container)

        self.master = master

        # Immagine
        self.picture = tk.Label(self, bg="white")
        self.picture.pack(side="top", expand=True)
        self.img = ImageTk.PhotoImage(file="sg.png")
        self.picture.configure(image=self.img)

        # Frame menu
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack()
        # Variabili menu
        self.com_port = tk.StringVar()
        self.number_of_channels = tk.StringVar()
        self.tempo_di_misura = tk.StringVar()
        self.smp_time = tk.StringVar()
        # Valori default
        self.com_port.set("COM3")
        self.tempo_di_misura.set("30")
        self.number_of_channels.set("1")
        self.smp_time.set("50")
        # Ddm Porta COM
        self.com_port_label = tk.Label(self.menu_frame, text="Porta\nArduino:")
        self.com_port_label.pack(side="left", fill="x", padx=10, pady=20, expand=True)
        self.ddm_com_port = tk.OptionMenu(self.menu_frame, self.com_port, "COM1", "COM2", "COM3", "COM4",
                                          "COM5", "COM6", "COM7", "COM8", "COM9")
        self.ddm_com_port.pack(side="left", fill="x", pady=20, expand=True)
        # Ddm numero di canali
        self.number_of_channels_label = tk.Label(self.menu_frame, text="Numero di\ncanali:")
        self.number_of_channels_label.pack(side="left", fill="x", padx=10, pady=20, expand=True)
        self.ddm_number_of_channels = tk.OptionMenu(self.menu_frame, self.number_of_channels, "1", "2", "3", "4")
        self.ddm_number_of_channels.pack(side="left", fill="x", pady=20, expand=True)
        # Entry intervallo di misura
        self.intervallo_di_misura_label = tk.Label(self.menu_frame, text="Intervallo di\nmisura (s):")
        self.intervallo_di_misura_label.pack(side="left", fill="x", padx=10, pady=20, expand=True)
        self.intervallo_di_misura_entry = tk.Entry(self.menu_frame, textvariable=self.tempo_di_misura, width=5)
        self.intervallo_di_misura_entry.pack(side="left", fill="x", pady=20, expand=True)
        # Entry periodo di campionamento
        self.periodo_campionamento_label = tk.Label(self.menu_frame, text="Periodo di\ncampionamento (ms):")
        self.periodo_campionamento_label.pack(side="left", fill="x", padx=10, pady=20, expand=True)
        self.periodo_campionamento_entry = tk.Entry(self.menu_frame, textvariable=self.smp_time, width=5)
        self.periodo_campionamento_entry.pack(side="left", fill="x", pady=20, expand=True)
        # Button Ok
        self.ok_button = tk.Button(self, text="Ok", bg="white", fg="black", command=self.finish_setup)
        self.ok_button.pack(side="bottom", ipadx=30, ipady=10, pady=20)

    def finish_setup(self):
        if int(self.tempo_di_misura.get()) < 0:
            tk.messagebox.showerror("Tempo di misura", "Tempo di misura non valido")
        elif int(self.smp_time.get()) < 0:
            tk.messagebox.showerror("Periodo di campionamento", "Periodo di campionamento non valido")
        else:
            self.master.switch_frame(self.com_port.get(), self.number_of_channels.get(),
                                     self.tempo_di_misura.get(), self.smp_time.get())
