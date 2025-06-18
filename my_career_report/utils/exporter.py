# File: utils/exporter.py
from weasyprint import HTML


def html_to_pdf(html_path, output_pdf):
    """Convert HTML file to PDF using WeasyPrint."""
    HTML(html_path).write_pdf(output_pdf)
    return output_pdf
