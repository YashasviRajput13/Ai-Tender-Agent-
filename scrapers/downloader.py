import os
from pathlib import Path
from typing import Optional

import requests


def download_file(url: str, output_dir: str, filename: Optional[str] = None) -> str:
    if filename is None:
        filename = os.path.basename(url.split('?')[0]) or 'downloaded_file'
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / filename

    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(file_path, 'wb') as handle:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    handle.write(chunk)

    return str(file_path)


if __name__ == '__main__':
    example_url = 'https://example.com/sample.pdf'
    output_path = download_file(example_url, 'downloads')
    print(f'Downloaded file to: {output_path}')
