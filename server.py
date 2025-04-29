
import socket
import psycopg2

# connects once
conn = psycopg2.connect(
    dbname="neondb",
    user="neondb_owner",
    password="Justin password", #change to test different neondb
    host="host id", #change to test different neondb
    sslmode="require"
)

def queries_handling1(): #handles queries and conversions
    pass
def queries_handling2(): #handles queries and conversions
    pass
def queries_handling3(): #handles queries and conversions
    pass



def run_server():
    try:
        host_ip = input("Enter the server's IP address (e.g., 127.0.0.1): ") #local connection ipconfig ipv4
        port = int(input("Enter the port number for the server: "))

        # Create a socket, bind it to the provided IP and port, start listening
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host_ip, port))
        server.listen(1)
        print(f"Server is running at {host_ip}:{port} and waiting for connections...")

        # Keep accepting connections from clients in a loop
        while True:
            conn, addr = server.accept()
            print(f"Connected to client at {addr}")

            # Continuously receive and process data from the client.
            while True:
                received_data = conn.recv(1024)
                if not received_data:
                    print("Client disconnected.")
                    break

                # decode
                received_text = received_data.decode()
                print(f"Received from client: {received_text}")

                modified_message = received_text.upper()

                # Handle specific queries
                if "What is the average moisture" in received_text:
                    modified_message = "Confirmation: Received request for average moisture."
                    queries_handling1()

                elif "What is the average water consumption" in received_text:
                    modified_message = "Confirmation: Received request for average water consumption."
                    queries_handling2()

                elif "consumed more electricity" in received_text:
                    modified_message = "Confirmation: Received request for electricity comparison."
                    queries_handling3()

                elif received_text.lower() == "exit":
                    print("Client requested disconnection.")
                    break

                print(f"Sending response: {modified_message}\n")
                conn.send(modified_message.encode())

            conn.close()

    except Exception as error:
        print(f"An error occurred on the server: {error}")
    finally:
        server.close()

if __name__ == "__main__":
    run_server()
