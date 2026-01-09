# http-header-analyzer
Simple Python tool to analyze web connections: TLS encryption, response headers, and page info.

## What it does

- Shows TLS protocol and cipher suite
- Displays all HTTP response headers
- Extracts page title
- Measures response time
- Uses Firefox headers to mimic real browser

## Installation

```bash
git clone https://github.com/majerity/http-header-analyzer
cd http-header-analyzer
pip install -r requirements.txt
```
## Usage

```bash
# With URL argument
python analyzer.py https://example.com

# Without argument (will ask for URL)
python analyzer.py
```
## Why use this?

- **Debug** API endpoints and web servers
- **Check** TLS security and encryption
- **Inspect** response headers (CORS, security headers, etc.)
- **Test** connection speed and availability
- **Prepare** for web scraping by seeing real header
