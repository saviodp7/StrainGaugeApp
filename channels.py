import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
import xlsxwriter
from arduinopuller import ArduinoPuller

# Stile grafici
from matplotlib import style
style.use("ggplot")
matplotlib.use("TkAgg")


class ChannelsFrame(ttk.Frame):

    def __init__(self, container, com_port, number_of_channels, tempo_di_misura, smp_time):
        super().__init__(container)

        # Modulo comunicazione con Arduino
        self.puller = ArduinoPuller(str(com_port))

        # Variabili
        self.running = True
        self.number_of_channels = int(number_of_channels)
        self.smp_time = int(smp_time)
        # Nomi canali
        self.channels_names = list()
        self.channel_name_entrys = list()
        # Plots canali
        self.fig = plt.figure()  # Figura
        self.plots = list()      # Grafici
        self.lines = list()      # Linee animate
        # Valori canali
        self.channels_rt_value = list()
        self.channels_min_value = list()
        self.channels_max_value = list()
        # Assi canali
        self.channels_x = np.arange(0, int(tempo_di_misura), self.smp_time/1000).tolist()
        self.channels_y = list()

        # FRAMES
        # Frame nomi canali
        self.channels_names_frame = ttk.Frame(self)
        self.channels_names_frame.pack(side="left", fill="y")
        # Frame Plots
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side="left", fill="both", expand=True)
        # Frame valori
        self.channels_values_frame = ttk.Frame(self)
        self.channels_values_frame.pack(ipadx=10, pady=20, fill="y", expand=True)

        # Inizializzazione singoli canali
        for channel_number in range(self.number_of_channels):
            # Creazione variabile nome
            self.channels_names.append(tk.StringVar())
            # Frame nome singolo canale
            self.channel_name_frame = ttk.Frame(self.channels_names_frame)
            self.channel_name_frame.pack(fill="y", expand=True)
            # Label e Entry nome canale
            self.channel_name_label = tk.Label(self.channel_name_frame,
                                               text="Nome canale #" + str(channel_number+1) + ":")
            self.channel_name_label.pack(fill="x")
            self.channel_name_entrys.append(tk.Entry(self.channel_name_frame,
                                                     textvariable=self.channels_names[channel_number]))
            self.channel_name_entrys[channel_number].pack(padx=15, fill="x")

            self.channel_name_frame.pack(fill="y", expand=True)
            # Crezione grafico e linea animata
            self.plots.append(plt.subplot(self.number_of_channels, 1, channel_number+1))
            self.plots[channel_number].set_ylim(-1, 1)
            self.plots[channel_number].set_xlim(0, int(tempo_di_misura))
            line, = self.plots[channel_number].plot([], [], lw=2)
            self.lines.append(line)
            # Creazione variabili valori (rt, min, max, y)
            self.channels_rt_value.append(tk.DoubleVar())
            self.channels_min_value.append(tk.DoubleVar())
            self.channels_max_value.append(tk.DoubleVar())
            self.channels_y.append([0]*len(self.channels_x))
            # Valore RT
            self.channel_rt_value_label = tk.Label(self.channels_values_frame, text="value:")
            self.channel_rt_value_label.pack(fill="x", expand=True)
            self.channel_rt_value = tk.Label(self.channels_values_frame,
                                             textvariable=self.channels_rt_value[channel_number],
                                             bg="grey", fg="black", width=10)
            self.channel_rt_value.pack()
            # Valore MIN
            self.channel_min_value_lab = tk.Label(self.channels_values_frame, text="min value:")
            self.channel_min_value_lab.pack(fill="x", expand=True)
            self.channel_min_value = tk.Label(self.channels_values_frame,
                                              textvariable=self.channels_min_value[channel_number],
                                              bg="grey", fg="black", width=10)
            self.channel_min_value.pack()
            # Valore MAX
            self.channel_max_value_lab = tk.Label(self.channels_values_frame, text="max value:")
            self.channel_max_value_lab.pack(fill="x", expand=True)
            self.channel_max_value = tk.Label(self.channels_values_frame,
                                              textvariable=self.channels_max_value[channel_number],
                                              bg="grey", fg="black", width=10)
            self.channel_max_value.pack()
        # Aggiornamento grafico
        self.canvas.draw()
        # Variabile di animazione
        self.ani = FuncAnimation(self.fig, self.animate, interval=self.smp_time/5, blit=True)

        self.reset()

    def animate(self, i):
        """Funzione di aggiornamento linee"""
        if self.running:  # Start/stop
            list_readed = self.puller.pull()
            for channel_number in range(self.number_of_channels):
                try:
                    rt_value = float(list_readed[channel_number])
                    self.channels_rt_value[channel_number].set(rt_value)
                    self.channels_y[channel_number].append(rt_value)
                    self.channels_y[channel_number].pop(0)
                    # Aggiornamento margini assi
                    if rt_value < self.channels_min_value[channel_number].get():
                        self.channels_min_value[channel_number].set(rt_value)
                        self.plots[channel_number].set_ylim(bottom=rt_value)
                        self.canvas.draw()
                    elif rt_value > self.channels_max_value[channel_number].get():
                        self.channels_max_value[channel_number].set(rt_value)
                        self.plots[channel_number].set_ylim(top=rt_value)
                        self.canvas.draw()
                except ValueError:
                    pass
                except IndexError:
                    pass
                self.lines[channel_number].set_data(self.channels_x, self.channels_y[channel_number])
        return self.lines

    def start_stop(self):
        """Funzione start/stop misurazione"""
        self.running = not self.running
        self.puller.flush()
        self.puller.pull()

    def reset(self):
        """Funzione reset grafico e misurazione"""
        for channel_number in range(self.number_of_channels):
            self.channels_y[channel_number] = [0]*len(self.channels_x)
            self.channels_min_value[channel_number].set(0)
            self.channels_max_value[channel_number].set(0)

    def tara(self):
        """Taratura sensore"""
        self.puller.write("tara")

    def export_to_csv(self):
        """Esportazione dati misurazione in excel"""
        workbook = xlsxwriter.Workbook("export.xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', "time")
        worksheet.write_column('A2', self.channels_x)
        for channel_number in range(self.number_of_channels):
            worksheet.write(0, channel_number+1, self.channels_names[channel_number].get())
            worksheet.write_column(1, channel_number+1,  self.channels_y[channel_number])
        workbook.close()
