"""Convert algorithm-report.md to PDF with Chinese font support."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Chinese font
pdfmetrics.registerFont(TTFont('SimHei', r'C:\Windows\Fonts\simhei.ttf'))
pdfmetrics.registerFont(TTFont('SimSun', r'C:\Windows\Fonts\simsun.ttc'))

styles = getSampleStyleSheet()
title = ParagraphStyle('T', parent=styles['Title'], fontName='SimHei', fontSize=18, spaceAfter=10)
h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='SimHei', fontSize=13, spaceAfter=6, spaceBefore=14)
h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='SimHei', fontSize=10, spaceAfter=4, spaceBefore=10)
body = ParagraphStyle('B', parent=styles['Normal'], fontName='SimSun', fontSize=9, leading=14)
body_bold = ParagraphStyle('BB', parent=body, fontName='SimHei')
code_style = ParagraphStyle('C', parent=styles['Normal'], fontName='Courier', fontSize=7.5, leading=10, backColor=colors.HexColor('#f5f5f5'))


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
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, 0), 7.5),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    return t


with open(r'F:\PyQQQ\docs\algorithm-report.md', encoding='utf-8') as f:
    lines = f.readlines()

doc = SimpleDocTemplate(
    r'F:\PyQQQ\docs\QuoNic_Algorithm_Report.pdf', pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=20 * mm, bottomMargin=18 * mm,
    title='QuoNic 算法模板扩展报告',
    author='QuoNic',
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
        # code block — skip content
        i += 1
        while i < len(lines) and not lines[i].strip().startswith('```'):
            i += 1
    elif '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
        # markdown table
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
        text = re.sub(r'`(.+?)`', r'<font face="Courier" size="7">\1</font>', text)
        story.append(Paragraph('\u2022 ' + text, body))
    elif line.strip() == '':
        story.append(Spacer(1, 2 * mm))
    else:
        text = line
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'`(.+?)`', r'<font face="Courier" size="7">\1</font>', text)
        story.append(Paragraph(text, body))

    i += 1

doc.build(story)
print('PDF generated: docs/QuoNic_Algorithm_Report.pdf')
