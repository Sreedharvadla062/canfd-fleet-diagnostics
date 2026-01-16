#!/usr/bin/env python3
"""
Data Export Script
Exports diagnostics data to JSON format
"""

import sys
import argparse
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
    """Export diagnostics data"""
    parser = argparse.ArgumentParser(
        description="Export fleet diagnostics data to JSON"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="diagnostics_export.json",
        help="Output file path (default: diagnostics_export.json)"
    )
    parser.add_argument(
        "--vehicle",
        type=str,
        default=None,
        help="Export specific vehicle (vehicle ID) or all vehicles"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting Data Export...")
    
    # Initialize fleet manager
    fleet = FleetManager()
    
    # Connect to fleet
    if not fleet.connect_fleet():
        logger.error("Failed to connect to fleet")
        return 1
    
    try:
        # Add sample vehicles and collect data
        vehicles = [
            ("VEH001", "WVW123456789ABCDE", "Volkswagen", "Golf", 2021),
            ("VEH002", "WAUZZZ3C5XE123456", "Audi", "A4", 2022),
        ]
        
        logger.info("Adding sample vehicles...")
        for vehicle_id, vin, make, model, year in vehicles:
            fleet.add_vehicle(vehicle_id, vin, make, model, year)
            # Collect diagnostics
            fleet.perform_diagnostics(vehicle_id)
        
        # Export data
        output_path = Path(args.output)
        output_path.parent.mkdir(exist_ok=True)
        
        if args.vehicle:
            logger.info(f"Exporting data for vehicle: {args.vehicle}")
        else:
            logger.info("Exporting data for all vehicles...")
        
        fleet.export_fleet_diagnostics(str(output_path))
        
        logger.info(f"Data exported successfully to {output_path}")
        logger.info(f"File size: {output_path.stat().st_size} bytes")
        
        return 0
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return 1
        
    finally:
        fleet.disconnect_fleet()
        logger.info("Disconnected from fleet")


if __name__ == "__main__":
    sys.exit(main())
