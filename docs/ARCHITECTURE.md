# 🏗️ Architecture & Design Documentation

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      Fleet Diagnostics Platform                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  User Applications & Scripts Layer                                   │  │
│  │  ├─ single_vehicle_diagnostic.py                                     │  │
│  │  ├─ fleet_scan.py                                                    │  │
│  │  ├─ data_export.py                                                   │  │
│  │  └─ Custom applications                                              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                 ▲                                            │
│                                 │                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Fleet Manager (Orchestration Layer)                                 │  │
│  │  ├─ Vehicle registration & tracking                                  │  │
│  │  ├─ Concurrent session management                                    │  │
│  │  ├─ Diagnostics scheduling                                           │  │
│  │  └─ Results aggregation & reporting                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│           ▲                            ▲                            ▲        │
│           │                            │                            │        │
│  ┌────────────────────┐    ┌────────────────────┐    ┌─────────────────┐   │
│  │ CAN-FD Handler     │    │ UDS Client         │    │ Diagnostics     │   │
│  ├────────────────────┤    ├────────────────────┤    │ Collector       │   │
│  │ • Frame Tx/Rx      │    │ • Session Control  │    ├─────────────────┤   │
│  │ • Protocol Mgmt    │    │ • DTC Reading      │    │ • Data Storage  │   │
│  │ • Error Handling   │    │ • Data ID Queries  │    │ • Aggregation   │   │
│  │ • Statistics       │    │ • Vehicle Info     │    │ • Export Format │   │
│  │ • Logging          │    │ • Keep-alive       │    │ • Indexing      │   │
│  └────────────────────┘    └────────────────────┘    └─────────────────┘   │
│           ▲                            ▲                            ▲        │
│           │                            │                            │        │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  CAN Bus Communication Layer (python-can)                          │    │
│  │  ├─ Virtual CAN (vcan0) - Testing                                  │    │
│  │  ├─ Hardware CAN (can0, COM1) - Production                         │    │
│  │  └─ CAN-FD frames (up to 64 bytes)                                 │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                 ▲                                            │
│                                 │                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Vehicle Network (ECUs & Diagnostic Adapters)                      │    │
│  │  ├─ Engine Control Unit (ECU)                                      │    │
│  │  ├─ Transmission Control Module (TCM)                              │    │
│  │  ├─ Body Control Module (BCM)                                      │    │
│  │  ├─ Diagnostics Gateway                                            │    │
│  │  └─ USB-to-CAN Adapter (FTDI, Silicon Labs, Peak, etc.)            │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

## Module Design

### 📦 CANFDHandler Module

**Responsibilities:**
- CAN-FD frame transmission and reception
- Protocol state management
- Hardware abstraction
- Performance statistics

**Key Methods:**
```
connect()              → Establish CAN connection
disconnect()           → Close CAN connection
send_frame(id, data)   → Transmit CAN frame
receive_frames()       → Listen for incoming frames
parse_frame()          → Decode frame data
get_statistics()       → Return performance metrics
```

**Performance:**
- Frame processing: 1000+ fps
- Latency: <10ms
- Support: Up to 64-byte frames

---

### 🔍 UDSClient Module

**Responsibilities:**
- UDS protocol implementation
- Diagnostic session management
- Vehicle communication
- DTC handling

**Key Methods:**
```
connect()                    → Initialize UDS session
session_control()            → Switch diagnostic mode
read_dtc()                   → Retrieve error codes
read_data_by_identifier()    → Query vehicle data
clear_dtc()                  → Clear error codes
tester_present()             → Keep session alive
```

**Supported Services:**
- 0x10 - Diagnostic Session Control
- 0x14 - Clear Diagnostic Information
- 0x19 - Read DTC Information
- 0x22 - Read Data By Identifier
- 0x27 - Security Access
- 0x3E - Tester Present

---

### 📊 DiagnosticsCollector Module

**Responsibilities:**
- Diagnostic data aggregation
- Vehicle profile management
- Data export and storage
- Fleet-wide statistics

**Key Methods:**
```
add_vehicle()            → Register vehicle
collect_diagnostics()    → Store diagnostic data
get_vehicle_diagnostics()→ Retrieve vehicle history
get_fleet_summary()      → Generate fleet statistics
export_diagnostics()     → Save to file
```

**Data Storage:**
- In-memory buffer: 1000 records
- File formats: JSON, CSV
- Database ready (v2.0)

---

### 🚗 FleetManager Module

**Responsibilities:**
- Multi-vehicle coordination
- Session orchestration
- Resource management
- Result aggregation

**Key Methods:**
```
add_vehicle()           → Register vehicle in fleet
remove_vehicle()        → Unregister vehicle
connect_fleet()         → Initialize connections
scan_fleet()            → Diagnostics all vehicles
perform_diagnostics()   → Single vehicle scan
get_fleet_status()      → Fleet health metrics
```

**Concurrency:**
- Multi-threading support
- Up to 5 concurrent sessions
- Thread-safe operations

---

## Data Flow Diagram

```
User Request
     │
     ▼
┌─────────────────────┐
│  Fleet Manager      │
│  (Orchestrator)     │
└─────────────────────┘
     │
     ├─────────────┬─────────────┬──────────────┐
     ▼             ▼             ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Vehicle 1 │  │Vehicle 2 │  │Vehicle 3 │  │Vehicle N │
│CAN Frame │  │CAN Frame │  │CAN Frame │  │CAN Frame │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
     │             │             │              │
     └─────────────┼─────────────┼──────────────┘
                   ▼
          ┌──────────────────┐
          │  CAN-FD Handler  │
          │  UDS Client      │
          └──────────────────┘
                   ▼
          ┌──────────────────┐
          │  CAN Bus Network │
          └──────────────────┘
                   ▼
          ┌──────────────────┐
          │  Vehicle ECUs    │
          └──────────────────┘
                   ▼
          ┌──────────────────┐
          │ Diagnostic Data  │
          │ (DTCs, Metrics)  │
          └──────────────────┘
                   ▼
         ┌──────────────────────┐
         │ DiagnosticsCollector │
         │ • Parse data         │
         │ • Store results      │
         │ • Aggregate stats    │
         └──────────────────────┘
                   ▼
         ┌──────────────────────┐
         │  Fleet Report        │
         │  • Summary stats     │
         │  • DTCs per vehicle  │
         │  • Performance data  │
         │  • Export options    │
         └──────────────────────┘
```

## Threading Model

```
Main Thread (User Script)
     │
     ├─ Fleet Manager Thread (Coordinator)
     │  │
     │  ├─ Worker Thread 1 (Vehicle 1 Scan)
     │  │  ├─ CAN Communication
     │  │  └─ UDS Diagnostics
     │  │
     │  ├─ Worker Thread 2 (Vehicle 2 Scan)
     │  │  ├─ CAN Communication
     │  │  └─ UDS Diagnostics
     │  │
     │  ├─ Worker Thread 3 (Vehicle 3 Scan)
     │  │  ├─ CAN Communication
     │  │  └─ UDS Diagnostics
     │  │
     │  ├─ Worker Thread 4 (Vehicle 4 Scan)
     │  │  ├─ CAN Communication
     │  │  └─ UDS Diagnostics
     │  │
     │  └─ Data Aggregation Thread
     │     ├─ Collect results
     │     ├─ Calculate metrics
     │     └─ Generate report
     │
     └─ Results Aggregator
        ├─ Parse vehicle data
        ├─ Store in collector
        └─ Export results
```

## Configuration Management

```
┌──────────────────────────────────┐
│  config/config.yaml              │
├──────────────────────────────────┤
│ CAN:                             │
│ ├─ interface: "vcan0"            │
│ ├─ bitrate: 500000               │
│ └─ timeout: 1.0                  │
│                                  │
│ UDS:                             │
│ ├─ ta: 0x7DF                     │
│ ├─ ta_rx: 0x7E8                  │
│ └─ timeout: 2.0                  │
│                                  │
│ Fleet:                           │
│ ├─ max_concurrent: 5             │
│ ├─ interval: 3600                │
│ └─ buffer_size: 1000             │
│                                  │
│ Logging:                         │
│ ├─ level: "INFO"                 │
│ ├─ file: "logs/diagnostic.log"   │
│ └─ size: 10MB                    │
└──────────────────────────────────┘
         ▼
   Loaded at startup
         ▼
   ┌──────────────────┐
   │ Application Code │
   │ ├─ CAN config    │
   │ ├─ UDS config    │
   │ └─ Fleet config  │
   └──────────────────┘
```

## Error Handling Strategy

```
Try Operation
     │
     ├─ Success ──► Return Result
     │
     └─ Failure
        │
        ├─ Retry Logic (max 3 attempts)
        │
        ├─ Escalate to higher level
        │
        ├─ Log error
        │
        └─ Graceful Degradation
           ├─ Cache previous data
           ├─ Use default values
           └─ Continue operation
```

## Performance Optimization

### Caching Strategy
- Vehicle profiles cached in memory
- Recent DTC data cached (15 min TTL)
- Configuration cached (runtime)

### Batch Processing
- Frame bundling (10+ frames)
- DTC batch reads
- Multi-vehicle scanning

### Resource Management
- Connection pooling
- Memory limit enforcement
- Automatic cleanup

---

## Security Considerations

✅ **Implemented:**
- Secure CAN communication
- Input validation
- Error message filtering
- Log sanitization

🚧 **Planned (v2.0):**
- Encryption (AES-256)
- Authentication tokens
- Access control lists
- Audit logging

---

## Testing Strategy

```
Unit Tests (src)
├─ canfd_handler_test.py
├─ uds_client_test.py
├─ diagnostics_collector_test.py
└─ fleet_manager_test.py

Integration Tests
├─ end_to_end_test.py
├─ fleet_scanning_test.py
└─ data_export_test.py

Performance Tests
├─ benchmark_throughput.py
├─ benchmark_latency.py
└─ stress_test.py

Coverage Target: 85%+
```

---

## Deployment Architecture

```
Development → Testing → Staging → Production
     │           │         │         │
  Local PC    Linux Box   Server   Fleet
                                   Devices
```

**Supported Platforms:**
- Windows 7+ (development, testing)
- Linux Ubuntu 18.04+ (production)
- macOS 10.13+ (development)
- Raspberry Pi (edge computing)

---

## Future Enhancements (v2.0+)

### 🔄 API Layer
```
REST Endpoints
├─ GET /api/fleet/status
├─ GET /api/vehicles/{id}
├─ POST /api/vehicles/{id}/scan
├─ GET /api/diagnostics/export
└─ WebSocket /api/live/stream
```

### 📊 Database Integration
```
Supported Databases
├─ PostgreSQL (primary)
├─ MySQL
├─ SQLite (local)
└─ MongoDB (future)
```

### 🌐 Cloud Sync
```
Cloud Integration
├─ AWS IoT Core
├─ Azure IoT Hub
├─ Google Cloud IoT
└─ Custom MQTT broker
```

### 🤖 AI/ML Features
```
Machine Learning
├─ Anomaly detection
├─ Predictive maintenance
├─ Pattern recognition
└─ Automated diagnosis
```

---

*Last Updated: January 16, 2026*
*Architecture Version: 1.0*
