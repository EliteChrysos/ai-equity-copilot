from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def create_pdf_report(title, report_text):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    for line in report_text.split("\n"):
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))

    pdf.build(story)

    buffer.seek(0)
    return buffer