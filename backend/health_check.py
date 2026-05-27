import urllib.request

for url in [
    'http://localhost:8002/health',
    'http://localhost:8000/health',
    'http://localhost:8000/tenders',
    'http://localhost:3000',
]:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            print(url, 'OK', r.read().decode())
    except Exception as exc:
        print(url, 'ERROR', exc)
