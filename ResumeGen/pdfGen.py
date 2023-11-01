

from flask import Flask, render_template, jsonify, render_template_string 

from io import BytesIO

import PyPDF2
from io import BytesIO
import pdfkit
import os


def count_pdf_pages(pdf_content):
    pdf_buffer = BytesIO(pdf_content)
    pdf = PyPDF2.PdfReader(pdf_buffer)
    num_pages = len(pdf.pages)
    return num_pages




def generatePdf(resumeData, design):
    html_template = None
    with open("templates/"+design+".html", errors="ignore") as f:
        html_template = f.read()
    pwd = os.getcwd()
    html_content = render_template_string(html_template, resumeData=resumeData, pwd=pwd)
    with open("tml.html", "w") as f:
        f.write(html_content)
    options={'page-size':'A4', 'enable-local-file-access': None, 'margin-top': '0.37in', 'margin-right': '0.37in', 'margin-bottom': '0.37in', 'margin-left': '0.37in'}#, 'dpi':400}
    result = pdfkit.from_string(html_content, options=options)
    # result = pdfkit.from_file("tml.html", options=options)
    num_pages = count_pdf_pages(result)
    return result, num_pages