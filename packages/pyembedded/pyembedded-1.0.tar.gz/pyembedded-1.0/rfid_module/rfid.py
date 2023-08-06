import serial


class RFID:
    def __init__(self, port, baud_rate):
        self.rfid_serial_port = serial.Serial(port, baud_rate)

    def get_rfid_id(self):
        id_num = []
        i = 0
        while True:
            serial_data = self.rfid_serial_port.read()
            data = serial_data.decode('utf-8')
            i = i + 1
            if i == 12:
                i = 0
                ID = "".join(map(str, id_num))
                return ID
            else:
                id_num.append(data)


if __name__ == '__main__':
    RFID(port="COM1", baud_rate=9600)
