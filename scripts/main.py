#!/usr/bin/env python3
"""
Main script to update and filter awesome lists data.
This script orchestrates the complete workflow:
1. Clone/update awesome lists repositories
2. Extract data from the repositories with URL filtering
3. Update metadata
"""

import os
import argparse
import logging
import sys
from pathlib import Path
import time

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the update script
from scripts.update_awesome_lists import (
    clone_or_update_repo, 
    update_metadata, 
    run_command, 
    AWESOME_REPOS
)

# Configure logging
logging.basicConfig(
    filename='logs/main.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log'),
        logging.StreamHandler()  # Also log to console
    ]
)

def main():
    parser = argparse.ArgumentParser(description='Update and filter awesome lists data')
    parser.add_argument('--source-dir', default='awesome-lists-sources', help='Directory to store repositories')
    parser.add_argument('--output-dir', default='data', help='Directory for output files')
    parser.add_argument('--skip-update', action='store_true', help='Skip repository updates')
    args = parser.parse_args()
    
    # Ensure logs and data directories exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)
    
    start_time = time.time()
    logging.info("Starting awesome lists main process")
    
    try:
        source_dir = Path(args.source_dir)
        output_dir = Path(args.output_dir)
        
        # Step 1: Clone or update repositories (unless skipped)
        if not args.skip_update:
            logging.info("Updating repositories...")
            os.makedirs(source_dir, exist_ok=True)
            
            for repo_url in AWESOME_REPOS:
                clone_or_update_repo(repo_url, source_dir)
        else:
            logging.info("Skipping repository updates as requested")
        
        # Step 2: Extract and filter data
        extract_script = Path("scripts/extract_data.py")
        if extract_script.exists():
            logging.info("Running extraction with URL filtering...")
            output_path = output_dir / "awesome-lists.json"
            
            result = run_command(
                f"python {extract_script} --source-dir {source_dir} --output {output_path} --filter-urls --url-stats"
            )
            
            if not result:
                logging.error("Extraction failed. Check logs for details.")
                return 1
            
            # Step 3: Update metadata
            update_metadata(output_dir)
        else:
            logging.error(f"Extraction script not found: {extract_script}")
            return 1
        
        elapsed_time = time.time() - start_time
        logging.info(f"Main process completed successfully in {elapsed_time:.2f} seconds")
        print(f"\nProcess completed successfully in {elapsed_time:.2f} seconds")
        print(f"Data saved to {output_dir}/awesome-lists.json")
        print(f"Metadata updated at {output_dir}/metadata.json")
        
        return 0
        
    except Exception as e:
        logging.error(f"Error in main process: {e}", exc_info=True)
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
