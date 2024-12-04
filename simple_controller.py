import serial
from communication import SerialCommunication
def decode_values(pan_and_tap):
    data_array=[0,0,0,0.5]
    pan=pan_and_tap&0xF0
    tap=pan_and_tap&0x0F

    if pan==0x80:
        print("no object detected")
    elif pan==0x00:
        print("zero off set")
    elif pan==0x30 :
        print("object on right")
    elif pan==0x10:
        print("object on left")
    else:
        print("invalid")

    tap_RR=tap&0x01
    tap_LR=(tap>>1)&0x01
    tap_RF=(tap>>2)&0x01
    tap_LF=(tap>>3)&0x01

    if tap_RR:
        print("right rear tap detected")
        # ser_mega.send_data_to_mega(data_array)
    if tap_LR:
        print("left rear tap detected")
    if tap_RF:
        print("right front tap detected")
    if tap_LF:
        print("left front tap detected")
    
    


# def read_data(ser):
#     while True:
#         if ser.read() == b'\xAA':  # Start byte
#             data = ser.read(3)     # Read next 4 bytes (Pan, Tape, Distance L, Distance R)
#             end_byte = ser.read()  # End byte

#             if end_byte == b'\xBB':  # Validate end byte
#                 pan_and_tap = data[0]
#                 distance_L = data[1]
#                 distance_R = data[2]
#                 return pan_and_tap, distance_L, distance_R
#             else:
#                 print("Invalid end byte. Resyncing...")

# Initialize serial
ser_uno = SerialCommunication(port='/dev/ttyACM1', baudrate=9600, timeout = 1)
ser_mega = SerialCommunication(port='/dev/ttyACM0', baudrate=115200, timeout = 1)
ser_uno.reset_input_buffer()
ser_mega.reset_input_buffer()


while True:
    try:
        pan_and_tape, dist_L, dist_R = ser_uno.read_data()
        decode_values(pan_and_tap=pan_and_tape)
        
        print(f"Pan and tape: {pan_and_tape}, Distance L: {dist_L}, Distance R: {dist_R}")
    except KeyboardInterrupt:
        break
