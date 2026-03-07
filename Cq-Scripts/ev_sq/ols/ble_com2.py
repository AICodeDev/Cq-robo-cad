import asyncio
from bleak import BleakScanner, BleakClient
import struct
from datetime import datetime
#C4:F6:76:15:35:73
class RobotBLE:
    """Complete BLE interface for ROBOBLOQ robot - with MAC address connection"""
    
    # Nordic UART Service UUIDs (common for many robots)
    SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Robot sends data here (notify)
    RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # We send commands here (write)
    
    # Common UART characteristic UUIDs (fallback)
    UART_CHARS = [
        "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",  # Nordic
        "0000FFE1-0000-1000-8000-00805F9B34FB",  # HM-10
        "49535343-1E4D-4BD9-BA61-23C647249616",  # Other
    ]
    
    def __init__(self):
        self.client = None
        self.mac_address = None
        self.data_callback = None
        self.connected = False
        self.tx_char_uuid = None  # Will be auto-detected if needed
        
    async def connect_by_mac(self, mac_address, timeout=20.0):
        """
        Connect directly to robot using MAC address
        
        Args:
            mac_address: MAC address (e.g., "D9:C6:D8:9E:8B:56")
            timeout: Connection timeout in seconds
            
        Returns:
            True if connected, False otherwise
        """
        self.mac_address = mac_address
        
        print(f"🔗 Connecting to {mac_address}...")
        
        try:
            self.client = BleakClient(mac_address, timeout=timeout)
            await self.client.connect()
            
            self.connected = True
            print(f"✓ Connected to {mac_address}")
            
            # Discover services and find TX characteristic
            await self._discover_services()
            await self._find_tx_characteristic()
            
            return True
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            print("\nTroubleshooting:")
            print(f"  - Verify MAC: {mac_address}")
            print("  - Check robot is powered on and nearby")
            print("  - Try unpairing device in Bluetooth settings")
            print("  - Run as Administrator (Windows)")
            return False
    
    async def scan_for_robot(self, timeout=10.0, rssi_min=-80):
        """
        Scan for ROBOBLOQ devices and return MAC address
        
        Args:
            timeout: Scan timeout in seconds
            rssi_min: Minimum signal strength (closer = higher number)
            
        Returns:
            MAC address string or None
        """
        print("\n🔍 Scanning for ROBOBLOQ devices...")
        print(f"   Timeout: {timeout}s")
        print(f"   Min RSSI: {rssi_min} dBm")
        print("-" * 50)
        
        devices = await BleakScanner.discover(timeout=timeout)
        
        robobloq_devices = []
        
        for device in devices:
            if device.name and device.name.startswith("ROBO"):
                # Get RSSI from advertisement data
                rssi = device.rssi if hasattr(device, 'rssi') else -100
                
                print(f"✓ Found: {device.name}")
                print(f"  Address: {device.address}")
                print(f"  RSSI: {rssi} dBm")
                
                if rssi >= rssi_min:
                    robobloq_devices.append((device, rssi))
                else:
                    print(f"  ✗ Signal too weak (below {rssi_min} dBm)")
                print()
        
        if not robobloq_devices:
            print("❌ No ROBOBLOQ devices found!")
            return None
        
        # Return MAC address of device with strongest signal
        best_device = max(robobloq_devices, key=lambda x: x[1])[0]
        print(f"✓ Selected: {best_device.name} ({best_device.address})")
        print(f"  Best signal: {best_device.rssi} dBm\n")
        
        return best_device.address
        
    async def _discover_services(self):
        """Discover and print all services/characteristics"""
        print("\n📋 Discovered Services:")
        print("-" * 50)
        
        for service in self.client.services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                properties = ", ".join(char.properties)
                print(f"  └─ Char: {char.uuid}")
                print(f"     Properties: {properties}")
        print()
    
    async def _find_tx_characteristic(self):
        """Auto-detect the TX (notification) characteristic"""
        # First try the default Nordic UART TX characteristic
        try:
            char = self.client.services.get_characteristic(self.TX_CHAR_UUID)
            if char and "notify" in char.properties:
                self.tx_char_uuid = self.TX_CHAR_UUID
                print(f"✓ Using default TX characteristic: {self.TX_CHAR_UUID}\n")
                return
        except:
            pass
        
        # Try other known UART characteristics
        for char_uuid in self.UART_CHARS:
            try:
                char = self.client.services.get_characteristic(char_uuid)
                if char and "notify" in char.properties:
                    self.tx_char_uuid = char_uuid
                    print(f"✓ Using TX characteristic: {char_uuid}\n")
                    return
            except:
                continue
        
        # Find any notifiable characteristic
        for service in self.client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    self.tx_char_uuid = char.uuid
                    print(f"✓ Auto-detected TX characteristic: {char.uuid}\n")
                    return
        
        print("⚠️  No notifiable characteristic found!")
        self.tx_char_uuid = None
        
    async def start_notifications(self, callback=None):
        """
        Subscribe to notifications from robot
        
        Args:
            callback: Function to call when data arrives (optional)
                      Signature: callback(data: bytes)
        """
        if not self.connected:
            print("❌ Not connected!")
            return False
        
        if not self.tx_char_uuid:
            print("❌ No TX characteristic available!")
            return False
        
        self.data_callback = callback
        
        print(f"📡 Starting notifications on {self.tx_char_uuid}...")
        
        try:
            await self.client.start_notify(
                self.tx_char_uuid,
                self._notification_handler
            )
            
            print("✓ Notifications enabled - listening for data...\n")
            return True
            
        except Exception as e:
            print(f"✗ Failed to start notifications: {e}\n")
            return False
        
    def _notification_handler(self, sender, data):
        """Handle incoming data from robot"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Display raw data
        hex_str = data.hex()
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)
        
        print(f"[{timestamp}] ← Received ({len(data)} bytes)")
        print(f"  HEX:   {hex_str}")
        print(f"  ASCII: {ascii_str}")
        
        # Call custom callback if provided
        if self.data_callback:
            self.data_callback(data)
        
    async def write_command(self, data, response=True):
        """
        Send command to robot
        
        Args:
            data: bytes to send
            response: wait for acknowledgment (True) or not (False)
        """
        if not self.connected:
            print("❌ Not connected!")
            return False
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"[{timestamp}] → Sending ({len(data)} bytes)")
        print(f"  HEX: {data.hex()}")
        
        try:
            await self.client.write_gatt_char(
                self.RX_CHAR_UUID,
                data,
                response=response
            )
            print("  ✓ Sent successfully\n")
            return True
        except Exception as e:
            print(f"  ✗ Send failed: {e}\n")
            return False
    
    async def disconnect(self):
        """Disconnect from robot"""
        if self.client and self.connected:
            await self.client.disconnect()
            self.connected = False
            print("\n✓ Disconnected from robot")


# Example usage functions

async def test_direct_mac_connection():
    """Connect using MAC address directly"""
    robot = RobotBLE()
    
    # Replace with your robot's MAC address
    MAC_ADDRESS = "C4:F6:76:15:35:73"  # <-- CHANGE THIS
    
    try:
        # Step 1: Connect by MAC
        if not await robot.connect_by_mac(MAC_ADDRESS):
            return
        
        # Step 2: Start listening for data
        await robot.start_notifications()
        
        # Step 3: Send a test command (optional - adjust to your protocol)
        # test_command = bytes([0xFF, 0x55, 0x04, 0x00, 0x01, 0x02])
        # await robot.write_command(test_command)
        
        # Step 4: Listen for 30 seconds
        print("📡 Listening for data (30 seconds)...\n")
        await asyncio.sleep(30)
        
    finally:
        await robot.disconnect()


async def test_scan_then_connect():
    """Scan for robot first, then connect by MAC"""
    robot = RobotBLE()
    
    # Step 1: Scan for robot
    mac_address = await robot.scan_for_robot(timeout=10.0, rssi_min=-80)
    
    if not mac_address:
        print("No robot found. Make sure it's powered on and nearby!")
        return
    
    try:
        # Step 2: Connect using found MAC address
        if not await robot.connect_by_mac(mac_address):
            return
        
        # Step 3: Start listening for data
        await robot.start_notifications()
        
        # Step 4: Listen for 30 seconds
        print("📡 Listening for data (30 seconds)...\n")
        await asyncio.sleep(30)
        
    finally:
        await robot.disconnect()


async def test_with_custom_callback():
    """Advanced test with custom data processing"""
    robot = RobotBLE()
    
    # Custom callback to process incoming data
    def process_sensor_data(data):
        """Parse sensor data from robot"""
        # Example: Parse first 2 bytes as distance sensor
        if len(data) >= 2:
            try:
                distance = struct.unpack('<H', data[:2])[0]
                print(f"  ➜ Parsed distance: {distance / 10} cm")
            except:
                pass
    
    MAC_ADDRESS = "D9:C6:D8:9E:8B:56"  # <-- CHANGE THIS
    
    try:
        if await robot.connect_by_mac(MAC_ADDRESS):
            await robot.start_notifications(callback=process_sensor_data)
            
            # Keep listening
            print("📡 Listening with custom parser...\n")
            await asyncio.sleep(60)
            
    finally:
        await robot.disconnect()


async def continuous_monitoring():
    """Monitor robot data continuously with logging"""
    robot = RobotBLE()
    
    # Log file
    log_file = f"robot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    def log_data(data):
        """Log data to file"""
        with open(log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            f.write(f"[{timestamp}] {data.hex()}\n")
    
    MAC_ADDRESS = "FE:F5:B8:73:09:64"  # <-- CHANGE THIS
    
    try:
        if await robot.connect_by_mac(MAC_ADDRESS):
            await robot.start_notifications(callback=log_data)
            
            print(f"📝 Logging to: {log_file}")
            print("📡 Press Ctrl+C to stop...\n")
            
            # Run until interrupted
            while True:
                await asyncio.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\nℹ️  Stopped by user")
    finally:
        await robot.disconnect()


# Main entry point
async def main():
    """Choose which test to run"""
    print("=" * 50)
    print("ROBOBLOQ BLE Data Reader - MAC Address Connection")
    print("=" * 50)
    
    # Choose one:
    
    # Option 1: Connect directly with MAC address (recommended if you know it)
    #await test_direct_mac_connection()
    #
    # Option 2: Scan first, then connect
    # await test_scan_then_connect()
    
    # Option 3: With custom callback
    # await test_with_custom_callback()
    
    # Option 4: Continuous monitoring with logging
    await continuous_monitoring()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")