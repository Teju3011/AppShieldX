# -*- coding: utf-8 -*-
"""
Report Helper Utilities for AppShieldX Academic Report
Ensures strict Times New Roman typography, 1.5 line spacing, academic margins,
table styling, figure embedding, and formula formatting.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_run_font(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    else:
        run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)

def add_para(doc, text, bold_prefix="", indent=True, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.39) # 1 cm indent
    else:
        p.paragraph_format.first_line_indent = Inches(0.0)

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        set_run_font(r_pre, size_pt=12, bold=True)
    r_text = p.add_run(text)
    set_run_font(r_text, size_pt=12, bold=False)
    return p

def add_bullet(doc, text, bold_prefix="", level=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.35 * (level + 1))
    p.paragraph_format.first_line_indent = Inches(-0.2)

    r_bullet = p.add_run("•  ")
    set_run_font(r_bullet, size_pt=12, bold=True)

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        set_run_font(r_pre, size_pt=12, bold=True)
    r_text = p.add_run(text)
    set_run_font(r_text, size_pt=12, bold=False)
    return p

def add_chapter_heading(doc, chap_num, chap_title):
    if chap_num != 1:
        doc.add_page_break()
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(12)
    p1.paragraph_format.space_after = Pt(4)
    p1.paragraph_format.first_line_indent = Inches(0.0)
    r1 = p1.add_run(f"CHAPTER {chap_num}")
    set_run_font(r1, size_pt=16, bold=True)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(18)
    p2.paragraph_format.first_line_indent = Inches(0.0)
    r2 = p2.add_run(chap_title.upper())
    set_run_font(r2, size_pt=14, bold=True)

def add_sec_heading(doc, sec_num, sec_title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Inches(0.0)
    r = p.add_run(f"{sec_num}. {sec_title.upper()}")
    set_run_font(r, size_pt=13, bold=True)

def add_subsec_heading(doc, subsec_num, subsec_title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Inches(0.0)
    r = p.add_run(f"{subsec_num}. {subsec_title}")
    set_run_font(r, size_pt=12, bold=True)

def add_subsubsec_heading(doc, subsubsec_num, subsubsec_title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.first_line_indent = Inches(0.0)
    r = p.add_run(f"{subsubsec_num}. {subsubsec_title}")
    set_run_font(r, size_pt=12, bold=True, italic=True)

def add_fig(doc, img_path, caption, width_in=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.first_line_indent = Inches(0.0)
        p_img.add_run().add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    p_cap.paragraph_format.first_line_indent = Inches(0.0)
    r_cap = p_cap.add_run(caption)
    set_run_font(r_cap, size_pt=11, bold=True, italic=True)

def add_tbl(doc, caption, headers, rows_data, col_widths=None):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.first_line_indent = Inches(0.0)
    r_cap = p_cap.add_run(caption)
    set_run_font(r_cap, size_pt=11, bold=True)

    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Format Header Row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        cell = hdr_cells[i]
        cell.text = header_text
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.paragraphs[0].paragraph_format.space_before = Pt(3)
        cell.paragraphs[0].paragraph_format.space_after = Pt(3)
        set_run_font(cell.paragraphs[0].runs[0], size_pt=10, bold=True)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9D9D9"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    # Format Data Rows
    for r_idx, row_values in enumerate(rows_data):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_values):
            cell = row_cells[c_idx]
            cell.text = str(val)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].paragraph_format.space_before = Pt(2)
            cell.paragraphs[0].paragraph_format.space_after = Pt(2)
            if cell.paragraphs[0].runs:
                set_run_font(cell.paragraphs[0].runs[0], size_pt=9.5)

    # Set Column Widths if provided
    if col_widths:
        for row in table.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Inches(w)

    # Table Borders
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_eq(doc, formula_text, eq_number):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Inches(0.0)
    r_f = p.add_run(f"    {formula_text}    ")
    set_run_font(r_f, size_pt=11, bold=True, italic=True)
    r_num = p.add_run(f"\t\t\t\t({eq_number})")
    set_run_font(r_num, size_pt=11, bold=False)

def add_code_block(doc, code_str, caption=""):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.first_line_indent = Inches(0.0)
        r_c = p_cap.add_run(caption)
        set_run_font(r_c, size_pt=10, bold=True, italic=True)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.25)
    
    cell = tbl.rows[0].cells[0]
    cell.paragraphs[0].text = code_str.strip()
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    cell.paragraphs[0].paragraph_format.line_spacing = 1.0
    cell.paragraphs[0].paragraph_format.space_before = Pt(4)
    cell.paragraphs[0].paragraph_format.space_after = Pt(4)
    cell.paragraphs[0].paragraph_format.first_line_indent = Inches(0.0)
    set_run_font(cell.paragraphs[0].runs[0], font_name="Courier New", size_pt=8.5)

    # Light grey background
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F5F5F5"/>')
    cell._tc.get_or_add_tcPr().append(shd)

    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'</w:tblBorders>'
    )
    tbl._tbl.tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
