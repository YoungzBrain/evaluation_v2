from pathlib import Path
import pdfplumber

path = Path('Documentation.pdf')
with pdfplumber.open(path) as pdf:
    print('pages', len(pdf.pages))
    for i in range(3, 11):
        page = pdf.pages[i - 1]
        out = Path(f'page_{i}.png')
        img = page.to_image(resolution=200)
        img.save(out)
        print('saved', out)
        try:
            import pytesseract
            text = pytesseract.image_to_string(out)
            print('OCR page', i)
            print(text)
        except Exception as e:
            print('OCR failed', e)
