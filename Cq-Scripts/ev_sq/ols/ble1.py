"""
BLE Serial Receiver - Python Script for Windows
Connects to Arduino BLE device and logs received data
Requires: bleak library (pip install bleak)
"""

import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime
"""
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    # _FLAG_READ | _FLAG_NOTIFY,
    _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
"""

# Nordic UART Service UUIDs
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Arduino TX (we receive)
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Arduino RX (we send)

# Device name to search for
DEVICE_NAME = "ROBOBLOQ-k1"
#MyQ-ACA
DEVICE_NAME = "MyQ-ACA"


# Optional: Log to file
LOG_TO_FILE = True
LOG_FILENAME = f"ble_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

log_file = None

def notification_handler(sender, data):
    """Handle incoming BLE notifications"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    message = data.decode('utf-8', errors='replace')
    
    log_line = f"[{timestamp}] {message}"
    print(log_line, end='')
    
    # Write to log file if enabled
    if LOG_TO_FILE and log_file:
        log_file.write(log_line)
        log_file.flush()

async def find_device():
    """Scan for the Arduino BLE device"""
    print(f"Scanning for BLE device '{DEVICE_NAME}'...")
    
    devices = await BleakScanner.discover(timeout=10.0)
    
    for device in devices:
        print (device.name)
        if device.name == DEVICE_NAME:
            print(f"Found device: {device.name} ({device.address})")
            return device.address
    
    return None

async def run_ble_client(address):
    """Connect to device and receive data"""
    global log_file
    
    if LOG_TO_FILE:
        log_file = open(LOG_FILENAME, 'w', encoding='utf-8')
        print(f"Logging to file: {LOG_FILENAME}")
    
    try:
        async with BleakClient(address) as client:
            print(f"Connected to {address}")
            print("Receiving data... (Press Ctrl+C to stop)\n")
            
            # Subscribe to notifications
            await client.start_notify(UART_TX_CHAR_UUID, notification_handler)
            
            # Keep connection alive
            while True:
                await asyncio.sleep(1)
                
                # Optional: Send data back to Arduino
                # await client.write_gatt_char(UART_RX_CHAR_UUID, b"Hello from PC\n")
                
    except KeyboardInterrupt:
        print("\n\nStopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if log_file:
            log_file.close()
            print(f"\nLog saved to: {LOG_FILENAME}")

async def main():
    """Main function"""
    print("=" * 60)
    print("BLE Serial Receiver for Windows")
    print("=" * 60)
    
    # Find the device
    address = await find_device()
    
    if address is None:
        print(f"\nDevice '{DEVICE_NAME}' not found!")
        print("Make sure:")
        print("  1. Arduino is powered on")
        print("  2. BLE sketch is running")
        print("  3. Bluetooth is enabled on your PC")
        return
    
    # Connect and receive data
    await run_ble_client(address)

if __name__ == "__main__":
    # Run the main async function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")