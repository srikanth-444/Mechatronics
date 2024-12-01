#!/usr/bin/env python3
import serial
import socket
import time
import pickle  # For serializing data into byte format
import zmq

class Publisher:
    def __init__(self, host='tcp://*:5555', topic='robot_data'):
        """Initialize the publisher with a given host and topic."""
        self.host = host
        self.topic = topic
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.host)

    def publish_data(self, data):
        """Publish data to the subscribers."""
        message = f"{self.topic} {data}"
        self.socket.send_string(message)
        print(f"Published: {message}")

    def close(self):
        """Close the socket and context."""
        self.socket.close()
        self.context.term()


class Subscriber:
    def __init__(self, host='tcp://localhost:5555', topic='robot_data'):
        """Initialize the subscriber with a given host and topic."""
        self.host = host
        self.topic = topic
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(self.host)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

    def receive_data(self):
        """Receive data from the publisher (non-blocking)."""
        try:
            message = self.socket.recv_string(flags=zmq.NOBLOCK)
            print(f"Received: {message}")
        except zmq.Again:
            pass

    def close(self):
        """Close the socket and context."""
        self.socket.close()
        self.context.term()


class SerialCommunication:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=1):
        """Initialize the serial communication with the given port, baudrate, and timeout."""
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.ser.reset_input_buffer()

    def read_data(self):
        """Read data from the serial port."""
        input_data = self.ser.read(7)  # Adjust size based on expected data length
        print(f"Received Data: {input_data}")
        return input_data

    def send_data(self, data):
        """Send data to the serial port."""
        # Make sure data is in byte format before sending
        self.ser.write(data)
        print(f"Sent Data: {data}")

    def close_connection(self):
        """Close the connection with the serial port."""
        self.ser.close()
        print("Connection closed.")

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