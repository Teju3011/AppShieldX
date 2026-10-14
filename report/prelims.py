# -*- coding: utf-8 -*-
"""
Preliminary Pages Generator for AppShieldX Project Report
Adheres strictly to Amrita School of Computing thesis template.
Features strict single-page preliminary sheets, lowerRoman page numbering,
and seamless section break to Chapter 1 starting at Page 1.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from report_helpers import set_run_font, add_para

def add_footer_page_number(section, start_fmt="lowerRoman", start_num=1):
    sectPr = section._sectPr
    pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="{start_num}" w:fmt="{start_fmt}"/>')
    sectPr.append(pgNumType)

    p_foot = section.footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(0)
    p_foot.paragraph_format.space_after = Pt(0)
    r = p_foot.add_run()
    set_run_font(r, font_name="Times New Roman", size_pt=11)
    fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
    r._r.append(fld)

def generate_preliminary_pages(doc, figures_dir, toc_mapping=None, lot_mapping=None, lof_mapping=None):
    logo1_path = os.path.join(figures_dir, "image1.png")
    logo2_path = os.path.join(figures_dir, "image2.png")

    s1 = doc.sections[0]
    s1.different_first_page_header_footer = True
    add_footer_page_number(s1, start_fmt="lowerRoman", start_num=1)

    # =========================================================================
    # 1. COVER PAGE (Page 1 - No footer displayed)
    # =========================================================================
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(16)
    p1.paragraph_format.space_after = Pt(10)
    p1.paragraph_format.first_line_indent = Inches(0.0)
    r1 = p1.add_run("APPSHIELDX – A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS")
    set_run_font(r1, size_pt=14, bold=True)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(10)
    p2.paragraph_format.space_after = Pt(12)
    p2.paragraph_format.first_line_indent = Inches(0.0)
    r2 = p2.add_run("A PROJECT REPORT")
    set_run_font(r2, size_pt=12.5, bold=True)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(4)
    p3.paragraph_format.space_after = Pt(2)
    p3.paragraph_format.first_line_indent = Inches(0.0)
    r3 = p3.add_run("Submitted by")
    set_run_font(r3, size_pt=11, italic=True)

    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p4.paragraph_format.space_before = Pt(6)
    p4.paragraph_format.space_after = Pt(2)
    p4.paragraph_format.first_line_indent = Inches(0.0)
    r4 = p4.add_run("U. TEJASWI\n[CH.SC.U4CYS23047]")
    set_run_font(r4, size_pt=11.5, bold=True)

    p5 = doc.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p5.paragraph_format.space_before = Pt(12)
    p5.paragraph_format.space_after = Pt(4)
    p5.paragraph_format.first_line_indent = Inches(0.0)
    r5 = p5.add_run("in partial fulfillment for the award of the degree of")
    set_run_font(r5, size_pt=11, italic=True)

    p6 = doc.add_paragraph()
    p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p6.paragraph_format.space_before = Pt(4)
    p6.paragraph_format.space_after = Pt(12)
    p6.paragraph_format.first_line_indent = Inches(0.0)
    r6 = p6.add_run("BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND\nENGINEERING (CYBER SECURITY)")
    set_run_font(r6, size_pt=12, bold=True)

    p7 = doc.add_paragraph()
    p7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p7.paragraph_format.space_before = Pt(6)
    p7.paragraph_format.space_after = Pt(2)
    p7.paragraph_format.first_line_indent = Inches(0.0)
    r7 = p7.add_run("Supervisor")
    set_run_font(r7, size_pt=11, italic=True)

    p8 = doc.add_paragraph()
    p8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p8.paragraph_format.space_before = Pt(2)
    p8.paragraph_format.space_after = Pt(10)
    p8.paragraph_format.first_line_indent = Inches(0.0)
    r8 = p8.add_run("Mr. PRABHU\nAssistant Professor")
    set_run_font(r8, size_pt=11.5, bold=True)

    p9 = doc.add_paragraph()
    p9.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p9.paragraph_format.space_before = Pt(4)
    p9.paragraph_format.space_after = Pt(4)
    p9.paragraph_format.first_line_indent = Inches(0.0)
    r9 = p9.add_run("Submitted to")
    set_run_font(r9, size_pt=11, italic=True)

    if os.path.exists(logo1_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(2)
        p_logo.paragraph_format.space_after = Pt(6)
        p_logo.paragraph_format.first_line_indent = Inches(0.0)
        p_logo.add_run().add_picture(logo1_path, width=Inches(2.3))

    p10 = doc.add_paragraph()
    p10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p10.paragraph_format.space_before = Pt(4)
    p10.paragraph_format.space_after = Pt(2)
    p10.paragraph_format.first_line_indent = Inches(0.0)
    r10 = p10.add_run("AMRITA SCHOOL OF COMPUTING\nAMRITA VISHWA VIDYAPEETHAM\nCHENNAI – 601103")
    set_run_font(r10, size_pt=12, bold=True)

    p11 = doc.add_paragraph()
    p11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p11.paragraph_format.space_before = Pt(8)
    p11.paragraph_format.space_after = Pt(0)
    p11.paragraph_format.first_line_indent = Inches(0.0)
    r11 = p11.add_run("October 2026")
    set_run_font(r11, size_pt=11.5, bold=True)

    # =========================================================================
    # 2. TITLE PAGE (Page i)
    # =========================================================================
    doc.add_page_break()

    pt1 = doc.add_paragraph()
    pt1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt1.paragraph_format.space_before = Pt(16)
    pt1.paragraph_format.space_after = Pt(10)
    pt1.paragraph_format.first_line_indent = Inches(0.0)
    rt1 = pt1.add_run("APPSHIELDX – A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS")
    set_run_font(rt1, size_pt=14, bold=True)

    pt2 = doc.add_paragraph()
    pt2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt2.paragraph_format.space_before = Pt(10)
    pt2.paragraph_format.space_after = Pt(12)
    pt2.paragraph_format.first_line_indent = Inches(0.0)
    rt2 = pt2.add_run("A PROJECT REPORT")
    set_run_font(rt2, size_pt=12.5, bold=True)

    pt3 = doc.add_paragraph()
    pt3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt3.paragraph_format.space_before = Pt(4)
    pt3.paragraph_format.space_after = Pt(2)
    pt3.paragraph_format.first_line_indent = Inches(0.0)
    rt3 = pt3.add_run("Submitted by")
    set_run_font(rt3, size_pt=11, italic=True)

    pt4 = doc.add_paragraph()
    pt4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt4.paragraph_format.space_before = Pt(6)
    pt4.paragraph_format.space_after = Pt(2)
    pt4.paragraph_format.first_line_indent = Inches(0.0)
    rt4 = pt4.add_run("U. TEJASWI\n[CH.SC.U4CYS23047]")
    set_run_font(rt4, size_pt=11.5, bold=True)

    pt5 = doc.add_paragraph()
    pt5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt5.paragraph_format.space_before = Pt(12)
    pt5.paragraph_format.space_after = Pt(4)
    pt5.paragraph_format.first_line_indent = Inches(0.0)
    rt5 = pt5.add_run("in partial fulfillment for the award of the degree of")
    set_run_font(rt5, size_pt=11, italic=True)

    pt6 = doc.add_paragraph()
    pt6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt6.paragraph_format.space_before = Pt(4)
    pt6.paragraph_format.space_after = Pt(12)
    pt6.paragraph_format.first_line_indent = Inches(0.0)
    rt6 = pt6.add_run("BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND\nENGINEERING (CYBER SECURITY)")
    set_run_font(rt6, size_pt=12, bold=True)

    pt7 = doc.add_paragraph()
    pt7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt7.paragraph_format.space_before = Pt(6)
    pt7.paragraph_format.space_after = Pt(2)
    pt7.paragraph_format.first_line_indent = Inches(0.0)
    rt7 = pt7.add_run("Supervisor")
    set_run_font(rt7, size_pt=11, italic=True)

    pt8 = doc.add_paragraph()
    pt8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt8.paragraph_format.space_before = Pt(2)
    pt8.paragraph_format.space_after = Pt(10)
    pt8.paragraph_format.first_line_indent = Inches(0.0)
    rt8 = pt8.add_run("Mr. PRABHU\nAssistant Professor")
    set_run_font(rt8, size_pt=11.5, bold=True)

    pt9 = doc.add_paragraph()
    pt9.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt9.paragraph_format.space_before = Pt(4)
    pt9.paragraph_format.space_after = Pt(4)
    pt9.paragraph_format.first_line_indent = Inches(0.0)
    rt9 = pt9.add_run("Submitted to")
    set_run_font(rt9, size_pt=11, italic=True)

    if os.path.exists(logo1_path):
        pt_logo = doc.add_paragraph()
        pt_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pt_logo.paragraph_format.space_before = Pt(2)
        pt_logo.paragraph_format.space_after = Pt(6)
        pt_logo.paragraph_format.first_line_indent = Inches(0.0)
        pt_logo.add_run().add_picture(logo1_path, width=Inches(2.3))

    pt10 = doc.add_paragraph()
    pt10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt10.paragraph_format.space_before = Pt(4)
    pt10.paragraph_format.space_after = Pt(2)
    pt10.paragraph_format.first_line_indent = Inches(0.0)
    rt10 = pt10.add_run("AMRITA SCHOOL OF COMPUTING\nAMRITA VISHWA VIDYAPEETHAM\nCHENNAI – 601103")
    set_run_font(rt10, size_pt=12, bold=True)

    pt11 = doc.add_paragraph()
    pt11.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt11.paragraph_format.space_before = Pt(8)
    pt11.paragraph_format.space_after = Pt(0)
    pt11.paragraph_format.first_line_indent = Inches(0.0)
    rt11 = pt11.add_run("October 2026")
    set_run_font(rt11, size_pt=11.5, bold=True)

    # =========================================================================
    # 3. BONAFIDE CERTIFICATE (Page ii)
    # =========================================================================
    doc.add_page_break()

    if os.path.exists(logo2_path):
        p_hdr2 = doc.add_paragraph()
        p_hdr2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_hdr2.paragraph_format.space_before = Pt(0)
        p_hdr2.paragraph_format.space_after = Pt(12)
        p_hdr2.paragraph_format.first_line_indent = Inches(0.0)
        p_hdr2.add_run().add_picture(logo2_path, width=Inches(3.2))

    p_bon = doc.add_paragraph()
    p_bon.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bon.paragraph_format.space_before = Pt(4)
    p_bon.paragraph_format.space_after = Pt(14)
    p_bon.paragraph_format.first_line_indent = Inches(0.0)
    r_bon = p_bon.add_run("BONAFIDE CERTIFICATE")
    set_run_font(r_bon, size_pt=13.5, bold=True)

    add_para(doc, 
        "Certified that this project report entitled “APPSHIELDX – A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS” is the Bonafide work of “U. TEJASWI (CH.SC.U4CYS23047)”, who carried out the project work under my supervision.",
        space_after=24
    )

    tbl_sig = doc.add_table(rows=2, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False
    tbl_sig.rows[0].cells[0].width = Inches(3.2)
    tbl_sig.rows[0].cells[1].width = Inches(3.2)

    c0 = tbl_sig.rows[0].cells[0].paragraphs[0]
    c0.text = "CHAIRPERSON SIGNATURE\n\n\n\nDr S Baghavathi Priya\nAssociate Professor\nDepartment of Computer Science and Engineering,\nAmrita School of Computing,\nAmrita Vishwa Vidyapeetham, Chennai."
    c0.paragraph_format.line_spacing = 1.2
    set_run_font(c0.runs[0], size_pt=10.5)

    c1 = tbl_sig.rows[0].cells[1].paragraphs[0]
    c1.text = "SUPERVISOR SIGNATURE\n\n\n\nMr. Prabhu\nAssistant Professor\nDepartment of Computer Science and Engineering,\nAmrita School of Computing,\nAmrita Vishwa Vidyapeetham, Chennai."
    c1.paragraph_format.line_spacing = 1.2
    set_run_font(c1.runs[0], size_pt=10.5)

    c2 = tbl_sig.rows[1].cells[0].paragraphs[0]
    c2.paragraph_format.space_before = Pt(28)
    c2.text = "INTERNAL EXAMINER"
    set_run_font(c2.runs[0], size_pt=10.5, bold=True)

    c3 = tbl_sig.rows[1].cells[1].paragraphs[0]
    c3.paragraph_format.space_before = Pt(28)
    c3.text = "EXTERNAL EXAMINER"
    set_run_font(c3.runs[0], size_pt=10.5, bold=True)

    # =========================================================================
    # 4. DECLARATION BY THE CANDIDATE (Page iii)
    # =========================================================================
    doc.add_page_break()

    if os.path.exists(logo2_path):
        p_hdr3 = doc.add_paragraph()
        p_hdr3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_hdr3.paragraph_format.space_before = Pt(0)
        p_hdr3.paragraph_format.space_after = Pt(14)
        p_hdr3.paragraph_format.first_line_indent = Inches(0.0)
        p_hdr3.add_run().add_picture(logo2_path, width=Inches(3.2))

    p_dec = doc.add_paragraph()
    p_dec.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec.paragraph_format.space_before = Pt(6)
    p_dec.paragraph_format.space_after = Pt(16)
    p_dec.paragraph_format.first_line_indent = Inches(0.0)
    r_dec = p_dec.add_run("DECLARATION BY THE CANDIDATE")
    set_run_font(r_dec, size_pt=13.5, bold=True)

    add_para(doc,
        "I declare that the report entitled “APPSHIELDX – A CLOUD-NATIVE RUNTIME PROTECTION AND API SECURITY FRAMEWORK FOR CLIENT–SERVER APPLICATIONS” submitted by me for the degree of Bachelor of Technology in Computer Science and Engineering (Cyber Security) is the record of the project work carried out by me under the guidance of Mr. Prabhu, Assistant Professor, Department of Computer Science and Engineering, Amrita School of Computing, Amrita Vishwa Vidyapeetham, Chennai, and this work has not formed the basis for the award of any degree, diploma, associateship, fellowship, titled in this or any other University or other similar institution of higher learning.",
        space_after=36
    )

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.paragraph_format.space_after = Pt(4)
    p_sig.paragraph_format.first_line_indent = Inches(0.0)
    r_sig = p_sig.add_run("SIGNATURE\n\n\n\nU. TEJASWI\n[CH.SC.U4CYS23047]")
    set_run_font(r_sig, size_pt=11, bold=True)

    # =========================================================================
    # 5. ABSTRACT (Page iv - Strictly One Page)
    # =========================================================================
    doc.add_page_break()

    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_before = Pt(8)
    p_abs.paragraph_format.space_after = Pt(14)
    p_abs.paragraph_format.first_line_indent = Inches(0.0)
    r_abs = p_abs.add_run("ABSTRACT")
    set_run_font(r_abs, size_pt=14, bold=True)

    add_para(doc,
        "Modern mobile applications heavily rely on cloud-native client-server architectures, where mobile clients communicate with backend microservices through REST APIs for authentication, transactions, and data storage. Although scalable, these architectures suffer from an Asymmetric Ingress Blind Spot: backend API gateways process incoming requests under the implicit assumption of client integrity, while mobile clients execute in untrusted host operating system environments persistently exposed to dynamic instrumentation (Frida, Xposed), kernel debuggers (ptrace), rooting tools (Magisk, KernelSU), and automated API abuse. Conventional solutions treat mobile endpoint protection and API security as disconnected silos—client RASP libraries crash locally without notifying backend gateways, while API firewalls evaluate bearer tokens in complete blindness to device execution state.",
        space_after=6
    )

    add_para(doc,
        "To resolve this fundamental gap, this thesis designs, implements, and evaluates AppShieldX, a unified cloud-native runtime protection and API security framework. On the mobile client, AppShieldX deploys native Linux kernel diagnostic probes via an asynchronous Flutter MethodChannel that interrogates /proc/self/status for debugger attachment (TracerPid != 0), checks su binaries, scans /proc/self/maps for dynamic memory hooks, and identifies emulator hypervisors. Telemetry is cryptographically signed using HMAC-SHA256 and streamed out-of-band to a cloud ingress architecture governed by a reactive Spring Cloud Gateway ZeroTrustSecurityFilter. A stateful Threat Correlation Engine evaluates security events against six cross-layer correlation rules, updating a centralized dynamic risk score governed by an exponential decay function (15-minute half-life) cached in Redis and persisted in PostgreSQL across four adaptive Zero-Trust policy bands: ALLOW, STEP_UP (MFA), RESTRICT, and TERMINATE.",
        space_after=6
    )

    add_para(doc,
        "Empirical validation across 400 experimental trials encompassing virtualized environments and a physical Motorola Edge 50 Fusion device running Android 16 demonstrates that AppShieldX achieves a threat detection Recall of 85.71% against sophisticated blended attacks (93.33% overall), 100% Precision with zero false positives under benign workloads, and a negligible median gateway latency overhead of only 3.76 ms (P50), providing a scalable Zero-Trust foundation for high-assurance FinTech and healthcare ecosystems.",
        space_after=8
    )

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(8)
    p_kw.paragraph_format.space_after = Pt(0)
    p_kw.paragraph_format.first_line_indent = Inches(0.0)
    r_kw_lbl = p_kw.add_run("Keywords: ")
    set_run_font(r_kw_lbl, size_pt=11.5, bold=True)
    r_kw_val = p_kw.add_run("Cloud-Native Security, Runtime Application Self-Protection (RASP), API Security, Zero-Trust Architecture, Cross-Layer Threat Correlation, Dynamic Instrumentation.")
    set_run_font(r_kw_val, size_pt=11.5, italic=True)

    # =========================================================================
    # 6. ACKNOWLEDGEMENT (Page v - Strictly One Page)
    # =========================================================================
    doc.add_page_break()

    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(8)
    p_ack.paragraph_format.space_after = Pt(14)
    p_ack.paragraph_format.first_line_indent = Inches(0.0)
    r_ack = p_ack.add_run("ACKNOWLEDGEMENT")
    set_run_font(r_ack, size_pt=14, bold=True)

    add_para(doc,
        "This project would not have been possible without the invaluable contribution, guidance, and encouragement of many esteemed individuals. It gives me immense pleasure to express my profound gratitude to our honorable Chancellor, Sri Mata Amritanandamayi Devi, for her divine blessings, grace, and eternal inspiration throughout my academic journey.",
        space_after=6
    )

    add_para(doc,
        "I extend my sincere thanks to Administrative Director, Sampoojya Swami Vinyamritananda Puri, Amrita Vishwa Vidyapeetham, Chennai Campus, for his constant guidance and support. I am deeply indebted to our Director, I B Manikantan, Amrita School of Computing, for providing all computational facilities and extended academic support that enabled me to gain rigorous cybersecurity education.",
        space_after=6
    )

    add_para(doc,
        "I extend my special thanks to Dr. V Jayakumar, Principal, Amrita School of Computing, for the institutional support provided during this work. I am exceptionally grateful to Dr. S Baghavathi Priya, Chairperson, Department of Computer Science and Engineering, and Dr. S Udhaya Kumar, Program Chair, Department of Computer Science and Engineering (Cyber Security), for their continuous academic vision, encouragement, and research facilities.",
        space_after=6
    )

    add_para(doc,
        "I express my deepest and heartfelt gratitude to my project supervisor, Mr. Prabhu, Assistant Professor, Department of Computer Science and Engineering, for his patient guidance, technical critique, and insightful feedback from the inception of this research to the empirical deployment of AppShieldX. Finally, I express my deepest appreciation to the project review panel, faculty members, my family, and friends for their enduring support.",
        space_after=16
    )

    p_ack_sig = doc.add_paragraph()
    p_ack_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack_sig.paragraph_format.space_before = Pt(12)
    p_ack_sig.paragraph_format.space_after = Pt(0)
    p_ack_sig.paragraph_format.first_line_indent = Inches(0.0)
    r_as = p_ack_sig.add_run("U. TEJASWI\n[CH.SC.U4CYS23047]")
    set_run_font(r_as, size_pt=11, bold=True)

    # =========================================================================
    # 7. TABLE OF CONTENTS (Page vi)
    # =========================================================================
    doc.add_page_break()

    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.paragraph_format.space_before = Pt(6)
    p_toc_h.paragraph_format.space_after = Pt(12)
    p_toc_h.paragraph_format.first_line_indent = Inches(0.0)
    r_toc_h = p_toc_h.add_run("TABLE OF CONTENTS")
    set_run_font(r_toc_h, size_pt=14, bold=True)

    # Exact measured page numbers matching Section 2 layout
    toc_items = [
        ("", "Abstract", "iv", False),
        ("", "List of Tables", "viii", False),
        ("", "List of Figures", "ix", False),
        ("", "List of Symbols and Abbreviations", "x", False),
        ("1", "INTRODUCTION", "1", True),
        ("1.1", "Background and Industry Context", "1", False),
        ("1.2", "Motivation and Security Paradigm Shift", "3", False),
        ("1.3", "Problem Formulation: Asymmetric Ingress Blind Spots", "5", False),
        ("1.4", "Research Objectives", "7", False),
        ("1.5", "Scope and Boundary Conditions", "8", False),
        ("1.6", "Thesis Organization", "9", False),
        ("2", "LITERATURE REVIEW", "11", True),
        ("2.1", "Evolution of Mobile Application Security Paradigms", "11", False),
        ("2.2", "Runtime Application Self-Protection (RASP) Mechanics", "12", False),
        ("2.3", "Cloud-Native Ingress and API Security Defenses", "14", False),
        ("2.4", "Zero-Trust Architecture and Continuous Attestation", "15", False),
        ("2.5", "Systematic Literature Review Methodology", "15", False),
        ("2.6", "Comprehensive Critical Analysis of Selected Literature", "17", False),
        ("2.7", "Identified Research Gaps and Architectural Limitations", "26", False),
        ("3", "PROBLEM STATEMENT AND METHODOLOGY", "29", True),
        ("3.1", "Formal Problem Definition and Mathematical Formulation", "29", False),
        ("3.2", "Threat Model and Adversary Capabilities", "30", False),
        ("3.3", "Data Flow Architecture and Trust Boundaries", "32", False),
        ("3.4", "Cross-Layer Telemetry and Adaptive Enforcement Hypothesis", "34", False),
        ("3.5", "Experimental Methodology and Empirical Evaluation Framework", "35", False),
        ("4", "SYSTEM DESIGN", "37", True),
        ("4.1", "Architectural Overview: Six-Tier Distributed Framework", "37", False),
        ("4.2", "Client-Side Security Layer: Kernel-Level RASP Engine", "39", False),
        ("4.3", "Secure Communication Layer: TLS 1.3 and Pinning", "41", False),
        ("4.4", "Cloud Ingress and API Gateway: ZeroTrustSecurityFilter", "42", False),
        ("4.5", "Threat Detection and Stateful Event Correlation Engine", "44", False),
        ("4.6", "Server-Side Dynamic Risk Scoring Engine and Decay Mechanics", "46", False),
        ("4.7", "Persistence and Shared Caching Architecture", "48", False),
        ("4.8", "Security Operations Center (SOC) Administrator Dashboard", "50", False),
        ("4.9", "Dual-Domain Reference Client Applications", "50", False),
        ("5", "RESULTS AND DISCUSSIONS", "53", True),
        ("5.1", "Experimental Evaluation Testbed and Setup", "53", False),
        ("5.2", "Ten Canonical Threat Scenarios Evaluation", "54", False),
        ("5.3", "Comparative Threat Detection Performance Metrics", "55", False),
        ("5.4", "Ablation Study Analysis", "57", False),
        ("5.5", "Gateway Latency and Runtime Performance Overhead Analysis", "58", False),
        ("5.6", "Physical Android Hardware Verification (Motorola Edge 50)", "60", False),
        ("5.7", "Security Analysis and Threats to Validity", "62", False),
        ("6", "CONCLUSIONS AND SCOPE FOR FURTHER WORK", "64", True),
        ("6.1", "Summary of Research Contributions", "64", False),
        ("6.2", "Industrial Significance and Practical Feasibility", "65", False),
        ("6.3", "Technical Limitations", "65", False),
        ("6.4", "Scope for Future Work", "66", False),
        ("", "REFERENCES", "68", True),
        ("", "APPENDICES", "70", True),
        ("Appendix A", "Plagiarism Evaluation Summary Report", "70", False),
        ("Appendix B", "Core System Implementation Source Code Listings", "71", False),
        ("Appendix C", "Threat Correlation and Zero-Trust Rule Specifications", "76", False),
        ("Appendix D", "Experimental Evaluation Raw Metric Dataset", "78", False),
    ]

    tbl_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_toc.autofit = False
    tbl_toc.rows[0].cells[0].width = Inches(1.3)
    tbl_toc.rows[0].cells[1].width = Inches(4.5)
    tbl_toc.rows[0].cells[2].width = Inches(0.8)

    tbl_toc.rows[0].cells[0].paragraphs[0].text = "CHAPTER NO."
    set_run_font(tbl_toc.rows[0].cells[0].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_toc.rows[0].cells[1].paragraphs[0].text = "TITLE"
    set_run_font(tbl_toc.rows[0].cells[1].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_toc.rows[0].cells[2].paragraphs[0].text = "PAGE NO."
    tbl_toc.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(tbl_toc.rows[0].cells[2].paragraphs[0].runs[0], size_pt=9.5, bold=True)

    for i, (chap_num, title, page_num, is_b) in enumerate(toc_items):
        row = tbl_toc.rows[i + 1]
        c_num = row.cells[0].paragraphs[0]
        c_num.text = chap_num
        c_num.paragraph_format.space_before = Pt(1)
        c_num.paragraph_format.space_after = Pt(1)
        set_run_font(c_num.runs[0], size_pt=9, bold=is_b)

        c_title = row.cells[1].paragraphs[0]
        c_title.text = title
        c_title.paragraph_format.space_before = Pt(1)
        c_title.paragraph_format.space_after = Pt(1)
        set_run_font(c_title.runs[0], size_pt=9, bold=is_b)

        c_pg = row.cells[2].paragraphs[0]
        c_pg.text = page_num
        c_pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        c_pg.paragraph_format.space_before = Pt(1)
        c_pg.paragraph_format.space_after = Pt(1)
        set_run_font(c_pg.runs[0], size_pt=9, bold=is_b)

    # =========================================================================
    # 8. LIST OF TABLES (Page viii)
    # =========================================================================
    doc.add_page_break()

    p_lot_h = doc.add_paragraph()
    p_lot_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot_h.paragraph_format.space_before = Pt(6)
    p_lot_h.paragraph_format.space_after = Pt(12)
    p_lot_h.paragraph_format.first_line_indent = Inches(0.0)
    r_lot_h = p_lot_h.add_run("LIST OF TABLES")
    set_run_font(r_lot_h, size_pt=14, bold=True)

    lot_items = [
        ("Table 2.1", "Taxonomy of Modern Client-Server Attack Surfaces and Threat Vectors", "12"),
        ("Table 2.2", "Systematic Literature Review Search Terms and Boolean Query Filters", "17"),
        ("Table 2.3", "Comprehensive Comparative Analysis of 20 Selected Academic Literature Studies (2021–2026)", "25"),
        ("Table 2.4", "Identified Research Gaps and Architectural Limitations in State-of-the-Art Solutions", "27"),
        ("Table 3.1", "Adversary Capability Matrix and Mapping to MITRE ATT&CK for Mobile Techniques", "31"),
        ("Table 3.2", "Data Flow Elements, Assets, and Trust Boundary Specifications", "33"),
        ("Table 4.1", "Core RASP Diagnostic Probes Implemented Across Native Kernel Channels", "40"),
        ("Table 4.2", "AppShieldX Deterministic Cross-Layer Correlation Rule Definitions (RULE-CORR-01 to 06)", "45"),
        ("Table 4.3", "Threat Severity Weight Matrix and Mathematical Score Calculations", "47"),
        ("Table 4.4", "Server-Side Zero-Trust Adaptive Response Bands and Policy Actions", "48"),
        ("Table 4.5", "Relational Database Schema Table Specifications and Indexing Strategy", "49"),
        ("Table 5.1", "Experimental Evaluation Testbed Hardware, Virtualization, and Network Specifications", "53"),
        ("Table 5.2", "Ten Canonical Experimental Threat Scenarios and Expected Enforcement Behaviors", "54"),
        ("Table 5.3", "Detection Confusion Matrix Metrics Across Four Architectural Configurations (400 Runs)", "55"),
        ("Table 5.4", "Five-Variant Ablation Study Results Evaluating Core Framework Innovations", "57"),
        ("Table 5.5", "End-to-End Latency Overhead Benchmarks for Gateway Ingress Filters (Milliseconds)", "59"),
        ("Table 5.6", "Physical Android Device Performance Benchmarks (Motorola Edge 50 Fusion)", "62"),
    ]

    tbl_lot = doc.add_table(rows=len(lot_items) + 1, cols=3)
    tbl_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lot.autofit = False
    tbl_lot.rows[0].cells[0].width = Inches(1.3)
    tbl_lot.rows[0].cells[1].width = Inches(4.5)
    tbl_lot.rows[0].cells[2].width = Inches(0.8)

    tbl_lot.rows[0].cells[0].paragraphs[0].text = "TABLE NO."
    set_run_font(tbl_lot.rows[0].cells[0].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_lot.rows[0].cells[1].paragraphs[0].text = "TITLE"
    set_run_font(tbl_lot.rows[0].cells[1].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_lot.rows[0].cells[2].paragraphs[0].text = "PAGE NO."
    tbl_lot.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(tbl_lot.rows[0].cells[2].paragraphs[0].runs[0], size_pt=9.5, bold=True)

    for i, (t_no, t_title, t_pg) in enumerate(lot_items):
        row = tbl_lot.rows[i + 1]
        r0 = row.cells[0].paragraphs[0]
        r0.text = t_no
        r0.paragraph_format.space_before = Pt(1)
        r0.paragraph_format.space_after = Pt(1)
        set_run_font(r0.runs[0], size_pt=9, bold=True)
        r1 = row.cells[1].paragraphs[0]
        r1.text = t_title
        r1.paragraph_format.space_before = Pt(1)
        r1.paragraph_format.space_after = Pt(1)
        set_run_font(r1.runs[0], size_pt=9)
        r2 = row.cells[2].paragraphs[0]
        r2.text = t_pg
        r2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2.paragraph_format.space_before = Pt(1)
        r2.paragraph_format.space_after = Pt(1)
        set_run_font(r2.runs[0], size_pt=9)

    # =========================================================================
    # 9. LIST OF FIGURES (Page ix)
    # =========================================================================
    doc.add_page_break()

    p_lof_h = doc.add_paragraph()
    p_lof_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof_h.paragraph_format.space_before = Pt(6)
    p_lof_h.paragraph_format.space_after = Pt(12)
    p_lof_h.paragraph_format.first_line_indent = Inches(0.0)
    r_lof_h = p_lof_h.add_run("LIST OF FIGURES")
    set_run_font(r_lof_h, size_pt=14, bold=True)

    lof_items = [
        ("Figure 1.1", "Modern Mobile Client-Server Threat Surface and Vector Attack Divergence", "2"),
        ("Figure 2.1", "PRISMA Academic Literature Selection and Filtering Funnel Flowchart", "16"),
        ("Figure 2.2", "Year-Wise Chronological Distribution of Selected Research Publications (2021–2026)", "17"),
        ("Figure 3.1", "Data Flow Diagram (Level 1) and Security Trust Boundaries Across Ingress Gateways", "33"),
        ("Figure 3.2", "Cross-Layer Closed-Loop Telemetry Ingestion and Adaptive Enforcement Feedback Loop", "34"),
        ("Figure 4.1", "AppShieldX Six-Tier Cloud-Native Architecture and Telemetry Processing Pipeline", "37"),
        ("Figure 4.2", "Native Android RASP Probe Execution Flowchart in Linux Kernel Space", "39"),
        ("Figure 4.3", "Server-Side Zero-Trust Adaptive Response Bands and Temporal Score Decay Curve", "46"),
        ("Figure 4.4", "Deterministic Threat Correlation State Machine Workflow (RULE-CORR-01 to 06)", "45"),
        ("Figure 4.5", "Relational Database Schema Entity-Relationship (ER) Diagram", "49"),
        ("Figure 4.6", "SOC Administrator Dashboard Live Telemetry and Threat Intelligence Architecture", "50"),
        ("Figure 4.7", "Dual-Domain Reference Client Applications (Banking Vault & Healthcare EHR Portal)", "51"),
        ("Figure 5.1", "Threat Detection Performance Comparison Across Architectural Variants (Recall, Precision, F1)", "56"),
        ("Figure 5.2", "Ablation Study: Detection Recall and False Positive Rate Across Five Framework Variants", "58"),
        ("Figure 5.3", "Ingress Gateway Processing Latency Overhead Distribution (Median, P95, and P99)", "59"),
        ("Figure 5.4", "Physical Motorola Edge 50 Fusion Device Verification Showing Active TracerPid Detection", "62"),
    ]

    tbl_lof = doc.add_table(rows=len(lof_items) + 1, cols=3)
    tbl_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_lof.autofit = False
    tbl_lof.rows[0].cells[0].width = Inches(1.3)
    tbl_lof.rows[0].cells[1].width = Inches(4.5)
    tbl_lof.rows[0].cells[2].width = Inches(0.8)

    tbl_lof.rows[0].cells[0].paragraphs[0].text = "FIGURE NO."
    set_run_font(tbl_lof.rows[0].cells[0].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_lof.rows[0].cells[1].paragraphs[0].text = "TITLE"
    set_run_font(tbl_lof.rows[0].cells[1].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_lof.rows[0].cells[2].paragraphs[0].text = "PAGE NO."
    tbl_lof.rows[0].cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run_font(tbl_lof.rows[0].cells[2].paragraphs[0].runs[0], size_pt=9.5, bold=True)

    for i, (f_no, f_title, f_pg) in enumerate(lof_items):
        row = tbl_lof.rows[i + 1]
        r0 = row.cells[0].paragraphs[0]
        r0.text = f_no
        r0.paragraph_format.space_before = Pt(1)
        r0.paragraph_format.space_after = Pt(1)
        set_run_font(r0.runs[0], size_pt=9, bold=True)
        r1 = row.cells[1].paragraphs[0]
        r1.text = f_title
        r1.paragraph_format.space_before = Pt(1)
        r1.paragraph_format.space_after = Pt(1)
        set_run_font(r1.runs[0], size_pt=9)
        r2 = row.cells[2].paragraphs[0]
        r2.text = f_pg
        r2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r2.paragraph_format.space_before = Pt(1)
        r2.paragraph_format.space_after = Pt(1)
        set_run_font(r2.runs[0], size_pt=9)

    # =========================================================================
    # 10. LIST OF SYMBOLS AND ABBREVIATIONS (Page x)
    # =========================================================================
    doc.add_page_break()

    p_abbr_h = doc.add_paragraph()
    p_abbr_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abbr_h.paragraph_format.space_before = Pt(6)
    p_abbr_h.paragraph_format.space_after = Pt(12)
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
    tbl_abbr.rows[0].cells[0].width = Inches(1.3)
    tbl_abbr.rows[0].cells[1].width = Inches(0.4)
    tbl_abbr.rows[0].cells[2].width = Inches(4.8)

    tbl_abbr.rows[0].cells[0].paragraphs[0].text = "ABBREVIATION"
    set_run_font(tbl_abbr.rows[0].cells[0].paragraphs[0].runs[0], size_pt=9.5, bold=True)
    tbl_abbr.rows[0].cells[1].paragraphs[0].text = "-"
    tbl_abbr.rows[0].cells[2].paragraphs[0].text = "FULL FORM / DESCRIPTION"
    set_run_font(tbl_abbr.rows[0].cells[2].paragraphs[0].runs[0], size_pt=9.5, bold=True)

    for i, (ab_short, ab_long) in enumerate(abbr_items):
        row = tbl_abbr.rows[i + 1]
        r0 = row.cells[0].paragraphs[0]
        r0.text = ab_short
        r0.paragraph_format.space_before = Pt(1)
        r0.paragraph_format.space_after = Pt(1)
        set_run_font(r0.runs[0], size_pt=9, bold=True)
        r1 = row.cells[1].paragraphs[0]
        r1.text = "-"
        r1.paragraph_format.space_before = Pt(1)
        r1.paragraph_format.space_after = Pt(1)
        set_run_font(r1.runs[0], size_pt=9)
        r2 = row.cells[2].paragraphs[0]
        r2.text = ab_long
        r2.paragraph_format.space_before = Pt(1)
        r2.paragraph_format.space_after = Pt(1)
        set_run_font(r2.runs[0], size_pt=9)

    # =========================================================================
    # CREATE SECTION 2: CHAPTER 1 MAIN BODY (Decimal Arabic Numbering Starting at 1)
    # =========================================================================
    s2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    s2.header.is_linked_to_previous = False
    s2.footer.is_linked_to_previous = False
    add_footer_page_number(s2, start_fmt="decimal", start_num=1)

    print("Preliminary pages generated with professional layout and Section 2 initialized.")
