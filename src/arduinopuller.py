import tkinter
import serial

class ArduinoPuller:

    def __init__(self, com_port):
        try:
            self.ser = serial.Serial(com_port, 9600)
            self.flush()
            try:
                self.ser.readline()
            except ValueError:
                pass
        except serial.serialutil.SerialException:
            tkinter.messagebox.showerror("COM PORT", "COM Port non trovata.")


    def pull(self):
        values = self.ser.readline().decode('ascii').strip()
        values = values.split(',')
        return values

    def flush(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def write(self, stringa):
        self.ser.write(stringa.encode())
