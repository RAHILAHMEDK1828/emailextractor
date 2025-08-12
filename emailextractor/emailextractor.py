#!/usr/bin/env python3
import sys
import re
import argparse
import requests
import os
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the version
__version__ = "v0.0.1"  # Current Version of pyxss

# ANSI color codes
REDCOLOR = '\033[91m'
GREENCOLOR = '\033[92m'
CYANCOLOR = '\033[96m'
RESETCOLOR = '\033[0m'

# Colorful banner
BANNER = rf"""{CYANCOLOR}
                           _  __             __                      __              
  ___   ____ ___   ____ _ (_)/ /___   _  __ / /_ _____ ____ _ _____ / /_ ____   _____
 / _ \ / __ `__ \ / __ `// // // _ \ | |/_// __// ___// __ `// ___// __// __ \ / ___/
/  __// / / / / // /_/ // // //  __/_>  < / /_ / /   / /_/ // /__ / /_ / /_/ // /    
\___//_/ /_/ /_/ \__,_//_//_/ \___//_/|_| \__//_/    \__,_/ \___/ \__/ \____//_/
                                                                        {__version__}
{RESETCOLOR}"""


exclude_patterns = ('.jpg', '.png', '.gif', '.webp', '.ico', '.mp4', '.pdf', '.eot', '.doc', '.docx', '.xls', '.xlsx', '.woff', '.woff2', '.css', '.json', '.xml', '.rss', '.svg', '.yaml', '.yml', '.csv', '.dockerfile', '.cfg', '.lock', '.js', '.md', '.toml')

def extract_emails_and_links(target_url, base_url, timeout, verbose):
    """Fetch a page and return emails + internal links"""
    if verbose:
        print(f"[PROCESSING] {target_url}")
    try:
        response = requests.get(target_url, timeout=timeout)
        html = response.text
    except Exception as e:
        if verbose:
            print(f"[ERROR] Could not fetch {target_url} -> {e}")
        return set(), set()

    # Extract href values
    pattern = r'href=(["\'])(.*?)\1'
    links = [m[1] for m in re.findall(pattern, html)]

    page_emails = set()
    internal_links = set()

    for link in links:
        link_lower = link.lower()

        # Skip unwanted file types
        if any(ext in link_lower for ext in exclude_patterns):
            continue

        # Emails
        if link_lower.startswith("mailto:"):
            email = link[7:].strip()
            page_emails.add(email)
            continue

        # Internal links only
        try:
            absolute_link = urljoin(target_url, link)
        except ValueError:
            continue  # skip malformed URL

        if absolute_link.startswith(base_url):
            internal_links.add(absolute_link)


    return page_emails, internal_links


def process_domain(url, max_workers, timeout, verbose):
    """Process a single domain one level deep, concurrent sub-URL fetching"""
    # Create output directory if not exists
    os.makedirs("output", exist_ok=True)

    # Extract domain for output filename
    domain = re.sub(r'^https?://', '', url).rstrip('/')
    output_file = os.path.join("output", f"{domain}.txt")

    emails = set()

    # Step 1: Process main page
    main_emails, found_links = extract_emails_and_links(url, url, timeout, verbose)
    emails.update(main_emails)

    # Step 2: Process each found internal link (one level only, concurrent)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(extract_emails_and_links, link, url, timeout, verbose): link
            for link in found_links
        }
        for future in as_completed(future_to_url):
            sub_emails, _ = future.result()
            emails.update(sub_emails)

    # Save unique emails
    if emails:
        with open(output_file, "w", encoding="utf-8") as f:
            for email in sorted(emails):
                f.write(email + "\n")
        print(f"[SAVED] {len(emails)} unique email(s) -> {output_file}")
    else:
        print(f"[NO EMAILS] {url}")


def main():
    parser = argparse.ArgumentParser(description="Extract emails from websites")
    parser.add_argument("-c", "--concurrent", type=int, default=30, help="Number of concurrent requests")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument('--silent', action='store_true', help='Run without printing the banner')
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__, help='Show current version of emailextractor')
    args = parser.parse_args()

    if not args.silent:
        print(BANNER)

    for line in sys.stdin:
        domain_url = line.strip()
        if domain_url:
            process_domain(domain_url, args.concurrent, args.timeout, args.verbose)


if __name__ == "__main__":
    main()