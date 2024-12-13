import time
import random
from communication import SerialCommunication
def decode_values(pan_and_tap):
    data_array=[0,0,0,0]
    #print(type(pan_and_tap))
    #print(type(0xF0))
    ##pan=int(pan_and_tap)&0xF0
    pan = pan_and_tap & 0xF0
    tilt=(pan>>6)&0x01
    pan=pan&0xBF
    tap = pan_and_tap & 0x0F

    ##tap=pan_and_tap&0x0F

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


    if tilt:
        print("poke")

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
    
    return pan, tilt,tap_LF,tap_LR,tap_RF,tap_RR
    
def if_frontcollision(tap_LF,tap_LR,tap_RF,tap_RR,dist_L, dist_R):

    if tap_LF:
        return 1
    if tap_RF:
        return 1
    # if tap_LR:
    #     return 1
    # if tap_RR:
    #     return 1
    
    if dist_L>0 and dist_L<40:
        return 1
    if dist_R>0 and dist_R<40:
        return 1  
    return 0
def if_rearcollision(tap_LF,tap_LR,tap_RF,tap_RR,dist_L, dist_R):

    if tap_LR:
        return 1
    if tap_RR:
        return 1
    # if tap_LR:
    #     return 1
    # if tap_RR:
    #     return 1
    
    # if dist_L<150:
    #     return 1
    # if dist_R<150:
    #     return 1  
    return 0


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
ser_uno = SerialCommunication(port='/dev/ttyACM1', baudrate=115200, timeout = 1)
ser_mega = SerialCommunication(port='/dev/ttyACM0', baudrate=115200, timeout = 1)
ser_uno.reset_input_buffer()
ser_mega.reset_input_buffer()

data_array=[0,0,0,1]
front_collision=0
rear_collision=0
while True:
    try:
        slide_dir = 0

        pan_and_tape, dist_L, dist_R = ser_uno.read_data()
        pan, tilt,tap_LF,tap_LR,tap_RF,tap_RR=decode_values(pan_and_tap=pan_and_tape)
        print(pan_and_tape,tilt)
        ser_uno.reset_input_buffer()
        if if_frontcollision(tap_LF=tap_LF,tap_LR=tap_LR,tap_RF=tap_RF,tap_RR=tap_RR,dist_L=dist_L,dist_R=dist_R):
            if(front_collision == 0):
                rand_dir = random.choice([-1,1])
            front_collision=1
            print("front_collision: ", front_collision)
            start_time=time.time()
        if if_rearcollision(tap_LF=tap_LF,tap_LR=tap_LR,tap_RF=tap_RF,tap_RR=tap_RR,dist_L=dist_L,dist_R=dist_R):
            if(front_collision == 0):
                rand_dir = random.choice([-1,1])
            rear_collision=1
            start_time=time.time()
        if tilt:
                data_array[3]=1
        else:
                data_array[3]=-1
        if pan!=0x80:
            if front_collision==1: 
                print("in [1,0]")
                

                if (time.time()-start_time<0.5):
                    print(time.time()-start_time)
                    data_array[1]=-1
                    data_array[2]=0
                elif(time.time()-start_time<0.75):
                    if dist_L>=dist_R:
                        data_array[0]=-1
                        data_array[1]=0
                        data_array[2]=0
                    elif dist_L<dist_R :
                        data_array[0]=1
                        data_array[1]=0
                        data_array[2]=0
                    else:
                        data_array[2]= rand_dir
                else:
                    data_array[1]=0
                    data_array[2]=0
                    front_collision=0

            # if front_collision == 0:
            #     data_array[1]=1
            #     data_array[0]=0
            # else:
            #     data_array[1]=0
            #     front_collision = 0
            #     if dist_L>dist_R:
            #         data_array[0] = -1
            #     elif dist_R>dist_L:
            #         data_array[0] = 1

                    

             # elif dist_L>dist_R and dist_L <50 and dist_R <50:
            #     data_array[1]=0
            #     data_array[0]=-1
            #     front_collision = 0

            # elif dist_L>dist_R and dist_L <50 and dist_R <50:
            #     data_array[0]=1
            #     data_array[1]=0
            else:
                if pan==0x00:
                    print("zero off set")
                elif pan==0x30 :
                    print("object on left")
                    data_array[2]=-0.5
                    data_array[0]=0
                    data_array[1]=1
                elif pan==0x10:
                    print("object on right")
                    data_array[2]=0.5
                    data_array[0]=0
                    data_array[1]=1
                else:
                    print("invalid")
            
            
        else:
            

            
            if front_collision==1 and rear_collision==0: 
                print("in [1,0]")
                

                if (time.time()-start_time<0.5):
                    print(time.time()-start_time)
                    data_array[1]=-1
                elif(time.time()-start_time<1.5):
                    if dist_L>=dist_R and dist_L <150 and dist_R <150:
                        data_array[2]=-1
                    elif dist_L<dist_R and dist_L <150 and dist_R <150:
                        data_array[2]=1
                    else:
                        data_array[2]= rand_dir
                else:
                    data_array[1]=0
                    data_array[2]=0
                    front_collision=0
                
            elif front_collision==0 and rear_collision==1: 
                print("in [0,1]")
                #start_time=time.time()

                if (time.time()-start_time<1):
                    data_array[1]= 1
                elif(time.time()-start_time<1.5):
                    data_array[1]= 0
                    if dist_L>=dist_R and dist_L <150 and dist_R <150:
                        data_array[2]=-1
                    elif dist_L<dist_R and dist_L <150 and dist_R <150:
                        data_array[2]=1
                    else:
                        data_array[2]= rand_dir
                else:
                    data_array[2]=0
                    rear_collision=0
            elif front_collision==1 and rear_collision==1:
                print("in [1,1]")
                if dist_L>=dist_R and dist_L <20 and dist_R <20:
                    data_array[2]=-1
                    data_array[1]=0
                elif dist_L<dist_R and dist_L <20 and dist_R <20:
                    data_array[2]=1
                    data_array[1]=0
                if not if_frontcollision(tap_LF=tap_LF,tap_LR=tap_LR,tap_RF=tap_RF,tap_RR=tap_RR,dist_L=dist_L,dist_R=dist_R):
                    front_collision=0
                    rear_collision=0

                    data_array=[0,0,0,0]
            
            else:
                    print("[0,0]")
                    data_array=[0,1,0,0]


            


        # # if tap_LF and tap_RF:
        # #     data_array[1]=-1
        # # if tap_LR and tap_RR:
        # #     data_array[1]= 1
        # # if tap_RR and tap_RF:
        # #     data_array[0]=-1
        # # if tap_LR and tap_LF:
        # #     data_array[0]=1

        # # else:
        # #     if tap_LF:
        # #         data_array[2]=1
        # #     if tap_RF:
        # #         data_array[2]=-1
        # #     if tap_LR:
        # #         if data_array[2]==0:
        # #             data_array[2]=-1
        # #         data_array[2]=0
        # #     if tap_RR:
        # #         if data_array[2]==0:
        # #             data_array[2]=1
        # #         data_array[2]=0

        # # real_distance_L=(dist_L*(16)/(255*100))+2
        # # real_distance_R=dist_R*(18-2)/(255*100)+2
        
        ser_mega.send_data_to_mega(data_array)
        ser_mega.reset_input_buffer()

        # time.sleep(1)
        print(f"Pan and tape: {pan_and_tape}, Distance L: {dist_L}, Distance R: {dist_R}")
    except KeyboardInterrupt:
        data_array=[0,0,0,-1]
        ser_mega.send_data_to_mega(data_array)
        break
