import tkinter as tk
from tkinter import ttk
from windows import dpi_awareness
from workpage import WorkPage
from settings import SettingsPage

# Miglioramento scritte
dpi_awareness()


class StrainGaugesApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Strain gauges app")
        self.geometry("850x700")

        # Frame finestra
        self.window = ttk.Frame(self)
        self.window.pack(fill="both", expand=True)

        # Creazione SettingPage
        self.workpage = None
        self.setting_page = SettingsPage(self.window, self)
        self.setting_page.pack(fill="both", expand=True)

        # Binding tasti
        self.bind("<Return>", self.ok_pressed)
        self.bind("1", self.mod_n_channels)
        self.bind("2", self.mod_n_channels)
        self.bind("3", self.mod_n_channels)
        self.bind("4", self.mod_n_channels)
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def switch_frame(self, com_port, number_of_channels, tempo_di_misura, smp_time):
        """Creazione WorkPage e distruzione SettingPage"""
        self.setting_page.pack_forget()
        self.setting_page.destroy()
        self.workpage = WorkPage(self.window, com_port, number_of_channels, tempo_di_misura, smp_time)
        self.workpage.pack(fill="both", expand=True)
        self.geometry("1400x"+str(int(number_of_channels)*300))

    def ok_pressed(self, event):
        """Gestione evento pressione Enter"""
        if not self.workpage:
            self.setting_page.finish_setup()

    def mod_n_channels(self, event):
        """Gestione evento cambio canali da tastiera"""
        if not self.workpage:
            if self.focus_get() != self.setting_page.intervallo_di_misura_entry:
                self.setting_page.number_of_channels.set(event.keysym)

    def on_closing(self):
        """Gestione evento chiusura finestra"""
        self.quit()
        self.destroy()


# Program Main
app = StrainGaugesApp()
app.focus_set()
app.mainloop()
