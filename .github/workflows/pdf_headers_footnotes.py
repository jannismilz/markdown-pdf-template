from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import Color
import io

def printRoman(number):
    num = [1, 4, 5, 9, 10, 40, 50, 90,
        100, 400, 500, 900, 1000]
    sym = ["i", "iv", "v", "ix", "x", "xl",
        "l", "xc", "c", "cd", "d", "cm", "m"]
    i = 12
    result = ""
    while number:
        div = number // num[i]
        number %= num[i]
 
        while div:
            result += sym[i]
            div -= 1
        i -= 1

    return result

# Step 1: Open the PDF file and read its pages.
pdf_path = 'pdfs/output.pdf'
pdf_pc_path = 'pdfs/chapters.pdf'
pdf = PdfReader(pdf_path)
pdf_pc = PdfReader(pdf_pc_path)

# Use temp file without ToC to get final page count
page_count = len(pdf_pc.pages)

# Step 2: Create a new PDF with page numbers.
width, height = pdf.pages[0].mediabox.upper_right
output = io.BytesIO()
c = Canvas(output, pagesize=(width, height))

for i in range(len(pdf.pages)):
    c.setFillColor(Color(0, 0, 0, alpha=0.5))
    c.setFont("Helvetica", 10)

    # If frontpage
    if i == 0:
        c.drawRightString(int(width) - 37, 30, f"Seite {printRoman(page_count)}")
    else:
        c.drawString(37, 30, "Jannis Milz")
        # If page not ToC
        if i + page_count >= len(pdf.pages):
            c.drawRightString(int(width) - 37, 30, f"Seite {str((i + page_count) - len(pdf.pages) + 1)} / {page_count}")
        else:
            c.drawRightString(int(width) - 37, 30, f"Seite {printRoman(page_count)}")
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
    # if i + page_count >= len(pdf.pages):
    #     page.merge_page(new_pdf.pages[len(pdf.pages) - (i + page_count)])
    page.merge_page(new_pdf.pages[i])
    pdf_writer.add_page(page)

# Step 4: Write to a new PDF file.
with open('pdfs/chapters.pdf', 'wb') as fh:
    pdf_writer.write(fh)
