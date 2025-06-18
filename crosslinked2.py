
#!/usr/bin/env python3
# Email Finder Tool


import re
import argparse
import time
import csv
from googlesearch import search

# --- Argument Parser ---
parser = argparse.ArgumentParser(
    description="Google Dork-based Email Finder Tool"
)
parser.add_argument("--company", required=True,
    help="Company name to search for (e.g., Navarino)"
)
parser.add_argument("--domain", required=True,
    help="Email domain to use for permutations (e.g., navarino.com)"
)
parser.add_argument("--pattern", required=True, nargs='+',
    help=(
        "Email pattern(s). Use placeholders: {first}, {last}, {f}, {domain}.\n"
        "E.g., {first}.{last}@{domain} {f}{last}@{domain}"
    )
)
parser.add_argument("--results", type=int, default=50,
    help="Total Google results to fetch (default: 50)"
)
parser.add_argument("--sleep", type=float, default=5,
    help="Sleep interval between paged requests (default: 5s)"
)
parser.add_argument("--proxy",
    help="Optional HTTP proxy URL (e.g., http://user:pass@host:port)"
)
parser.add_argument("--csv",
    help="Output generated emails to CSV file"
)
parser.add_argument("-v", "--verbose", action="store_true",
    help="Enable verbose output"
)
args = parser.parse_args()

# --- Helper Functions ---
def extract_name_from_linkedin_url(url):
    """
    Extract first and last name from a LinkedIn profile URL.
    Returns tuple (first, last) or (None, None).
    """
    match = re.search(r"linkedin\.com/in/([a-zA-Z0-9\-]+)", url)
    if not match:
        return None, None
    parts = [p for p in match.group(1).split('-') if p.isalpha()]
    if len(parts) >= 2:
        return parts[0].capitalize(), parts[1].capitalize()
    if len(parts) == 1:
        return parts[0].capitalize(), ''
    return None, None


def generate_emails(first, last, domain, patterns):
    """
    Generate a set of email permutations given the name and patterns.
    """
    f = first[0].lower() if first else ''
    first_lower = first.lower() if first else ''
    last_lower = last.lower() if last else ''
    emails = set()
    for pat in patterns:
        try:
            emails.add(pat.format(first=first_lower, last=last_lower, f=f, domain=domain))
        except KeyError:
            continue
    return emails


def find_profiles(company, total, sleep_interval, verbose=False, proxy=None):
    """
    Use googlesearch to fetch all results in one call, leveraging its internal paging.
    """
    query = f'site:linkedin.com/in "{company}"'
    profiles = []
    seen = set()

    # Single call: library handles pagination for num_results > 100
    results = search(
        query,
        num_results=total,
        advanced=True,
        sleep_interval=sleep_interval,
        proxy=proxy,
        ssl_verify=False,
        unique=True
    )
    for item in results:
        url = getattr(item, 'url', item)
        if 'linkedin.com/in/' in url and url not in seen:
            seen.add(url)
            profiles.append(url)
            if verbose:
                print(f"[+] Found: {url}")

    return profiles


def main():
    profiles = find_profiles(
        args.company,
        args.results,
        args.sleep,
        verbose=args.verbose,
        proxy=args.proxy
    )

    all_emails = set()
    for url in profiles:
        first, last = extract_name_from_linkedin_url(url)
        if first:
            all_emails.update(generate_emails(first, last, args.domain, args.pattern))
        elif args.verbose:
            print(f"[-] Could not parse name from {url}")

    # Output
    if not args.verbose:
        print(f"\n[+] {len(all_emails)} email(s) generated.")
    else:
        for e in sorted(all_emails):
            print(e)

    if args.csv:
        with open(args.csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Email'])
            for e in sorted(all_emails):
                writer.writerow([e])
        print(f"[+] Results saved to {args.csv}")

if __name__ == "__main__":
    main()
