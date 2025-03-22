#!/usr/bin/env python3
import os
import json
import logging
import argparse
from urllib.parse import urlparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename='logs/url_filtering.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def is_valid_url(url):
    """
    Check if a URL is valid.
    A valid URL must have both a scheme (http, https) and a netloc (domain).
    """
    try:
        if not url or not isinstance(url, str):
            return False
        
        # Parse the URL
        result = urlparse(url)
        
        # Check if URL has scheme (http, https) and netloc (domain)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception as e:
        logging.error(f"Error validating URL '{url}': {e}")
        return False

def filter_invalid_resources(data):
    """
    Filter out resources that don't have valid URLs from the awesome lists data.
    Returns the filtered data and statistics about the filtering.
    """
    total_resources = 0
    removed_resources = 0
    filtered_lists = []
    
    # Process each awesome list
    for awesome_list in data:
        filtered_categories = []
        
        # Process each category in the list
        for category in awesome_list.get('categories', []):
            valid_resources = []
            
            # Check each resource for a valid URL
            for resource in category.get('resources', []):
                total_resources += 1
                url = resource.get('url', '')
                
                if is_valid_url(url):
                    valid_resources.append(resource)
                else:
                    removed_resources += 1
                    logging.info(f"Removing resource '{resource.get('name', 'Unknown')}' with invalid URL: '{url}'")
            
            # Only keep categories that still have resources
            if valid_resources:
                filtered_category = category.copy()
                filtered_category['resources'] = valid_resources
                filtered_categories.append(filtered_category)
        
        # Only keep lists that still have categories
        if filtered_categories:
            filtered_list = awesome_list.copy()
            filtered_list['categories'] = filtered_categories
            filtered_lists.append(filtered_list)
    
    stats = {
        'total_resources': total_resources,
        'removed_resources': removed_resources,
        'percentage_removed': round(removed_resources / max(total_resources, 1) * 100, 2)
    }
    
    return filtered_lists, stats

def main():
    parser = argparse.ArgumentParser(description='Filter resources with invalid URLs from awesome lists data')
    parser.add_argument('--input', default='data/awesome-lists.json', help='Input JSON file path')
    parser.add_argument('--output', default='data/filtered-awesome-lists.json', help='Output filtered JSON file path')
    parser.add_argument('--backup', action='store_true', help='Create a backup of the original file before replacing it')
    parser.add_argument('--replace', action='store_true', help='Replace the original file with the filtered version')
    args = parser.parse_args()
    
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    input_path = args.input
    output_path = args.output if not args.replace else args.input
    
    # Load the awesome lists data
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logging.info(f"Loaded data from {input_path}")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        print(f"Error: Failed to load data from {input_path}: {e}")
        return
    
    # Create a backup if requested
    if args.backup or args.replace:
        backup_path = f"{input_path}.backup"
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logging.info(f"Backup created at {backup_path}")
            print(f"Backup created at {backup_path}")
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            print(f"Warning: Failed to create backup: {e}")
    
    # Filter the data
    filtered_data, stats = filter_invalid_resources(data)
    
    # Save the filtered data
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2)
        logging.info(f"Filtered data saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving filtered data: {e}")
        print(f"Error: Failed to save filtered data to {output_path}: {e}")
        return
    
    # Print statistics
    print(f"\nURL Filtering Complete:")
    print(f"Total resources processed: {stats['total_resources']}")
    print(f"Resources removed: {stats['removed_resources']} ({stats['percentage_removed']}%)")
    print(f"Filtered data saved to: {output_path}")
    
    if args.replace:
        print(f"Original file has been replaced with filtered data.")
    
    logging.info(f"Filtering complete. Removed {stats['removed_resources']} of {stats['total_resources']} resources.")

if __name__ == "__main__":
    main()
