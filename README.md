# CrossLinked2

**crosslinked2** is a command-line utility that automates the discovery of employee email addresses by:

1. Performing Google Dork searches for LinkedIn profiles of a target company.
2. Extracting first and last names from the profile URLs.
3. Generating common email permutations based on user-defined patterns.

This tool mimics the behavior of the original **crosslinked** but is actively maintained and compatible with the latest `googlesearch-python` library.


## Features

* **Google Dork-based Recon**: Leverage `site:linkedin.com/in` searches to find public LinkedIn profiles.
* **Internal Pagination**: Requests large result sets in one call, using `sleep_interval` to respect rate limits.
* **Flexible Email Patterns**: Define any pattern using placeholders:

  * `{first}`: full first name (lowercase)
  * `{last}`: full last name (lowercase)
  * `{f}`: first initial (lowercase)
  * `{domain}`: target email domain
* **Proxy Support**: Route traffic through an HTTP(S) proxy.
* **CSV Export**: Save generated email list to a file.
* **Verbose Mode**: Print detailed progress and parsed URLs.


## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your_org>/crosslinked2.git
   cd crosslinked2
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```


## Usage

```bash
./crosslinked2.py \
  -c <Company_Name> \
  -d company.com \
  -p "{first}.{last}@{domain}" "{f}{last}@{domain}" \
  -r 100 \
  -sleep 20 \
  [-x http://user:pass@host:port] \
  [-o emails.csv] \
  
```

### Required Arguments

* `-c | --company` \<string>: Target company name (e.g., `Navarino`).
* `-d | --domain` \<string>: Email domain for permutations (e.g., `navarino.com`).
* `-p | --pattern` \<patterns>: One or more email patterns. Use placeholders `{first}`, `{last}`, `{f}`, `{domain}`.

### Optional Arguments

* `-r | --results` \<int>: Total number of Google results to fetch (default: 50).
* `-s | --sleep` \<float>: Seconds to wait between paged requests (default: 20).
* `-x | --proxy` \<URL>: HTTP(S) proxy URL.
* `-o | --out` \<file>: Path to CSV file for saving emails.


## Examples

1. **Basic run**

   ```bash
   ./crosslinked2.py  --company Company --domain company.com --pattern {f}{last}@{domain} -o test.csv -r 100 -s 30
   ```

2. **Multiple patterns + CSV export**

   ```bash
   ./crosslinked2.py \
     --company "Acme Inc" \
     --domain acme.com \
     --pattern "{first}.{last}@{domain}" "{f}{last}@{domain}" \
     --results 100 \
     --sleep 30 \
     --out output/emails.csv
   ```



Use this tool responsibly and only against targets for which you have explicit permission. Unauthorized scraping of Google or LinkedIn profiles may violate their terms of service.
