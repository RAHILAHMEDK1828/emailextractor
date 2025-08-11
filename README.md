## emailextractor
Extract emails from a domain one level deep.

## Installation
```
git clone https://github.com/rix4uni/emailextractor.git
cd emailextractor
pip3 install -r requirements.txt
python3 emailextractor.py -h
```

## Usage
```
usage: emailextractor.py [-h] [-c CONCURRENT] [-t TIMEOUT] [-v]

Extract emails from a domain one level deep.

options:
  -h, --help            show this help message and exit
  -c CONCURRENT, --concurrent CONCURRENT
                        Number of concurrent URL fetches (default: 30)
  -t TIMEOUT, --timeout TIMEOUT
                        Request timeout in seconds (default: 10)
  -v, --verbose         Show processing details
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
cat domains.txt | python3 emailextractor.py -c 50 -t 5 -v
```