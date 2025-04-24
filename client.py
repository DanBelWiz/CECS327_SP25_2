import socket

# Get server details from user
server_ip = input("Enter server IP: ")
server_port = int(input("Enter server port: "))

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, server_port))  # Connect to the server
    print(f"Connected to {server_ip}:{server_port}")

    while True:
        message = input("Enter message (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        client_socket.send(message.encode())  # Send message to server
        response = client_socket.recv(1024).decode()  # Receive response
        print(f"Server response: {response}")

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()  # Close the connection
