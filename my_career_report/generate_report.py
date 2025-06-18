# File: generate_report.py
import os
import yaml

from utils.loader import load_data
from utils.renderer import render_html
from utils.exporter import html_to_pdf
from utils.fontconfig import set_korean_font
from charts.chartjs_data import generate_chartjs_data

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

    data = load_data(DATA_PATH)

    os.makedirs(os.path.join(BASE_DIR, 'dist'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'charts', 'output'), exist_ok=True)


    generate_chartjs_data(data, cfg['charts']['data'])

    html_path = render_html(data, cfg)

    pdf_path = html_to_pdf(html_path, cfg['output']['pdf'])

    print(f'Successfully generated PDF report at {pdf_path}')


if __name__ == '__main__':
    main()
