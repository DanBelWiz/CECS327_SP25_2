import socket

# Displays the list of valid queries for the user
def display_menu():
    queries = {
        "1": "What is the average moisture inside my kitchen fridge in the past three hours?",
        "2": "What is the average water consumption per cycle in my smart dishwasher?",
        "3": "Which device consumed more electricity among my three IoT devices?",
        "4": "Exit"
    }
    print("\nAvailable Queries:")
    for key, text in queries.items():
        print(f"{key}. {text}")
    return queries

# Main client function to connect, send queries, and receive results
def main():
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))

    # Create TCP client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((server_ip, server_port))
            print(f"Connected to {server_ip}:{server_port}")
            queries = display_menu()

            while True:
                choice = input("Enter your choice (1-4): ").strip()

                if choice == "4":
                    print("Closing connection.")
                    sock.send("exit".encode())
                    break
                elif choice in queries:
                    sock.send(queries[choice].encode())
                    response = sock.recv(4096).decode()
                    print(f"\nServer response:\n{response}")
                else:
                    print("\nInvalid choice. Please try again.")
                    display_menu()

        except Exception as err:
            print(f"Connection error: {err}")

if __name__ == "__main__":
    main()

finally:
    client_socket.close()
