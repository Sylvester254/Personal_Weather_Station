import uos
import ujson

def log_data_csv(timestamp, temperature, humidity, pressure, altitude, rainfall_status, rainfall_inches):
    file_name = "weather_data.csv"

    def file_exists(file_name):
        try:
            uos.stat(file_name)
            return True
        except OSError:
            return False

    file_name = "weather_data.csv"

    if not file_exists(file_name):
        with open(file_name, 'w') as f:
            f.write("timestamp,temperature,humidity,pressure,altitude,rainfall_status,rainfall_inches\n")
            print("data logged successfully into weather_data.csv")

    
    with open(file_name, 'a') as f:
        f.write(f"{timestamp},{temperature},{humidity},{pressure},{altitude},{rainfall_status},{rainfall_inches}\n")
        print("data logged successfully")

def serve_weather_data():
    file_name = "weather_data.csv"
    data = ""

    with open(file_name, 'r') as f:
        data = f.read()

    return data

