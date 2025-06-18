# File: generate_report.py
import os
import yaml

from utils.loader import load_data
from utils.renderer import render_html
from utils.exporter import html_to_pdf
from utils.fontconfig import set_korean_font
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
    for key in ['big5', 'interest', 'values', 'ai', 'tech', 'soft']:
        cfg['charts'][key] = os.path.join(BASE_DIR, cfg['charts'][key])

    data = load_data(DATA_PATH)

    os.makedirs(os.path.join(BASE_DIR, 'dist'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'charts', 'output'), exist_ok=True)

    render_big5(data, cfg['charts']['big5'], cfg)
    render_interest(data, cfg['charts']['interest'], cfg)
    render_values(data, cfg['charts']['values'], cfg)
    render_ai(data, cfg['charts']['ai'], cfg)
    render_tech(data, cfg['charts']['tech'], cfg)
    render_soft(data, cfg['charts']['soft'], cfg)

    html_path = render_html(data, cfg)

    pdf_path = html_to_pdf(html_path, cfg['output']['pdf'])

    print(f'Successfully generated PDF report at {pdf_path}')


if __name__ == '__main__':
    main()
