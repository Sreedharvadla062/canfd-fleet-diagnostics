#!/usr/bin/env python3
"""
Single Vehicle Diagnostics Script
Performs diagnostics on a single vehicle
"""

import sys
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
    """Run single vehicle diagnostics"""
    logger.info("Starting Single Vehicle Diagnostics...")
    
    # Initialize fleet manager
    fleet = FleetManager()
    
    # Connect to fleet
    if not fleet.connect_fleet():
        logger.error("Failed to connect to fleet")
        return 1
    
    try:
        # Add a vehicle to the fleet
        vehicle_id = "VEH001"
        fleet.add_vehicle(
            vehicle_id=vehicle_id,
            vin="WVW123456789ABCDE",
            make="Volkswagen",
            model="Golf",
            year=2021
        )
        
        # Update vehicle status to online
        fleet.update_vehicle_status(vehicle_id, online=True)
        
        # Perform diagnostics
        logger.info(f"Performing diagnostics for vehicle: {vehicle_id}")
        result = fleet.perform_diagnostics(vehicle_id)
        
        if result:
            logger.info(f"Diagnostics Result:")
            logger.info(f"  - Vehicle ID: {result['vehicle_id']}")
            logger.info(f"  - DTC Count: {result['dtc_count']}")
            logger.info(f"  - DTC Codes: {result['dtc_codes']}")
        else:
            logger.error("Diagnostics failed")
            return 1
        
        # Get vehicle diagnostics history
        history = fleet.diagnostics_collector.get_vehicle_diagnostics(vehicle_id, limit=5)
        logger.info(f"Diagnostics History: {len(history)} records")
        
        return 0
        
    finally:
        # Disconnect
        fleet.disconnect_fleet()
        logger.info("Disconnected from fleet")


if __name__ == "__main__":
    sys.exit(main())
