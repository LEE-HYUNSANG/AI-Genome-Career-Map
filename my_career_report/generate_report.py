# File: generate_report.py
import os
import yaml

from utils.loader import load_data
from utils.renderer import render_html
from utils.exporter import html_to_pdf
from utils.fontconfig import set_korean_font
from utils.rounder import round_floats
from charts.chartjs_data import generate_chartjs_data
from charts.big5_chart import render_big5
from charts.other_charts import (
    render_interest,
    render_values,
    render_ai,
    render_tech,
    render_soft,
)

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'config.yaml')
DATA_PATH = os.path.join(BASE_DIR, 'data/sample_input.json')


def main():
    set_korean_font()
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    # Resolve relative paths based on project directory
    cfg['output']['html'] = os.path.join(BASE_DIR, cfg['output']['html'])
    cfg['output']['pdf'] = os.path.join(BASE_DIR, cfg['output']['pdf'])
    cfg['charts']['data'] = os.path.join(BASE_DIR, cfg['charts']['data'])
    cfg['charts']['images'] = os.path.join(BASE_DIR, cfg['charts'].get('images', 'charts/output'))

    chart_dir = cfg['charts']['images']
    os.makedirs(chart_dir, exist_ok=True)

    chart_paths = {
        'big5': os.path.join(chart_dir, 'big5.png'),
        'interest': os.path.join(chart_dir, 'interest.png'),
        'values': os.path.join(chart_dir, 'values.png'),
        'ai': os.path.join(chart_dir, 'ai.png'),
        'tech': os.path.join(chart_dir, 'tech.png'),
        'soft': os.path.join(chart_dir, 'soft.png'),
    }

    data = load_data(DATA_PATH)
    data = round_floats(data, 1)

    os.makedirs(os.path.join(BASE_DIR, 'dist'), exist_ok=True)

    # Create static chart images for the PDF
    render_big5(data, chart_paths['big5'], cfg)
    render_interest(data, chart_paths['interest'], cfg)
    render_values(data, chart_paths['values'], cfg)
    render_ai(data, chart_paths['ai'], cfg)
    render_tech(data, chart_paths['tech'], cfg)
    render_soft(data, chart_paths['soft'], cfg)

    generate_chartjs_data(data, cfg['charts']['data'])

    # Provide chart image paths to the template
    cfg['charts']['images'] = chart_paths

    html_path = render_html(data, cfg)

    pdf_path = html_to_pdf(html_path, cfg['output']['pdf'])

    print(f'Successfully generated PDF report at {pdf_path}')


if __name__ == '__main__':
    main()
