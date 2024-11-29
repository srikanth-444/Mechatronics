#!/usr/bin/env python3
import serial
import socket
import time
import pickle  # For serializing data into byte format

class TCPSender:
    def __init__(self, host='127.0.0.1', port=12345):
        """Initialize the server with the given host and port."""
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None

    def start_server(self):
        """Start the server, bind the socket, and wait for a client connection."""
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        self.server_socket.bind((self.host, self.port))

        # Start listening for incoming connections
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")

        # Wait for a client to connect
        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"Connected to {self.client_address}")

    def send_data(self, data_array):
        """Send an array as a serialized byte stream."""
        # Serialize the array to a byte stream using pickle
        data_bytes = pickle.dumps(data_array)
        # Send the byte stream to the client
        self.client_socket.sendall(data_bytes)
        print(f"Sent: {data_array}")

    def close_connection(self):
        """Close the connection with the client."""
        self.client_socket.close()
        self.server_socket.close()
        print("Connection closed.")


class TCPReceiver:
    def __init__(self, host='127.0.0.1', port=12345):
        """Initialize the client with the given host and port."""
        self.host = host
        self.port = port
        self.client_socket = None

    def connect_to_server(self):
        """Connect to the TCP server."""
        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def receive_data(self):
        """Receive and deserialize the data sent by the server."""
        while True:
            data = self.client_socket.recv(1024)  # Receive up to 1024 bytes of data
            if not data:
                break
            # Deserialize the received data using pickle
            data_array = pickle.loads(data)
            print(f"Received: {data_array}")

    def close_connection(self):
        """Close the connection to the server."""
        self.client_socket.close()
        print("Connection closed.")

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
    sender = TCPSender()  # Create the TCP sender object
    sender.start_server()  # Start the server

    # Simulate sending arrays of data
    for _ in range(10):
        data = [45.0, -15.0]  # Example array (e.g., roll and pitch values)
        sender.send_data(data)  # Send the array to the client
        time.sleep(1)  # Delay for 1 second before sending the next data

    sender.close_connection()  # Close the connection after sending all data

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