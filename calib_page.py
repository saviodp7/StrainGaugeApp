import tkinter as tk
from tkinter import ttk

from arduinopuller import ArduinoPuller
import settings_scales


class CalibPage(ttk.Frame):
    def __init__(self, master, container, com_port):
        super().__init__(container)

        self.puller = ArduinoPuller(com_port)
        self.container = container
        self.master = master
        self.master.geometry("400x350")

        # Frame menu
        self.nome_frame = ttk.Frame(self)
        self.nome_frame.pack(pady=10)
        self.peso_frame = ttk.Frame(self)
        self.peso_frame.pack(pady=20)

        # Variabili
        self.nome_calibrazione = tk.StringVar()
        self.peso_di_calibrazione = tk.DoubleVar()
        self.istruzioni = tk.StringVar()
        self.istruzioni.set("Liberare la bilancia e avviare la calibrazione")
        self.calibration_factors = list()

        # Entry: Nome calibrazione
        self.nome_calibrazione_label = tk.Label(self.nome_frame, text="Nome calibrazione:")
        self.nome_calibrazione_label.pack(fill="x", expand=True)
        self.nome_calibrazione_entry = tk.Entry(self.nome_frame, textvariable=self.nome_calibrazione,justify="center")
        self.nome_calibrazione_entry.pack(padx=25)

        # Entry : Peso di calibrazione
        self.campione_di_calibrazione_label = tk.Label(self.peso_frame, text="Campione di calibrazione:")
        self.campione_di_calibrazione_label.pack(fill="x", expand=True)
        self.campione_di_calibrazione_entry = tk.Entry(self.peso_frame, textvariable=self.peso_di_calibrazione, width=7, justify="center")
        self.campione_di_calibrazione_entry.pack(side="left")
        self.unita_di_misura_label = tk.Label(self.peso_frame, text="kg", justify="left")
        self.unita_di_misura_label.pack(fill="x", expand=True)

        # Istruzioni
        self.istruzioni_label = tk.Label(self, textvariable=self.istruzioni, justify="center", bg="light grey",)
        self.istruzioni_label.pack(ipady=5, ipadx=15, pady=10, expand=True)

        # Progress Bar
        self.bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", maximum=20)
        self.bar.pack(fill="x", padx=30, expand=True)

        # Buttons
        self.avvia_button = tk.Button(self, text="Avvia", bg="white", fg="black", command=self.avvia_calib)
        self.avvia_button.pack(side="left", ipadx=30, ipady=10, pady=20, expand=True)
        self.termina_button = tk.Button(self, text="Termina", bg="white", fg="black", command=self.termina_calib)
        self.termina_button.pack(side="right", ipadx=30, ipady=10, pady=20, expand=True)

        self.focus_set()

    def avvia_calib(self):
        if(not self.peso_di_calibrazione.get()):
            tk.messagebox.showerror("Peso di calibrazione","Inserire un peso di calibrazione\nprima di avviare il processo")
        else:
            self.puller.write("calib")
            self.bar.start()
            self.istruzioni.set("Inserire il campione sulla bilancia\n e premere 'continua'")
            self.avvia_button.pack_forget()
            self.avvia_button.destroy()
            self.continua_button = tk.Button(self, text="Continua", bg="white", fg="black", command=self.continua_calib)
            self.continua_button.pack(side="left", ipadx=30, ipady=10, pady=20, expand=True)

    def continua_calib(self):
        self.istruzioni.set("Calibrando...")
        self.puller.write(str(self.peso_di_calibrazione.get()))
        done = False
        while not done:
            self.calibration_factors = self.puller.pull()
            if self.calibration_factors[0] == "calib_done":
                done = True
        self.calibration_factors = (self.calibration_factors[1],self.calibration_factors[2])
        self.avvia_button = tk.Button(self, text="Avvia", bg="white", fg="black", command=self.avvia_calib)
        self.avvia_button.pack(side="left", ipadx=30, ipady=10, pady=20, expand=True)
        self.continua_button.pack_forget()
        self.continua_button.destroy()
        self.bar.stop()
        self.istruzioni.set("Calibrazione effettuata")

    def termina_calib(self):
        try:
            if(not self.nome_calibrazione.get()):
                tk.messagebox.showerror("Nome calibrazione","Dare un nome alla calibrazione\nprima di terminare il processo")
            else:
                saved_calib = open("calibrations.txt", "a")
                saved_calib.writelines("\n" + self.nome_calibrazione.get() + "," + str(self.calibration_factors[0]) + "," + str(self.calibration_factors[1]))
                saved_calib.close()
                self.puller.ser.close()
                self.master.switch_frame(settings_scales.SettingsPage, self.container, {})

        except IndexError:
            tk.messagebox.showerror("Calibrazione incompleta", "Completare la calibrazione\nprima di terminare il processo")
