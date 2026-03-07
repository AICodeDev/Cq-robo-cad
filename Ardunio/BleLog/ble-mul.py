"""
BLE All MAC Finder and Tester
Finds ALL unique MAC addresses (even with duplicate names)
Tests each MAC address individually
"""

import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime

DEVICE_PREFIXES = ["ROBO", "MyQ"]

UART_TX_CHAR_UUIDS = [
    "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",  # Nordic TX
    "0000FFE1-0000-1000-8000-00805F9B34FB",  # HM-10 characteristic
    "49535343-1E4D-4BD9-BA61-23C647249616",  # Other TX
]

data_received = {}

def create_handler(mac_address):
    """Create notification handler"""
    def handler(sender, data):
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        try:
            message = data.decode('utf-8', errors='replace').strip()
            print(f"  [{timestamp}] ✓✓✓ DATA: {message}")
            
            if mac_address not in data_received:
                data_received[mac_address] = []
            data_received[mac_address].append(message)
        except:
            hex_str = ' '.join([f'{b:02X}' for b in data])
            print(f"  [{timestamp}] ✓✓✓ HEX: {hex_str}")
            
            if mac_address not in data_received:
                data_received[mac_address] = []
            data_received[mac_address].append(hex_str)
    
    return handler

async def find_uart_char(client):
    """Find notifiable characteristic"""
    for char_uuid in UART_TX_CHAR_UUIDS:
        try:
            char = client.services.get_characteristic(char_uuid)
            if char and "notify" in char.properties:
                return char_uuid
        except:
            continue
    
    for service in client.services:
        for char in service.characteristics:
            if "notify" in char.properties:
                return char.uuid
    return None

async def test_mac_address(mac_address, device_name, test_duration=10):
    """Test a specific MAC address"""
    print(f"\n{'='*80}")
    print(f"Testing MAC: {mac_address}")
    print(f"Name: {device_name}")
    print('='*80)
    
    try:
        async with BleakClient(mac_address, timeout=15.0) as client:
            print(f"  ✓ Connected successfully")
            
            char_uuid = await find_uart_char(client)
            if not char_uuid:
                print(f"  ✗ No UART characteristic found")
                print(f"  Available characteristics:")
                for service in client.services:
                    for char in service.characteristics:
                        print(f"    - {char.uuid} ({', '.join(char.properties)})")
                return False
            
            print(f"  ✓ Found characteristic: {char_uuid}")
            print(f"  ⏳ Listening for {test_duration} seconds...")
            print(f"  (Waiting for data from Arduino...)")
            
            handler = create_handler(mac_address)
            await client.start_notify(char_uuid, handler)
            
            # Listen and show progress
            for i in range(test_duration):
                await asyncio.sleep(1)
                if mac_address in data_received and len(data_received[mac_address]) > 0:
                    count = len(data_received[mac_address])
                    print(f"  ✓ Received {count} message(s) so far...")
            
            await client.stop_notify(char_uuid)
            
            if mac_address in data_received and len(data_received[mac_address]) > 0:
                print(f"\n  ✓✓✓ SUCCESS! Received {len(data_received[mac_address])} messages")
                print(f"  Last message: {data_received[mac_address][-1]}")
                return True
            else:
                print(f"\n  ✗ No data received from this device")
                return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

async def main():
    global data_received
    
    print("=" * 80)
    print("BLE MAC ADDRESS FINDER - Test Every Unique MAC")
    print("=" * 80)
    print()
    
    # Scan multiple times to catch all devices
    print("Scanning for devices (will scan 3 times to find all MACs)...")
    all_devices = {}  # MAC -> device object
    
    for scan_num in range(3):
        print(f"\nScan {scan_num + 1}/3...")
        devices = await BleakScanner.discover(timeout=10.0)
        
        for device in devices:
            if device.name and any(device.name.startswith(p) for p in DEVICE_PREFIXES):
                all_devices[device.address] = device
                print(f"  Found: {device.name} @ {device.address}")
        
        await asyncio.sleep(1)
    
    if not all_devices:
        print(f"\n✗ No devices found starting with {DEVICE_PREFIXES}")
        print("\nAll devices seen in last scan:")
        for d in devices:
            print(f"  - {d.name if d.name else '(Unknown)'} @ {d.address}")
        return
    
    # Show all unique MAC addresses
    print(f"\n{'='*80}")
    print(f"FOUND {len(all_devices)} UNIQUE MAC ADDRESS(ES)")
    print('='*80)
    
    for i, (mac, device) in enumerate(all_devices.items(), 1):
        print(f"{i}. {device.name}")
        print(f"   MAC: {mac}")
        print(f"   RSSI: {device.rssi} dBm")
        print()
    
    # Test each unique MAC address
    print(f"{'='*80}")
    print("TESTING EACH MAC ADDRESS")
    print("="*80)
    
    working_macs = []
    
    for mac, device in all_devices.items():
        data_received[mac] = []  # Reset
        
        if await test_mac_address(mac, device.name, test_duration=10):
            working_macs.append((mac, device.name))
        
        await asyncio.sleep(1)  # Brief pause between tests
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print("="*80)
    
    if working_macs:
        print(f"\n✓✓✓ {len(working_macs)} MAC ADDRESS(ES) ARE SENDING DATA:\n")
        
        for mac, name in working_macs:
            msg_count = len(data_received[mac])
            print(f"┌─ Device: {name}")
            print(f"│  MAC: {mac}")
            print(f"│  Messages received: {msg_count}")
            if msg_count > 0:
                print(f"│  Sample: {data_received[mac][0]}")
            print(f"└─{'─'*76}")
            print()
        
        print("=" * 80)
        print("RECOMMENDATION")
        print("=" * 80)
        
        if len(working_macs) == 1:
            mac, name = working_macs[0]
            print(f"\n✓ Use this MAC address:")
            print(f"\n  {mac}")
            print(f"\nUpdate your receiver script with:")
            print(f'  TARGET_ADDRESS = "{mac}"')
            
        else:
            print(f"\n⚠ Multiple MAC addresses are sending data!")
            print("\nPossible reasons:")
            print("  1. Same module advertising on multiple addresses")
            print("  2. Multiple BLE modules in range")
            print("\nTo identify which is your Arduino:")
            print("  - Check signal strength (RSSI) - closest device usually strongest")
            print("  - Power off Arduino and scan again to see which disappears")
            print("  - Check if your module has a MAC printed on it")
    
    else:
        print(f"\n✗ NONE of the MAC addresses sent any data\n")
        print("Troubleshooting checklist:")
        print("  [ ] Arduino is powered on")
        print("  [ ] BLE_Minimal_Test.ino is uploaded")
        print("  [ ] Arduino Serial Monitor shows 'Sent: Hello'")
        print("  [ ] Serial3 baud rate matches BLE module (try 9600 or 115200)")
        print("  [ ] BLE module has power (LED on?)")
        print("\nNext steps:")
        print("  1. Upload BLE_AT_Config.ino to verify Arduino↔BLE communication")
        print("  2. Run: python ble_explorer.py to see device services")
        print("  3. Check if device needs pairing in Windows Bluetooth settings")
    
    print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")