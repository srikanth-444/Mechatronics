import serial
import time
from communication import Subscriber

w=50
state=0   #0,1,2 for vx,vy,wz
state_vector=[]
velocity_array=[]
dt=0.1
Position = Subscriber(host='tcp://localhost:5555',topic="XandY")
Orientation=Subscriber(host='tcp://localhost:5556',topic="theta")
def send_two_bytes_to_arduino(byte1, byte2):
    """Send two bytes to the Arduino."""
    # Ensure both byte values are in the range 0-255
    if not (0 <= byte1 <= 255 and 0 <= byte2 <= 255):
        raise ValueError("Both byte values must be between 0 and 255.")

    # Open the serial port
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)  # Adjust port as needed
    time.sleep(2)  # Allow time for the connection to establish

    # Send the two bytes
    ser.write(byte1.to_bytes(1, 'big'))
    ser.write(byte2.to_bytes(1, 'big'))
    print(f"Sent bytes: {byte1}, {byte2}")

    # Close the serial connection
    ser.close()

# Example usage:
send_two_bytes_to_arduino(w, state)  # Sends the byte values 128 and 64

start_time=time.time()


previous_position=0
while(time.time()-start_time)<20:
    xandy=Position.receive_data()
    theta=Orientation.receive_data()
    state_vector=[xandy[0],xandy[1],theta[0]]
    velocity=(state_vector[state]-previous_position)/dt
    previous_position=state_vector[state]
    velocity_array.append(velocity)
