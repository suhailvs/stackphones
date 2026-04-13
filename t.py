import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Missing dependencies. Run: pip install requests beautifulsoup4 lxml")

DEFAULT_OUTPUT_DIR = "scraped_pages"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_with_bs4(raw_html: bytes, encoding: str) -> str:
    for parser in ("lxml", "html.parser"):
        try:
            soup = BeautifulSoup(raw_html, parser, from_encoding=encoding)
            title = soup.find("title")
            if title:
                print(f"  📄 Title  : {title.get_text(strip=True)}")
            return soup.prettify()   # nicely indented HTML
        except Exception as e:
            print(f"  ⚠ Parser '{parser}' failed: {e}. Trying next …")
    return raw_html.decode(encoding, errors="replace")


def scrape(url: str, output_path: str, session: requests.Session, retries: int = 3) -> bool:
    """Fetch URL, parse with BS4, and write to output_path. Returns True on success."""
    for attempt in range(1, retries + 1):
        try:
            print(f"  [{attempt}/{retries}] GET {url}")
            response = session.get(url, timeout=20)
            response.raise_for_status()

            encoding = response.apparent_encoding or response.encoding or "utf-8"

            # Parse and prettify via BeautifulSoup
            html_out = parse_with_bs4(response.content, encoding)

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_out)

            size_kb = len(response.content) / 1024
            print(f"  ✓ Saved → {output_path}  ({size_kb:.1f} KB, HTTP {response.status_code})")
            return True

        except requests.exceptions.HTTPError as e:
            print(f"  ✗ HTTP error: {e}")
            if response.status_code in (403, 404, 410):
                break  # no point retrying
            if response.status_code == 429:
                # Too Many Requests
                print('Too Many Requests')
                print(f"  ↻ Retrying in 1 hour ...")
                time.sleep(60*60*2) # sleep 2 hour
        except requests.exceptions.ConnectionError as e:
            print(f"  ✗ Connection error: {e}")
        except requests.exceptions.Timeout:
            print(f"  ✗ Request timed out")
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")

        if attempt < retries:
            wait = 2 ** attempt
            print(f"  ↻ Retrying in {wait:.1f}s ...")
            time.sleep(wait)

    return False


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    URL = "https://www.gsmarena.com/"
    END = 14_501 - 1
    START = 14_600 # 14_000
    
    session = requests.Session()
    session.headers.update(HEADERS)
    results = {"ok": 0, "fail": 0}
    for i in range(START,END,-1):
        print(f"\n[{i}/{END+1}]")
        out_path = os.path.join(DEFAULT_OUTPUT_DIR, f"{i}.html")
        if scrape(f"{URL}a-{i}.php", out_path, session, retries=5):
            results["ok"] += 1
        else:
            results["fail"] += 1
        time.sleep(20) # to prevent Too Many Requests 

    print(f"\n{'─' * 50}")
    print(f"Done.  ✓ {results['ok']} saved   ✗ {results['fail']} failed")


if __name__ == "__main__":
    main()
