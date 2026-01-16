# CAN-FD + UDS Vehicle Data Collector - Fleet Diagnostics

A comprehensive Python-based fleet diagnostics system that uses CAN-FD (Controller Area Network with Flexible Data-rate) and UDS (Unified Diagnostic Services) protocols to collect and manage vehicle diagnostic data from multiple vehicles in real-time.

## Features

- **CAN-FD Communication**: Full support for CAN-FD protocol with extended data frames (up to 64 bytes)
- **UDS Diagnostics**: Unified Diagnostic Services implementation for vehicle diagnostics
- **Fleet Management**: Manage and coordinate diagnostics across multiple vehicles
- **Real-time Data Collection**: Collects DTCs, engine data, emission data, and performance metrics
- **Multi-threaded Support**: Handles concurrent diagnostic sessions
- **Data Export**: Export diagnostics data to JSON format
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Easy Configuration**: YAML-based configuration system

## Project Structure

```
canfd-fleet-diagnostics/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── canfd_handler.py           # CAN-FD communication handler
│   ├── uds_client.py              # UDS diagnostic client
│   ├── diagnostics_collector.py   # Diagnostics data collection
│   └── fleet_manager.py           # Fleet management system
├── scripts/
│   ├── single_vehicle_diagnostic.py      # Single vehicle diagnostics
│   ├── fleet_scan.py                      # Fleet-wide scan
│   └── data_export.py                     # Data export utility
├── tests/
│   └── test_fleet_manager.py             # Unit tests
├── config/
│   └── config.yaml                        # Configuration file
├── logs/                                  # Log directory (auto-created)
├── data/                                  # Data directory (auto-created)
├── requirements.txt                       # Python dependencies
├── setup.py                               # Setup configuration
├── .gitignore                             # Git ignore rules
├── LICENSE                                # Apache 2.0 License
└── README.md                              # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sreedharvadla062/canfd-fleet-diagnostics.git
cd canfd-fleet-diagnostics
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Development Dependencies (Optional)

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Fleet Manager Example

```python
from src.fleet_manager import FleetManager

# Initialize fleet manager
fleet = FleetManager()

# Connect to the fleet
if fleet.connect_fleet():
    # Add vehicles to fleet
    fleet.add_vehicle("VEH001", "WVW123456789ABCDE", "Volkswagen", "Golf", 2021)
    fleet.add_vehicle("VEH002", "WAUZZZ3C5XE123456", "Audi", "A4", 2022)
    
    # Perform diagnostics on specific vehicle
    result = fleet.perform_diagnostics("VEH001")
    print(f"Diagnostics: {result}")
    
    # Scan entire fleet
    scan_results = fleet.scan_fleet()
    print(f"Fleet Status: {scan_results}")
    
    # Export diagnostics
    fleet.export_fleet_diagnostics("diagnostics_export.json")
    
    # Get fleet status
    status = fleet.get_fleet_status()
    print(f"Fleet Status: {status}")
    
    # Disconnect
    fleet.disconnect_fleet()
```

### Using Individual Components

#### CAN-FD Handler

```python
from src.canfd_handler import CANFDHandler

handler = CANFDHandler(interface="vcan0", bitrate=500000)
if handler.connect():
    # Send CAN frame
    handler.send_frame(0x123, b"\x01\x02\x03\x04")
    
    # Receive frames
    frames = handler.receive_frames(timeout=1.0)
    
    # Get statistics
    stats = handler.get_statistics()
    print(f"Statistics: {stats}")
    
    handler.disconnect()
```

#### UDS Client

```python
from src.uds_client import UDSClient, UDSSessionType

uds = UDSClient()
if uds.connect():
    # Change session
    uds.session_control(UDSSessionType.EXTENDED)
    
    # Read DTCs
    dtcs = uds.read_dtc()
    print(f"DTCs: {dtcs}")
    
    # Read data by identifier
    data = uds.read_data_by_identifier([0xF190])
    
    # Keep session alive
    uds.tester_present()
    
    uds.disconnect()
```

### Running Sample Scripts

#### Single Vehicle Diagnostics

```bash
python scripts/single_vehicle_diagnostic.py
```

#### Fleet-wide Scan

```bash
python scripts/fleet_scan.py
```

#### Export Data

```bash
python scripts/data_export.py --output diagnostics.json
```

## Configuration

Edit `config/config.yaml` to customize:

- CAN interface and bitrate
- UDS parameters
- Fleet settings
- Logging configuration
- Database settings
- API configuration

## Supported DTC Codes

The system supports standard OBD-II DTC codes:

- **P-codes**: Powertrain (e.g., P0101, P0102)
- **C-codes**: Chassis (e.g., C0010)
- **B-codes**: Body (e.g., B0010)
- **U-codes**: Network (e.g., U1001)

## Logging

Logs are automatically created in the `logs/` directory. Configure logging in `config/config.yaml`:

```yaml
logging:
  level: "INFO"
  file: "logs/fleet_diagnostics.log"
```

## Testing

Run unit tests:

```bash
pytest tests/
pytest tests/ --cov=src  # With coverage
```

## Performance Considerations

- Maximum 5 concurrent diagnostic sessions (configurable)
- Buffer size: 1000 records (configurable)
- CAN frame size: Up to 64 bytes (CAN-FD)
- Typical scan time: 5-10 seconds per vehicle

## Troubleshooting

### CAN Interface Not Found

```
Error: Failed to connect to CAN bus
```

**Root Causes:**
- ❌ CAN interface not configured or unavailable
- ❌ Incorrect interface name in config.yaml
- ❌ Missing CAN drivers
- ❌ No CAN hardware connected
- ❌ Virtual CAN module not loaded (Linux)

**Step-by-Step Solutions:**

**🪟 Windows:**
```bash
# Step 1: List all COM ports
wmic logicaldisk get name
# or open Device Manager > Ports (COM & LPT)

# Step 2: Test connection to specific port
mode COM1:9600,N,8,1

# Step 3: Update config.yaml with correct port
# Edit config/config.yaml and set:
can:
  interface: "COM1"      # Replace with your port (COM1, COM3, etc.)
  bitrate: 500000
  timeout: 1.0

# Step 4: Verify driver installation
# Device Manager > Universal Serial Bus controllers
# Should show your CAN adapter (FTDI, Silicon Labs, Peak, etc.)

# Step 5: Test with Python
python -c "import serial; print(serial.tools.list_ports.comports())"
```

**🐧 Linux:**
```bash
# Step 1: List all CAN interfaces
ip link show
# or
ifconfig | grep -i can
# or
ls /dev/can* /dev/vcan*

# Step 2: Check if interface is UP
ip link show vcan0
# Output should show "UP" in the state

# Step 3: If no CAN interface exists, create virtual one for testing
sudo modprobe can
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Step 4: Verify virtual CAN is working
ip -d link show vcan0

# Step 5: For real CAN hardware (if using actual CAN card)
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0

# Step 6: Test CAN communication
python3 -c "import can; print(can.Bus('vcan0', bustype='virtual'))"
```

**🍎 macOS:**
```bash
# Step 1: List USB devices
system_profiler SPUSBDataType | grep -i can
# or
ls -la /dev/tty.* /dev/cu.*

# Step 2: Check for FTDI or Silicon Labs adapters
system_profiler SPUSBDataType | grep -A 5 "FTDI\|Silicon"

# Step 3: Install drivers if needed (see "Driver Installation" section below)

# Step 4: Test connection
python3 -c "import serial; print(serial.tools.list_ports.comports())"
```

**Verification Test:**
```python
# Create test_can_connection.py
import sys
sys.path.insert(0, '.')

from src.canfd_handler import CANFDHandler

handler = CANFDHandler(interface="vcan0")  # or COM1, can0, etc.
if handler.connect():
    print("✅ CAN connection successful!")
    print(f"Connected to: {handler.interface}")
    handler.disconnect()
else:
    print("❌ CAN connection failed!")
    sys.exit(1)

# Run: python test_can_connection.py
```

---

### UDS Connection Timeout

```
Error: Read DTC failed: timeout
```

**Root Causes:**
- ❌ Vehicle engine not running
- ❌ CAN bus not properly connected
- ❌ Incorrect UDS addresses
- ❌ Timeout too short
- ❌ Vehicle in sleep/standby mode
- ❌ ECU not responding

**Step-by-Step Solutions:**

```yaml
# Step 1: Increase timeout in config/config.yaml
uds:
  timeout: 5.0          # Increase from 2.0 to 5.0 seconds
  ta: 0x7DF             # Transmission Address (broadcast)
  ta_rx: 0x7E8          # Response Address
  session_type: 1       # 1=default, 3=extended
```

**Pre-flight Checklist:**
```
✅ Vehicle Requirements:
   □ Engine is ON or in ACC/ignition mode
   □ Battery voltage is 12V minimum
   □ No immobilizer active
   □ ECU is responding to other systems

✅ Hardware Requirements:
   □ CAN bus wiring is secure and not damaged
   □ Termination resistors installed (120Ω at both CAN ends)
   □ No loose or corroded connectors
   □ Proper CAN_H and CAN_L connections (not reversed)

✅ Configuration Requirements:
   □ Baudrate = 500kbps (common, verify for your vehicle)
   □ TA (Transmission Address) = 0x7DF or vehicle-specific
   □ TA_RX = 0x7E8 or vehicle-specific
   □ Timeout ≥ 3.0 seconds for first request

✅ Vehicle-Specific Issues:
   □ Vehicle supports UDS on CAN (not all do)
   □ Vehicle variant has diagnostics enabled
   □ No active DTCs blocking diagnostics access
```

**Diagnostic Steps:**
```bash
# Create diagnose_uds.py
import sys
sys.path.insert(0, '.')

from src.uds_client import UDSClient, UDSSessionType

uds = UDSClient()

print("Step 1: Attempting UDS connection...")
if not uds.connect():
    print("❌ UDS connection failed - check CAN interface first")
    sys.exit(1)

print("✅ UDS connected")

print("Step 2: Attempting to change session...")
if not uds.session_control(UDSSessionType.EXTENDED):
    print("⚠️  Session change failed - ECU may not be responding")

print("Step 3: Reading DTCs...")
dtcs = uds.read_dtc()
print(f"DTCs found: {len(dtcs)}")
for code, description in dtcs:
    print(f"  - {code}: {description}")

uds.disconnect()
print("✅ All tests passed!")

# Run: python diagnose_uds.py
```

---

### ImportError: No module named 'python-can'

```
ModuleNotFoundError: No module named 'can'
or
ModuleNotFoundError: No module named 'uds'
```

**Root Causes:**
- ❌ Dependencies not installed
- ❌ Wrong Python interpreter
- ❌ Virtual environment not activated
- ❌ pip install failed silently

**Step-by-Step Solutions:**

```bash
# Step 1: Verify Python version (should be 3.8+)
python --version
python -c "import sys; print(sys.executable)"

# Step 2: Ensure pip is up to date
python -m pip install --upgrade pip setuptools wheel

# Step 3: Full clean reinstall
python -m venv venv_clean
# Windows:
venv_clean\Scripts\activate
# Linux/macOS:
source venv_clean/bin/activate

# Step 4: Install with verbose output to see any errors
pip install -v -r requirements.txt

# Step 5: Verify each package
pip show python-can
pip show python-uds
python -c "import can; print('can:', can.__version__)"
python -c "import uds; print('uds module imported successfully')"

# Step 6: If issues persist, install individually with specific versions
pip install python-can==4.2.0 --force-reinstall --no-cache-dir
pip install python-uds==1.3.1 --force-reinstall --no-cache-dir

# Step 7: Test import
python -c "from src.canfd_handler import CANFDHandler; print('✅ Import successful')"
```

---

### Permission Denied on CAN Interface

```
Error: [Errno 13] Permission denied
or
Error: [Errno 1] Operation not permitted
```

**Root Cause:**
- ❌ User doesn't have permission to access CAN interface

**Solution (Linux):**

```bash
# Step 1: Check current user and groups
whoami
groups

# Step 2: Add user to can and dialout groups
sudo usermod -a -G can $USER
sudo usermod -a -G dialout $USER

# Step 3: Alternative - Run with sudo (not recommended)
sudo python scripts/single_vehicle_diagnostic.py

# Step 4: Log out and back in for group changes to take effect
# Then verify:
groups
# Should show: your_username can dialout

# Step 5: Test permission
ip link show vcan0  # Should work without sudo now
```

---

### Hardware Not Detected

```
Error: CAN device not found
or
Serial port not recognized
```

**Root Causes:**
- ❌ USB adapter not connected
- ❌ Drivers not installed
- ❌ Incorrect USB port
- ❌ Device not recognized by OS

**Hardware Detection Steps:**

```bash
# Windows - Check Device Manager or run:
wmic logicaldisk get name
# Or use PowerShell:
[System.IO.Ports.SerialPort]::GetPortNames()

# Linux - Check for USB devices:
lsusb
# Output should show: FTDI, Silicon Labs, Peak, Kvaser, etc.
# Example: Bus 001 Device 005: ID 0403:6001 Future Technology Devices International, Ltd FT232 Serial (UART) IC

dmesg | tail -50  # Check kernel messages for USB events

# macOS - Check USB devices:
system_profiler SPUSBDataType
ioreg -p IOUSB -l -w 0 | grep -A 5 "FT232"
```

**Driver Installation:**

| Adapter | Driver Link | Notes |
|---------|-------------|-------|
| **FTDI (FT232)** | [ftdichip.com/drivers](https://ftdichip.com/drivers/) | Most common USB-to-CAN |
| **Silicon Labs** | [silabs.com/drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) | CP2102, CP2103, CP2104 |
| **Peak PCAN** | [peak-system.com](https://www.peak-system.com/Drivers.523.0.html) | Professional CAN adapters |
| **Kvaser** | [kvaser.com/drivers](https://www.kvaser.com/drivers/) | High-quality CAN devices |
| **Vector** | [vector.com/drivers](https://www.vector.com/int/en/products/products-a-z/software/drivers/) | CANoe, VN series |

**After Installing Drivers:**
```bash
# Windows - Restart (required for driver installation)
# Linux/macOS - Unplug and replug USB device

# Verify device is recognized
# Windows: Device Manager > Ports (COM & LPT)
# Linux: lsusb and dmesg
# macOS: system_profiler SPUSBDataType
```

---

### Configuration File Not Found

```
FileNotFoundError: [Errno 2] No such file or directory: 'config/config.yaml'
```

**Root Causes:**
- ❌ Running script from wrong directory
- ❌ config.yaml was deleted
- ❌ Wrong project path

**Step-by-Step Solutions:**

```bash
# Step 1: Verify project structure
ls -la config/
# Should show: config.yaml

# Step 2: If config.yaml is missing, restore from git
git checkout config/config.yaml

# Step 3: Verify you're in correct directory
pwd
# Should end with: /canfd-fleet-diagnostics

# Step 4: Run script from project root
python scripts/single_vehicle_diagnostic.py

# DO NOT run from scripts/ directory
cd scripts
python single_vehicle_diagnostic.py  # ❌ Wrong - will fail

# Step 5: If still missing, copy from backup
cp config/config.yaml config/config.yaml.bak
```

---

### Cannot Connect to Vehicle / No Response

```
Error: Vehicle not responding to UDS requests
or
Read timeout - no data received
```

**Diagnostic Steps:**

```python
# Create debug_connection.py
import sys
sys.path.insert(0, '.')

from src.canfd_handler import CANFDHandler
from src.uds_client import UDSClient
import time

print("=== CAN-FD Fleet Diagnostics - Connection Debug ===\n")

# Test 1: CAN Connection
print("TEST 1: CAN Bus Connection")
can = CANFDHandler()
if can.connect():
    print("✅ CAN connection OK")
    stats = can.get_statistics()
    print(f"   Interface: {can.interface}")
    print(f"   Bitrate: {can.bitrate} bps")
else:
    print("❌ CAN connection FAILED")
    print("   → Check CAN interface in config.yaml")
    sys.exit(1)

# Test 2: CAN Communication
print("\nTEST 2: Attempting CAN frame transmission")
if can.send_frame(0x7DF, b"\x02\x10\x01"):
    print("✅ CAN frame sent successfully")
else:
    print("❌ CAN frame send FAILED")

time.sleep(0.5)

# Test 3: UDS Connection
print("\nTEST 3: UDS Session")
uds = UDSClient()
if uds.connect():
    print("✅ UDS connection OK")
else:
    print("❌ UDS connection FAILED")
    print("   → Check UDS addresses in config.yaml")

# Test 4: Tester Present
print("\nTEST 4: Tester Present (keep-alive)")
if uds.tester_present():
    print("✅ Tester present sent")
else:
    print("❌ Tester present FAILED")

can.disconnect()
uds.disconnect()

print("\n=== All diagnostics complete ===")

# Run: python debug_connection.py
```

---

### Common Error Messages & Solutions

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `OSError: [Errno 2]` | Wrong interface name | Update `interface:` in config.yaml |
| `SerialException: write_timeout` | Baud rate mismatch | Verify `bitrate:` = 500000 |
| `Timeout reading from device` | No ECU response | Check vehicle power and CAN wiring |
| `Permission denied /dev/can0` | Linux permissions | Add user to `can` group |
| `ModuleNotFoundError: can` | Dependencies missing | Run `pip install -r requirements.txt` |
| `FTDI device not found` | Driver missing | Install FTDI drivers |
| `Port COM1 unavailable` | Port in use | Close other serial apps |



## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Status

**Active Development (v1.0.0)** - Last Updated: January 2026
