import requests
from urllib.parse import urljoin

COMMON_FILES = [
    ".git/", ".env", "backup.zip", "backup.tar.gz", "db.sql", "db.sql.bak",
    "config.php", "config.bak", "wp-config.php", ".htpasswd", "robots.txt",
    "sitemap.xml", "id_rsa", "id_rsa.pub", "dump.sql", "backup.sql"
]

TIMEOUT = 8

def scan_target(base_url):
    print(f"\nScanning {base_url}")
    for p in COMMON_FILES:
        url = urljoin(base_url, p)
        try:
            r = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            if r.status_code == 200:
                print(f"[FOUND] {url} (200)")
            elif r.status_code == 403:
                print(f"[POSSIBLE] {url} (403 - exists but forbidden)")
            
        except requests.RequestException as e:
            print(f"[ERROR] {url} -> {e}")

if __name__ == "__main__":
    target = input("Enter base URL (include https://, end with / recommended): ").strip()
    if not target:
        print("No target provided.")
    else:
        scan_target(target)
