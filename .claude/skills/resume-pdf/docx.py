"""Rebuild the ATS .docx body from resumes/index.html (single column, same content).

Keeps every other part of the existing .docx (styles, settings, page setup) and
replaces only what sits between <w:body> and <w:sectPr>.
Run from the repo root:  python .claude/skills/resume-pdf/docx.py
"""
import html, re, zipfile, shutil, os
from xml.sax.saxutils import escape

SRC = 'resumes/index.html'
DOCX = 'resumes/Thayagapriyan_Dravidamani_Integration_Lead_Resume.docx'
SZ = 18          # body size in half-points (9pt)
TEXT_W = 12240 - 2 * 720   # letter width minus 0.5in side margins, for the right-aligned dates
FONT = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'


def run(t, b=False, i=False, color='2B2B2B', sz=SZ):
    rpr = FONT + ('<w:b/>' if b else '') + ('<w:i/>' if i else '') + f'<w:color w:val="{color}"/><w:sz w:val="{sz}"/>'
    t = escape(t).replace('\t', '</w:t><w:tab/><w:t xml:space="preserve">')
    return f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{t}</w:t></w:r>'


def para(runs, before=0, after=20, extra=''):
    return (f'<w:p><w:pPr>{extra}<w:spacing w:before="{before}" w:after="{after}" '
            f'w:line="240" w:lineRule="auto"/></w:pPr>{"".join(runs)}</w:p>')


def text(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()


def rich(h, **kw):
    """<b>…</b> becomes bold runs; everything else is plain text."""
    parts = re.split(r'(<b>.*?</b>)', h, flags=re.S)
    out = []
    for p in parts:
        t = text(p)
        if not t:
            continue
        # keep the single spaces that sat next to the bold span
        if p.startswith('<b>'):
            out.append(run(t, b=True, color='12181A', **kw))
        else:
            lead = ' ' if p[:1].isspace() else ''
            trail = ' ' if p[-1:].isspace() else ''
            out.append(run(lead + t + trail, **kw))
    return out


def section(title):
    border = '<w:keepNext/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="BFC4C9"/></w:pBdr>'
    return para([run(title, b=True, color='12181A', sz=21)], before=80, after=40, extra=border)


def bullet(h):
    return para([run('•  ')] + rich(h), after=10, extra='<w:ind w:left="300" w:hanging="200"/>')


s = open(SRC, encoding='utf-8').read()
body = s[s.index('<div class="sheet">'):]
P = []

# masthead
P.append(para([run(text(re.search(r'<h1>(.*?)</h1>', body).group(1)).upper(), b=True, color='12181A', sz=32)],
              after=20, extra='<w:jc w:val="center"/>'))
role = text(re.search(r'class="role">(.*?)<', body).group(1))
yrs = text(re.search(r'class="yrs">(.*?)<', body).group(1))
P.append(para([run(f'{role}  |  {yrs}', color='0B7C7A', sz=21)], after=20, extra='<w:jc w:val="center"/>'))
contact = re.search(r'<div class="contact">(.*?)</div>', body, re.S).group(1)
links = [text(a) for a in re.findall(r'<a [^>]*>(.*?)</a>', contact)]
P.append(para([run('  |  '.join(links), color='6B797C', sz=SZ)], after=60, extra='<w:jc w:val="center"/>'))

# skills
P.append(section('TECHNICAL SKILLS'))
skills = re.search(r'<dl class="skills">(.*?)</dl>', body, re.S).group(1)
for dt, dd in re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', skills, re.S):
    P.append(para([run(text(dt) + ':  ', b=True, color='12181A')] + rich(dd), after=10))

# experience, in document order
P.append(section('PROFESSIONAL EXPERIENCE'))
main = re.search(r'<main>(.*?)</main>', body, re.S).group(1)
tok = re.compile(r'<h3>(?P<h3>.*?)</h3>|class="dates">(?P<dates>.*?)<|<p class="org">(?P<org>.*?)</p>'
                 r'|<p class="summary">(?P<summary>.*?)</p>|<h4>(?P<h4>.*?)</h4>|<li>(?P<li>.*?)</li>', re.S)
first = True
for m in tok.finditer(main):
    k, v = m.lastgroup, m.group(m.lastgroup)
    if k == 'h3':
        title = text(v)
    elif k == 'dates':
        tab = f'<w:keepNext/><w:tabs><w:tab w:val="right" w:pos="{TEXT_W}"/></w:tabs>'
        P.append(para([run(title, b=True, color='12181A', sz=22), run('\t' + text(v), color='6B797C')],
                      before=0 if first else 60, after=0, extra=tab))
        first = False
    elif k == 'org':
        P.append(para([run(text(v).replace(' · ', '  |  '), b=True, color='0B7C7A')], after=20, extra='<w:keepNext/>'))
    elif k == 'summary':
        P.append(para([run(text(v), i=True, color='6B797C')], after=20, extra='<w:keepNext/>'))
    elif k == 'h4':
        P.append(para([run(text(v), b=True, color='B8492A')], before=30, after=10, extra='<w:keepNext/>'))
    else:
        P.append(bullet(v))

# Key Achievements is left out: it repeats experience bullets, and one page is the limit.


# write: swap the body, keep everything else
tmp = DOCX + '.tmp'
with zipfile.ZipFile(DOCX) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == 'word/document.xml':
            x = data.decode('utf-8')
            a = x.index('<w:body>') + len('<w:body>')
            b = x.index('<w:sectPr')
            x = x[:a] + ''.join(P) + x[b:]
            x = re.sub(r'<w:pgMar [^>]*/>', '<w:pgMar w:top="576" w:right="720" w:bottom="576" w:left="720" '
                       'w:header="720" w:footer="720" w:gutter="0"/>', x)
            data = x.encode('utf-8')
        zout.writestr(item, data)
shutil.move(tmp, DOCX)
print(f'{DOCX}: {len(P)} paragraphs')
