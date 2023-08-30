import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate

input_pdf = "pdfs/chapters.pdf"
output_pdf = "pdfs/chapters.pdf"

# Get total number of pages
pdf = PdfReader(input_pdf)
total_pages = len(pdf.pages)

# Create a new PDF with headers and footers
output = PdfWriter()
style = getSampleStyleSheet()["Normal"]
footer_style = style.clone("Footer")
footer_style.alignment = 2  # Right-aligned

for page_number in range(total_pages):
    packet = io.BytesIO()
    # Create a new PDF with the footer content
    footer = SimpleDocTemplate(packet, pagesize=letter)
    formatted_footer = "<para align='right'>Page {} of {}</para>".format(
        page_number + 1, total_pages
    )
    footer.build([Paragraph(formatted_footer, footer_style)])

    # Move to the beginning of the "virtual" file
    packet.seek(0)
    new_pdf = PdfReader(packet)

    # Merge the footer PDF with the page
    page = pdf.pages[page_number]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

# Save the final output PDF
with open(output_pdf, "wb") as output_stream:
    output.write(output_stream)

print("Done.")