import socket

# Server setup
server_ip = input("Enter server IP: ")
server_port = int(input("Enter server port: "))

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# List of valid queries
valid_queries = {
    "1": "What is the average moisture inside my kitchen fridge in the past three hours?",
    "2": "What is the average water consumption per cycle in my smart dishwasher?",
    "3": "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
}

try:
    client_socket.connect((server_ip, server_port))
    print(f"Connected to {server_ip}:{server_port}")

    while True:
        print("\nAvailable Queries:")
        for key, query in valid_queries.items():
            print(f"{key}. {query}")
        print("4. Exit")

        user_input = input("Enter your choice (1-4): ").strip()

        if user_input == "4":
            print("Disconnecting from server.")
            client_socket.send("exit".encode())
            break

        elif user_input in valid_queries:
            message = valid_queries[user_input]
            client_socket.send(message.encode())
            response = client_socket.recv(4096).decode()
            print(f"\nServer response:\n{response}")

        else:
            print("\nSorry, this query cannot be processed. Please try one of the following:")
            for query in valid_queries.values():
                print(f"- {query}")

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
