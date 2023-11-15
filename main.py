import serial
import time
import tkinter as tk
import tk_tools
import threading

#initialize serial port
ser = serial.Serial()
ser.port = 'COM5' #Arduino serial port
ser.baudrate = 115200
ser.timeout = 10 #specify timeout when using readline()
ser.open()

root = tk.Tk()
# rs = tk_tools.RotaryScale(root, max_value=0.3, size=100, unit='km/h')
# rs.grid(row=0, column=0)
max_voltage = 0.4
height = 350
width = 1.2*height
g1 = tk_tools.Gauge(root, max_value =max_voltage, label = "voltage", unit = 'V',height=height,width=width)
g1.grid(row=0, column=0)
g2= tk_tools.Gauge(root, max_value = max_voltage, label = "voltage", unit = 'V',height=height,width=width)
g2.grid(row=0, column=1)
g3 = tk_tools.Gauge(root, max_value = max_voltage, label = "voltage", unit = 'V',height=height,width=width)
g3.grid(row=0, column=2)
led_size=50
l1 = tk_tools.Led(root, size=led_size)
l2 = tk_tools.Led(root, size=led_size)
l3 = tk_tools.Led(root, size=led_size)
l1.grid(row=1,column=0)
l2.grid(row=1,column=1)
l3.grid(row=1,column=2)
data = []

if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters


def listen_serial():
    global data
    while True:
          out = [float(x) for x in ser.readline().decode('utf-8').strip('\r\n').split(',')]
          data = out
          root.event_generate("<<SerialData>>", when="tail")
          
def set_led_for_max(data, l1, l2, l3):
    max_index = data.index(max(data))  # Find the index of the maximum value

    for index, instance in enumerate([l1, l2, l3]):
        if index == max_index:
            instance.to_yellow(on=True)
        else:
            instance.to_yellow(on=False)

def update_gauge(event):
    #data = event.data
    # rs.set_value(data[0])
    g1.set_value(data[0])
    g2.set_value(data[1])
    g3.set_value(data[2])
    set_led_for_max(data,l1,l2,l3)

root.bind("<<SerialData>>", update_gauge)

serial_thread = threading.Thread(target=listen_serial)
serial_thread.start()

root.mainloop()
serial_thread.join()





	