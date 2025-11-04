import requests

SECURITY_HEADERS = [
    "X-Frame-Options",
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy",
    "Expect-CT",
    "Cache-Control",
    "Pragma",
    "Access-Control-Allow-Origin"
]

def analyze_headers(url):
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching {url}: {e}")
        return

    print(f"\n Analyzing headers for: {url}")
    print(f"HTTP Status: {response.status_code}\n")

    headers = {k.lower(): v for k, v in response.headers.items()}

    for header in SECURITY_HEADERS:
        hname = header.lower()
        if hname not in headers:
            print(f"[MISSING] {header} ")
        else:
            value = headers[hname]
            print(f"[FOUND] {header}: {value}")

            
            if header == "X-Frame-Options" and not any(x in value.upper() for x in ["DENY", "SAMEORIGIN"]):
                print("Weak value! Should be 'DENY' or 'SAMEORIGIN'")
            if header == "Content-Security-Policy" and "unsafe-inline" in value.lower():
                print("Contains 'unsafe-inline' (risky for XSS)")
            if header == "Strict-Transport-Security" and "max-age" not in value:
                print("Missing 'max-age' directive")
            if header == "X-Content-Type-Options" and "nosniff" not in value.lower():
                print("Should be 'nosniff'")
            if header == "Referrer-Policy" and "unsafe-url" in value.lower():
                print("'unsafe-url' leaks referrer info")
            if header == "Cache-Control" and "no-store" not in value.lower():
                print("Should include 'no-store' or 'no-cache'")
            if header == "Access-Control-Allow-Origin" and value == "*":
                print("Allows all origins! Potential CORS risk")
            if header == "Expect-CT" and "max-age" not in value:
                print("'Expect-CT' missing 'max-age' directive")

if __name__ == "__main__":
    target = input("Enter target URL: ").strip()
    analyze_headers(target)
