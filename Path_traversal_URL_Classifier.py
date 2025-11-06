from urllib.parse import urlparse, parse_qsl, unquote

INPUT_FILE = "urls.txt"
OUTPUT_FILE = "traversal_candidates.txt"


PATTERNS = ["../", "..\\", "%2e%2e", "%2f", "%5c"]

def looks_like_traversal(value: str) -> bool:
    v = unquote(value.lower())
    return any(p in v for p in PATTERNS)

def main():
    try:
        urls = [line.strip() for line in open(INPUT_FILE, "r", encoding="utf-8") if line.strip()]
    except FileNotFoundError:
        print(f"[!] '{INPUT_FILE}' not found.")
        return

    candidates = []
    for url in urls:
        parsed = urlparse(url)
        query = parse_qsl(parsed.query, keep_blank_values=True)

        
        if any(looks_like_traversal(v) for _, v in query) or looks_like_traversal(parsed.path):
            candidates.append(url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(candidates))

    print(f"[+] Found {len(candidates)} potential path traversal URLs.")
    print(f"[+] Saved to '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
