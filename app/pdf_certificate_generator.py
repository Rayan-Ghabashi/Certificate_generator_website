import io

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_certificate(name,  template_path, output_path, font,color):
    try:
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        width, height = letter

        c.setFont(font, 30)
        c.setFillColor(color)
        c.drawCentredString(width/1.43, height/2.56, name)
        c.save()

        packet.seek(0)

    # Read the existing PDF
        existing_pdf = PdfReader(template_path)
        output = PdfWriter()

        # Read your newly created PDF with ReportLab
        new_pdf = PdfReader(packet)

        # Add the "watermark" (new_pdf) on the existing page
        page = existing_pdf.pages[0]
        page.merge_page(new_pdf.pages[0])

        output.add_page(page)

        # Write to a new file
        with open(output_path, "wb") as outputStream:
            output.write(outputStream)
    except:
      print(f'\n\nerror on generating a certificate for {name}\n\n')
    
