#!/usr/bin/env python3
import os
import subprocess
import logging
import argparse
import json
from pathlib import Path
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='logs/update_awesome_lists.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# List of awesome repositories to clone/update
AWESOME_REPOS = [
    "https://github.com/vinta/awesome-python",
    "https://github.com/awesome-selfhosted/awesome-selfhosted",
    "https://github.com/avelino/awesome-go",
    "https://github.com/Hack-with-Github/Awesome-Hacking",
    "https://github.com/jaywcjlove/awesome-mac",
    "https://github.com/MunGell/awesome-for-beginners",
    "https://github.com/enaqx/awesome-react",
    "https://github.com/fffaraz/awesome-cpp",
    "https://github.com/binhnguyennus/awesome-scalability",
    "https://github.com/sindresorhus/awesome-nodejs",
    "https://github.com/Solido/awesome-flutter",
    "https://github.com/rust-unofficial/awesome-rust",
    "https://github.com/vsouza/awesome-ios",
    "https://github.com/dkhamsing/open-source-ios-apps",
    "https://github.com/brillout/awesome-react-components",
    "https://github.com/serhii-londar/open-source-mac-os-apps",
    "https://github.com/akullpp/awesome-java",
    "https://github.com/docker/awesome-compose",
    "https://github.com/alebcay/awesome-shell",
    "https://github.com/veggiemonk/awesome-docker",
    "https://github.com/ziadoz/awesome-php",
    "https://github.com/viatsko/awesome-vscode",
    "https://github.com/matteocrippa/awesome-swift"
]

def run_command(command, cwd=None):
    """Run a shell command and log the output"""
    try:
        logging.info(f"Running command: {command}")
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        logging.info(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        logging.error(f"Error output: {e.stderr}")
        return False

def clone_or_update_repo(repo_url, target_dir):
    """Clone a repository if it doesn't exist, or pull updates if it does"""
    repo_name = repo_url.split('/')[-1]
    repo_path = os.path.join(target_dir, repo_name)
    
    if os.path.exists(repo_path):
        logging.info(f"Updating repository: {repo_name}")
        return run_command("git pull", cwd=repo_path)
    else:
        logging.info(f"Cloning repository: {repo_url}")
        return run_command(f"git clone {repo_url}", cwd=target_dir)

def update_metadata(output_dir):
    """Update metadata file with timestamp information"""
    metadata_path = os.path.join(output_dir, "metadata.json")
    
    metadata = {
        "last_updated": datetime.now().isoformat(),
        "update_count": 1
    }
    
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                existing_metadata = json.load(f)
                metadata["update_count"] = existing_metadata.get("update_count", 0) + 1
        except Exception as e:
            logging.error(f"Error reading metadata: {e}")
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    logging.info(f"Updated metadata: {metadata}")

def main():
    parser = argparse.ArgumentParser(description='Update awesome lists data')
    parser.add_argument('--source-dir', default='awesome-lists-sources', help='Directory to store repositories')
    parser.add_argument('--output-dir', default='data', help='Directory for output files')
    args = parser.parse_args()
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    start_time = time.time()
    logging.info("Starting awesome lists update process")
    
    # Create directories if they don't exist
    source_dir = Path(args.source_dir)
    output_dir = Path(args.output_dir)
    
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Clone or update repositories
    for repo_url in AWESOME_REPOS:
        clone_or_update_repo(repo_url, source_dir)
    
    # Run the extraction script with URL filtering
    extract_script = Path("scripts/extract_data.py")
    if extract_script.exists():
        output_path = output_dir / "awesome-lists.json"
        # Add the --filter-urls flag to automatically filter out resources with invalid URLs
        run_command(f"python {extract_script} --source-dir {source_dir} --output {output_path} --filter-urls --url-stats")
    else:
        logging.error(f"Extraction script not found: {extract_script}")
    
    # Update metadata
    update_metadata(output_dir)
    
    elapsed_time = time.time() - start_time
    logging.info(f"Update process completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
