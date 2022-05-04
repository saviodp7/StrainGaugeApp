import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import time

from workpage import WorkPage
from calib_page import CalibPage
import arduinopuller as ap

class SettingsPage(ttk.Frame):
    def __init__(self, master, container):
        super().__init__(container)

        self.puller = ap.ArduinoPuller(com_port="COM3")
        self.container = container
        self.master = master
        self.master.geometry("1000x700")

        # Immagine
        self.picture = tk.Label(self, bg="white")
        self.picture.pack(side="top", expand=True)
        self.img = ImageTk.PhotoImage(file="sg.png")
        self.picture.configure(image=self.img)

        # Binding tasti
        self.bind("<Return>", lambda event: self.finish_setup())
        self.bind("1", self.mod_n_channels)
        self.bind("2", self.mod_n_channels)
        self.bind("3", self.mod_n_channels)
        self.bind("4", self.mod_n_channels)
        self.bind_all("<Button-1>", self.stay_focused)

        # Frame menu
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack()
        # Variabili menu
        self.saved_calibration_dict = self.saved_calibration_get()
        self.selected_calibration = tk.StringVar()
        self.com_port = tk.StringVar()
        self.number_of_channels = tk.StringVar()
        self.tempo_di_misura = tk.StringVar()
        self.smp_time = tk.StringVar()
        # Valori default
        self.com_port.set("COM3")
        self.tempo_di_misura.set("30")
        self.number_of_channels.set("1")
        self.smp_time.set("50")
        self.selected_calibration.set(list(self.saved_calibration_dict.keys())[0])

        # Ddm calibrazioni, bottone "+"
        self.calibrations_frame = ttk.Frame(self.menu_frame)
        self.calibrations_frame.pack(side="left", fill="x", padx=10, pady=20, expand=True)
        self.calibration_label = tk.Label(self.calibrations_frame, text="Calibrazione:")
        self.calibration_label.pack(side="left", fill="x", padx=10, pady=20, expand=True)
        self.ddm_saved_calibrations = tk.OptionMenu(self.calibrations_frame, self.selected_calibration, *self.saved_calibration_dict.keys())
        self.ddm_saved_calibrations.pack(side="left", fill="x", pady=20, expand=True)
        self.button_add = tk.Button(self.calibrations_frame, text="+", bg="white", fg="black", command=self.add_calib)
        self.button_add.pack(side="left", ipadx=4)
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

        self.focus_set()

    def finish_setup(self):
        try:
            if int(self.tempo_di_misura.get()) < 0:
                tk.messagebox.showerror("Tempo di misura", "Tempo di misura non valido")
            elif int(self.smp_time.get()) < 0:
                tk.messagebox.showerror("Periodo di campionamento", "Periodo di campionamento non valido")
            else:
                self.shortkeys_unbind()
                self.send_datas_toArduino()
                self.master.switch_frame(WorkPage, self.container, {"com_port":self.com_port.get(),
                                                                    "number_of_channels":self.number_of_channels.get(),
                                                                    "intervallo_di_misura":self.tempo_di_misura.get(),
                                                                    "periodo_di_campionamento":self.smp_time.get()})
        except ValueError:
            pass

    def saved_calibration_get(self):
        saved_calib_dict = dict()
        saved_calib_file = open("calibrations.txt", "r")
        for line in saved_calib_file:
            if line != "\n":
                line_list = line.split(",")
                saved_calib_dict[line_list[0]] = dict()
                saved_calib_dict[line_list[0]]["offset"] = line_list[1].rstrip()
                saved_calib_dict[line_list[0]]["calib_factor"] = line_list[2].rstrip()
        saved_calib_file.close()
        return saved_calib_dict

    def add_calib(self):
        self.puller.ser.close()
        self.shortkeys_unbind()
        self.master.switch_frame(CalibPage, self.container, {"com_port":self.com_port.get()})

    def mod_n_channels(self, event):
        """Gestione evento cambio canali da tastiera"""
        if self.focus_get() != self.intervallo_di_misura_entry and event.widget != self.periodo_campionamento_entry:
                self.number_of_channels.set(event.keysym)

    def stay_focused(self, event):
        if event.widget != self.intervallo_di_misura_entry and event.widget != self.periodo_campionamento_entry:
            self.focus_set()

    def shortkeys_unbind(self):
        self.unbind("<Return>")
        self.unbind("1")
        self.unbind("2")
        self.unbind("3")
        self.unbind("4")
        self.unbind_all("<Button-1>")

    def send_datas_toArduino(self):
        self.puller.write("load")
        time.sleep(2)
        self.puller.write(str(self.saved_calibration_dict[self.selected_calibration.get()]["offset"]))
        time.sleep(2)
        self.puller.write(str(self.saved_calibration_dict[self.selected_calibration.get()]["calib_factor"]))
        time.sleep(4)
        done = False
        while not done:
            if self.puller.pull()[0] == "loaded":
                done = True
        self.puller.ser.close()