import tkinter as tk
from tkinter import ttk
from windows import dpi_awareness
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

        # Creazione schermata
        self.workpage = None

        # Inizializzazione workpage
        self.switch_frame(SettingsPage)

        # Binding tasti
        self.protocol("WM_DELETE_WINDOW", self.close_app)

    def switch_frame(self, Page, **kwargs):
        """Creazione WorkPage e distruzione SettingPage"""
        if(self.workpage):
            self.workpage.pack_forget()
            self.workpage.destroy()
        self.workpage = Page(self, self.window, **kwargs)
        self.workpage.pack(fill="both", expand=True)

    def close_app(self):
        """Gestione evento chiusura finestra"""
        self.quit()
        self.destroy()


# Program Main
app = StrainGaugesApp()
app.focus_set()
app.mainloop()
