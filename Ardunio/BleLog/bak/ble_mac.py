"""
BLE Receiver - Connect by MAC Address Only
No name searching, just direct MAC connection
"""

import asyncio
from bleak import BleakClient
from datetime import datetime

# YOUR MAC ADDRESS
MAC_ADDRESS = "d9:c6:d8:9e:8b:56"
#0C:95:05:0F:FB:20
MAC_ADDRESS = "0C:95:05:0F:FB:20"
#C4:F6:76:15:35:73
MAC_ADDRESS = "C4:F6:76:15:35:73"


# Common UART characteristic UUIDs
UART_CHARS = [
    "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",  # Nordic
    "0000FFE1-0000-1000-8000-00805F9B34FB",  # HM-10
    "49535343-1E4D-4BD9-BA61-23C647249616",  # Other
]

LOG_TO_FILE = True
LOG_FILENAME = f"ble_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
log_file = None

def notification_handler(sender, data):
    """Handle received data"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    
    try:
        message = data.decode('utf-8', errors='replace')
        log_line = f"[{timestamp}] {message}"
    except:
        hex_str = ' '.join([f'{b:02X}' for b in data])
        log_line = f"[{timestamp}] HEX: {hex_str}\n"
    
    print(log_line, end='')
    
    if LOG_TO_FILE and log_file:
        log_file.write(log_line)
        log_file.flush()

async def find_uart_char(client):
    """Find notifiable characteristic"""
    # Try known UUIDs
    for char_uuid in UART_CHARS:
        try:
            char = client.services.get_characteristic(char_uuid)
            if char and "notify" in char.properties:
                return char_uuid
        except:
            continue
    
    # Find any notifiable characteristic
    for service in client.services:
        for char in service.characteristics:
            if "notify" in char.properties:
                return char.uuid
    
    return None

async def main():
    global log_file
    
    print("=" * 60)
    print("BLE Receiver - Direct MAC Connection")
    print("=" * 60)
    print(f"MAC: {MAC_ADDRESS}")
    
    if LOG_TO_FILE:
        log_file = open(LOG_FILENAME, 'w', encoding='utf-8')
        print(f"Log: {LOG_FILENAME}")
    
    print("\nConnecting...")
    
    try:
        async with BleakClient(MAC_ADDRESS, timeout=20.0) as client:
            print(f"✓ Connected to {MAC_ADDRESS}")
            
            # Find characteristic
            char_uuid = await find_uart_char(client)
            
            if not char_uuid:
                print("\n✗ No UART characteristic found")
                print("\nAvailable characteristics:")
                for service in client.services:
                    for char in service.characteristics:
                        print(f"  {char.uuid} - {', '.join(char.properties)}")
                return
            
            print(f"✓ Using characteristic: {char_uuid}")
            print("\n" + "=" * 60)
            print("Receiving data... (Ctrl+C to stop)")
            print("=" * 60 + "\n")
            
            # Start receiving
            await client.start_notify(char_uuid, notification_handler)
            
            # Keep alive
            while client.is_connected:
                await asyncio.sleep(1)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print(f"  - Verify MAC: {MAC_ADDRESS}")
        print("  - Check Arduino is running (Serial Monitor shows 'Sent')")
        print("  - Try unpair device in Windows Bluetooth settings")
        print("  - Run as Administrator")
    
    finally:
        if log_file:
            log_file.close()
            print(f"\n✓ Log saved: {LOG_FILENAME}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")