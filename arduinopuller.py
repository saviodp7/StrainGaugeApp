import serial

class ArduinoPuller:

    def __init__(self, com_port):
        self.ser = serial.Serial(com_port, 9600)
        self.flush()
        try:
            self.ser.readline()
        except ValueError:
            pass

    def pull(self):
        values = self.ser.readline().decode('ascii').strip()
        values = values.split(',')
        print(values)
        return values

    def flush(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def write(self, stringa):
        self.ser.write(stringa.encode())
