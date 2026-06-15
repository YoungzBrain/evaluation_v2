from pathlib import Path
import pdfplumber

path = Path('Documentation.pdf')
with pdfplumber.open(path) as pdf:
    for i in range(14, 18):
        page = pdf.pages[i-1]
        print(f'--- page {i} ---')
        print(page.extract_text())
        print('WORDS:')
        for w in page.extract_words():
            print(w)
        print()