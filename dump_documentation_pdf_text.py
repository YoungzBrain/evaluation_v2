from pathlib import Path
import pdfplumber

path = Path('Documentation.pdf')
out = Path('documentation_pdf_text_utf8.txt')
with pdfplumber.open(path) as pdf, open(out, 'w', encoding='utf-8') as f:
    for i, page in enumerate(pdf.pages, start=1):
        f.write(f'--- page {i} ---\n')
        text = page.extract_text()
        f.write((text or '(no text)') + '\n')
        f.write('\n')
print('wrote', out)
