import tkinter as tk
from tkinter import ttk
from windows import dpi_awareness
from workpage import WorkPage
from settings_scales import SettingsPage
from calib_page import CalibPage

# Miglioramento scritte
dpi_awareness()


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Scales app")

        # Frame finestra
        self.window = ttk.Frame(self)
        self.window.pack(fill="both", expand=True)

        # Creazione frame attuale
        self.page = None
        self.switch_frame(SettingsPage, self.window, {})

        # Chiusura programma
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def switch_frame(self, frame_class, container, args):
        """Creazione WorkPage e distruzione SettingPage"""
        if self.page:
            self.page.pack_forget()
            self.page.destroy()
        self.page = frame_class(self, container, **args)
        self.page.pack(fill="both", expand=True)

    def on_closing(self):
        """Gestione evento chiusura finestra"""
        self.quit()
        self.destroy()

# Program Main
app = App()
app.focus_set()
app.mainloop()
