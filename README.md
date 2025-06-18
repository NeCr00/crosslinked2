# crosslinked2

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
  --company "Navarino" \
  --domain navarino.com \
  --pattern "{first}.{last}@{domain}" "{f}{last}@{domain}" \
  --results 100 \
  --sleep 5 \
  [--proxy http://user:pass@host:port] \
  [--csv emails.csv] \
  [--verbose]
```

### Required Arguments

* `--company` \<string>: Target company name (e.g., `Navarino`).
* `--domain` \<string>: Email domain for permutations (e.g., `navarino.com`).
* `--pattern` \<patterns>: One or more email patterns. Use placeholders `{first}`, `{last}`, `{f}`, `{domain}`.

### Optional Arguments

* `--results` \<int>: Total number of Google results to fetch (default: 50).
* `--sleep` \<float>: Seconds to wait between paged requests (default: 20).
* `--proxy` \<URL>: HTTP(S) proxy URL.
* `--csv` \<file>: Path to CSV file for saving emails.
* `--verbose` : Enable detailed output.


## Examples

1. **Basic run**

   ```bash
   ./crosslinked2.py --company "ExampleCorp" --domain example.com --pattern "{first}@{domain}" --results 30
   ```

2. **Multiple patterns + CSV export**

   ```bash
   ./crosslinked2.py \
     --company "Acme Inc" \
     --domain acme.com \
     --pattern "{first}.{last}@{domain}" "{f}{last}@{domain}" \
     --results 100 \
     --sleep 4 \
     --csv output/emails.csv \
     --verbose
   ```



Use this tool responsibly and only against targets for which you have explicit permission. Unauthorized scraping of Google or LinkedIn profiles may violate their terms of service.
