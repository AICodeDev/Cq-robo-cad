import asyncio
from bleak import BleakScanner, BleakClient
import struct
from datetime import datetime
import time

# Global variables for connection management
GLOBAL_MAC_ADDRESS = None
LAST_DATA_TIME = None
RECONNECT_DELAY = 1  # seconds between reconnect attempts
WATCHDOG_TIMEOUT = 10  # seconds without data before reconnect

class RobotBLE:
    """Complete BLE interface for ROBOBLOQ robot with auto-reconnect"""
    
    # Nordic UART Service UUIDs
    SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Robot sends data here (notify)
    RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # We send commands here (write)
    
    # Common UART characteristic UUIDs (fallback)
    UART_CHARS = [
        "6E400003-B5A3-F393-E0A9-E50E24DCCA9E",  # Nordic
        "0000FFE1-0000-1000-8000-00805F9B34FB",  # HM-10
        "49535343-1E4D-4BD9-BA61-23C647249616",  # Other
    ]
    
    # Known MAC addresses (from your script)
    KNOWN_MACS = [
        "C4:F6:76:15:35:73",
        "D9:C6:D8:9E:8B:56",
        "FE:F5:B8:73:09:64",
        "DF:9B:A1:06:8B:1A",
    ]
    
    def __init__(self):
        self.client = None
        self.mac_address = None
        self.data_callback = None
        self.connected = False
        self.tx_char_uuid = None
        self.disconnect_callback = None
        
    async def scan_for_robot(self, timeout=10.0, rssi_min=-150):
        """
        Scan for ROBOBLOQ devices (name starts with ROBO) or known MAC addresses
        
        Args:
            timeout: Scan timeout in seconds
            rssi_min: Minimum signal strength
            
        Returns:
            MAC address string or None
        """
        global GLOBAL_MAC_ADDRESS
        
        print("\n🔍 Scanning for ROBOBLOQ devices...")
        print(f"   Timeout: {timeout}s | Min RSSI: {rssi_min} dBm")
        print("-" * 60)
        
        devices = await BleakScanner.discover(timeout=timeout)
        
        robobloq_devices = []
        
        for device in devices:
            # Check if name starts with ROBO or MAC is in known list
            is_robo_name = device.name and device.name.upper().startswith("ROBO")
            is_known_mac = device.address in self.KNOWN_MACS
            
            
            if is_robo_name or is_known_mac:
                  
                rssi = device.rssi if hasattr(device, 'rssi') else -1000
                robobloq_devices.append((device, rssi))  
                print(f"✓ Found: {device.name or 'Unknown'}")
                print(f"  Address: {device.address}")
                print(f"  RSSI: {rssi} dBm", end="")
                
                print()
        
        if not robobloq_devices:
            print("❌ No ROBOBLOQ devices found!")
            print("\nKnown MAC addresses to look for:")
            for mac in self.KNOWN_MACS:
                print(f"  • {mac}")
            return None
        
        # Return MAC address of device with strongest signal
        best_device = max(robobloq_devices, key=lambda x: x[1])[0]
        GLOBAL_MAC_ADDRESS = best_device.address
        
        print(f"✓ Selected: {best_device.name or 'Unknown'} ({best_device.address})")
        #print(f"  Best signal: {best_device.rssi} dBm\n")
        
        return best_device.address
        
    async def connect_by_mac(self, mac_address, timeout=20.0):
        """
        Connect directly to robot using MAC address
        
        Args:
            mac_address: MAC address
            timeout: Connection timeout in seconds
            
        Returns:
            True if connected, False otherwise
        """
        global GLOBAL_MAC_ADDRESS, LAST_DATA_TIME
        
        self.mac_address = mac_address
        GLOBAL_MAC_ADDRESS = mac_address
        
        print(f"🔗 Connecting to {mac_address}...")
        
        try:
            self.client = BleakClient(
                mac_address, 
                timeout=timeout,
                disconnected_callback=self._handle_disconnect
            )
            await self.client.connect()
            
            self.connected = True
            LAST_DATA_TIME = time.time()  # Reset watchdog
            
            print(f"✓ Connected to {mac_address}")
            
            # Discover services and find TX characteristic
            await self._discover_services()
            await self._find_tx_characteristic()
            
            return True
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            self.connected = False
            return False
    
    def _handle_disconnect(self, client):
        """Handle unexpected disconnections"""
        print(f"\n⚠️  DISCONNECTED from {self.mac_address}")
        self.connected = False
        if self.disconnect_callback:
            self.disconnect_callback()
    
    async def _discover_services(self):
        """Discover services (simplified output)"""
        try:
            services = self.client.services
            print(f"📋 Discovered {len(services)} services")
        except Exception as e:
            print(f"⚠️  Service discovery error: {e}")
    
    async def _find_tx_characteristic(self):
        """Auto-detect the TX (notification) characteristic"""
        # First try the default Nordic UART TX characteristic
        try:
            char = self.client.services.get_characteristic(self.TX_CHAR_UUID)
            if char and "notify" in char.properties:
                self.tx_char_uuid = self.TX_CHAR_UUID
                print(f"✓ Using TX characteristic: {self.TX_CHAR_UUID}\n")
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
        """Subscribe to notifications from robot"""
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
        global LAST_DATA_TIME
        log_data = data.decode('ascii', errors='ignore')
        LAST_DATA_TIME = time.time()  # Update watchdog timer
        
          
        print(f"{log_data}")
        
        # Call custom callback if provided
        if self.data_callback:
            self.data_callback(log_data)
    
    async def disconnect(self):
        """Disconnect from robot"""
        if self.client and self.connected:
            try:
                await self.client.disconnect()
            except:
                pass
            self.connected = False
            print("\n✓ Disconnected from robot")
    
    def is_connected(self):
        """Check if connected"""
        return self.connected and self.client and self.client.is_connected


async def monitor_with_auto_reconnect():
    """Monitor robot data with automatic reconnection"""
    global GLOBAL_MAC_ADDRESS, LAST_DATA_TIME
    
    robot = RobotBLE()
    
    # Log file
    log_file = f"robot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    def log_data(data):
        """Log data to file and console"""
        #loggable_string = data.decode('ascii', errors='ignore')
        
        with open(log_file, 'a') as f:            
            f.write(data)
    
    def on_disconnect():
        """Callback when disconnected"""
        print("⚠️  Disconnect detected - will attempt reconnect...")
    
    robot.disconnect_callback = on_disconnect
    
    print("=" * 60)
    print("ROBOBLOQ BLE Monitor - Auto-Reconnect Enabled")
    print("=" * 60)
    print(f"📁 Log file: {log_file}")
    print(f"⏱️  Watchdog timeout: {WATCHDOG_TIMEOUT} seconds")
    print(f"🔄 Auto-reconnect delay: {RECONNECT_DELAY} seconds")
    print("🛑 Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Step 1: Scan or use stored MAC
            if not GLOBAL_MAC_ADDRESS:
                print("\n🔍 No stored MAC address - scanning...")
                mac_address = await robot.scan_for_robot(timeout=10.0, rssi_min=-85)
                
                if not mac_address:
                    print("❌ No robot found. Retrying in 5 seconds...")
                    await asyncio.sleep(5)
                    continue
                
                GLOBAL_MAC_ADDRESS = mac_address
            else:
                print(f"\n🔄 Using stored MAC: {GLOBAL_MAC_ADDRESS}")
                mac_address = GLOBAL_MAC_ADDRESS
            
            # Step 2: Connect
            if not robot.is_connected():
                if not await robot.connect_by_mac(mac_address):
                    print(f"❌ Connection failed. Retrying in {RECONNECT_DELAY}s...")
                    await asyncio.sleep(RECONNECT_DELAY)
                    continue
                
                # Start notifications
                if not await robot.start_notifications(callback=log_data):
                    print("❌ Failed to start notifications. Reconnecting...")
                    await robot.disconnect()
                    await asyncio.sleep(RECONNECT_DELAY)
                    continue
                
                LAST_DATA_TIME = time.time()
            
            # Step 3: Monitor connection and watchdog
            while robot.is_connected():
                await asyncio.sleep(0.5)
                
                # Check watchdog - no data for WATCHDOG_TIMEOUT seconds
                if LAST_DATA_TIME and (time.time() - LAST_DATA_TIME) > WATCHDOG_TIMEOUT:
                    print(f"\n⚠️  No data for {WATCHDOG_TIMEOUT}s - checking connection...")
                    
                    if not robot.is_connected():
                        print("❌ Connection lost - reconnecting...")
                        break
                    else:
                        print("✓ Still connected - resetting watchdog")
                        LAST_DATA_TIME = time.time()
            
            # Connection lost - cleanup and retry
            print("\n🔄 Connection lost - attempting reconnect...")
            await robot.disconnect()
            await asyncio.sleep(RECONNECT_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    finally:
        await robot.disconnect()
        print(f"\n📁 Data logged to: {log_file}")


async def main():
    """Main entry point"""
    await monitor_with_auto_reconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")