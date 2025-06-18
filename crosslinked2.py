#!/usr/bin/env python3
# crosslinked2: CLI email finder via Google Dorks (always verbose)

import re
import argparse
import csv
from googlesearch import search

# --- Argument Parser ---
parser = argparse.ArgumentParser(
    description="Discover LinkedIn profiles and generate email addresses"
)
parser.add_argument("-c", "--company", required=True,
    help="Target company name (e.g., Navarino)"
)
parser.add_argument("-d", "--domain", required=True,
    help="Email domain for permutations (e.g., navarino.com)"
)
parser.add_argument("-p", "--pattern", nargs='+',
    help=(
        "Email pattern(s) with {first},{last},{f},{domain}.\n"
        "E.g.: {first}.{last}@{domain} {f}{last}@{domain}."
    )
)
parser.add_argument("-n", "--num", type=int, default=50,
    help="Number of Google results to fetch (default: 50)"
)
parser.add_argument("-s", "--sleep", type=float, default=5,
    help="Sleep between paged requests in seconds (default: 5)"
)
parser.add_argument("-x", "--proxy",
    help="HTTP(S) proxy URL (e.g., http://user:pass@host:port)"
)
parser.add_argument("-o", "--out",
    help="Path to CSV file to save emails"
)
args = parser.parse_args()

# --- Helper Functions ---
def extract_name(url):
    m = re.search(r"linkedin\.com/in/([A-Za-z0-9\-]+)", url)
    if not m:
        return None, None
    parts = [p for p in m.group(1).split('-') if p.isalpha()]
    if len(parts) >= 2:
        return parts[0].lower(), parts[1].lower()
    if len(parts) == 1:
        return parts[0].lower(), ''
    return None, None


def generate_emails(first, last, domain, patterns):
    if not first:
        return set()
    # single-part: always first@domain
    if not last:
        return {f"{first}@{domain}"}
    f0 = first[0]
    emails = set()
    for pat in patterns:
        try:
            emails.add(pat.format(first=first, last=last, f=f0, domain=domain))
        except Exception:
            pass
    return emails

# --- Fetch and display profiles ---
print(f"Fetching LinkedIn profiles for '{args.company}'...")
results = search(
    f'site:linkedin.com/in "{args.company}"',
    num_results=args.num,
    advanced=True,
    sleep_interval=args.sleep,
    proxy=args.proxy,
    ssl_verify=False,
    unique=True
)
seen = set()
profiles = []
print("Found URLs:")
for item in results:
    url = getattr(item, 'url', item)
    if 'linkedin.com/in/' in url and url not in seen:
        seen.add(url)
        profiles.append(url)
        print(f"  {url}")

# --- Generate and display emails ---
def_patterns = args.pattern or []
if not def_patterns:
    def_patterns = ["{first}@{domain}"]

print("\nGenerating emails from profiles...")
all_emails = set()
for url in profiles:
    first, last = extract_name(url)
    all_emails |= generate_emails(first, last, args.domain, def_patterns)

print(f"\nTotal emails generated: {len(all_emails)}")
for e in sorted(all_emails):
    print(e)

# --- CSV export ---
if args.out:
    with open(args.out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['email'])
        for e in sorted(all_emails):
            writer.writerow([e])
    print(f"\nSaved emails to {args.out}")
