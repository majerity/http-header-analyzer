import sys
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl
import socket
FIREFOX_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

def get_tls_info(hostname, port=443):
    try:
        context = ssl.create_default_context()
        
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cipher = ssock.cipher()
                version = ssock.version()
                
                return {
                    'protocol': version,
                    'cipher': cipher[0] if cipher else 'Unknown',
                    'cipher_bits': cipher[2] if cipher and len(cipher) > 2 else 'Unknown'
                }
    except Exception as e:
        return {
            'error': str(e),
            'protocol': 'N/A',
            'cipher': 'N/A'
        }


def extract_title(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            if title_text:
                return title_text
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title.get('content').strip()
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title and twitter_title.get('content'):
            return twitter_title.get('content').strip()
        h1 = soup.find('h1')
        if h1:
            h1_text = h1.get_text().strip()
            if h1_text:
                return f"{h1_text} (from h1)"
        
        return "No title found"
    except Exception as e:
        return f"Error extracting title: {str(e)}"


def analyze_url(url):
    """Main function to analyze URL"""
    
    print(f"\n[#] Analyzing: {url}\n")
    parsed = urlparse(url)
    hostname = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    if parsed.scheme == 'https':
        print("[#] TLS INFORMATION")
        tls_info = get_tls_info(hostname, port)
        
        if 'error' in tls_info:
            print(f"    TLS Error: {tls_info['error']}")
        else:
            print(f"    Protocol: {tls_info['protocol']}")
            print(f"    Cipher: {tls_info['cipher']}")
            if tls_info.get('cipher_bits') != 'Unknown':
                print(f"    Cipher Strength: {tls_info['cipher_bits']} bits")
        print()
    try:
        response = requests.get(
            url,
            headers=FIREFOX_HEADERS,
            timeout=10,
            allow_redirects=True
        )
        print(f"[#] Status Code: {response.status_code}")
        print(f"[#] Response Time: {response.elapsed.total_seconds():.3f}s")
        print()
        print("[#] RESPONSE HEADERS")
        for header, value in response.headers.items():
            print(f"    {header}: {value}")
        print()
        print("[#] PAGE TITLE")
        title = extract_title(response.text)
        print(f"    {title}")
        print()
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}\n")
        return False


def main():
    if len(sys.argv) < 2:
        try:
            url = input("Enter URL to analyze: ").strip()
            if not url:
                print("Error: URL cannot be empty")
                sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled")
            sys.exit(1)
    else:
        url = sys.argv[1]
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    success = analyze_url(url)
    sys.exit(0 if success else 1)
if __name__ == "__main__":
    main()