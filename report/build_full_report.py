# -*- coding: utf-8 -*-
"""
Master Compiler for AppShieldX Academic Project Report
Amrita School of Computing, Amrita Vishwa Vidyapeetham, Chennai Campus
B.Tech in Computer Science and Engineering (Cyber Security)
Compiles all chapters, prelims, references, and appendices into a 70+ page document,
updates TOC fields via Word COM, and exports directly to PDF.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Import module generators
from report_helpers import set_run_font
from prelims import generate_preliminary_pages
from chapter1 import generate_chapter1
from chapter2 import generate_chapter2
from chapter3 import generate_chapter3
from chapter4 import generate_chapter4
from chapter5 import generate_chapter5
from chapter6 import generate_chapter6
from references_appendices import generate_references_and_appendices

def build_full_document():
    base_dir = os.path.dirname(__file__)
    figures_dir = os.path.join(base_dir, "figures")
    output_docx = os.path.join(base_dir, "AppShieldX_Project_Report_70_Pages.docx")
    output_pdf = os.path.join(base_dir, "AppShieldX_Project_Report_70_Pages.pdf")

    print("=================================================================")
    print("Initializing Document Setup: Times New Roman, 1.5 line spacing...")
    print("=================================================================")
    doc = docx.Document()

    # Base Page Setup: Standard Academic Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)   # 1.25" for binding margin
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Configure Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # 1. Preliminary Pages
    print("Step 1: Generating Preliminary Pages (Cover, Certificate, TOC, Lists)...")
    generate_preliminary_pages(doc, figures_dir)

    # 2. Chapter 1: Introduction
    print("Step 2: Generating Chapter 1: Introduction...")
    generate_chapter1(doc, figures_dir)

    # 3. Chapter 2: Literature Review
    print("Step 3: Generating Chapter 2: Literature Review (20 Papers Analyzed)...")
    generate_chapter2(doc, figures_dir)

    # 4. Chapter 3: Problem Statement and Methodology
    print("Step 4: Generating Chapter 3: Problem Statement and Methodology...")
    generate_chapter3(doc, figures_dir)

    # 5. Chapter 4: System Design
    print("Step 5: Generating Chapter 4: System Design (Architecture, Kernel Probes, Gateway, Risk Engine)...")
    generate_chapter4(doc, figures_dir)

    # 6. Chapter 5: Results and Discussions
    print("Step 6: Generating Chapter 5: Results and Discussions (400 Runs, Ablation, Benchmarks)...")
    generate_chapter5(doc, figures_dir)

    # 7. Chapter 6: Conclusions and Scope for Further Work
    print("Step 7: Generating Chapter 6: Conclusions and Scope for Further Work...")
    generate_chapter6(doc)

    # 8. References and Appendices
    print("Step 8: Generating References and Appendices A-D...")
    generate_references_and_appendices(doc)

    # Save DOCX
    print(f"Saving compiled document to: {output_docx}")
    doc.save(output_docx)
    print("DOCX successfully generated.")

    return output_docx, output_pdf

def convert_to_pdf_and_update_fields(docx_path, pdf_path):
    print("=================================================================")
    print("Connecting to Microsoft Word COM Automation...")
    print("=================================================================")
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False

        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)

        doc = word.Documents.Open(abs_docx)
        print("Document opened in Word. Updating all fields and TOC pagination...")

        # Update all document fields
        doc.Fields.Update()
        for toc in doc.TablesOfContents:
            toc.Update()

        # Compute page statistics
        wdStatisticPages = 2
        page_count = doc.ComputeStatistics(wdStatisticPages)
        print(f"CURRENT COMPUTED PAGE COUNT IN MICROSOFT WORD: {page_count} PAGES")

        # Export to PDF (wdFormatPDF = 17)
        print(f"Exporting to PDF: {abs_pdf}")
        wdFormatPDF = 17
        doc.SaveAs(abs_pdf, FileFormat=wdFormatPDF)
        
        # Save any updated fields back to the docx
        doc.Save()
        doc.Close(False)
        word.Quit()

        print(f"PDF Successfully Exported: {abs_pdf}")
        return page_count
    except Exception as e:
        print(f"Word COM Automation encountered an error: {e}")
        return None

if __name__ == "__main__":
    docx_file, pdf_file = build_full_document()
    pages = convert_to_pdf_and_update_fields(docx_file, pdf_file)
    print(f"Master Build Completed! Final Verified Page Count: {pages}")
