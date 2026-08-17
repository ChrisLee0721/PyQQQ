"""Convert algorithm-report.md to PDF."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

styles = getSampleStyleSheet()
title = ParagraphStyle('T', parent=styles['Title'], fontSize=18, spaceAfter=10)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, spaceAfter=6, spaceBefore=14)
h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=10, spaceAfter=4, spaceBefore=10)
body = ParagraphStyle('B', parent=styles['Normal'], fontSize=9, leading=13)


def make_table(lines):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        rows.append(cells)
    if not rows:
        return None
    t = Table(rows, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('FONTSIZE', (0, 1), (-1, -1), 6.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


with open(r'F:\PyQQQ\docs\algorithm-report.md', encoding='utf-8') as f:
    lines = f.readlines()

doc = SimpleDocTemplate(
    r'F:\PyQQQ\docs\QuoNic_Algorithm_Report.pdf', pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title='QuoNic Algorithm Report', author='QuoNic',
)

story = []
i = 0
while i < len(lines):
    line = lines[i].rstrip()

    if line.startswith('# ') and not line.startswith('##'):
        story.append(Paragraph(line[2:], title))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:], h2))
    elif line.startswith('### '):
        story.append(Paragraph(line[4:], h3))
    elif line.startswith('```'):
        i += 1
        while i < len(lines) and not lines[i].strip().startswith('```'):
            i += 1
    elif '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
        table_lines = []
        while i < len(lines) and '|' in lines[i]:
            if '---' not in lines[i]:
                table_lines.append(lines[i].rstrip())
            i += 1
        t = make_table(table_lines)
        if t:
            story.append(t)
            story.append(Spacer(1, 3 * mm))
        continue
    elif line.startswith('- '):
        text = line[2:]
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
        story.append(Paragraph('  \u2022 ' + text, body))
    elif line.strip() == '':
        story.append(Spacer(1, 2 * mm))
    else:
        text = line
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
        story.append(Paragraph(text, body))

    i += 1

doc.build(story)
print('PDF generated: docs/QuoNic_Algorithm_Report.pdf')
