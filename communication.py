#!/usr/bin/env python3
import serial
# import zmq
import re
import time

# class Publisher:
#     def __init__(self, host='tcp://*:5555', topic='robot_data'):
#         """Initialize the publisher with a given host and topic."""
#         self.host = host
#         self.topic = topic
#         self.context = zmq.Context()
#         self.socket = self.context.socket(zmq.PUB)
#         self.socket.bind(self.host)

#     def publish_data(self, data):
#         """Publish data to the subscribers."""
#         message = f"{self.topic} {data}"
#         self.socket.send_string(message)
#         print(f"Published: {message}")

#     def close(self):
#         """Close the socket and context."""
#         self.socket.close()
#         self.context.term()


# class Subscriber:
#     def __init__(self, host='tcp://localhost:5555', topic='robot_data'):
#         """Initialize the subscriber with a given host and topic."""
#         self.host = host
#         self.topic = topic
#         self.context = zmq.Context()
#         self.socket = self.context.socket(zmq.SUB)
#         self.socket.connect(self.host)
#         self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
#         self.socket.setsockopt(zmq.SNDTIMEO, 1000)

#     def receive_data(self):
#         """Receive data from the publisher (non-blocking)."""
#         try:
#             message = self.socket.recv_string(flags=zmq.NOBLOCK).strip()
#             # print(f"Received: {message}")
#             numbers=re.findall(r"[-+]?\d*\.\d+|\d+", message)
#             values=[float(num) for num in numbers]
#             return values
#         except zmq.Again:
#             pass

#     def close(self):
#         """Close the socket and context."""
#         self.socket.close()
#         self.context.term()


class SerialCommunication:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        """Initialize the serial communication with the given port, baudrate, and timeout."""
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.reset_input_buffer()

    def read_data(self):
        while True:
            if self.ser.read() == b'\xAA':  # Start byte
                data = self.ser.read(3)     # Read next 4 bytes (Pan, Tape, Distance L, Distance R)
                end_byte = self.ser.read()  # End byte

                if end_byte == b'\xBB':  # Validate end byte
                    pan_and_tap = data[0]
                    distance_L = data[1]
                    distance_R = data[2]
                    
                    return pan_and_tap, distance_L, distance_R
                else:
                    print("Invalid end byte. Resyncing...")


    def send_data(self, data):
        """Send data to the serial port."""
        # Make sure data is in byte format before sending
        self.ser.write(data)
        print(f"Sent Data: {data}")
    
    def send_data_to_mega(self,data):
        if (len(self.ser.read(8)) != 0) :
            self.ser.write(b"Start\n")
            # Send each value in the array as ASCII decimal string
            for value in data:
                # Convert the floating-point value to a string in ASCII decimal format
                value_str = f"{value:.3f}"  # Adjust the number of decimal places as needed
                self.ser.write(value_str.encode() + b'\n')
            # time.sleep(0.1)
            print(data)

    def close_connection(self):
        """Close the connection with the serial port."""
        self.ser.close()
        print("Connection closed.")
    
    def reset_input_buffer(self,):
        self.ser.reset_input_buffer()

if __name__ == "__main__":
 

    serial_comm = SerialCommunication()

    try:
        # Main loop for sending and receiving data
        while True:
            # Read data from the serial port
            received_data = serial_comm.read_data()

            # Simulate some data to send back to the serial port (e.g., echoing received data)
            serial_comm.send_data(received_data)

    except KeyboardInterrupt:
        print("\nInterrupt detected. Closing connection.")
        serial_comm.close_connection() 