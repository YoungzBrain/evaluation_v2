import importlib.util
import sys

print(sys.executable)
for mod in ['reportlab', 'PyPDF2', 'pdf2image', 'pytesseract']:
    found = importlib.util.find_spec(mod)
    print(mod, 'OK' if found else 'MISSING')
