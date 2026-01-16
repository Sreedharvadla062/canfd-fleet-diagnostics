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

**Causes:**
- CAN interface not configured or unavailable
- Incorrect interface name in config.yaml
- Missing CAN drivers
- No CAN hardware connected

**Solutions:**

**Windows:**
```bash
# Check available COM ports
mode
# or use Device Manager to find COM port

# Update config.yaml
can:
  interface: "COM1"  # or COM3, COM4, etc.
  bitrate: 500000
```

**Linux:**
```bash
# List available CAN interfaces
ip link show
# or
ifconfig

# Enable virtual CAN interface (for testing)
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Check CAN interface status
ip -d link show vcan0
```

**macOS:**
```bash
# Check for USB-to-CAN adapters
system_profiler SPUSBDataType | grep -i "can"

# List serial ports
ls -la /dev/tty.*
```

### UDS Connection Timeout

```
Error: Read DTC failed: timeout
```

**Causes:**
- Vehicle not powered on
- CAN bus not connected properly
- Incorrect UDS addresses in config
- Vehicle in sleep mode

**Solutions:**
```yaml
# Increase timeout in config/config.yaml
uds:
  timeout: 5.0          # Increase from 2.0 to 5.0 seconds
  ta: 0x7DF             # Verify correct address
  ta_rx: 0x7E8          # Verify correct receive address
```

**Checklist:**
- ✅ Vehicle engine is ON or in ACC mode
- ✅ CAN bus wiring is secure
- ✅ Termination resistors are installed (120Ω at both ends)
- ✅ Correct baudrate configured (usually 500kbps)
- ✅ Vehicle supports UDS on CAN

### ImportError: No module named 'python-can'

```
ModuleNotFoundError: No module named 'can'
```

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Or install individual packages
pip install python-can==4.2.0
pip install python-uds==1.3.1
```

### Permission Denied on CAN Interface

```
Error: [Errno 13] Permission denied
```

**Solution (Linux):**
```bash
# Add user to can group
sudo usermod -a -G can $USER
sudo usermod -a -G dialout $USER

# Log out and back in, then test
groups  # verify 'can' is listed
```

### Hardware Not Detected

```
Error: CAN device not found
```

**Check:**
```bash
# Windows - Device Manager
# Look for: USB Serial Port, FTDI, or similar

# Linux
lsusb
dmesg | tail -20

# macOS
system_profiler SPUSBDataType
```

**Install Drivers:**
- FTDI: https://ftdichip.com/drivers/
- Silicon Labs: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- Peak PCAN: https://www.peak-system.com/Drivers.523.0.html
- Vector CANoe: https://www.vector.com/int/en/products/products-a-z/software/drivers/

### Configuration File Not Found

```
FileNotFoundError: config/config.yaml not found
```

**Solution:**
```bash
cd /path/to/canfd-fleet-diagnostics
ls -la config/
# If missing, copy from repository
git checkout config/config.yaml
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Status

**Active Development (v1.0.0)** - Last Updated: January 2026
