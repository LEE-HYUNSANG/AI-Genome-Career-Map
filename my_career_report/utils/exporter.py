# File: utils/exporter.py
from weasyprint import HTML


def html_to_pdf(html_path: str, output_pdf: str) -> str:
    """Convert an HTML file to PDF and return the PDF path."""
    HTML(html_path).write_pdf(output_pdf)
    return output_pdf
