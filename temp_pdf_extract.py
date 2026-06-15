import pdfplumber
from pathlib import Path
path = Path('Documentation.pdf')
with pdfplumber.open(path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        print(f'--- page {i} ---')
        text = page.extract_text()
        if not text:
            print('(no text)')
            continue
        for line in text.splitlines():
            print(repr(line))
        print()
