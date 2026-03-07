import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import time

# Global connection cache
GLOBAL_MAC_ADDRESS = None
CACHED_TX_CHAR = None
CACHED_RX_CHAR = None
LAST_DATA_TIME = None

# Settings
RECONNECT_DELAY = 1
WATCHDOG_TIMEOUT = 10

class RobotBLE:
    """Simplified BLE interface with characteristic caching"""
    
    # Known devices
    KNOWN_MACS = [
        "C4:F6:76:15:35:73",
        "D9:C6:D8:9E:8B:56",
        "FE:F5:B8:73:09:64",
        "DF:9B:A1:06:8B:1A",
    ]
    
    # Default characteristics (Nordic UART)
    DEFAULT_TX = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
    DEFAULT_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    
    def __init__(self):
        self.client = None
        self.mac_address = None
        self.connected = False
        self.data_callback = None
        
    async def scan_for_robot(self, timeout=10.0):
        """Scan for ROBO devices or known MACs"""
        global GLOBAL_MAC_ADDRESS
        
        print("🔍 Scanning...")
        devices = await BleakScanner.discover(timeout=timeout)
        
        found = []
        for device in devices:
            is_robo = device.name and device.name.upper().startswith("ROBO")
            is_known = device.address in self.KNOWN_MACS
            
            if is_robo or is_known:
                rssi = getattr(device, 'rssi', -1000)
                found.append((device, rssi))
                print(f"✓ {device.name or 'Unknown'} @ {device.address} ({rssi} dBm)")
        
        if not found:
            return None
        
        # Select strongest signal
        best = max(found, key=lambda x: x[1])[0]
        GLOBAL_MAC_ADDRESS = best.address
        print(f"→ Selected: {best.address}\n")
        return best.address
        
    async def connect(self, mac_address, timeout=15.0):
        """Connect with cached characteristics for speed"""
        global GLOBAL_MAC_ADDRESS, LAST_DATA_TIME, CACHED_TX_CHAR, CACHED_RX_CHAR
        
        self.mac_address = mac_address
        GLOBAL_MAC_ADDRESS = mac_address
        
        print(f"🔗 Connecting to {mac_address}...")
        
        try:
            self.client = BleakClient(
                mac_address,
                timeout=timeout,
                disconnected_callback=self._on_disconnect
            )
            await self.client.connect()
            self.connected = True
            LAST_DATA_TIME = time.time()
            
            print(f"✓ Connected")
            
            # Use cached characteristics if available
            if CACHED_TX_CHAR and CACHED_RX_CHAR:
                print(f"✓ Using cached characteristics")
                return True
            
            # Find and cache characteristics
            await self._find_and_cache_characteristics()
            return True
            
        except Exception as e:
            print(f"✗ Failed: {e}")
            self.connected = False
            return False
    
    async def _find_and_cache_characteristics(self):
        """Find TX/RX characteristics and cache them globally"""
        global CACHED_TX_CHAR, CACHED_RX_CHAR
        
        # Try default first
        try:
            tx_char = self.client.services.get_characteristic(self.DEFAULT_TX)
            rx_char = self.client.services.get_characteristic(self.DEFAULT_RX)
            
            if tx_char and "notify" in tx_char.properties:
                CACHED_TX_CHAR = self.DEFAULT_TX
                CACHED_RX_CHAR = self.DEFAULT_RX
                print(f"✓ Cached Nordic UART characteristics\n")
                return
        except:
            pass
        
        # Search for notifiable characteristic
        for service in self.client.services:
            for char in service.characteristics:
                if "notify" in char.properties and not CACHED_TX_CHAR:
                    CACHED_TX_CHAR = char.uuid
                    print(f"✓ Found TX: {char.uuid}")
                if "write" in char.properties and not CACHED_RX_CHAR:
                    CACHED_RX_CHAR = char.uuid
                    print(f"✓ Found RX: {char.uuid}")
        
        print()
    
    def _on_disconnect(self, client):
        """Handle disconnect"""
        self.connected = False
    
    async def start_notifications(self, callback=None):
        """Start receiving data"""
        global CACHED_TX_CHAR
        
        if not self.connected or not CACHED_TX_CHAR:
            return False
        
        self.data_callback = callback
        
        try:
            await self.client.start_notify(CACHED_TX_CHAR, self._on_data)
            print("✓ Notifications started\n")
            return True
        except Exception as e:
            print(f"✗ Notify failed: {e}")
            return False
    
    def _on_data(self, sender, data):
        """Handle incoming data"""
        global LAST_DATA_TIME
        LAST_DATA_TIME = time.time()
        
        # Decode and print
        text = data.decode('utf-8', errors='ignore')
        print(text, end='', flush=True)
        
        # Callback for logging
        if self.data_callback:
            self.data_callback(text)
    
    async def disconnect(self):
        """Disconnect"""
        if self.client and self.connected:
            try:
                await self.client.disconnect()
            except:
                pass
            self.connected = False
    
    def is_connected(self):
        """Check connection status"""
        return self.connected and self.client and self.client.is_connected


async def main():
    """Main monitoring loop with auto-reconnect"""
    global GLOBAL_MAC_ADDRESS, LAST_DATA_TIME
    
    robot = RobotBLE()
    log_file = f"robot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Fast logging - write immediately with flush
    def log_data(text):
        with open(log_file, 'a', buffering=1) as f:  # Line buffered
            f.write(text)
    
    print("=" * 60)
    print("ROBOBLOQ BLE Monitor v3 - Fast Reconnect")
    print("=" * 60)
    print(f"📁 Log: {log_file}")
    print(f"⏱️  Watchdog: {WATCHDOG_TIMEOUT}s")
    print(f"🔄 Reconnect delay: {RECONNECT_DELAY}s")
    print("🛑 Ctrl+C to stop\n")
    
    try:
        while True:
            # Get MAC address (scan once or use cached)
            if not GLOBAL_MAC_ADDRESS:
                mac = await robot.scan_for_robot(timeout=10.0)
                if not mac:
                    print("❌ No device found. Retrying...\n")
                    await asyncio.sleep(5)
                    continue
            else:
                mac = GLOBAL_MAC_ADDRESS
            
            # Connect if not connected
            if not robot.is_connected():
                if not await robot.connect(mac):
                    await asyncio.sleep(RECONNECT_DELAY)
                    continue
                
                if not await robot.start_notifications(callback=log_data):
                    await robot.disconnect()
                    await asyncio.sleep(RECONNECT_DELAY)
                    continue
                
                LAST_DATA_TIME = time.time()
            
            # Monitor connection
            while robot.is_connected():
                await asyncio.sleep(0.5)
                
                # Watchdog check
                if LAST_DATA_TIME and (time.time() - LAST_DATA_TIME) > WATCHDOG_TIMEOUT:
                    if not robot.is_connected():
                        print("\n❌ Connection lost")
                        break
                    else:
                        LAST_DATA_TIME = time.time()
            
            # Reconnect
            print("\n🔄 Reconnecting...")
            await robot.disconnect()
            await asyncio.sleep(RECONNECT_DELAY)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped")
    finally:
        await robot.disconnect()
        print(f"📁 Logged to: {log_file}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")