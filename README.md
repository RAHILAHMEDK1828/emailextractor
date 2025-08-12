## emailextractor
Extract emails from websites.

## Installation
```
git clone https://github.com/rix4uni/emailextractor.git
cd emailextractor
python3 setup.py install
```

## Usage
```
usage: emailextractor [-h] [-c CONCURRENT] [-t TIMEOUT] [--silent] [--verbose] [--version]

Extract emails from websites

options:
  -h, --help            show this help message and exit
  -c CONCURRENT, --concurrent CONCURRENT
                        Number of concurrent requests
  -t TIMEOUT, --timeout TIMEOUT
                        Request timeout in seconds
  --silent              Run without printing the banner
  --verbose             Enable verbose output
  --version             Show current version of emailextractor
```

## Usage Examples
**Single domain:**
```
echo "http://testphp.vulnweb.com" | python3 emailextractor.py
```

**Multiple domains:**
```
cat domains.txt | python3 emailextractor.py
```

**domains.txt example:**
```
http://testphp.vulnweb.com
https://subdomain.test.org
```

**Multiple domains with concurrency & timeout**
```
cat domains.txt | python3 emailextractor.py -c 50 -t 5 --verbose
```