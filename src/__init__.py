"""
CAN-FD Fleet Diagnostics - Vehicle Data Collector Package
"""

__version__ = "1.0.0"
__author__ = "Fleet Diagnostics Team"

from src.canfd_handler import CANFDHandler
from src.uds_client import UDSClient
from src.diagnostics_collector import DiagnosticsCollector
from src.fleet_manager import FleetManager

__all__ = [
    "CANFDHandler",
    "UDSClient",
    "DiagnosticsCollector",
    "FleetManager",
]
