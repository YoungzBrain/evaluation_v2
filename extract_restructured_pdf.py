from pathlib import Path
import pdfplumber

path = Path('Restructured_Evaluation_Form.pdf')
print('exists', path.exists())
with pdfplumber.open(path) as pdf:
    print('pages', len(pdf.pages))
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ''
        print('--- page', i, '---')
        print(text)
        print()
