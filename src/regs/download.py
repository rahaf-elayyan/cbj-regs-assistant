import hashlib
import json
from pathlib import Path

import httpx

RAW = Path("data/raw")


def download_all(manifest="data/sources.json"):
    RAW.mkdir(parents=True, exist_ok=True)
    for src in json.loads(Path(manifest).read_text(encoding="utf-8")):
        r = httpx.get(src["url"], follow_redirects=True, timeout=60)
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise ValueError(f"{src['id']}: got HTML, not a PDF")
        (RAW / src["file"]).write_bytes(r.content)
        print(src["id"], hashlib.sha256(r.content).hexdigest()[:12])


if __name__ == "__main__":
    download_all()
