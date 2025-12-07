import requests
import base64
import re

BASE = "http://15.206.47.5:9090"
s = requests.Session()

while True:
    # 1. Fetch token
    r = s.get(BASE + "/task")
    text = r.text.strip()

    # Extract only base64-ish tokens, ignore words like "string"
    m = re.search(r"([A-Za-z0-9+/=]{8,})", text)
    if not m:
        print("No token found:", text)
        continue

    token = m.group(1)

    # 2. Transform
    rev = token[::-1]
    b64 = base64.b64encode(rev.encode()).decode()
    final = f"CSK__{b64}__2025"

    # 3. Submit
    r2 = s.post(BASE + "/submit", data=final)
    print("Token:", token)
    print("Payload:", final)
    print("Server:", r2.text)
    print("-" * 40)

    if "flag" in r2.text.lower() or "ctf{" in r2.text:
        break
