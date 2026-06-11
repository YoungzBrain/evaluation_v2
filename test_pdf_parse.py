import PyPDF2
path = 'sample_questions.pdf'
reader = PyPDF2.PdfReader(path)
print('Pages:', len(reader.pages))
for i,p in enumerate(reader.pages, start=1):
    text = p.extract_text() or ''
    print('--- page', i, '---')
    print(text[:300].replace('\n', ' '))
