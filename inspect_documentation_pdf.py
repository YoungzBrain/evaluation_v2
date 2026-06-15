import csv
from pathlib import Path
import pdfplumber

path = Path('Documentation.pdf')
with pdfplumber.open(path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        print(f'--- page {i} ---')
        text = page.extract_text()
        if text:
            print(text)
        else:
            print('(no text)')
        print('words:')
        words = page.extract_words()
        print(words[:40])
        print('---')
