# File: generate_report.py
import os
import yaml

from utils.loader import load_data
from utils.renderer import render_html
from utils.exporter import html_to_pdf
from charts.big5_chart import render_big5

CONFIG_PATH = 'config.yaml'
DATA_PATH = 'data/sample_input.json'


def main():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    data = load_data(DATA_PATH)

    os.makedirs('dist', exist_ok=True)
    os.makedirs('charts/output', exist_ok=True)

    render_big5(data, cfg['charts']['big5'], cfg)

    html_path = render_html(data, cfg)

    pdf_path = html_to_pdf(html_path, cfg['output']['pdf'])

    print(f'Report generated: {pdf_path}')


if __name__ == '__main__':
    main()
