"""
Diagnostics Collector Module
Collects and aggregates vehicle diagnostic data from fleet
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class VehicleDiagnostics:
    """Vehicle diagnostic data container"""
    vehicle_id: str
    timestamp: float
    dtc_codes: List[str] = field(default_factory=list)
    engine_data: Dict[str, Any] = field(default_factory=dict)
    emission_data: Dict[str, Any] = field(default_factory=dict)
    performance_data: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


class DiagnosticsCollector:
    """Collects and manages vehicle diagnostic data"""
    
    def __init__(self, max_buffer_size: int = 1000):
        """
        Initialize Diagnostics Collector
        
        Args:
            max_buffer_size: Maximum number of diagnostic records to buffer
        """
        self.max_buffer_size = max_buffer_size
        self.diagnostics_buffer: List[VehicleDiagnostics] = []
        self.vehicle_profiles: Dict[str, Dict] = {}
        logger.info(f"Diagnostics Collector initialized (buffer size: {max_buffer_size})")
    
    def add_vehicle(self, vehicle_id: str, vehicle_info: Dict[str, Any]) -> bool:
        """
        Register a vehicle in the collector
        
        Args:
            vehicle_id: Unique vehicle identifier
            vehicle_info: Vehicle information (VIN, model, year, etc.)
        
        Returns:
            bool: True if vehicle added successfully
        """
        try:
            self.vehicle_profiles[vehicle_id] = {
                "id": vehicle_id,
                "info": vehicle_info,
                "added_at": datetime.now().isoformat(),
                "last_diagnostic": None,
                "diagnostics_count": 0,
            }
            logger.info(f"Vehicle added: {vehicle_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add vehicle: {e}")
            return False
    
    def collect_diagnostics(
        self,
        vehicle_id: str,
        dtc_codes: List[str],
        engine_data: Dict = None,
        emission_data: Dict = None,
        performance_data: Dict = None,
    ) -> Optional[VehicleDiagnostics]:
        """
        Collect diagnostic data for a vehicle
        
        Args:
            vehicle_id: Vehicle identifier
            dtc_codes: List of diagnostic trouble codes
            engine_data: Engine diagnostics
            emission_data: Emission-related data
            performance_data: Performance metrics
        
        Returns:
            VehicleDiagnostics object or None if failed
        """
        if vehicle_id not in self.vehicle_profiles:
            logger.warning(f"Vehicle {vehicle_id} not registered")
            return None
        
        try:
            diagnostic = VehicleDiagnostics(
                vehicle_id=vehicle_id,
                timestamp=datetime.now().timestamp(),
                dtc_codes=dtc_codes or [],
                engine_data=engine_data or {},
                emission_data=emission_data or {},
                performance_data=performance_data or {},
            )
            
            # Add to buffer (FIFO)
            if len(self.diagnostics_buffer) >= self.max_buffer_size:
                self.diagnostics_buffer.pop(0)
            
            self.diagnostics_buffer.append(diagnostic)
            
            # Update vehicle profile
            self.vehicle_profiles[vehicle_id]["last_diagnostic"] = diagnostic.timestamp
            self.vehicle_profiles[vehicle_id]["diagnostics_count"] += 1
            
            logger.info(f"Diagnostics collected for {vehicle_id}: {len(dtc_codes)} DTCs")
            return diagnostic
        except Exception as e:
            logger.error(f"Failed to collect diagnostics: {e}")
            return None
    
    def get_vehicle_diagnostics(self, vehicle_id: str, limit: int = 10) -> List[VehicleDiagnostics]:
        """
        Get diagnostic history for a vehicle
        
        Args:
            vehicle_id: Vehicle identifier
            limit: Maximum records to return
        
        Returns:
            List of VehicleDiagnostics
        """
        return [d for d in self.diagnostics_buffer if d.vehicle_id == vehicle_id][-limit:]
    
    def get_fleet_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for entire fleet
        
        Returns:
            Dictionary with fleet statistics
        """
        total_vehicles = len(self.vehicle_profiles)
        vehicles_with_dtc = sum(
            1 for d in self.diagnostics_buffer 
            if len(d.dtc_codes) > 0
        )
        
        return {
            "total_vehicles": total_vehicles,
            "vehicles_with_dtc": vehicles_with_dtc,
            "total_diagnostics_collected": len(self.diagnostics_buffer),
            "buffer_usage": f"{len(self.diagnostics_buffer)}/{self.max_buffer_size}",
        }
    
    def export_diagnostics(self, filepath: str, vehicle_id: Optional[str] = None) -> bool:
        """
        Export diagnostics to JSON file
        
        Args:
            filepath: Output file path
            vehicle_id: Export only specific vehicle or all if None
        
        Returns:
            bool: True if export successful
        """
        try:
            if vehicle_id:
                data = self.get_vehicle_diagnostics(vehicle_id)
            else:
                data = self.diagnostics_buffer
            
            export_data = [
                {
                    "vehicle_id": d.vehicle_id,
                    "timestamp": d.timestamp,
                    "dtc_codes": d.dtc_codes,
                    "engine_data": d.engine_data,
                    "emission_data": d.emission_data,
                    "performance_data": d.performance_data,
                }
                for d in data
            ]
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Diagnostics exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
    
    def get_vehicles(self) -> List[str]:
        """Get list of registered vehicles"""
        return list(self.vehicle_profiles.keys())
