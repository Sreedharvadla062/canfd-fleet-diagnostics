"""
Fleet Manager Module
Manages multiple vehicles and coordinates fleet diagnostics
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import threading
from datetime import datetime, timedelta

from src.canfd_handler import CANFDHandler
from src.uds_client import UDSClient
from src.diagnostics_collector import DiagnosticsCollector

logger = logging.getLogger(__name__)


@dataclass
class FleetVehicle:
    """Fleet vehicle record"""
    vehicle_id: str
    vin: str
    make: str
    model: str
    year: int
    last_seen: Optional[float] = None
    online: bool = False
    diagnostics_enabled: bool = True


class FleetManager:
    """Manages fleet of vehicles for diagnostics"""
    
    def __init__(self, max_concurrent_diagnostics: int = 5):
        """
        Initialize Fleet Manager
        
        Args:
            max_concurrent_diagnostics: Maximum concurrent diagnostic sessions
        """
        self.vehicles: Dict[str, FleetVehicle] = {}
        self.canfd_handler = CANFDHandler()
        self.uds_client = UDSClient()
        self.diagnostics_collector = DiagnosticsCollector()
        self.max_concurrent_diagnostics = max_concurrent_diagnostics
        self.diagnostic_threads: List[threading.Thread] = []
        self.lock = threading.Lock()
        logger.info("Fleet Manager initialized")
    
    def add_vehicle(
        self,
        vehicle_id: str,
        vin: str,
        make: str,
        model: str,
        year: int,
    ) -> bool:
        """
        Add vehicle to fleet
        
        Args:
            vehicle_id: Unique vehicle identifier
            vin: Vehicle Identification Number
            make: Vehicle manufacturer
            model: Vehicle model
            year: Manufacturing year
        
        Returns:
            bool: True if vehicle added successfully
        """
        try:
            with self.lock:
                vehicle = FleetVehicle(
                    vehicle_id=vehicle_id,
                    vin=vin,
                    make=make,
                    model=model,
                    year=year,
                )
                self.vehicles[vehicle_id] = vehicle
                self.diagnostics_collector.add_vehicle(
                    vehicle_id,
                    {
                        "vin": vin,
                        "make": make,
                        "model": model,
                        "year": year,
                    }
                )
                logger.info(f"Vehicle added to fleet: {vehicle_id} ({make} {model})")
                return True
        except Exception as e:
            logger.error(f"Failed to add vehicle: {e}")
            return False
    
    def remove_vehicle(self, vehicle_id: str) -> bool:
        """Remove vehicle from fleet"""
        try:
            with self.lock:
                if vehicle_id in self.vehicles:
                    del self.vehicles[vehicle_id]
                    logger.info(f"Vehicle removed from fleet: {vehicle_id}")
                    return True
        except Exception as e:
            logger.error(f"Failed to remove vehicle: {e}")
        return False
    
    def update_vehicle_status(self, vehicle_id: str, online: bool) -> bool:
        """Update vehicle online status"""
        try:
            with self.lock:
                if vehicle_id in self.vehicles:
                    self.vehicles[vehicle_id].online = online
                    self.vehicles[vehicle_id].last_seen = datetime.now().timestamp()
                    status = "online" if online else "offline"
                    logger.info(f"Vehicle {vehicle_id} is now {status}")
                    return True
        except Exception as e:
            logger.error(f"Failed to update vehicle status: {e}")
        return False
    
    def connect_fleet(self) -> bool:
        """Connect to fleet vehicles"""
        try:
            if self.canfd_handler.connect() and self.uds_client.connect():
                logger.info("Fleet connection established")
                return True
        except Exception as e:
            logger.error(f"Fleet connection failed: {e}")
        return False
    
    def disconnect_fleet(self) -> bool:
        """Disconnect from fleet"""
        try:
            self.canfd_handler.disconnect()
            self.uds_client.disconnect()
            logger.info("Fleet connection closed")
            return True
        except Exception as e:
            logger.error(f"Fleet disconnection failed: {e}")
        return False
    
    def perform_diagnostics(self, vehicle_id: str) -> Optional[Dict]:
        """
        Perform diagnostics on a specific vehicle
        
        Args:
            vehicle_id: Vehicle identifier
        
        Returns:
            Diagnostic results dictionary or None
        """
        if vehicle_id not in self.vehicles:
            logger.warning(f"Vehicle {vehicle_id} not found")
            return None
        
        try:
            vehicle = self.vehicles[vehicle_id]
            logger.info(f"Starting diagnostics for {vehicle_id}...")
            
            # Read DTCs
            dtc_codes = [code for code, _ in self.uds_client.read_dtc()]
            
            # Collect diagnostics
            diagnostic = self.diagnostics_collector.collect_diagnostics(
                vehicle_id=vehicle_id,
                dtc_codes=dtc_codes,
                engine_data={
                    "rpm": 0,
                    "coolant_temp": 90,
                    "intake_air_temp": 45,
                },
                emission_data={
                    "o2_sensor_1": 0.8,
                    "co2_level": 250,
                },
                performance_data={
                    "fuel_consumption": 8.5,
                    "acceleration": 6.2,
                },
            )
            
            logger.info(f"Diagnostics completed for {vehicle_id}: {len(dtc_codes)} DTCs found")
            return {
                "vehicle_id": vehicle_id,
                "dtc_count": len(dtc_codes),
                "dtc_codes": dtc_codes,
            }
        except Exception as e:
            logger.error(f"Diagnostics failed for {vehicle_id}: {e}")
            return None
    
    def scan_fleet(self) -> Dict[str, Any]:
        """
        Scan entire fleet for diagnostics
        
        Returns:
            Dictionary with scan results
        """
        logger.info("Starting fleet-wide diagnostics scan...")
        results = {
            "total_vehicles": len(self.vehicles),
            "vehicles_scanned": 0,
            "vehicles_with_issues": 0,
            "total_dtcs": 0,
            "scan_time": datetime.now().isoformat(),
        }
        
        for vehicle_id in self.vehicles:
            result = self.perform_diagnostics(vehicle_id)
            if result:
                results["vehicles_scanned"] += 1
                if result["dtc_count"] > 0:
                    results["vehicles_with_issues"] += 1
                    results["total_dtcs"] += result["dtc_count"]
        
        logger.info(f"Fleet scan complete: {results['vehicles_scanned']}/{results['total_vehicles']} vehicles scanned")
        return results
    
    def get_fleet_status(self) -> Dict[str, Any]:
        """Get current fleet status"""
        online_vehicles = sum(1 for v in self.vehicles.values() if v.online)
        
        return {
            "total_vehicles": len(self.vehicles),
            "online_vehicles": online_vehicles,
            "offline_vehicles": len(self.vehicles) - online_vehicles,
            "diagnostics_summary": self.diagnostics_collector.get_fleet_summary(),
        }
    
    def export_fleet_diagnostics(self, filepath: str) -> bool:
        """Export fleet diagnostics to file"""
        return self.diagnostics_collector.export_diagnostics(filepath)
