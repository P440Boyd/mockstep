import telnetlib
import time
import math
import argparse
import os

# --- Graphing Constants ---
GRAPH_WIDTH = 50
AMPLITUDE = 2.0
Y_BASELINE = 9.8

def plot_data_point(y_value):
    """
    Plots a single y-value as a text-based bar on the command line.
    """
    min_y = Y_BASELINE - AMPLITUDE
    max_y = Y_BASELINE + AMPLITUDE

    # Ensure the value is within bounds to prevent normalization errors at device level
    y_value_clamped = max(min_y, min(y_value, max_y))
    normalized_value = (y_value_clamped - min_y) / (max_y - min_y)
    bar_length = int(normalized_value * GRAPH_WIDTH)
    bar = '#' * bar_length
    print(f"{y_value:5.2f} | {bar}")


def connect_to_emulator(host, port, auth_token):
    """
    Establishes and authenticates a telnet connection to the Android emulator.
    """
    try:
        emulator = telnetlib.Telnet(host, port, timeout=10)
        emulator.read_until(b"OK", timeout=10)

        if not auth_token:
            print("Authentication token is missing...")
            return None

        emulator.write(f'auth {auth_token}\n'.encode())
        response = emulator.read_until(b"OK", timeout=10)

        if b"KO" in response:
            print("Authentication failed.")
            return None

        print(f"Connected and authenticated with emulator on port {port}.")
        return emulator
    except Exception as e:
        print(f"An error occurred during connection: {e}")
        return None

def set_sensor_data(emulator, sensor, x, y, z):
    """
    Sends a command to the emulator to set the specified sensor's data.
    """
    try:
        command = f'sensor set {sensor} {x:.2f}:{y:.2f}:{z:.2f}\n'
        emulator.write(command.encode())
        emulator.read_until(b"OK", timeout=2)
    except Exception as e:
        print(f"An error occurred while setting {sensor} data: {e}")

def generate_walking_acceleration(step):
    """
    Generates accelerometer data that simulates a realistic walking pattern.
    """
    frequency = 1.25  # Approximate frequency for 120 steps/min with a 0.1s sleep

    x = 0.0
    y = Y_BASELINE + AMPLITUDE * math.sin(frequency * step)
    z = 0.0

    return x, y, z

def run_simulation(emulator):
    """
    Contains the main loop for sending sensor data to the emulator.
    """
    step_counter = 0
    previous_y = Y_BASELINE
    was_rising = False
    print("\nSimulating walking steps and displaying live graph...")
    print("-" * (GRAPH_WIDTH + 8))
    try:
        while True:
            x, y, z = generate_walking_acceleration(step_counter)
            set_sensor_data(emulator, "acceleration", x, y, z)
            plot_data_point(y)

            is_rising_now = y > previous_y
            if was_rising and not is_rising_now:
                print("-------------------- STEP IMPACT --------------------")
            
            was_rising = is_rising_now
            previous_y = y
            step_counter += 1
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping simulation.")
    finally:
        print("Resetting sensor data.")
        set_sensor_data(emulator, "acceleration", 0, 9.8, 0)
        emulator.close()
        print("Telnet connection closed.")

def main():
    """
    Handles argument parsing, emulator connection, and starts the simulation.
    """
    parser = argparse.ArgumentParser(description="Simulate walking steps on an Android emulator and display a live graph.")
    parser.add_argument(
        "--port",
        type=int,
        default=5554,
        help="The telnet port of the Android emulator (default: 5554)."
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="The auth token. Tries to read from ~/.emulator_console_auth_token if not provided."
    )
    args = parser.parse_args()

    emulator_host = "localhost"
    emulator_port = args.port
    auth_token = args.token

    if not auth_token:
        try:
            token_path = os.path.expanduser("~/.emulator_console_auth_token")
            with open(token_path, "r") as f:
                auth_token = f.read().strip()
            print(f"Read auth token from {token_path}")
        except FileNotFoundError:
            print("Warning: Auth token file not found and --token was not provided.")

    emulator = connect_to_emulator(emulator_host, emulator_port, auth_token)

    if emulator:
        run_simulation(emulator)

if __name__ == "__main__":
    main()
