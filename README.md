# Emulator Step Simulator (`mockstep.py`)

## Overview

This Python script simulates realistic walking steps on an Android emulator. It connects to the emulator's console via Telnet and sends accelerometer data that mimics the rhythmic, forceful pattern of a firm walk.

It is designed to help test and debug applications that rely on Android's step counter sensor, providing a consistent and repeatable stream of data. The script also provides a live visualization of the generated sensor data directly in the command line.

## Features

*   **Realistic Simulation:** Generates a sine wave of accelerometer data corresponding to a firm walk at **120 steps per minute (2 steps/second)**.
*   **Live Data Graph:** Displays a real-time, text-based graph of the vertical acceleration (`y-axis`) being sent to the emulator.
*   **Visual Step Impact:** Prints a 5-line ASCII art boot at the peak of each simulated step, making it easy to visually confirm the 2 step-per-second pace.
*   **Emulator Integration:** Connects directly to the Android emulator's Telnet port for sensor manipulation.
*   **Authentication:** Automatically handles authentication by reading the token from the default location (`~/.emulator_console_auth_token`).

## Requirements

*   Python 3
*   An Android emulator running on the same machine.

## How to Use

The script is run from your command line.

### 1. Find Emulator Port and Token

*   **Port:** The title bar of the emulator window shows the port it is running on (e.g., "Android Emulator - Pixel_6_API_33: **5554**"). The default is `5554`.
*   **Token:** The emulator requires an authentication token for console commands. This script automatically reads the token from the `~/.emulator_console_auth_token` file, which is the standard location where Android Studio stores it. You typically do not need to provide this manually.

### 2. Run the Script

Open a terminal or command prompt, navigate to the directory containing `fakesteps.py`, and run the following command.

**Basic Usage (most common):**
This command connects to the default port (`5554`) and uses the automatically found auth token.

```bash
python fakesteps.py
```

**Connecting to a Different Port:**
If your emulator is running on a different port (e.g., `5556`), use the `--port` argument.

```bash
python fakesteps.py --port 5556
```

**Providing the Token Manually:**
If the script cannot find your auth token file, you can provide it directly with the `--token` argument.

```bash
python fakesteps.py --token <your_auth_token>
```

### 3. Stop the Simulation

To stop sending data, press `Ctrl+C` in the terminal. The script will gracefully disconnect from the emulator and reset the sensor data to its default resting state.

## How It Works

The simulation is based on generating a sine wave to represent the vertical acceleration of a person walking.

*   `AMPLITUDE`: Controls the force or "firmness" of the step. A higher value creates a stronger, more easily detectable signal.
*   `FREQUENCY` & `time.sleep`: These values are tuned together to control the pace of the walk. The current settings produce a signal that completes exactly two full cycles (steps) every second.
*   **Impact Detection:** The script tracks the `y-value` of the sine wave. When it detects that the value has just peaked (i.e., it was rising and has now started to fall), it prints the boot logo to mark the "impact" of the foot hitting the ground.


```
~/mockstep main* ❯ python3 mockstep.py                                   17:44:36
Read auth token from /Users/boydp/.emulator_console_auth_token
Connected and authenticated with emulator on port 5554.

Simulating walking steps and displaying live graph...
----------------------------------------------------------
 9.80 | #########################
11.70 | ################################################
11.00 | #######################################
-------------------- STEP IMPACT --------------------
 8.66 | ##########
 7.88 | #
 9.73 | ########################
11.68 | ################################################
11.05 | ########################################
-------------------- STEP IMPACT --------------------
 8.71 | ###########
 7.86 |
 9.67 | #######################
11.65 | ################################################
11.10 | #########################################
-------------------- STEP IMPACT --------------------
 8.77 | ############
 7.85 |
 9.60 | ######################
11.63 | ###############################################
11.15 | #########################################
-------------------- STEP IMPACT --------------------
 8.83 | ############
 7.84 |
 9.54 | #####################
11.60 | ###############################################
11.20 | ##########################################
-------------------- STEP IMPACT --------------------
```