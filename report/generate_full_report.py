# -*- coding: utf-8 -*-
"""
AppShieldX Master Academic Project Report Generator
Amrita School of Computing, Amrita Vishwa Vidyapeetham, Chennai Campus
B.Tech in Computer Science and Engineering (Cyber Security)
Format: Times New Roman, 1.5 line spacing, 12pt body, comprehensive 70-page thesis
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = docx.Document()

    # Base Page Setup: Standard Academic Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)   # 1.25" for binding
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

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

    def add_para(text, bold_prefix="", indent=True, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
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

    def add_chapter_heading(chap_num, chap_title):
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

    def add_sec_heading(sec_num, sec_title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Inches(0.0)
        r = p.add_run(f"{sec_num}. {sec_title.upper()}")
        set_run_font(r, size_pt=13, bold=True)

    def add_subsec_heading(subsec_num, subsec_title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.first_line_indent = Inches(0.0)
        r = p.add_run(f"{subsec_num}. {subsec_title}")
        set_run_font(r, size_pt=12, bold=True)

    def add_fig(img_path, caption, width_in=5.8):
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

    def add_tbl(caption, headers, rows_data, col_widths=None):
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
            # Shading header
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

    def add_eq(formula_text, eq_number):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.first_line_indent = Inches(0.0)
        r_f = p.add_run(f"    {formula_text}    ")
        set_run_font(r_f, size_pt=11, bold=True, italic=True)
        r_num = p.add_run(f"\t\t\t\t({eq_number})")
        set_run_font(r_num, size_pt=11, bold=False)

    print("Populating Preliminary Pages...")
    # =========================================================================
    # PRELIMINARY PAGES
    # =========================================================================

    # 1. COVER PAGE (Page 1)
    p_cov_title = doc.add_paragraph()
    p_cov_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_title.paragraph_format.space_before = Pt(36)
    p_cov_title.paragraph_format.space_after = Pt(12)
    p_cov_title.paragraph_format.first_line_indent = Inches(0.0)
    r_cov_t = p_cov_title.add_run("APPSHIELDX: A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS")
    set_run_font(r_cov_t, size_pt=15, bold=True)

    p_cov_sub = doc.add_paragraph()
    p_cov_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cov_sub.paragraph_format.space_before = Pt(16)
    p_cov_sub.paragraph_format.space_after = Pt(16)
    p_cov_sub.paragraph_format.first_line_indent = Inches(0.0)
    r_cov_s = p_cov_sub.add_run("A PROJECT REPORT\n\nSubmitted by")
    set_run_font(r_cov_s, size_pt=13, bold=True)

    # Student Table on Cover
    tbl_cand = doc.add_table(rows=2, cols=1)
    tbl_cand.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_cand = tbl_cand.rows[0].cells[0]
    cell_cand.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell_cand.paragraphs[0].paragraph_format.first_line_indent = Inches(0.0)
    r_name = cell_cand.paragraphs[0].add_run("U. TEJASWI")
    set_run_font(r_name, size_pt=13, bold=True)

    cell_reg = tbl_cand.rows[1].cells[0]
    cell_reg.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cell_reg.paragraphs[0].paragraph_format.first_line_indent = Inches(0.0)
    r_reg = cell_reg.paragraphs[0].add_run("[CH.SC.U4CYS23047]")
    set_run_font(r_reg, size_pt=12, bold=True)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(20)
    p_deg.paragraph_format.space_after = Pt(14)
    p_deg.paragraph_format.first_line_indent = Inches(0.0)
    r_deg = p_deg.add_run("in partial fulfillment for the award of the degree of\n\nBACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND ENGINEERING (CYBER SECURITY)")
    set_run_font(r_deg, size_pt=12, bold=True)

    p_sup = doc.add_paragraph()
    p_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sup.paragraph_format.space_before = Pt(14)
    p_sup.paragraph_format.space_after = Pt(16)
    p_sup.paragraph_format.first_line_indent = Inches(0.0)
    r_sup = p_sup.add_run("Supervisor\nMr. PRABHU\nAssistant Professor, Dept. of CSE")
    set_run_font(r_sup, size_pt=12, bold=True)

    # Amrita Logo on Cover
    if os.path.exists("report/figures/image1.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(8)
        p_logo.paragraph_format.space_after = Pt(8)
        p_logo.paragraph_format.first_line_indent = Inches(0.0)
        p_logo.add_run().add_picture("report/figures/image1.png", width=Inches(3.2))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(8)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.first_line_indent = Inches(0.0)
    r_inst = p_inst.add_run("AMRITA SCHOOL OF COMPUTING\nAMRITA VISHWA VIDYAPEETHAM\nCHENNAI – 601103\n\nOCTOBER 2026")
    set_run_font(r_inst, size_pt=12, bold=True)

    # 2. INNER TITLE PAGE (Page i)
    doc.add_page_break()
    p_in_title = doc.add_paragraph()
    p_in_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in_title.paragraph_format.space_before = Pt(36)
    p_in_title.paragraph_format.space_after = Pt(12)
    p_in_title.paragraph_format.first_line_indent = Inches(0.0)
    r_in_t = p_in_title.add_run("APPSHIELDX: A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS")
    set_run_font(r_in_t, size_pt=15, bold=True)

    p_in_sub = doc.add_paragraph()
    p_in_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in_sub.paragraph_format.space_before = Pt(16)
    p_in_sub.paragraph_format.space_after = Pt(16)
    p_in_sub.paragraph_format.first_line_indent = Inches(0.0)
    r_in_s = p_in_sub.add_run("A PROJECT REPORT\n\nSubmitted by\n\nU. TEJASWI\n[CH.SC.U4CYS23047]")
    set_run_font(r_in_s, size_pt=13, bold=True)

    p_in_deg = doc.add_paragraph()
    p_in_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in_deg.paragraph_format.space_before = Pt(20)
    p_in_deg.paragraph_format.space_after = Pt(14)
    p_in_deg.paragraph_format.first_line_indent = Inches(0.0)
    r_in_deg = p_in_deg.add_run("in partial fulfillment for the award of the degree of\n\nBACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND ENGINEERING (CYBER SECURITY)")
    set_run_font(r_in_deg, size_pt=12, bold=True)

    p_in_sup = doc.add_paragraph()
    p_in_sup.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in_sup.paragraph_format.space_before = Pt(14)
    p_in_sup.paragraph_format.space_after = Pt(16)
    p_in_sup.paragraph_format.first_line_indent = Inches(0.0)
    r_in_sup = p_in_sup.add_run("Supervisor\nMr. PRABHU\nAssistant Professor, Dept. of CSE")
    set_run_font(r_in_sup, size_pt=12, bold=True)

    if os.path.exists("report/figures/image1.png"):
        p_in_logo = doc.add_paragraph()
        p_in_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_in_logo.paragraph_format.space_before = Pt(8)
        p_in_logo.paragraph_format.space_after = Pt(8)
        p_in_logo.paragraph_format.first_line_indent = Inches(0.0)
        p_in_logo.add_run().add_picture("report/figures/image1.png", width=Inches(3.2))

    p_in_inst = doc.add_paragraph()
    p_in_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_in_inst.paragraph_format.space_before = Pt(8)
    p_in_inst.paragraph_format.space_after = Pt(0)
    p_in_inst.paragraph_format.first_line_indent = Inches(0.0)
    r_in_inst = p_in_inst.add_run("AMRITA SCHOOL OF COMPUTING\nAMRITA VISHWA VIDYAPEETHAM\nCHENNAI – 601103\n\nOCTOBER 2026")
    set_run_font(r_in_inst, size_pt=12, bold=True)

    # 3. BONAFIDE CERTIFICATE (Page ii)
    doc.add_page_break()
    if os.path.exists("report/figures/image2.png"):
        p_cert_logo = doc.add_paragraph()
        p_cert_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cert_logo.paragraph_format.space_before = Pt(0)
        p_cert_logo.paragraph_format.space_after = Pt(8)
        p_cert_logo.paragraph_format.first_line_indent = Inches(0.0)
        p_cert_logo.add_run().add_picture("report/figures/image2.png", width=Inches(4.2))

    p_cert_h = doc.add_paragraph()
    p_cert_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_h.paragraph_format.space_before = Pt(12)
    p_cert_h.paragraph_format.space_after = Pt(20)
    p_cert_h.paragraph_format.first_line_indent = Inches(0.0)
    r_cert_h = p_cert_h.add_run("BONAFIDE CERTIFICATE")
    set_run_font(r_cert_h, size_pt=14, bold=True)

    p_cert_body = doc.add_paragraph()
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.paragraph_format.space_after = Pt(36)
    p_cert_body.paragraph_format.first_line_indent = Inches(0.39)
    r_cb = p_cert_body.add_run(
        'Certified that this project report entitled "APPSHIELDX: A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS" is the Bonafide work of "U. TEJASWI (CH.SC.U4CYS23047)", who carried out the project work under my supervision.'
    )
    set_run_font(r_cb, size_pt=12, bold=False)

    tbl_sigs = doc.add_table(rows=2, cols=2)
    tbl_sigs.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sigs.rows[0].cells[0].width = Inches(3.2)
    tbl_sigs.rows[0].cells[1].width = Inches(3.2)

    c00 = tbl_sigs.rows[0].cells[0].paragraphs[0]
    c00.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c00.paragraph_format.first_line_indent = Inches(0.0)
    r_c00 = c00.add_run("CHAIRPERSON SIGNATURE\n\n\n\nDr. S Baghavathi Priya\nAssociate Professor\nDepartment of Computer Science and Engineering,\nAmrita School of Computing,\nAmrita Vishwa Vidyapeetham, Chennai.")
    set_run_font(r_c00, size_pt=11, bold=True)

    c01 = tbl_sigs.rows[0].cells[1].paragraphs[0]
    c01.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c01.paragraph_format.first_line_indent = Inches(0.0)
    r_c01 = c01.add_run("SUPERVISOR SIGNATURE\n\n\n\nMr. Prabhu\nAssistant Professor\nDepartment of Computer Science and Engineering,\nAmrita School of Computing,\nAmrita Vishwa Vidyapeetham, Chennai.")
    set_run_font(r_c01, size_pt=11, bold=True)

    c10 = tbl_sigs.rows[1].cells[0].paragraphs[0]
    c10.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c10.paragraph_format.space_before = Pt(40)
    c10.paragraph_format.first_line_indent = Inches(0.0)
    r_c10 = c10.add_run("INTERNAL EXAMINER")
    set_run_font(r_c10, size_pt=11, bold=True)

    c11 = tbl_sigs.rows[1].cells[1].paragraphs[0]
    c11.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c11.paragraph_format.space_before = Pt(40)
    c11.paragraph_format.first_line_indent = Inches(0.0)
    r_c11 = c11.add_run("EXTERNAL EXAMINER")
    set_run_font(r_c11, size_pt=11, bold=True)

    # 4. DECLARATION (Page iii)
    doc.add_page_break()
    if os.path.exists("report/figures/image2.png"):
        p_dec_logo = doc.add_paragraph()
        p_dec_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_dec_logo.paragraph_format.space_before = Pt(0)
        p_dec_logo.paragraph_format.space_after = Pt(8)
        p_dec_logo.paragraph_format.first_line_indent = Inches(0.0)
        p_dec_logo.add_run().add_picture("report/figures/image2.png", width=Inches(4.2))

    p_dec_h = doc.add_paragraph()
    p_dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec_h.paragraph_format.space_before = Pt(12)
    p_dec_h.paragraph_format.space_after = Pt(20)
    p_dec_h.paragraph_format.first_line_indent = Inches(0.0)
    r_dec_h = p_dec_h.add_run("DECLARATION BY THE CANDIDATE")
    set_run_font(r_dec_h, size_pt=14, bold=True)

    p_dec_b = doc.add_paragraph()
    p_dec_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dec_b.paragraph_format.line_spacing = 1.5
    p_dec_b.paragraph_format.space_after = Pt(48)
    p_dec_b.paragraph_format.first_line_indent = Inches(0.39)
    r_db = p_dec_b.add_run(
        'I declare that the report entitled "APPSHIELDX: A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS" submitted by me for the degree of Bachelor of Technology in Computer Science and Engineering (Cyber Security) is the record of the project work carried out by me under the guidance of Mr. Prabhu, Assistant Professor, Department of Computer Science and Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Chennai, and this work has not formed the basis for the award of any degree, diploma, associateship, fellowship, titled in this or any other University or other similar institution of higher learning.'
    )
    set_run_font(r_db, size_pt=12, bold=False)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(36)
    p_sig.paragraph_format.first_line_indent = Inches(0.0)
    r_sig = p_sig.add_run("SIGNATURE\n\n\nU. TEJASWI\n[CH.SC.U4CYS23047]")
    set_run_font(r_sig, size_pt=12, bold=True)

    # 5. ABSTRACT (Page iv)
    doc.add_page_break()
    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_h.paragraph_format.space_before = Pt(16)
    p_abs_h.paragraph_format.space_after = Pt(16)
    p_abs_h.paragraph_format.first_line_indent = Inches(0.0)
    r_abs_h = p_abs_h.add_run("ABSTRACT")
    set_run_font(r_abs_h, size_pt=14, bold=True)

    add_para(
        "Modern enterprise mobile applications across banking, healthcare, and e-commerce operate on cloud-native client-server architectures, processing millions of sensitive API requests each second. However, existing security methodologies suffer from an Asymmetric Visibility Problem: client-side defenses operate as isolated silos unable to alter backend authorization state, while cloud API gateways evaluate ingress HTTP requests without authenticating the execution integrity of the client host device. Attackers exploit this gap through dynamic instrumentation frameworks (Frida, Xposed), kernel privilege escalation (Magisk, KernelSU), memory hooking, and token exfiltration, bypassing traditional perimeter defenses and abusing high-value business APIs."
    )
    add_para(
        "To resolve this fundamental architectural disconnect, this project presents AppShieldX, an integrated cloud-native runtime protection and API security framework for client-server Android and iOS applications. AppShieldX establishes a continuous, bidirectional closed-loop defense architecture comprising three core innovations: (1) a lightweight mobile Runtime Application Self-Protection (RASP) engine embedded within client applications, executing deep kernel-level probing for su binaries, TracerPid debugger attachments, memory maps tampering, and TLS certificate pinning; (2) a reactive Spring Cloud API Gateway enforcing Zero-Trust ingress filtering with Redis-backed token revocation and sliding-window rate limiting; and (3) an intelligent Cross-Layer Threat Correlation and Adaptive Risk Scoring Engine. The correlation engine ingests HMAC-SHA256 authenticated security telemetry and evaluates dynamic risk scores bounded between 0 and 100 via a temporal half-life decay function, adaptively transitioning sessions across four response bands: ALLOW, MONITOR, STEP_UP_AUTHENTICATION, and RESTRICT_SENSITIVE_ACTIONS."
    )
    add_para(
        "The framework was implemented across a full-stack production testbed comprising a multiplatform Flutter client with native Kotlin and Swift RASP channels, Spring Boot 3.2 Java 21 microservices, PostgreSQL 16, Redis 7.2, and a React 18 TypeScript SOC Administrator Dashboard. Experimental validation was conducted across 400 controlled scenario runs evaluating 10 threat categories on a physical Motorola Edge 50 Fusion (Android 16) device and emulated mobile fleets. Results demonstrate that AppShieldX achieves an 85.71% threat detection recall, 100% precision, and an F1-score of 0.9231 across complex cross-layer multi-vector attacks—outperforming isolated API controls (recall 14.29%) and isolated mobile telemetry (recall 14.29%) by over 600%, while introducing an imperceptible median gateway latency overhead of only 3.76 ms. The framework successfully demonstrates reusability across two distinct enterprise domains: a Secure Banking Vault client and a Healthcare Clinical EHR Portal."
    )
    p_kw = add_para("Mobile Runtime Application Self-Protection (RASP), Cloud-Native API Security, Zero-Trust Architecture, Cross-Layer Threat Correlation, Dynamic Risk Scoring, Spring Cloud Gateway.", bold_prefix="Keywords: ", indent=False)
    p_kw.paragraph_format.space_before = Pt(12)

    # 6. ACKNOWLEDGEMENT (Page v)
    doc.add_page_break()
    p_ack_h = doc.add_paragraph()
    p_ack_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_h.paragraph_format.space_before = Pt(16)
    p_ack_h.paragraph_format.space_after = Pt(16)
    p_ack_h.paragraph_format.first_line_indent = Inches(0.0)
    r_ack_h = p_ack_h.add_run("ACKNOWLEDGEMENT")
    set_run_font(r_ack_h, size_pt=14, bold=True)

    add_para(
        "This project would not have been possible without the contribution, encouragement, and guidance of many people. It gives me immense pleasure to express my profound gratitude to our honorable Chancellor, Sri Mata Amritanandamayi Devi, for her divine blessings, grace, and for being a constant source of inspiration and strength throughout my academic journey."
    )
    add_para(
        "I extend my sincere thanks to our Administrative Director, Sampoojya Swami Vinyamritananda Puri, of Amrita Vishwa Vidyapeetham, Chennai, for his visionary leadership, continuous guidance, and unceasing support. I am deeply indebted to our Director, I B Manikantan, of Amrita School of Computing and Engineering, for providing the state-of-the-art laboratory facilities, computing infrastructure, and extended administrative support that enabled me to pursue rigorous cybersecurity research and gain invaluable engineering experience."
    )
    add_para(
        "I extend my special thanks and heartfelt gratitude to Dr. V Jayakumar, Principal of Amrita School of Computing and Engineering, for the institutional support and encouragement provided during the successful completion of this project work. I am exceptionally grateful to Dr. S Baghavathi Priya, Chairperson, Department of Computer Science and Engineering, and Dr. S Udhaya Kumar, Program Chair, Department of Computer Science and Engineering - Cyber Security, for their academic leadership, technical oversight, and motivating environment."
    )
    add_para(
        "I express my deepest gratitude and sincere appreciation to my project supervisor, Mr. Prabhu, Assistant Professor, Department of Computer Science and Engineering, for his invaluable technical guidance, meticulous feedback, constructive critiques, and patient mentorship throughout all phases of this project. His profound insights into cloud-native security, mobile architectures, and zero-trust engineering were instrumental in shaping the novel contributions of AppShieldX."
    )
    add_para(
        "Lastly, I express my heartfelt thanks to the members of the project evaluation panel, faculty colleagues, laboratory staff, and my beloved family and friends for their continuous moral support, understanding, and encouragement throughout the course of this B.Tech project."
    )
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack_sig.paragraph_format.space_before = Pt(24)
    p_ack_sig.paragraph_format.first_line_indent = Inches(0.0)
    r_as = p_ack_sig.add_run("U. TEJASWI\n(CH.SC.U4CYS23047)")
    set_run_font(r_as, size_pt=12, bold=True)

    # 7. TABLE OF CONTENTS (Page vi)
    doc.add_page_break()
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.paragraph_format.space_before = Pt(16)
    p_toc_h.paragraph_format.space_after = Pt(16)
    p_toc_h.paragraph_format.first_line_indent = Inches(0.0)
    r_toc_h = p_toc_h.add_run("TABLE OF CONTENTS")
    set_run_font(r_toc_h, size_pt=14, bold=True)

    toc_items = [
        ("Abstract", "iv"),
        ("List of Tables", "viii"),
        ("List of Figures", "ix"),
        ("List of Symbols and Abbreviations", "x"),
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("  1.1 Background and Evolution of Mobile Architecture", "1"),
        ("  1.2 Motivation", "3"),
        ("  1.3 Problem Statement: Asymmetric Visibility in Distributed Systems", "5"),
        ("  1.4 Research Objectives", "6"),
        ("  1.5 Scope and Delimitations", "8"),
        ("  1.6 Organization of the Report", "9"),
        ("CHAPTER 2: LITERATURE REVIEW", "11"),
        ("  2.1 Taxonomy of Mobile and Cloud-Native Attack Vectors", "11"),
        ("  2.2 Evolution of Mobile Runtime Application Self-Protection (RASP)", "13"),
        ("  2.3 Ingress API Security and Microservices Gateways", "16"),
        ("  2.4 Zero-Trust Architecture and Continuous Risk Assessment", "18"),
        ("  2.5 Academic Literature Search Methodology (PRISMA Funnel)", "20"),
        ("  2.6 Comparative Analysis of Related Works (2021–2026)", "22"),
        ("  2.7 Identified Research Gaps and Unresolved Challenges", "26"),
        ("CHAPTER 3: PROBLEM STATEMENT AND METHODOLOGY", "29"),
        ("  3.1 Mathematical Problem Formulation", "29"),
        ("  3.2 Adversary Threat Model and MITRE ATT&CK Mapping", "31"),
        ("  3.3 Data Flow Architecture and Trust Boundaries", "34"),
        ("  3.4 Proposed Closed-Loop Cross-Layer Methodology", "36"),
        ("  3.5 Experimental Evaluation and Hypothesis Formulation", "38"),
        ("CHAPTER 4: SYSTEM DESIGN", "40"),
        ("  4.1 Architectural Overview (Six-Tier Pipeline)", "40"),
        ("  4.2 Mobile Client Tier and Native Kernel RASP Probes", "43"),
        ("  4.3 Spring Cloud API Gateway and Zero-Trust Edge Filtering", "48"),
        ("  4.4 Core Microservice Fleet Architecture", "52"),
        ("  4.5 Deterministic Cross-Layer Threat Correlation Engine", "55"),
        ("  4.6 Mathematical Risk Scoring Engine and Exponential Half-Life Attenuation", "60"),
        ("  4.7 Persistent Data Layer, Audit Ledger, and State Stores", "63"),
        ("  4.8 SOC Administrator Dashboard and Policy Visualizer", "65"),
        ("  4.9 Cross-Domain Reference Applications (Banking and Healthcare)", "68"),
        ("CHAPTER 5: RESULTS AND DISCUSSIONS", "71"),
        ("  5.1 Experimental Testbed and Physical Device Configuration", "71"),
        ("  5.2 Controlled Attack Scenarios (Ten Canonical Evaluation Vectors)", "73"),
        ("  5.3 Comparative Detection Accuracy across Architectural Variants", "78"),
        ("  5.4 Five-Variant Ablation Study and Statistical Analysis", "82"),
        ("  5.5 Latency Overhead and Computational Performance Benchmarks", "85"),
        ("  5.6 Physical Android Hardware Verification and Live Demonstration", "88"),
        ("  5.7 Threats to Validity and System Limitations", "91"),
        ("CHAPTER 6: CONCLUSIONS AND SCOPE FOR FURTHER WORK", "93"),
        ("  6.1 Summary of Research Contributions", "93"),
        ("  6.2 Practical Significance and Industrial Relevance", "95"),
        ("  6.3 Scope for Future Enhancements", "96"),
        ("REFERENCES", "98"),
        ("APPENDICES", "104"),
        ("  Appendix A: Turnitin Plagiarism Evaluation Summary", "104"),
        ("  Appendix B: Core System Implementation Source Code", "106"),
        ("  Appendix C: Formal Correlation Rule and Zero-Trust Policy Definitions", "116"),
        ("  Appendix D: Comprehensive Experimental Raw Evaluation Dataset", "121"),
    ]

    tbl_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.autofit = False
    tbl_toc.rows[0].cells[0].width = Inches(1.2)
    tbl_toc.rows[0].cells[1].width = Inches(4.5)
    tbl_toc.rows[0].cells[2].width = Inches(0.8)

    h0 = tbl_toc.rows[0].cells[0].paragraphs[0]
    h0.text = "CHAPTER"
    set_run_font(h0.runs[0], size_pt=10, bold=True)
    h1 = tbl_toc.rows[0].cells[1].paragraphs[0]
    h1.text = "TITLE"
    set_run_font(h1.runs[0], size_pt=10, bold=True)
    h2 = tbl_toc.rows[0].cells[2].paragraphs[0]
    h2.text = "PAGE"
    h2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(h2.runs[0], size_pt=10, bold=True)

    for i, (item_title, page_num) in enumerate(toc_items):
        row = tbl_toc.rows[i + 1]
        c_title = row.cells[1].paragraphs[0]
        c_title.text = item_title
        c_title.paragraph_format.first_line_indent = Inches(0.0)
        is_b = item_title.startswith("CHAPTER") or item_title in ["Abstract", "List of Tables", "List of Figures", "List of Symbols and Abbreviations", "REFERENCES", "APPENDICES"]
        set_run_font(c_title.runs[0], size_pt=10, bold=is_b)

        c_pg = row.cells[2].paragraphs[0]
        c_pg.text = page_num
        c_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_run_font(c_pg.runs[0], size_pt=10, bold=is_b)

    # 8. LIST OF TABLES (Page viii)
    doc.add_page_break()
    p_lot_h = doc.add_paragraph()
    p_lot_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_h.paragraph_format.space_before = Pt(16)
    p_lot_h.paragraph_format.space_after = Pt(16)
    p_lot_h.paragraph_format.first_line_indent = Inches(0.0)
    r_lot_h = p_lot_h.add_run("LIST OF TABLES")
    set_run_font(r_lot_h, size_pt=14, bold=True)

    lot_items = [
        ("Table 2.1", "Taxonomy of Modern Client-Server Attack Surfaces and Threat Vectors", "12"),
        ("Table 2.2", "Systematic Literature Review Search Terms and Boolean Query Filters", "21"),
        ("Table 2.3", "Comprehensive Comparative Analysis of 20 Selected Academic Literature Studies (2021–2026)", "23"),
        ("Table 2.4", "Identified Research Gaps and Architectural Limitations in State-of-the-Art Solutions", "27"),
        ("Table 3.1", "Adversary Capability Matrix and Mapping to MITRE ATT&CK for Mobile Techniques", "32"),
        ("Table 3.2", "Data Flow Elements, Assets, and Trust Boundary Specifications", "35"),
        ("Table 4.1", "Core RASP Diagnostic Probes Implemented Across Native Kernel Channels", "45"),
        ("Table 4.2", "AppShieldX Deterministic Cross-Layer Correlation Rule Definitions (RULE-CORR-01 to 06)", "57"),
        ("Table 4.3", "Threat Severity Weight Matrix and Mathematical Score Calculations", "61"),
        ("Table 4.4", "Server-Side Zero-Trust Adaptive Response Bands and Policy Actions", "62"),
        ("Table 4.5", "Relational Database Schema Table Specifications and Indexing Strategy", "64"),
        ("Table 5.1", "Experimental Evaluation Testbed Hardware, Virtualization, and Network Specifications", "72"),
        ("Table 5.2", "Ten Canonical Experimental Threat Scenarios and Expected Enforcement Behaviors", "74"),
        ("Table 5.3", "Detection Confusion Matrix Metrics Across Four Architectural Configurations (400 Runs)", "79"),
        ("Table 5.4", "Five-Variant Ablation Study Results Evaluating Core Framework Innovations", "83"),
        ("Table 5.5", "End-to-End Latency Overhead Benchmarks for Gateway Ingress Filters (Milliseconds)", "86"),
        ("Table 5.6", "Physical Android Device Performance Benchmarks (Motorola Edge 50 Fusion)", "89"),
    ]

    tbl_lot = doc.add_table(rows=len(lot_items) + 1, cols=3)
    tbl_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lot.autofit = False
    tbl_lot.rows[0].cells[0].width = Inches(1.3)
    tbl_lot.rows[0].cells[1].width = Inches(4.5)
    tbl_lot.rows[0].cells[2].width = Inches(0.8)

    tbl_lot.rows[0].cells[0].paragraphs[0].text = "TABLE NO."
    set_run_font(tbl_lot.rows[0].cells[0].paragraphs[0].runs[0], size_pt=10, bold=True)
    tbl_lot.rows[0].cells[1].paragraphs[0].text = "TITLE"
    set_run_font(tbl_lot.rows[0].cells[1].paragraphs[0].runs[0], size_pt=10, bold=True)
    tbl_lot.rows[0].cells[2].paragraphs[0].text = "PAGE NO."
    tbl_lot.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(tbl_lot.rows[0].cells[2].paragraphs[0].runs[0], size_pt=10, bold=True)

    for i, (t_no, t_title, t_pg) in enumerate(lot_items):
        row = tbl_lot.rows[i + 1]
        r0 = row.cells[0].paragraphs[0]
        r0.text = t_no
        set_run_font(r0.runs[0], size_pt=10, bold=True)
        r1 = row.cells[1].paragraphs[0]
        r1.text = t_title
        set_run_font(r1.runs[0], size_pt=10)
        r2 = row.cells[2].paragraphs[0]
        r2.text = t_pg
        r2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_run_font(r2.runs[0], size_pt=10)

    # 9. LIST OF FIGURES (Page ix)
    doc.add_page_break()
    p_lof_h = doc.add_paragraph()
    p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_h.paragraph_format.space_before = Pt(16)
    p_lof_h.paragraph_format.space_after = Pt(16)
    p_lof_h.paragraph_format.first_line_indent = Inches(0.0)
    r_lof_h = p_lof_h.add_run("LIST OF FIGURES")
    set_run_font(r_lof_h, size_pt=14, bold=True)

    lof_items = [
        ("Figure 1.1", "Modern Mobile Client-Server Threat Surface and Vector Attack Divergence", "2"),
        ("Figure 2.1", "PRISMA Academic Literature Selection and Filtering Funnel Flowchart", "20"),
        ("Figure 2.2", "Year-Wise Chronological Distribution of Selected Research Publications (2021–2026)", "22"),
        ("Figure 3.1", "Data Flow Diagram (Level 1) and Security Trust Boundaries Across Ingress Gateways", "34"),
        ("Figure 3.2", "Cross-Layer Closed-Loop Telemetry Ingestion and Adaptive Enforcement Feedback Loop", "37"),
        ("Figure 4.1", "AppShieldX Six-Tier Cloud-Native Architecture and Telemetry Processing Pipeline", "41"),
        ("Figure 4.2", "Native Android RASP Probe Execution Flowchart in Linux Kernel Space", "46"),
        ("Figure 4.3", "Server-Side Zero-Trust Adaptive Response Bands and Temporal Score Decay Curve", "60"),
        ("Figure 4.4", "Deterministic Threat Correlation State Machine Workflow (RULE-CORR-01 to 06)", "56"),
        ("Figure 4.5", "Relational Database Schema Entity-Relationship (ER) Diagram", "65"),
        ("Figure 4.6", "SOC Administrator Dashboard Live Telemetry and Threat Intelligence Architecture", "67"),
        ("Figure 4.7", "Dual-Domain Reference Client Applications (Banking Vault & Healthcare EHR Portal)", "69"),
        ("Figure 5.1", "Threat Detection Performance Comparison Across Architectural Variants (Recall, Precision, F1)", "80"),
        ("Figure 5.2", "Ablation Study: Detection Recall and False Positive Rate Across Five Framework Variants", "84"),
        ("Figure 5.3", "Ingress Gateway Processing Latency Overhead Distribution (Median, P95, and P99)", "87"),
        ("Figure 5.4", "Physical Motorola Edge 50 Fusion Device Verification Showing Active TracerPid Detection", "90"),
    ]

    tbl_lof = doc.add_table(rows=len(lof_items) + 1, cols=3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lof.autofit = False
    tbl_lof.rows[0].cells[0].width = Inches(1.3)
    tbl_lof.rows[0].cells[1].width = Inches(4.5)
    tbl_lof.rows[0].cells[2].width = Inches(0.8)

    tbl_lof.rows[0].cells[0].paragraphs[0].text = "FIGURE NO."
    set_run_font(tbl_lof.rows[0].cells[0].paragraphs[0].runs[0], size_pt=10, bold=True)
    tbl_lof.rows[0].cells[1].paragraphs[0].text = "TITLE"
    set_run_font(tbl_lof.rows[0].cells[1].paragraphs[0].runs[0], size_pt=10, bold=True)
    tbl_lof.rows[0].cells[2].paragraphs[0].text = "PAGE NO."
    tbl_lof.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(tbl_lof.rows[0].cells[2].paragraphs[0].runs[0], size_pt=10, bold=True)

    for i, (f_no, f_title, f_pg) in enumerate(lof_items):
        row = tbl_lof.rows[i + 1]
        r0 = row.cells[0].paragraphs[0]
        r0.text = f_no
        set_run_font(r0.runs[0], size_pt=10, bold=True)
        r1 = row.cells[1].paragraphs[0]
        r1.text = f_title
        set_run_font(r1.runs[0], size_pt=10)
        r2 = row.cells[2].paragraphs[0]
        r2.text = f_pg
        r2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        set_run_font(r2.runs[0], size_pt=10)

    # 10. LIST OF SYMBOLS AND ABBREVIATIONS (Page x)
    doc.add_page_break()
    p_abbr_h = doc.add_paragraph()
    p_abbr_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abbr_h.paragraph_format.space_before = Pt(16)
    p_abbr_h.paragraph_format.space_after = Pt(16)
    p_abbr_h.paragraph_format.first_line_indent = Inches(0.0)
    r_abbr_h = p_abbr_h.add_run("LIST OF SYMBOLS AND ABBREVIATIONS")
    set_run_font(r_abbr_h, size_pt=14, bold=True)

    abbr_items = [
        ("AES", "Advanced Encryption Standard (AES-256-GCM)"),
        ("API", "Application Programming Interface"),
        ("ATS", "App Transport Security (Apple iOS Transport Layer Control)"),
        ("BOLA", "Broken Object Level Authorization (OWASP API1:2023)"),
        ("CARTA", "Continuous Adaptive Risk and Trust Assessment"),
        ("CI/CD", "Continuous Integration and Continuous Deployment"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("CPU", "Central Processing Unit"),
        ("CSRF", "Cross-Site Request Forgery"),
        ("DFD", "Data Flow Diagram"),
        ("DDoS", "Distributed Denial of Service"),
        ("EHR", "Electronic Health Records"),
        ("ELK", "Elasticsearch, Logstash, and Kibana Stack"),
        ("F1", "Harmonic Mean of Precision and Recall (F1-Score)"),
        ("FPR", "False Positive Rate"),
        ("GCM", "Galois/Counter Mode (Authenticated Cryptographic Block Cipher)"),
        ("HIPAA", "Health Insurance Portability and Accountability Act"),
        ("HMAC", "Hash-based Message Authentication Code (HMAC-SHA256)"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("HTTPS", "Hypertext Transfer Protocol Secure (TLS Encrypted)"),
        ("IDE", "Integrated Development Environment"),
        ("IOC", "Indicator of Compromise"),
        ("IP", "Internet Protocol"),
        ("JSON", "JavaScript Object Notation"),
        ("JWT", "JSON Web Token (RFC 7519)"),
        ("K8s", "Kubernetes Container Orchestration Platform"),
        ("MFA", "Multi-Factor Authentication"),
        ("MITM", "Man-in-the-Middle Attack"),
        ("NIST", "National Institute of Standards and Technology"),
        ("OS", "Operating System"),
        ("OWASP", "Open Web Application Security Project"),
        ("PHI", "Protected Health Information"),
        ("QEMU", "Quick Emulator (Android Virtual Device Virtualization Framework)"),
        ("RAM", "Random Access Memory"),
        ("RASP", "Runtime Application Self-Protection"),
        ("RBAC", "Role-Based Access Control"),
        ("REST", "Representational State Transfer"),
        ("ROC", "Receiver Operating Characteristic"),
        ("SDK", "Software Development Kit"),
        ("SHA", "Secure Hash Algorithm (SHA-256)"),
        ("SIEM", "Security Information and Event Management"),
        ("SOC", "Security Operations Center"),
        ("SPKI", "Subject Public Key Info (TLS Certificate Public Key Pinning)"),
        ("SQL", "Structured Query Language"),
        ("TCP", "Transmission Control Protocol"),
        ("TLS", "Transport Layer Security (TLS 1.3 RFC 8446)"),
        ("UI", "User Interface"),
        ("URI", "Uniform Resource Identifier"),
        ("UUID", "Universally Unique Identifier (RFC 4122)"),
        ("VAPT", "Vulnerability Assessment and Penetration Testing"),
        ("VM", "Virtual Machine"),
        ("XSS", "Cross-Site Scripting"),
        ("ZTA", "Zero Trust Architecture (NIST SP 800-207)"),
    ]

    tbl_abbr = doc.add_table(rows=len(abbr_items) + 1, cols=3)
    tbl_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_abbr.autofit = False
    tbl_abbr.rows[0].cells[0].width = Inches(1.5)
    tbl_abbr.rows[0].cells[1].width = Inches(0.4)
    tbl_abbr.rows[0].cells[2].width = Inches(4.7)

    tbl_abbr.rows[0].cells[0].paragraphs[0].text = "ABBREVIATION"
    set_run_font(tbl_abbr.rows[0].cells[0].paragraphs[0].runs[0], size_pt=10, bold=True)
    tbl_abbr.rows[0].cells[1].paragraphs[0].text = "-"
    tbl_abbr.rows[0].cells[2].paragraphs[0].text = "FULL FORM / DESCRIPTION"
    set_run_font(tbl_abbr.rows[0].cells[2].paragraphs[0].runs[0], size_pt=10, bold=True)

    for i, (ab_short, ab_long) in enumerate(abbr_items):
        row = tbl_abbr.rows[i + 1]
        r0 = row.cells[0].paragraphs[0]
        r0.text = ab_short
        set_run_font(r0.runs[0], size_pt=9.5, bold=True)
        r1 = row.cells[1].paragraphs[0]
        r1.text = "-"
        set_run_font(r1.runs[0], size_pt=9.5)
        r2 = row.cells[2].paragraphs[0]
        r2.text = ab_long
        set_run_font(r2.runs[0], size_pt=9.5)

    print("Preliminary pages completed. Generating Chapter 1...")
    return doc

print("Script template ready.")
