
import socket
import psycopg2


def connection(): # connect to data
    conn = psycopg2.connect(
    host="postgresql://neondb_owner:npg_lionbI65pfAr@ep-polished-poetry-a5m7eet5-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require", 
    database="neondb",
    user="newegss242@gmail.com",
    password="your_password", # change personal
    port=5432,  
    sslmode="require"  
)
    pass


def queries_handling(): #handles queries and conversions
    pass

def run_server():
    try:
        host_ip = input("Enter the server's IP address (e.g., 127.0.0.1): ")
        port = int(input("Enter the port number for the server: "))

        # Create a socket, bind it to the provided IP and port, and start listening.
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host_ip, port))
        server.listen(1)
        print(f"Server is running at {host_ip}:{port} and waiting for connections...")

        # Keep accepting connections from clients in a loop.
        while True:
            conn, addr = server.accept()
            print(f"Connected to client at {addr}")

            # Continuously receive and process data from the client.
            while True:
                received_data = conn.recv(1024)
                if not received_data:
                    print("Client disconnected.")
                    break

                # Convert received text to uppercase and send it back.
                modified_message = received_data.decode().upper()
                print(f"Received from client: {received_data.decode()}")
                print(f"Sending response: {modified_message}")
                conn.send(modified_message.encode())

            conn.close()

    except Exception as error:
        print(f"An error occurred on the server: {error}")
    finally:
        server.close()

if __name__ == "__main__":
    run_server()
