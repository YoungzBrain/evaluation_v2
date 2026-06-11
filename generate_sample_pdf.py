from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

sample_questions = [
    {
        'text': "L'intervenant explique clairement les notions abordées",
        'type': 'scored',
    },
    {
        'text': "Les supports de cours sont adaptés et compréhensibles",
        'type': 'scored',
    },
    {
        'text': "Le rythme de la formation était adéquat",
        'type': 'scored',
    },
    {
        'text': "Quelles améliorations proposeriez-vous pour ce cours ?",
        'type': 'open',
    },
    {
        'text': "Avez-vous des commentaires supplémentaires sur le formateur ?",
        'type': 'open',
    },
]

output_path = 'sample_questions.pdf'

c = canvas.Canvas(output_path, pagesize=A4)
width, height = A4
margin = 20 * mm
x = margin
y = height - margin
c.setFont('Helvetica-Bold', 18)
c.drawString(x, y, 'Exemple de questions PDF')
y -= 15 * mm
c.setFont('Helvetica', 11)
intro = 'Ce document présente un exemple de questions importables. Les questions notées attendent une note de 1 à 5 ; les questions ouvertes sont des champs de texte.' 
for line in intro.split('\n'):
    c.drawString(x, y, line)
    y -= 6 * mm

for idx, q in enumerate(sample_questions, start=1):
    if y < margin + 40 * mm:
        c.showPage()
        y = height - margin
        c.setFont('Helvetica', 11)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, f'Q{idx}. ')
    text = q['text']
    c.setFont('Helvetica', 11)
    text_lines = []
    while text:
        if len(text) > 80:
            split_at = text.rfind(' ', 0, 80)
            if split_at <= 0:
                split_at = 80
            text_lines.append(text[:split_at])
            text = text[split_at+1:]
        else:
            text_lines.append(text)
            text = ''
    for line in text_lines:
        c.drawString(x + 15 * mm, y, line)
        y -= 6 * mm
    if q['type'] == 'scored':
        y -= 2 * mm
        c.drawString(x + 15 * mm, y, 'Note (1-5) : _____')
        y -= 10 * mm
    else:
        y -= 2 * mm
        for _ in range(4):
            c.line(x + 15 * mm, y, width - margin, y)
            y -= 8 * mm
        y -= 4 * mm

c.save()
print(f'Generated {output_path}')
