# CECS 327 – Assignment 8: End-to-End IoT System

This project demonstrates a working end-to-end IoT system using a TCP client-server architecture and a NeonDB PostgreSQL database. Sensor data is streamed from Dataniz virtual devices and stored in the database. The server retrieves this data in response to client queries and returns the processed results.

## Required Environment

- Two virtual machines (VMs), one for the server and one for the client
- Python 3.8 or higher installed on both VMs
- PostgreSQL database hosted on NeonDB with a table named `Devices_virtual`
- Dependencies: `psycopg2-binary` (install using pip)

## Remote Machine Setup

### Server VM
- External IP: 34.132.116.204

### Client VM
- External IP: 34.72.32.33

Both machines should be accessed using Remote Desktop Connection (RDP). Once logged into each VM, open a terminal.

## Setup Instructions (Run on Both VMs)

1. Clone or upload your project folder containing `client.py`, `server.py`, and sample JSON files.
2. Install required dependencies:
   ```
   sudo apt update
   sudo apt install python3 python3-pip -y
   pip3 install psycopg2-binary
   ```

## NeonDB Configuration

1. Create a free NeonDB account at https://neon.tech and start a new project.
2. Set up a PostgreSQL database and create a table called `Devices_virtual`.
3. Insert data records matching the structure used by Dataniz.
4. Copy the connection string provided by NeonDB. It should contain:
   - `dbname`
   - `user`
   - `password`
   - `host`
   - `sslmode=require`
5. Ensure these values are correctly entered in the `connect_to_database()` function inside `server.py`.

Example (already included in code):
```python
psycopg2.connect(
    dbname="neondb",
    user="neondb_owner",
    password="your_password",
    host="your_project_region.neon.tech",
    sslmode="require"
)
```

Ensure the NeonDB project is active, and that public access is enabled if needed for external VM connections.

## Running the Server (On Server VM)

1. Open a terminal and navigate to the project directory.
2. Run the server:
   ```
   python3 server.py
   ```
3. Enter the following when prompted:
   - IP: `0.0.0.0`
   - Port: `511`

The server will now listen for incoming TCP connections from any IP on port 511.

## Running the Client (On Client VM)

1. Open a terminal and navigate to the project directory.
2. Run the client:
   ```
   python3 client.py
   ```
3. Enter the following when prompted:
   - Server IP: `34.132.116.204`
   - Port: `511`

You will be shown a menu with four options.

## Using the Client

Select one of the following options:

- `1` – Retrieve average moisture data from the fridge over the last 3 hours
- `2` – Retrieve average water consumption from the dishwasher
- `3` – Compare electricity usage across all three devices
- `4` – Exit the client

Enter the corresponding number when prompted.

## Notes

- Ensure port 511 is open and not blocked by any VM firewall.
- Ensure both VMs are online and accessible.
- Ensure the NeonDB project is active and the `Devices_virtual` table contains data from Dataniz.
- Sample JSON files are included for reference only and do not replace the need for actual database connectivity.


## Screenshots 
Connecting to a remote server 
![image](https://github.com/user-attachments/assets/e4e8cd76-2884-49d2-970a-fc76e7b46402)
