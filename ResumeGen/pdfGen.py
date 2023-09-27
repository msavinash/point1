from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont


# Rest of your code (including font registration, styles, and PDF generation functions)...
# Import our font
registerFont(TTFont('Inconsolata', 'fonts/Inconsolata-Regular.ttf'))
registerFont(TTFont('InconsolataBold', 'fonts/Inconsolata-Bold.ttf'))
registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')

# Set the page height and width
HEIGHT = 11 * inch
WIDTH = 8.5 * inch

# Set our styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Content',
                          fontFamily='Inconsolata',
                          fontSize=8,
                          spaceAfter=.1*inch))






def generate_print_pdf(pdf_buffer, data, contact):

    pdfData = [
        ['OBJECTIVE', Paragraph(data['objective'], styles['Content'])],
        ['SUMMARY', Paragraph(data['summary'], styles['Content'])],
        ['EDUCATION', Paragraph(data['education'], styles['Content'])],
        ['SKILLS', Paragraph(data['skills'], styles['Content'])],
        ['EXPERIENCE', [Paragraph(x, styles['Content']) for x in data['experience']]],
        ['PROJECTS', [Paragraph(x, styles['Content']) for x in data['projects']]]
    ]


    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        bottomMargin=.5 * inch,
        topMargin=.7 * inch,
        rightMargin=.4 * inch,
        leftMargin=.4 * inch)

    style = styles["Normal"]  # set the style to normal
    story = []  # create a blank story to tell
    contentTable = Table(
        pdfData,
        colWidths=[
            0.8 * inch,
            6.9 * inch])
    tblStyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONT', (0, 0), (-1, -1), 'Inconsolata'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')])
    contentTable.setStyle(tblStyle)
    story.append(contentTable)
    doc.build(
        story,
        onFirstPage=myPageWrapper(
            contact)
        )
    
def myPageWrapper(contact):
    # template for static, non-flowables, on the first page
    # draws all of the contact information at the top of the page
    def myPage(canvas, doc):
        canvas.saveState()  # save the current state
        canvas.setFont('InconsolataBold', 16)  # set the font for the name
        canvas.drawString(
            .4 * inch,
            HEIGHT - (.4 * inch),
            contact['name'])  # draw the name on top left page 1
        canvas.setFont('Inconsolata', 8)  # sets the font for contact
        canvas.drawRightString(
            WIDTH - (.4 * inch),
            HEIGHT - (.4 * inch),
            contact['website'])  
        canvas.line(.4 * inch, HEIGHT - (.47 * inch), 
            WIDTH - (.4 * inch), HEIGHT - (.47 * inch))
        canvas.drawString(
            .4 * inch,
            HEIGHT - (.6 * inch),
            contact['phone'])
        canvas.drawCentredString(
			WIDTH / 2.0,
			HEIGHT - (.6 * inch),
			contact['address'])
        canvas.drawRightString(
			WIDTH - (.4 * inch),
			HEIGHT - (.6 * inch),
			contact['email'])
        # restore the state to what it was when saved
        canvas.restoreState()
    return myPage