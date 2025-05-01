import socket
import psycopg2
import json
from datetime import datetime, timedelta

# Establishes connection to NeonDB PostgreSQL database
def connect_to_database():
    return psycopg2.connect(
        dbname="neondb",
        user="neondb_owner",
        password="npg_B2teoLV4MHIn",
        host="ep-lucky-cloud-a5fgqzb2-pooler.us-east-2.aws.neon.tech",
        sslmode="require"
    )

# Converts raw sensor values into amperage based on calibration
def convert_raw_to_amps(raw_value):
    zero_offset = 22.5
    sensor_span = 123
    max_amperage = 30
    amps = ((raw_value - zero_offset) / sensor_span) * max_amperage
    return max(amps, 0)

# Maps asset UIDs to device names and sensor field keys
DEVICE_MAPPING = {
    "7z1-903-9xe-74j": {
        "name": "Fridge 1",
        "sensors": {
            "moisture": "DHT11 - moisture",
            "current": "ACS712 - Ammeter",
            "pressure": "BMP180 - thermistor"
        }
    },
    "4d0e408d-7fd6-46a9-8eb6-7ea754d30f6d": {
        "name": "Fridge 2",
        "sensors": {
            "moisture": "sensor 1 d398b907-8995-4429-b538-b3fb26a304a2",
            "current": "sensor 3 d398b907-8995-4429-b538-b3fb26a304a2",
            "pressure": "sensor 2 d398b907-8995-4429-b538-b3fb26a304a2"
        }
    },
    "8sp-910-ftk-9pg": {
        "name": "Dishwasher",
        "sensors": {
            "water": "Capacitive Liquid Level Sensor - WaterConsumption",
            "current": "ACS712 - Ammeter_Dishwasher"
        }
    }
}

# Loads and organizes recent virtual sensor data by device and metric
def fetch_sensor_data():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('SELECT payload FROM "Devices_virtual";')
    rows = cursor.fetchall()
    connection.close()

    structured_data = {}
    for row in rows:
        try:
            payload = json.loads(row[0]) if isinstance(row[0], str) else row[0]
            uid = payload.get("asset_uid")
            timestamp = datetime.fromtimestamp(int(payload.get("timestamp", 0)))
            if uid not in DEVICE_MAPPING:
                continue

            if uid not in structured_data:
                structured_data[uid] = {"moisture": [], "current": [], "water": []}

            for metric, sensor_key in DEVICE_MAPPING[uid]["sensors"].items():
                if sensor_key in payload:
                    value = float(payload[sensor_key])
                    structured_data[uid][metric].append((timestamp, value))
        except Exception:
            continue
    return structured_data

# Processes the query received from the client
def process_query(query):
    sensor_data = fetch_sensor_data()

    if "average moisture" in query:
        uid = "7z1-903-9xe-74j"
        readings = [val for ts, val in sensor_data[uid]["moisture"] if ts >= datetime.now() - timedelta(hours=3)]
        if not readings:
            return "No moisture data available in the past 3 hours."
        avg = round(sum(readings) / len(readings), 2)
        return f"Average Relative Humidity in Fridge 1 (last 3 hours): {avg}% RH"

    if "average water consumption" in query:
        uid = "8sp-910-ftk-9pg"
        readings = [val for _, val in sensor_data[uid]["water"]]
        if not readings:
            return "No water consumption data found."

        # Updated logic: assume max 2000mm = 6 gallons capacity
        MAX_MM = 2000.0
        MAX_GALLONS = 6.0
        avg_mm = sum(readings) / len(readings)
        gallons = round((avg_mm / MAX_MM) * MAX_GALLONS, 2)
        return f"Average dishwasher water consumption: {gallons} gallons"

    if "consumed more electricity" in query:
        usage = {}
        for uid, metrics in sensor_data.items():
            current = sorted(metrics["current"])
            energy = 0
            for i in range(1, len(current)):
                t1, a1 = current[i - 1]
                t2, a2 = current[i]
                hrs = (t2 - t1).total_seconds() / 3600
                avg_amp = (convert_raw_to_amps(a1) + convert_raw_to_amps(a2)) / 2
                energy += (avg_amp * 120 / 1000) * hrs
            usage[DEVICE_MAPPING[uid]["name"]] = round(energy, 3)
        if not usage:
            return "No electricity usage data found."
        most = max(usage, key=usage.get)
        breakdown = "\n".join(f"{name}: {kwh} kWh" for name, kwh in usage.items())
        return f"Electricity usage:\n{breakdown}\n\nHighest: {most}"

    return (
        "Invalid query. Please ask one of the following:\n"
        "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
        "2. What is the average water consumption per cycle in my smart dishwasher?\n"
        "3. Which device consumed more electricity among my three IoT devices?"
    )

# Launches the TCP server and listens for client requests
def launch_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        try:
            server.bind((ip, port))
            server.listen()
            print(f"Server running on {ip}:{port}")
            conn, addr = server.accept()
            with conn:
                print(f"Client connected: {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("Client disconnected.")
                        break
                    query = data.decode()
                    print(f"Received: {query}")
                    try:
                        response = process_query(query)
                    except Exception as error:
                        response = f"Error: {error}"
                    conn.send(response.encode())
        except Exception as e:
            print(f"Server startup failed: {e}")

if __name__ == "__main__":
    ip = input("Enter server IP (e.g., 0.0.0.0): ").strip()
    port = int(input("Enter port (e.g., 511): ").strip())
    launch_server(ip, port)
