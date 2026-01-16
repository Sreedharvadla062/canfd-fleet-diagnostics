#!/usr/bin/env python3
"""
Fleet Scan Script
Scans entire fleet for diagnostics issues
"""

import sys
import json
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fleet_manager import FleetManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run fleet-wide diagnostic scan"""
    logger.info("Starting Fleet-wide Diagnostic Scan...")
    
    # Initialize fleet manager
    fleet = FleetManager()
    
    # Connect to fleet
    if not fleet.connect_fleet():
        logger.error("Failed to connect to fleet")
        return 1
    
    try:
        # Add multiple vehicles to the fleet
        vehicles = [
            ("VEH001", "WVW123456789ABCDE", "Volkswagen", "Golf", 2021),
            ("VEH002", "WAUZZZ3C5XE123456", "Audi", "A4", 2022),
            ("VEH003", "JH2RC5004LM101111", "Honda", "Civic", 2020),
            ("VEH004", "1G1FB1E30D1234567", "Chevrolet", "Cruze", 2019),
        ]
        
        logger.info(f"Adding {len(vehicles)} vehicles to fleet...")
        for vehicle_id, vin, make, model, year in vehicles:
            fleet.add_vehicle(vehicle_id, vin, make, model, year)
            fleet.update_vehicle_status(vehicle_id, online=True)
        
        # Perform fleet-wide scan
        logger.info("Scanning entire fleet...")
        scan_results = fleet.scan_fleet()
        
        # Display results
        logger.info("=== FLEET SCAN RESULTS ===")
        logger.info(f"Total Vehicles: {scan_results['total_vehicles']}")
        logger.info(f"Vehicles Scanned: {scan_results['vehicles_scanned']}")
        logger.info(f"Vehicles with Issues: {scan_results['vehicles_with_issues']}")
        logger.info(f"Total DTCs Found: {scan_results['total_dtcs']}")
        logger.info(f"Scan Time: {scan_results['scan_time']}")
        
        # Get fleet status
        fleet_status = fleet.get_fleet_status()
        logger.info("\n=== FLEET STATUS ===")
        logger.info(f"Online Vehicles: {fleet_status['online_vehicles']}")
        logger.info(f"Offline Vehicles: {fleet_status['offline_vehicles']}")
        logger.info(f"Fleet Summary: {fleet_status['diagnostics_summary']}")
        
        # Export results
        export_file = Path("logs/fleet_scan_results.json")
        export_file.parent.mkdir(exist_ok=True)
        
        results = {
            "scan_results": scan_results,
            "fleet_status": fleet_status,
        }
        
        with open(export_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results exported to {export_file}")
        return 0
        
    finally:
        # Disconnect
        fleet.disconnect_fleet()
        logger.info("Disconnected from fleet")


if __name__ == "__main__":
    sys.exit(main())
