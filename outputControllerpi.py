import serial
import pygame
import time
from communication import SerialCommunication

# Define your array of floating-point values
isRecieved = False
data_array = [0,0,0,0.5]

# Open the serial port 
# Update 'COMX' with your specific serial port name for Windows
# or '/dev/cu.usbserial-14101' or similar for Mac and linux
ser = SerialCommunication(port='/dev/ttyACM0', baudrate=115200, timeout = 1)
ser.reset_input_buffer()

# pygame.init()
# if pygame.joystick.get_count()<1:
#     print("Waiting for controller to be connected")

# while pygame.joystick.get_count()<1:
#     pygame.event.pump()
#     time.sleep(2)

# print("Controller connected...")

# time.sleep(2)
# pygame.event.pump()
# pygame.joystick.init()


# # List the available joystick devices
# joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# print(len(joysticks))

# # Initialize all detected joysticks
# for joystick in joysticks:
#     joystick.init()
#     print(f"Joystick {joystick.get_id()}: {joystick.get_name()}")



# Define your array of floating-point values

while True:
    # Send the start of data marker
    # pygame.event.pump()
    # pygame.event.get()
    # for joystick in joysticks:
    #     left_x_axis = joystick.get_axis(0)
    #     left_y_axis = -joystick.get_axis(1)
    #     right_x_axis = joystick.get_axis(2)
    #     right_y_axis = joystick.get_axis(3)
    #     left_trigger = joystick.get_axis(5)
    #     right_trigger = joystick.get_axis(4)
        # data_array = [left_x_axis, left_y_axis, right_x_axis, right_trigger]
        
    # if (len(ser.read(8)) != 0) :
    #     ser.write(b"Start\n")
    #     # Send each value in the array as ASCII decimal string
    #     for value in data_array:
    #         # Convert the floating-point value to a string in ASCII decimal format
    #         value_str = f"{value:.3f}"  # Adjust the number of decimal places as needed
    #         ser.write(value_str.encode() + b'\n')
    #     #time.sleep(0.1)
    #     print(data_array)
    ser.send_data_to_mega(data_array)
