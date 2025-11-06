import re
import sys
from urllib.parse import urlparse
import requests

PATTERNS = [
    r"https?://[^\s'\"\\]+",            
    r"/[a-zA-Z0-9._/-]*\.(php|jsp|asp)",
    r"/api/[^\s'\"\\]+",                
    r"/v\d+[^\s'\"\\]*",                
    r"[a-zA-Z0-9_/.-]+\.php[^\s'\"\\]*" 
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in PATTERNS]

def fetch_text(source):
    if urlparse(source).scheme in ("http", "https"):
        r = requests.get(source, timeout=10)
        r.raise_for_status()
        return r.text
    else:
        with open(source, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def extract_endpoints(text):
    found = set()
    for rx in COMPILED:
        for m in rx.findall(text):
            found.add(m.strip().strip("'\""))
    return sorted(found)

def main():
    if len(sys.argv) != 2:
        print("Usage: python js_endpoint_extractor_simple.py <js_file_or_url>")
        return
    src = sys.argv[1]
    try:
        txt = fetch_text(src)
    except Exception as e:
        print(f"Error reading {src}: {e}")
        return

    endpoints = extract_endpoints(txt)
    if not endpoints:
        print("No endpoints found.")
        return

    print("Found endpoints:")
    for e in endpoints:
        print(" -", e)

    with open("endpoints.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(endpoints))
    print("\nSaved endpoints to endpoints.txt")

if __name__ == "__main__":
    main()
