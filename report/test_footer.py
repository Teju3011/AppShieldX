import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START

doc = docx.Document()
s1 = doc.sections[0]
s1.different_first_page_header_footer = True

# Roman numerals in section 1
sectPr1 = s1._sectPr
pgNumType1 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1" w:fmt="lowerRoman"/>')
sectPr1.append(pgNumType1)

p_foot1 = s1.footer.paragraphs[0]
p_foot1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r1 = p_foot1.add_run()
fld1 = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
r1._r.append(fld1)

doc.add_paragraph("Cover Page (No footer)")
doc.add_page_break()
doc.add_paragraph("Title Page (Footer i)")

# Section 2: Body
s2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
s2.header.is_linked_to_previous = False
s2.footer.is_linked_to_previous = False

sectPr2 = s2._sectPr
pgNumType2 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1" w:fmt="decimal"/>')
sectPr2.append(pgNumType2)

p_foot2 = s2.footer.paragraphs[0]
p_foot2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p_foot2.add_run()
fld2 = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
r2._r.append(fld2)

doc.add_paragraph("Chapter 1 Body (Footer 1)")

doc.save("test_footer.docx")
print("test_footer.docx created successfully!")
