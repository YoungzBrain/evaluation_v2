from pathlib import Path
import csv

infile = Path('documentation_pdf_text_utf8.txt')
outfile = Path('documentation_all_questions.csv')

skip_patterns = [
    'EVALUATION of LECTURERS',
    'https://',
    'Choose an answer',
    'Choisir une réponse',
    'of 18',
    'page',
    'ÉVALUATION',
]

lines = []
for raw in infile.read_text(encoding='utf-8').splitlines():
    s = raw.strip()
    if not s:
        continue
    if any(p in s for p in skip_patterns):
        continue
    if s.lower().startswith('1 of') or s.lower().endswith('of 18'):
        continue
    # skip short words that are likely labels
    if len(s) < 5:
        continue
    lines.append(s)

# Deduplicate while preserving order
seen = set()
uniq = []
for l in lines:
    if l in seen:
        continue
    seen.add(l)
    uniq.append(l)

# Heuristic: if contains '?' or 'comment' or 'suggest' or 'Positive' etc -> open
open_keywords = ['?', 'comment', 'suggest', 'Suggestion', 'General comments', 'Positive', 'Negative', 'Appréciation', 'Any suggestion', 'comments', 'suggestion', 'Appreciation']

with outfile.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['text', 'type', 'is_active'])
    for l in uniq:
        qtype = 'scored'
        # check for French equivalents
        if any(k.lower() in l.lower() for k in open_keywords) or l.endswith('/') or l.endswith(' /'):
            qtype = 'open'
        # also mark as open if it ends with a question mark
        if l.endswith('?'):
            qtype = 'open'
        writer.writerow([l, qtype, '1'])

print('Wrote', outfile)
