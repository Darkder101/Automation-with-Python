import requests
from urllib.parse import urlparse, urlencode, urljoin, parse_qsl, urlunparse, quote_plus

PAYLOAD = "https://evil.com/"

def build_test_url(original_url, param_name="redirect", payload=PAYLOAD):
    parsed = urlparse(original_url)
    q = dict(parse_qsl(parsed.query))
    q[param_name] = payload
    new_query = urlencode(q)
    new_parsed = parsed._replace(query=new_query)
    return urlunparse(new_parsed)

def detect_open_redirect(url):
    try:
       
        resp = requests.get(url, timeout=10, allow_redirects=True)
    except requests.RequestException as e:
        print(f"[!] Request error: {e}")
        return False, None

    final = resp.url
    loc = resp.headers.get("Location", "")
    body = resp.text

    
    if PAYLOAD.rstrip("/") in final:
        return True, f"Final URL redirects to payload ({final})"
    if PAYLOAD in loc or PAYLOAD in body:
        return True, "Payload found in Location header or response body"
    return False, None

if __name__ == "__main__":
    target = input("Enter target URL (include https://): ").strip()
    test_url = build_test_url(target)
    print(f"Testing: {test_url}")
    found, info = detect_open_redirect(test_url)
    if found:
        print("[VULN] Open redirect likely detected!")
        print("Details:", info)
    else:
        print("[OK] No obvious open redirect detected with this payload.")
