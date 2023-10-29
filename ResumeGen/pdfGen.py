

from flask import Flask, render_template, jsonify, render_template_string 

from io import BytesIO
from xhtml2pdf import pisa

import PyPDF2
from io import BytesIO

def count_pdf_pages(pdf_content):
    pdf_buffer = BytesIO(pdf_content)
    pdf = PyPDF2.PdfReader(pdf_buffer)
    num_pages = len(pdf.pages)
    return num_pages


def create_pdf(html_content, page_width="8.5in", page_height="11in"):


    custom_style = f"""
    <style type="text/css">
        @page {{
            size: {page_width} {page_height};
            margin: 1cm;
        }}
    </style>
    """

    html_with_style = f"{custom_style}{html_content}"
    # Create a PDF document
    # pdf_document = open(pdf_file, "w+b")
    
    # Generate the PDF from HTML

    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_with_style, dest=pdf_buffer)
    pdf_bytes = None
    # Check if PDF generation was successful
    if pisa_status.err:
        print(f"Error during PDF generation: {pisa_status.err}")
    else:
        # Get the PDF content as bytes
        pdf_bytes = pdf_buffer.getvalue()

        # Now, pdf_bytes contains the PDF content as bytes
        # You can assign it to a variable or use it as needed

        # If you want to save it to a file, you can do so like this:
        # with open('output.pdf', 'wb') as f:
        #     f.write(pdf_bytes)

    # Remember to close the BytesIO object when you're done with it
    pdf_buffer.close()
    return pdf_bytes


def generatePdf(resumeData):
    html_template = None
    with open("templates/resumeTemplate.html", errors="ignore") as f:
        html_template = f.read()
    html_content = render_template_string(html_template, resumeData=resumeData)
    # print(html_content)
    # with open("tml.html", "w") as f:
    #     f.write(html_content)
    result = create_pdf(html_content)
    num_pages = count_pdf_pages(result)
    return result, num_pages