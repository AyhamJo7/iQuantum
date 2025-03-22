#!/usr/bin/env python3
import os
import re
import json
import logging
import argparse
from pathlib import Path
from urllib.parse import urlparse
import markdown   # type: ignore
from bs4 import BeautifulSoup  # type: ignore # Requires: pip install beautifulsoup4

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure logging to record debug info to a log file.
logging.basicConfig(
    filename='logs/extraction.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Common headings to ignore as categories.
IGNORED_CATEGORIES = set(['contents', 'contributing', 'license'])

def extract_resources_from_ul(ul):
    """Extracts resource objects from a <ul> element."""
    resources = []
    # Only process direct <li> children to avoid nested list issues.
    for li in ul.find_all('li', recursive=False):
        a_tag = li.find('a')
        if a_tag:
            name = a_tag.get_text().strip()
            url = a_tag.get('href', '').strip()
            # Extract the full text of the list item and remove the link text.
            full_text = li.get_text(separator=' ', strip=True)
            description = full_text.replace(name, '', 1).strip(' -')
            tags = re.findall(r'`(.*?)`', description)
            resources.append({
                'name': name,
                'url': url,
                'description': description,
                'tags': tags
            })
        else:
            logging.warning("List item without a link: %s", li)
    return resources

def parse_table(table):
    """Parses a <table> element to extract resource data."""
    resources = []
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        if not cells:
            continue
        # Heuristic: look for the first cell containing a link.
        name, url, description = None, None, ''
        for cell in cells:
            a_tag = cell.find('a')
            if a_tag and not name:
                name = a_tag.get_text().strip()
                url = a_tag.get('href', '').strip()
            else:
                description += ' ' + cell.get_text(separator=' ', strip=True)
        if name:
            tags = re.findall(r'`(.*?)`', description)
            resources.append({
                'name': name,
                'url': url,
                'description': description.strip(' -'),
                'tags': tags
            })
    return resources

def parse_awesome_list(readme_path, list_name):
    """
    Parses a README.md file from an awesome list repository and extracts structured data.
    Supports headers with bullet lists, tables, and a fallback to list items.
    """
    logging.info("Parsing file: %s", readme_path)
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logging.error("Error reading %s: %s", readme_path, e)
        raise

    # Convert markdown to HTML.
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, 'html.parser')

    categories = []
    header_tags = soup.find_all(['h2', 'h3'])
    if header_tags:
        # Process sections defined by headers.
        for header in header_tags:
            cat_name = header.get_text().strip()
            if cat_name.lower() in IGNORED_CATEGORIES:
                continue

            category_resources = []
            sibling = header.find_next_sibling()
            # Continue until the next header is encountered.
            while sibling and sibling.name not in ['h1', 'h2', 'h3']:
                if sibling.name == 'ul':
                    category_resources.extend(extract_resources_from_ul(sibling))
                sibling = sibling.find_next_sibling()
            categories.append({
                'name': cat_name,
                'resources': category_resources
            })
    else:
        # No headers found; check for table structures.
        tables = soup.find_all('table')
        if tables:
            for table in tables:
                resources = parse_table(table)
                if resources:
                    categories.append({
                        'name': 'Resources',
                        'resources': resources
                    })
        else:
            # Fallback: extract all list items in the document.
            lis = soup.find_all('li')
            # Wrap them in a dummy <ul> to reuse our extraction logic.
            dummy_ul = BeautifulSoup('<ul>' + ''.join(str(li) for li in lis) + '</ul>', 'html.parser').find('ul')
            resources = extract_resources_from_ul(dummy_ul)
            if resources:
                categories.append({
                    'name': 'Resources',
                    'resources': resources
                })

    return {
        'name': list_name,
        'categories': categories
    }

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

def main():
    parser = argparse.ArgumentParser(description='Extract data from awesome lists')
    parser.add_argument('--output', default='data/awesome-lists.json', help='Output JSON file path')
    parser.add_argument('--source-dir', default='awesome-lists-sources', help='Directory containing awesome list repositories')
    parser.add_argument('--filter-urls', action='store_true', help='Filter out resources with invalid URLs')
    parser.add_argument('--url-stats', action='store_true', help='Show statistics about valid/invalid URLs')
    args = parser.parse_args()

    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    base_dir = Path(args.source_dir)
    # Look for directories that start with "awesome-"
    awesome_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('awesome-')]
    all_lists = []
    
    # For URL stats
    total_resources = 0
    valid_urls = 0
    invalid_urls = 0

    for awesome_dir in awesome_dirs:
        readme_path = awesome_dir / 'README.md'
        if readme_path.exists():
            list_name = awesome_dir.name.replace('-', ' ').title()
            logging.info("Processing %s", list_name)
            try:
                parsed_data = parse_awesome_list(readme_path, list_name)
                
                # Filter out resources with invalid URLs if requested
                if args.filter_urls:
                    filtered_categories = []
                    for category in parsed_data['categories']:
                        valid_resources = []
                        for resource in category['resources']:
                            total_resources += 1
                            url = resource.get('url', '')
                            
                            if is_valid_url(url):
                                valid_resources.append(resource)
                                valid_urls += 1
                            else:
                                invalid_urls += 1
                                logging.info(f"Filtering out resource '{resource['name']}' with invalid URL: '{url}'")
                        
                        if valid_resources:
                            filtered_category = category.copy()
                            filtered_category['resources'] = valid_resources
                            filtered_categories.append(filtered_category)
                    
                    if filtered_categories:
                        filtered_data = parsed_data.copy()
                        filtered_data['categories'] = filtered_categories
                        all_lists.append(filtered_data)
                else:
                    all_lists.append(parsed_data)
                    
                    # Count valid/invalid URLs if stats requested
                    if args.url_stats:
                        for category in parsed_data['categories']:
                            for resource in category['resources']:
                                total_resources += 1
                                url = resource.get('url', '')
                                if is_valid_url(url):
                                    valid_urls += 1
                                else:
                                    invalid_urls += 1
                
                list_resources = sum(len(cat['resources']) for cat in parsed_data['categories'])
                logging.info(f"Found {list_resources} resources in {len(parsed_data['categories'])} categories")
            except Exception as e:
                logging.error(f"Error processing {list_name}: {e}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(all_lists, f, indent=2)
    
    logging.info(f"Processed {len(all_lists)} awesome lists; data saved to {args.output}")
    
    # Print URL statistics if requested
    if args.url_stats or args.filter_urls:
        print("\nURL Statistics:")
        print(f"Total resources: {total_resources}")
        print(f"Valid URLs: {valid_urls} ({valid_urls/max(total_resources, 1)*100:.1f}%)")
        print(f"Invalid URLs: {invalid_urls} ({invalid_urls/max(total_resources, 1)*100:.1f}%)")
        
        if args.filter_urls:
            print(f"\nFiltered data saved to {args.output}")
            print(f"Removed {invalid_urls} resources with invalid URLs")

if __name__ == '__main__':
    main()
