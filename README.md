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
  -n 100 \
  -sleep 20 \
  [-x http://user:pass@host:port] \
  [-o emails.csv] \
  
```

### Required Arguments

* `-c | --company` \<string>: Target company name (e.g., `Navarino`).
* `-d | --domain` \<string>: Email domain for permutations (e.g., `navarino.com`).
* `-p | --pattern` \<patterns>: One or more email patterns. Use placeholders `{first}`, `{last}`, `{f}`, `{domain}`.

### Optional Arguments

* `-n | --num` \<int>: Total number of Google results to fetch (default: 50).
* `-s | --sleep` \<float>: Seconds to wait between paged requests (default: 20).
* `-x | --proxy` \<URL>: HTTP(S) proxy URL.
* `-o | --out` \<file>: Path to CSV file for saving emails.


## Examples

 **Basic run**
   ```bash
   python3 crosslinked2.py  --company Tesla --domain tesla.com --pattern {f}{last}@{domain}

   https://www.linkedin.com/in/roshant
   https://www.linkedin.com/in/westbrookmorrill
   https://www.linkedin.com/in/marcusroffey
   https://www.linkedin.com/in/jaimej1
   https://gr.linkedin.com/in/konstantinos-xanthopoulos-067a35140
   https://gr.linkedin.com/in/bourchas
   https://gr.linkedin.com/in/tesla-model-520280145
   https://www.linkedin.com/in/timothyer
   https://www.linkedin.com/in/eddie914
   https://www.linkedin.com/in/matt-reddick-4a913411
   https://gr.linkedin.com/in/konstantinos-deligiannis-9859b6202
   https://gr.linkedin.com/in/stathis-laios-059a831a
   https://www.linkedin.com/in/colinbreck
   https://www.linkedin.com/in/nageshsaldi
   https://www.linkedin.com/in/javier-verdura-4689521
   https://www.linkedin.com/in/troyjones2
   https://www.linkedin.com/in/konstantinos-gklantzounis
   [snip]
   https://gr.linkedin.com/in/maria-chamilaki
   https://www.linkedin.com/in/eashokkumar
   https://www.linkedin.com/in/kiranrak
   https://gr.linkedin.com/in/giorgos-panagiotidis-287b94133
 
   Generating emails from profiles...
   
   Total emails generated: 46
   alexguion@tesla.com
   asahota@tesla.com
   astewart@tesla.com
   bonneeggleston@tesla.com
   bourchas@tesla.com
   carlmoren@tesla.com
   cemerino@tesla.com
   colinbreck@tesla.com
   dhavalshroff@tesla.com
   dpriestley@tesla.com
   [snip]
   dtalkington@tesla.com
   dylankim@tesla.com
   eashokkumar@tesla.com
   elafargue@tesla.com
   elihammer@tesla.com
```
Use this tool responsibly and only against targets for which you have explicit permission. Unauthorized scraping of Google or LinkedIn profiles may violate their terms of service.
