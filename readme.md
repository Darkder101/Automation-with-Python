# Automation-with-Python

Small, readable Python scripts to demonstrate web-pentest automation skills.

## Contains

* `open_redirect_simple.py` — simple open-redirect checks
* `security_headers_check.py` — checks common HTTP security headers
* `sensitive_finder_simple.py` — searches for common sensitive filenames/paths

## Quick notes

* Language: Python 3
* Intended for code review / skill demonstration only.
* Do **not** run these against targets you don't own or have permission to test.

## How to run (example)

```bash
python3 open_redirect_simple.py --url "https://example.com/?next=https://attacker.com"
python3 security_headers_check.py --url https://example.com
python3 sensitive_finder_simple.py --base-url https://example.com
```

## Contact

If you need a walkthrough of any script, I can add short comments or a demo GIF on request.
