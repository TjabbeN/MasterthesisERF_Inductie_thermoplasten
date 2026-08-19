import serial
import csv
import datetime
import sys
import os

# -- Configuration ------------------------------------------------------------
PORT = "COM3"
BAUD = 115200
# -----------------------------------------------------------------------------

def main():
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"experiment_B_{timestamp}.csv"

    print(f"Connecting to {PORT} at {BAUD} baud...")
    
    try:
        ser = serial.Serial(PORT, BAUD, timeout=2)
    except serial.SerialException as e:
        print(f"Error: could not open port {PORT}. Is the Arduino connected?\n{e}")
        sys.exit(1)

    print(f"Logging to: {filename}")
    print("Press Ctrl+C to stop.\n")

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time_s", "temp_c", "cold_junction_c"])

        try:
            while True:
                line = ser.readline().decode("utf-8", errors="ignore").strip()

                if not line:
                    continue

                # Print to terminal
                print(line)

                # Skip the header row from Arduino
                if "time_s" in line:
                    continue

                # Write data rows
                parts = line.split(",")
                if len(parts) == 3:
                    try:
                        # Validate that all three values are numbers
                        float(parts[0])
                        float(parts[1])
                        float(parts[2])
                        writer.writerow(parts)
                        csvfile.flush()  # Write immediately
                    except ValueError:
                        # Not a data line (e.g. error message from Arduino) — skip
                        pass

        except KeyboardInterrupt:
            print(f"\nStopped. Data saved to: {os.path.abspath(filename)}")
        finally:
            ser.close()

if __name__ == "__main__":
    main()