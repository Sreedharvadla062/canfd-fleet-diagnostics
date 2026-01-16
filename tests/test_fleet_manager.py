"""
Unit tests for Fleet Manager
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fleet_manager import FleetManager
from src.canfd_handler import CANFDHandler
from src.uds_client import UDSClient
from src.diagnostics_collector import DiagnosticsCollector


class TestFleetManager(unittest.TestCase):
    """Test Fleet Manager functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.fleet = FleetManager()
    
    def test_fleet_initialization(self):
        """Test fleet initialization"""
        self.assertIsNotNone(self.fleet)
        self.assertEqual(len(self.fleet.vehicles), 0)
    
    def test_add_vehicle(self):
        """Test adding vehicle to fleet"""
        result = self.fleet.add_vehicle(
            "VEH001",
            "WVW123456789ABCDE",
            "Volkswagen",
            "Golf",
            2021
        )
        self.assertTrue(result)
        self.assertIn("VEH001", self.fleet.vehicles)
    
    def test_remove_vehicle(self):
        """Test removing vehicle from fleet"""
        self.fleet.add_vehicle("VEH001", "WVW123456789ABCDE", "Volkswagen", "Golf", 2021)
        result = self.fleet.remove_vehicle("VEH001")
        self.assertTrue(result)
        self.assertNotIn("VEH001", self.fleet.vehicles)
    
    def test_update_vehicle_status(self):
        """Test updating vehicle status"""
        self.fleet.add_vehicle("VEH001", "WVW123456789ABCDE", "Volkswagen", "Golf", 2021)
        result = self.fleet.update_vehicle_status("VEH001", online=True)
        self.assertTrue(result)
        self.assertTrue(self.fleet.vehicles["VEH001"].online)
    
    def test_fleet_connection(self):
        """Test fleet connection"""
        result = self.fleet.connect_fleet()
        self.assertTrue(result)
        result = self.fleet.disconnect_fleet()
        self.assertTrue(result)
    
    def test_get_fleet_status(self):
        """Test getting fleet status"""
        self.fleet.connect_fleet()
        self.fleet.add_vehicle("VEH001", "WVW123456789ABCDE", "Volkswagen", "Golf", 2021)
        self.fleet.update_vehicle_status("VEH001", online=True)
        
        status = self.fleet.get_fleet_status()
        self.assertEqual(status["total_vehicles"], 1)
        self.assertEqual(status["online_vehicles"], 1)
        
        self.fleet.disconnect_fleet()


class TestCANFDHandler(unittest.TestCase):
    """Test CAN-FD Handler functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = CANFDHandler()
    
    def test_handler_initialization(self):
        """Test handler initialization"""
        self.assertIsNotNone(self.handler)
        self.assertEqual(self.handler.bitrate, 500000)
    
    def test_connect_disconnect(self):
        """Test connect and disconnect"""
        result = self.handler.connect()
        self.assertTrue(result)
        self.assertTrue(self.handler.is_connected)
        
        result = self.handler.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.handler.is_connected)
    
    def test_send_frame(self):
        """Test sending CAN frame"""
        self.handler.connect()
        result = self.handler.send_frame(0x123, b"\x01\x02\x03\x04")
        self.assertTrue(result)
        self.handler.disconnect()
    
    def test_statistics(self):
        """Test statistics"""
        self.handler.connect()
        self.handler.send_frame(0x123, b"\x01\x02\x03\x04")
        
        stats = self.handler.get_statistics()
        self.assertEqual(stats["frames_sent"], 1)
        
        self.handler.disconnect()


class TestUDSClient(unittest.TestCase):
    """Test UDS Client functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.uds = UDSClient()
    
    def test_client_initialization(self):
        """Test client initialization"""
        self.assertIsNotNone(self.uds)
        self.assertEqual(self.uds.address_ta, 0x7DF)
    
    def test_connect_disconnect(self):
        """Test connect and disconnect"""
        result = self.uds.connect()
        self.assertTrue(result)
        self.assertTrue(self.uds.is_connected)
        
        result = self.uds.disconnect()
        self.assertTrue(result)
        self.assertFalse(self.uds.is_connected)
    
    def test_read_dtc(self):
        """Test reading DTC"""
        self.uds.connect()
        dtcs = self.uds.read_dtc()
        self.assertIsInstance(dtcs, list)
        self.uds.disconnect()


class TestDiagnosticsCollector(unittest.TestCase):
    """Test Diagnostics Collector functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.collector = DiagnosticsCollector()
    
    def test_collector_initialization(self):
        """Test collector initialization"""
        self.assertIsNotNone(self.collector)
        self.assertEqual(len(self.collector.vehicles), 0)
    
    def test_add_vehicle(self):
        """Test adding vehicle"""
        result = self.collector.add_vehicle(
            "VEH001",
            {"vin": "WVW123456789ABCDE"}
        )
        self.assertTrue(result)
        self.assertIn("VEH001", self.collector.vehicle_profiles)
    
    def test_collect_diagnostics(self):
        """Test collecting diagnostics"""
        self.collector.add_vehicle("VEH001", {"vin": "WVW123456789ABCDE"})
        diagnostic = self.collector.collect_diagnostics(
            "VEH001",
            ["P0101", "P0102"],
            engine_data={"rpm": 1000}
        )
        self.assertIsNotNone(diagnostic)
        self.assertEqual(len(diagnostic.dtc_codes), 2)
    
    def test_get_fleet_summary(self):
        """Test getting fleet summary"""
        summary = self.collector.get_fleet_summary()
        self.assertIn("total_vehicles", summary)
        self.assertIn("vehicles_with_dtc", summary)


if __name__ == "__main__":
    unittest.main()
