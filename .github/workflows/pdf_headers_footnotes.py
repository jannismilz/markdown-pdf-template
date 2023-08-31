from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import Color
import io

# Step 1: Open the PDF file and read its pages.
pdf_path = 'pdfs/chapters.pdf'
pdf_pc_path = 'pdfs/temp/chapters.pdf'
pdf = PdfReader(pdf_path)
pdf_pc = PdfReader(pdf_pc_path)

# Use temp file without ToC to get final page count
page_count = len(pdf_pc.pages)

# Step 2: Create a new PDF with page numbers.
width, height = pdf.pages[0].mediabox.upper_right
output = io.BytesIO()
c = Canvas(output, pagesize=(width, height))

for i in range(page_count):
    c.setFillColor(Color(0, 0, 0, alpha=0.5))
    c.setFont("Helvetica", 10)
    c.drawString(37, 30, "Jannis Milz")
    c.drawRightString(int(width) - 37, 30, f"{str(i + 1)} / {page_count}")
    c.drawRightString(int(width) - 37, int(height) - 35, "Ein Name")
    c.showPage()

c.save()

# Move to the beginning of the StringIO buffer
output.seek(0)
new_pdf = PdfReader(output)

# Step 3: Merge the original PDF and the new PDF with page numbers.
pdf_writer = PdfWriter()

for i in range(len(pdf.pages)):
    page = pdf.pages[i]
    if i + page_count >= len(pdf.pages):
        page.merge_page(new_pdf.pages[i + len(pdf.pages) - page_count])
    pdf_writer.add_page(page)

# Step 4: Write to a new PDF file.
with open('pdfs/chapters.pdf', 'wb') as fh:
    pdf_writer.write(fh)
