#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    try:
        while True:
                state=[]
                input1=ser.read(7)
                i=0
                print("give x_direc, velocity_x, y_direc, velocity_y,rotaion_direction,angular_velocity")
                for i in range(6):
                  a= int(input())
                  state.append(a) 
                ser.write(bytes(state))
                
                
                
    except KeyboardInterrupt:
            data=[0,0,0] 
            ser.write(bytes(data))