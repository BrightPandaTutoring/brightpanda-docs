#!/usr/bin/env python3
"""Bright Panda Docent Gids — PDF Builder v1.1

Usage:
  python3 build.py [lang]
  lang: 'nl' (default) or 'en'

Requirements:
  pip install reportlab pypdf pillow cairosvg

Paths (adjust if running outside the build environment):
  IMG_DIR  = directory with all bsport_*.png screenshots
  LOGO_*   = logo PNG files (generated from SVG via cairosvg)
  md path  = nl.md or en.md in same directory as this script
"""

import re, os, sys
from io import BytesIO
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, KeepTogether, Image, Table, TableStyle, CondPageBreak
)
from reportlab.pdfgen import canvas as rl_canvas
from pypdf import PdfWriter, PdfReader

W, H = A4
ML = MR = 2.2 * cm
MB = 2.8 * cm
TW = W - ML - MR

BLUE  = colors.HexColor("#1d467f")
GOLD  = colors.HexColor("#f59e0c")
LIGHT = colors.HexColor("#f4f8fd")
WARN  = colors.HexColor("#fffbf0")
GREY  = colors.HexColor("#666666")
LGREY = colors.HexColor("#aaaaaa")

LOGO_COLOR = "/home/claude/docent_gids/logo_color.png"
LOGO_WHITE = "/home/claude/docent_gids/logo_white.png"
LOGO_TRANSPARENT = "/home/claude/docent_gids/logo_transparent.png"
LOGO_W = 3.8 * cm
LOGO_H = LOGO_W * (60/142)
LOGO_TOP_MARGIN = 0.4 * cm
MT = LOGO_TOP_MARGIN + LOGO_H + 0.6 * cm

IMG_DIR = "/home/claude/docent_gids/images"


def sized_image(path, max_w, max_h=None):
    if not os.path.exists(path):
        return None
    try:
        with PILImage.open(path) as im:
            iw, ih = im.size
        ratio = iw / ih
        if max_h is None:
            max_h = max_w / ratio
        if iw / max_w > ih / max_h:
            w, h = max_w, max_w / ratio
        else:
            h, w = max_h, max_h * ratio
        img = Image(path, width=w, height=h)
        img.hAlign = 'CENTER'
        return img
    except Exception as e:
        print(f"Image error {path}: {e}")
        return None


def make_styles():
    return {
        "body":      ParagraphStyle("body", fontName="Helvetica", fontSize=10,
                                    leading=15, alignment=TA_JUSTIFY,
                                    textColor=colors.HexColor("#333333"), spaceAfter=5),
        "intro":     ParagraphStyle("intro", fontName="Helvetica-Oblique", fontSize=10,
                                    leading=15, textColor=GREY, spaceAfter=8),
        "h2":        ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5,
                                    leading=15, textColor=BLUE, spaceAfter=4, spaceBefore=8),
        "bullet":    ParagraphStyle("bullet", fontName="Helvetica", fontSize=10,
                                    leading=14, leftIndent=14, firstLineIndent=-8,
                                    textColor=colors.HexColor("#333333"), spaceAfter=2),
        "numbered":  ParagraphStyle("numbered", fontName="Helvetica", fontSize=10,
                                    leading=14, leftIndent=22, firstLineIndent=-14,
                                    textColor=colors.HexColor("#333333"), spaceAfter=2),
        "caption":   ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=8.5,
                                    leading=12, textColor=GREY, alignment=TA_CENTER,
                                    spaceAfter=10),
        "bold_head": ParagraphStyle("bold_head", fontName="Helvetica-Bold", fontSize=10,
                                    leading=14, textColor=colors.HexColor("#333333"),
                                    spaceAfter=2, spaceBefore=6),
        "toc_ch":    ParagraphStyle("toc_ch", fontName="Helvetica-Bold", fontSize=11,
                                    leading=15, textColor=BLUE, spaceBefore=10, spaceAfter=3),
        "toc_p":     ParagraphStyle("toc_p", fontName="Helvetica", fontSize=9.5,
                                    leading=13, textColor=colors.HexColor("#555555"),
                                    leftIndent=14, spaceAfter=1),
    }


def draw_cover(c, cfg):
    c.setFillColor(BLUE); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, 0, 0.7*cm, H, fill=1, stroke=0)
    cx, cy, r = 3.8*cm, H-3.5*cm, 1.8*cm
    c.setFillColor(colors.white); c.circle(cx, cy, r, fill=1, stroke=0)
    logo_w = 3.2*cm; logo_h = logo_w * (60/142)
    c.drawImage(LOGO_TRANSPARENT, cx-logo_w/2, cy-logo_h/2,
                width=logo_w, height=logo_h, mask='auto', preserveAspectRatio=True)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 36)
    c.drawString(2.4*cm, H-7.5*cm, cfg["cover_title"])
    c.setFont("Helvetica", 15); c.setFillColor(colors.HexColor("#c8d8f0"))
    c.drawString(2.4*cm, H-9.0*cm, "Bright Panda Bijles")
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.line(2.4*cm, H-9.8*cm, W-2.4*cm, H-9.8*cm)
    c.setFont("Helvetica", 11); c.setFillColor(colors.HexColor("#adc4e0"))
    for i, line in enumerate(cfg["cover_tagline"]):
        c.drawString(2.4*cm, H-11.0*cm - i*1.2*cm, line)
    bw = (W-4.8*cm-0.6*cm)/3; bh = 5.5*cm; by = 4.5*cm
    bx = 2.4*cm
    for num, title, desc in cfg["cover_boxes"]:
        c.setFillColor(colors.HexColor("#163a6e"))
        c.roundRect(bx, by, bw, bh, 5, fill=1, stroke=0)
        c.setFillColor(GOLD); c.roundRect(bx, by+bh-5, bw, 5, 3, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 8); c.setFillColor(GOLD)
        c.drawString(bx+0.4*cm, by+bh-1.2*cm, num)
        c.setFont("Helvetica-Bold", 11); c.setFillColor(colors.white)
        c.drawString(bx+0.4*cm, by+bh-2.1*cm, title)
        c.setFont("Helvetica", 8.5); c.setFillColor(colors.HexColor("#adc4e0"))
        dy = by+bh-3.1*cm
        for dl in desc.split('\n'):
            c.drawString(bx+0.4*cm, dy, dl); dy -= 0.9*cm
        bx += bw+0.3*cm
    c.setFont("Helvetica", 8.5); c.setFillColor(colors.HexColor("#7a9abf"))
    c.drawString(2.4*cm, 1.2*cm, f'{cfg["version"]}  |  {cfg["date"]}')
    c.drawRightString(W-2.4*cm, 1.2*cm, "brightpanda.nl")


def draw_blank(c):
    c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_chapter(c, number, info, para_list, cfg):
    c.setFillColor(BLUE); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, 0, 0.7*cm, H, fill=1, stroke=0)
    logo_cx = W-ML-LOGO_W/2; logo_cy = H-LOGO_TOP_MARGIN-LOGO_H/2
    r = max(LOGO_W, LOGO_H) * 0.65
    c.setFillColor(colors.white); c.circle(logo_cx, logo_cy, r, fill=1, stroke=0)
    c.drawImage(LOGO_TRANSPARENT, logo_cx-LOGO_W/2, logo_cy-LOGO_H/2,
                width=LOGO_W, height=LOGO_H, mask='auto', preserveAspectRatio=True)
    section_top = H-4.2*cm
    bx, by = 2.4*cm, section_top-1.6*cm
    c.setFillColor(colors.HexColor("#163a6e"))
    c.roundRect(bx, by, 2.6*cm, 1.6*cm, 6, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 26)
    c.drawString(bx+0.3*cm, by+0.32*cm, f"H{number}")
    c.setFillColor(colors.HexColor("#adc4e0")); c.setFont("Helvetica", 11)
    c.drawString(bx+3.0*cm, by+0.55*cm, f'{cfg["chapter_label"]} {number}')
    divider_y = by-0.5*cm
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.line(2.4*cm, divider_y, W-2.4*cm, divider_y)
    title_y = divider_y-1.0*cm
    title_text = info["short"]
    max_title_w = W-4.8*cm
    fs = 22
    while fs > 12:
        if c.stringWidth(title_text, "Helvetica-Bold", fs) <= max_title_w:
            break
        fs -= 1
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", fs)
    c.drawString(2.4*cm, title_y, title_text)
    desc_top = title_y-0.7*cm; desc_h = 2.8*cm; desc_y = desc_top-desc_h
    box_x = 2.4*cm; box_w = W-4.8*cm
    c.setFillColor(colors.HexColor("#163a6e"))
    c.roundRect(box_x, desc_y, box_w, desc_h, 6, fill=1, stroke=0)
    c.setFillColor(GOLD); c.roundRect(box_x, desc_y+desc_h-4, box_w, 4, 3, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#c8d8f0")); c.setFont("Helvetica", 9.5)
    words = info["desc"].split(); lines_d = []; line_d = ""
    for w in words:
        test = (line_d+" "+w).strip()
        if c.stringWidth(test, "Helvetica", 9.5) < box_w-1.0*cm:
            line_d = test
        else:
            if line_d: lines_d.append(line_d)
            line_d = w
    if line_d: lines_d.append(line_d)
    ty = desc_y+desc_h-0.65*cm
    for ln in lines_d:
        c.drawString(box_x+0.5*cm, ty, ln); ty -= 0.42*cm
        if ty < desc_y+0.2*cm: break
    if para_list:
        list_y = desc_y-0.65*cm
        c.setFillColor(colors.HexColor("#adc4e0")); c.setFont("Helvetica-Bold", 9)
        c.drawString(2.4*cm, list_y, cfg["in_this_chapter"])
        list_y -= 0.45*cm
        c.setStrokeColor(colors.HexColor("#2a5a9f")); c.setLineWidth(0.5)
        c.line(2.4*cm, list_y+0.1*cm, W-2.4*cm, list_y+0.1*cm)
        list_y -= 0.38*cm
        col_w = (W-4.8*cm-0.6*cm)/2
        left_x = 2.4*cm; right_x = left_x+col_w+0.6*cm
        mid = len(para_list)//2+len(para_list)%2
        for col_items, col_x in [(para_list[:mid], left_x), (para_list[mid:], right_x)]:
            for i, (num_str, title) in enumerate(col_items):
                y = list_y-i*0.52*cm
                if y < 1.5*cm: break
                c.setFillColor(GOLD); c.setFont("Helvetica-Bold", 8)
                c.drawString(col_x, y, num_str)
                c.setFillColor(colors.white); c.setFont("Helvetica", 8)
                max_w = col_w-0.9*cm; t = title
                while c.stringWidth(t, "Helvetica", 8) > max_w and len(t) > 10:
                    t = t[:-1]
                if t != title: t = t[:-1]+"..."
                c.drawString(col_x+0.8*cm, y, t)


def full_page_pdf(fn, *args):
    buf = BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
    fn(c, *args)
    c.showPage(); c.save(); buf.seek(0)
    return buf


def make_on_page(cfg):
    def on_page(canv, doc):
        canv.saveState()
        logo_y = H-LOGO_TOP_MARGIN-LOGO_H
        canv.drawImage(LOGO_COLOR, W-ML-LOGO_W, logo_y,
                       width=LOGO_W, height=LOGO_H, mask='auto', preserveAspectRatio=True)
        canv.setFont("Helvetica", 8); canv.setFillColor(LGREY)
        canv.setStrokeColor(colors.HexColor("#e0e8f0")); canv.setLineWidth(0.5)
        canv.line(ML, 1.6*cm, W-ML, 1.6*cm)
        canv.drawString(ML, 1.2*cm, cfg["footer_text"])
        canv.drawRightString(W-ML, 1.2*cm, str(doc.page))
        canv.restoreState()
    return on_page


def sec_title(number_str, title):
    p = Paragraph(f'<b>{number_str}  {title}</b>',
        ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=12.5,
                       leading=17, textColor=BLUE))
    tbl = Table([[p]], colWidths=[TW])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),LIGHT),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LINEBEFORE',(0,0),(0,-1),4,GOLD),
    ]))
    return KeepTogether([tbl, Spacer(1,0.2*cm)])


def box_flowable(text, btype, cfg):
    prefix = cfg["warn_prefix"] if btype == "warn" else cfg["info_prefix"]
    fc = "#b45309" if btype == "warn" else "#1d467f"
    bg = WARN if btype == "warn" else LIGHT
    bc = GOLD if btype == "warn" else BLUE
    p = Paragraph(f'<font color="{fc}"><b>{prefix}</b></font>{text}',
        ParagraphStyle("box", fontName="Helvetica", fontSize=9.5, leading=14,
                       textColor=colors.HexColor("#333333")))
    tbl = Table([[p]], colWidths=[TW])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LINEBEFORE',(0,0),(0,-1),3,bc),
    ]))
    return [Spacer(1,0.12*cm), tbl, Spacer(1,0.12*cm)]


def photo_flowable(img_path, caption_text, styles):
    fn = os.path.basename(img_path)
    fp = os.path.join(IMG_DIR, fn)
    result = [Spacer(1,0.3*cm)]
    if os.path.exists(fp):
        img = sized_image(fp, TW, TW*0.65)
        if img:
            tbl = Table([[img]], colWidths=[TW])
            tbl.setStyle(TableStyle([
                ('BOX',(0,0),(-1,-1),0.5,colors.HexColor("#dddddd")),
                ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
            ]))
            result.append(tbl)
        else:
            result.append(Paragraph(f"[Image: {fn}]", styles["intro"]))
    else:
        result.append(Paragraph(f"[Image not found: {fn}]", styles["intro"]))
    if caption_text:
        result.append(Paragraph(caption_text, styles["caption"]))
    result.append(Spacer(1,0.1*cm))
    return result


def parse_md(path, chapter_marker="HOOFDSTUK"):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    sections, cur, content = [], None, []
    ch, pc, skip = None, {}, False

    def flush():
        if cur:
            cur["content"] = content[:]
            sections.append(dict(cur))

    for raw in lines:
        line = raw.rstrip('\n')
        if '<!--' in line: skip = True
        if skip:
            if '-->' in line: skip = False
            continue
        if line.strip() == '---': continue
        if re.match(rf'^# {chapter_marker}', line):
            flush(); content = []; cur = None
            m = re.search(r'(\d+)', line); n = m.group(1) if m else '?'
            ch = n; pc[f"H{n}"] = 0
            sections.append({"type":"chapter","number":n})
            continue
        if line in ('## INTRO', '## INTRODUCTION'):
            flush(); content = []
            cur = {"type":"intro_section","title":"INTRO","content":[]}
            continue
        if re.match(r'^## ', line) and not re.match(r'^### ', line):
            flush(); content = []
            title = line[3:].strip()
            k = f"H{ch}" if ch else "H1"
            pc[k] = pc.get(k,0)+1
            cur = {"type":"para","chapter":ch,"number":pc[k],"title":title,"content":[]}
            continue
        if re.match(r'^### ', line):
            if cur: content.append({"type":"subhead","text":line[4:].strip()})
            continue
        if cur is not None:
            s = line.strip()
            if not s: continue
            if s.startswith('[icon:'): continue
            if s.startswith('[foto:'):
                m = re.search(r'\[foto:\s*([^\]]+)\]', s)
                if m: content.append({"type":"foto","path":m.group(1).strip()})
                continue
            if s.startswith('[warning]') or s.startswith('[waarschuwing]'):
                txt = s[9:].strip() if s.startswith('[warning]') else s[14:].strip()
                content.append({"type":"warn","text":txt}); continue
            if s.startswith('[info]'):
                content.append({"type":"info","text":s[6:].strip()}); continue
            if s.startswith('[intro]'):
                content.append({"type":"intro","text":s[7:].strip()}); continue
            if s.startswith('- '):
                content.append({"type":"bullet","text":s[2:].strip()}); continue
            if re.match(r'^\*\*', s) and s.endswith('**') and len(s) < 80:
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
                content.append({"type":"bold_head","text":text}); continue
            if re.match(r'^\d+\. ', s):
                content.append({"type":"numbered","text":re.sub(r'^\d+\. ','',s)}); continue
            t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
            t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
            content.append({"type":"para","text":t})
    flush()
    return sections


def build_pdf(md_path, out_path, cfg, chapter_marker="HOOFDSTUK"):
    styles = make_styles()
    sections = parse_md(md_path, chapter_marker)
    on_page = make_on_page(cfg)

    ch_para_map = {}
    current_ch = None
    for s in sections:
        if s["type"] == "chapter":
            current_ch = s["number"]; ch_para_map[current_ch] = []
        elif s["type"] == "para" and current_ch:
            t = re.sub(r'\[icon:[^\]]+\]','',s["title"]).strip()
            t = re.sub(r'^\d+\.\s+','',t)
            ch_para_map[current_ch].append((f'{current_ch}.{s["number"]}', t))

    chapters = [s for s in sections if s["type"] == "chapter"]

    # TOC
    toc_story = [Spacer(1,0.5*cm)]
    toc_story.append(Paragraph(cfg["toc_title"],
        ParagraphStyle("tocT",fontName="Helvetica-Bold",fontSize=20,
                       leading=26,textColor=BLUE,spaceAfter=10)))
    toc_story.append(HRFlowable(width=TW,thickness=2,color=GOLD,spaceAfter=14))
    for s in [s for s in sections if s["type"] in ("chapter","para")]:
        if s["type"] == "chapter":
            info = cfg["chapters"].get(s["number"],{})
            toc_story.append(Paragraph(
                f'{cfg["chapter_label"]} {s["number"]} — {info.get("short","")}',
                styles["toc_ch"]))
        else:
            t = re.sub(r'\[icon:[^\]]+\]','',s["title"]).strip()
            t = re.sub(r'^\d+\.\s+','',t)
            ch = s["chapter"] or "1"
            toc_story.append(Paragraph(f'{ch}.{s["number"]}  {t}', styles["toc_p"]))
    toc_story.append(PageBreak())

    intro = next((s for s in sections if s["type"] == "intro_section"), None)
    if intro:
        toc_story.append(Spacer(1,0.4*cm))
        toc_story.append(Paragraph(cfg["welcome_title"],
            ParagraphStyle("wt",fontName="Helvetica-Bold",fontSize=20,
                           leading=26,textColor=BLUE,spaceAfter=8)))
        toc_story.append(HRFlowable(width=TW,thickness=2,color=GOLD,spaceAfter=14))
        for item in intro.get("content",[]):
            if item["type"] == "para":
                t = item["text"]
                if t.startswith("<b>"):
                    toc_story.append(Paragraph(t,
                        ParagraphStyle("bh",fontName="Helvetica-Bold",fontSize=11,
                                       leading=16,textColor=BLUE,spaceAfter=4,spaceBefore=10)))
                else:
                    toc_story.append(Paragraph(t,styles["body"]))
        toc_story.append(PageBreak())

    toc_pdf = "/home/claude/docent_gids/toc_tmp.pdf"
    doc = SimpleDocTemplate(toc_pdf,pagesize=A4,
        leftMargin=ML,rightMargin=MR,topMargin=MT,bottomMargin=MB)
    doc.build(toc_story,onFirstPage=on_page,onLaterPages=on_page)

    chapter_pdfs = []
    for ch_sec in chapters:
        ch_num = ch_sec["number"]
        ch_story = []
        for s in [s for s in sections if s["type"]=="para" and s["chapter"]==ch_num]:
            num_str = f'{ch_num}.{s["number"]}'
            title_clean = re.sub(r'\[icon:[^\]]+\]','',s["title"]).strip()
            title_clean = re.sub(r'^\d+\.\s+','',title_clean)
            ch_story.append(Spacer(1,0.2*cm))
            ch_story.append(sec_title(num_str,title_clean))
            nc = [0]
            for item in s.get("content",[]):
                tp = item["type"]
                if tp=="intro": ch_story.append(Paragraph(item["text"],styles["intro"]))
                elif tp=="para": ch_story.append(Paragraph(item["text"],styles["body"]))
                elif tp=="bold_head":
                    ch_story.append(KeepTogether([Spacer(1,0.1*cm),Paragraph(item["text"],styles["bold_head"])]))
                elif tp=="subhead":
                    ch_story.append(KeepTogether([Spacer(1,0.1*cm),Paragraph(item["text"],styles["h2"])]))
                elif tp=="bullet":
                    ch_story.append(Paragraph(f"•  {item['text']}",styles["bullet"]))
                elif tp=="numbered":
                    nc[0]+=1; ch_story.append(Paragraph(f"{nc[0]}.  {item['text']}",styles["numbered"]))
                elif tp in ("warn","info"):
                    ch_story.extend(box_flowable(item["text"],tp,cfg))
                elif tp=="foto":
                    fn = os.path.basename(item["path"])
                    caption = cfg["captions"].get(fn,"")
                    ch_story.extend(photo_flowable(item["path"],caption,styles))
            ch_story.append(Spacer(1,0.2*cm))
        ch_path = f"/home/claude/docent_gids/ch{ch_num}_tmp.pdf"
        doc_ch = SimpleDocTemplate(ch_path,pagesize=A4,
            leftMargin=ML,rightMargin=MR,topMargin=MT,bottomMargin=MB)
        doc_ch.build(ch_story,onFirstPage=on_page,onLaterPages=on_page)
        chapter_pdfs.append((ch_num,ch_path))
        print(f"  Chapter {ch_num}: {len(list(PdfReader(ch_path).pages))} pages")

    writer = PdfWriter()
    writer.add_page(PdfReader(full_page_pdf(draw_cover,cfg)).pages[0])
    for page in PdfReader(toc_pdf).pages:
        writer.add_page(page)
    for ch_num, ch_path in chapter_pdfs:
        info = cfg["chapters"].get(ch_num,{"short":f"Chapter {ch_num}","desc":""})
        para_list = ch_para_map.get(ch_num,[])
        writer.add_page(PdfReader(full_page_pdf(draw_blank)).pages[0])
        writer.add_page(PdfReader(full_page_pdf(draw_chapter,ch_num,info,para_list,cfg)).pages[0])
        for page in PdfReader(ch_path).pages:
            writer.add_page(page)

    with open(out_path,"wb") as f:
        writer.write(f)
    print(f"\nPDF ready: {out_path}")
    print(f"Size: {os.path.getsize(out_path)//1024} KB, Pages: {len(writer.pages)}")


# ── Language configs ────────────────────────────────────────────────────────────
NL_CAPTIONS = {
    "bsport_login_scherm.png":           "Stap 1: ga naar de inlogpagina en vul je e-mailadres en wachtwoord in. Gebruik 'Forgot your password?' als je nog geen wachtwoord hebt ingesteld.",
    "bsport_login_keuze.png":            "Stap 2: kies na het inloggen altijd voor Teacher. Klik nooit op Member.",
    "bsport_agenda_leeg.png":            "Een lege agenda — er is nog geen beschikbaarheid opgegeven. Ouders kunnen nu geen les inboeken.",
    "bsport_agenda_menu.png":            "Klik op 'Add availability' om een tijdslot toe te voegen aan je agenda.",
    "bsport_agenda_popup.png":           "Laat de toggle 'Add for certain establishments only' uitgeschakeld en klik op Save.",
    "bsport_agenda_groen.png":           "Een groen blok in de agenda betekent dat je beschikbaarheid succesvol is opgeslagen.",
    "bsport_agenda_ingeboekt.png":       "Een ingeboekte les verschijnt als blauw blok in je Schedule met de naam van de les en het tijdstip.",
    "bsport_payroll_normaal.png":        "De Payroll pagina: selecteer de eerste dag van de maand en kies Monthly als periode.",
    "bsport_payroll_agenda.png":         "Gebruik de datumkiezer om de juiste maand te selecteren. Kies altijd de eerste dag van de maand.",
    "bsport_payroll_calculate.png":      "Klik op Calculate om de uitbetalingsoverzicht te laden. Zonder Calculate zijn er geen gegevens zichtbaar.",
    "bsport_payroll_appointments.png":   "Klik op het tabblad Appointments voor een overzicht van alle ingeboekte lessen, uren en het totale uitbetalingsbedrag.",
    "bsport_stap1_vak_kiezen.png":       "De ouder kiest het vak waarvoor bijles gewenst is.",
    "bsport_stap2_geen_beschikbaarheid.png": "Als jij geen beschikbaarheid hebt opgegeven, ziet de ouder deze melding. Er kan dan geen les worden ingeboekt.",
    "bsport_stap2_tijdsloten.png":       "Zodra jij beschikbaarheid hebt opgegeven, ziet de ouder jouw tijdsloten en kan er een moment worden gekozen.",
    "bsport_stap3_confirm_adres.png":    "Na het kiezen van een tijdslot verschijnt dit scherm. Let op: de les is hier nog NIET definitief geboekt.",
    "bsport_stap4_book_knop.png":        "Pas na het klikken op de knop 'Book' is de les definitief ingeboekt. Jij en de ouder ontvangen dan een bevestigingsmail.",
    "bsport_stap5_my_bookings.png":      "Na de boeking is de les zichtbaar voor de ouder onder My bookings, tabblad Appointments.",
}

EN_CAPTIONS = {
    "bsport_login_scherm.png":           "Step 1: go to the login page and enter your email address and password. Use 'Forgot your password?' if you have not set a password yet.",
    "bsport_login_keuze.png":            "Step 2: after logging in, always choose Teacher. Never click Member.",
    "bsport_agenda_leeg.png":            "An empty schedule — no availability has been added yet. Parents cannot book a lesson.",
    "bsport_agenda_menu.png":            "Click 'Add availability' to add a time slot to your schedule.",
    "bsport_agenda_popup.png":           "Leave the 'Add for certain establishments only' toggle off and click Save.",
    "bsport_agenda_groen.png":           "A green block in the schedule means your availability has been saved successfully.",
    "bsport_agenda_ingeboekt.png":       "A booked lesson appears as a blue block in your Schedule showing the lesson name and time.",
    "bsport_payroll_normaal.png":        "The Payroll page: select the first day of the month and choose Monthly as the period.",
    "bsport_payroll_agenda.png":         "Use the date picker to select the correct month. Always choose the first day of the month.",
    "bsport_payroll_calculate.png":      "Click Calculate to load the payout overview. Without clicking Calculate no data will appear.",
    "bsport_payroll_appointments.png":   "Click the Appointments tab for a full overview of all booked lessons, hours and your total payout.",
    "bsport_stap1_vak_kiezen.png":       "The parent selects the subject for which tutoring is needed.",
    "bsport_stap2_geen_beschikbaarheid.png": "If you have not added any availability, the parent sees this message and cannot book a lesson.",
    "bsport_stap2_tijdsloten.png":       "Once you have added availability, the parent sees your time slots and can choose a moment.",
    "bsport_stap3_confirm_adres.png":    "After selecting a time slot this screen appears. Note: the lesson is NOT yet definitively booked at this point.",
    "bsport_stap4_book_knop.png":        "Only after clicking 'Book' is the lesson definitively booked. Both you and the parent will receive a confirmation email.",
    "bsport_stap5_my_bookings.png":      "After booking, the lesson is visible to the parent under My bookings, Appointments tab.",
}

CFG_NL = {
    "version": "v1.1", "date": "17 april 2026",
    "cover_title": "Docent Gids",
    "cover_tagline": ["Alles wat je nodig hebt om als docent", "succesvol bij les te geven via Bright Panda."],
    "cover_boxes": [
        ("H1","Bijles geven","Matching, proefles,\ndidactiek en meer"),
        ("H2","Gedragscode","Professionaliteit,\nprivacy en grenzen"),
        ("H3","Boekingssysteem","Bsport: inloggen,\nbeschikbaarheid\nen uitbetaling"),
    ],
    "toc_title": "Inhoudsopgave",
    "welcome_title": "Welkom bij Bright Panda",
    "chapter_label": "Hoofdstuk",
    "in_this_chapter": "IN DIT HOOFDSTUK",
    "footer_text": "Bright Panda Docent Gids  v1.1",
    "warn_prefix": "Let op: ", "info_prefix": "Info: ",
    "captions": NL_CAPTIONS,
    "chapters": {
        "1": {"short":"Hoe maak je van bijles geven een succes?","desc":"In dit hoofdstuk vind je alles wat je nodig hebt om als docent goed van start te gaan. Van het matchingproces en de voorbereiding op je eerste proefles tot didactische aanpakken, het begeleiden van uiteenlopende leerlingen en praktische tools die je werk makkelijker maken. Dit is het inhoudelijke hart van de docent gids: lees dit zorgvuldig voordat je aan je eerste les begint."},
        "2": {"short":"Gedragscode","desc":"Als docent bij Bright Panda vertegenwoordig je ons bedrijf. In dit hoofdstuk lees je welke professionele standaarden, gedragsregels en grenzen gelden voor alle docenten die via Bright Panda lesgeven. Van communicatie met ouders en leerlingen tot privacy, social media en uiterlijke verzorging. Deze regels zijn er om jou, de leerling en Bright Panda te beschermen."},
        "3": {"short":"Ons boekingssysteem","desc":"Bright Panda werkt met Bsport als boekingssysteem. In dit hoofdstuk leer je stap voor stap hoe je inlogt, je beschikbaarheid instelt, ingeboekte lessen controleert en je uitbetalingen bekijkt. Lees dit hoofdstuk goed door voordat je begint met lesgeven. Alleen ingeboekte lessen worden uitbetaald."},
    },
}

CFG_EN = {
    "version": "v1.1", "date": "17 April 2026",
    "cover_title": "Teacher Guide",
    "cover_tagline": ["Everything you need to give great lessons", "as a tutor at Bright Panda."],
    "cover_boxes": [
        ("H1","Tutoring","Matching, trial lesson,\ndidactics and more"),
        ("H2","Code of Conduct","Professionalism,\nprivacy and boundaries"),
        ("H3","Booking System","Bsport: login,\navailability\nand payroll"),
    ],
    "toc_title": "Table of Contents",
    "welcome_title": "Welcome to Bright Panda",
    "chapter_label": "Chapter",
    "in_this_chapter": "IN THIS CHAPTER",
    "footer_text": "Bright Panda Teacher Guide  v1.1",
    "warn_prefix": "Note: ", "info_prefix": "Info: ",
    "captions": EN_CAPTIONS,
    "chapters": {
        "1": {"short":"How to make tutoring a success?","desc":"This chapter contains everything you need to get started as a tutor. From the matching process and preparing for your first trial lesson to didactic approaches, guiding diverse students and practical tools that make your work easier. This is the core of the teacher guide — read it carefully before your first lesson."},
        "2": {"short":"Code of Conduct","desc":"As a tutor at Bright Panda you represent our company. This chapter covers the professional standards, conduct rules and boundaries that apply to all tutors working via Bright Panda. From communication with parents and students to privacy, social media and personal presentation. These rules protect you, the student and Bright Panda."},
        "3": {"short":"Our booking system","desc":"Bright Panda uses Bsport as its booking system. This chapter walks you through logging in, setting your availability, checking booked lessons and viewing your payouts — step by step. Read this chapter carefully before you start teaching. Only booked lessons are paid out."},
    },
}


def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "nl"
    if lang == "en":
        md  = "/home/claude/docent_gids/en.md"
        out = "/mnt/user-data/outputs/Bright_Panda_Teacher_Guide_EN_v1.1.pdf"
        cfg = CFG_EN
        ch_marker = "CHAPTER"
    else:
        md  = "/home/claude/docent_gids/nl.md"
        out = "/mnt/user-data/outputs/Bright_Panda_Docent_Gids_NL_v1.1.pdf"
        cfg = CFG_NL
        ch_marker = "HOOFDSTUK"
    build_pdf(md, out, cfg, ch_marker)

if __name__ == "__main__":
    main()
