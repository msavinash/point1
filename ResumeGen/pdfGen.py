

from flask import Flask, render_template, jsonify, render_template_string 

from io import BytesIO

import PyPDF2
from io import BytesIO
import pdfkit


def count_pdf_pages(pdf_content):
    pdf_buffer = BytesIO(pdf_content)
    pdf = PyPDF2.PdfReader(pdf_buffer)
    num_pages = len(pdf.pages)
    return num_pages




def generatePdf(resumeData):
    html_template = None
    with open("templates/resumeTemplate.html", errors="ignore") as f:
        html_template = f.read()
    html_content = render_template_string(html_template, resumeData=resumeData)
    # with open("tml.html", "w") as f:
    #     f.write(html_content)
    options={'page-size':'A4'}#, 'dpi':400}
    result = pdfkit.from_string(html_content, options=options)
    num_pages = count_pdf_pages(result)
    return result, num_pages