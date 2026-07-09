from pathlib import Path
import pdfplumber

path = Path('Restructured_Evaluation_Form.pdf')
out_path = Path('restructured_pdf_text_utf8.txt')
with pdfplumber.open(path) as pdf, out_path.open('w', encoding='utf-8') as out:
    out.write(f'pages {len(pdf.pages)}\n')
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ''
        out.write(f'--- page {i} ---\n')
        out.write(text + '\n')
        out.write('\n')
print('wrote', out_path)
