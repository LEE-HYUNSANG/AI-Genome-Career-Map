# File: generate_report.py
import os
import yaml

from utils.loader import load_data
from utils.renderer import render_html
from utils.exporter import html_to_pdf
from utils.fontconfig import set_korean_font
from utils.rounder import round_floats
from charts.chartjs_data import generate_chartjs_data
import json
import subprocess
import shutil

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

    # Ensure required Node.js packages are installed
    node_modules = os.path.join(BASE_DIR, 'node_modules')
    datalabels_pkg = os.path.join(node_modules, 'chartjs-plugin-datalabels')
    if not os.path.exists(datalabels_pkg):
        raise RuntimeError(
            "Node dependencies not found. Please run 'npm install' in the "
            "my_career_report directory before generating the report."
        )

    # Copy a local copy of Chart.js so the report works offline
    chartjs_src = os.path.join(BASE_DIR, 'node_modules', 'chart.js', 'dist', 'chart.umd.js')
    chartjs_dest = os.path.join(os.path.dirname(cfg['output']['html']), 'chart.js')
    shutil.copy2(chartjs_src, chartjs_dest)
    cfg['scripts'] = {'chartjs': chartjs_dest}

    # Create static chart images for the PDF using Chart.js
    chart_data_tmp = os.path.join(chart_dir, 'chartjs_input.json')
    with open(chart_data_tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    node_script = os.path.join(BASE_DIR, 'charts', 'render_chartjs_images.js')
    subprocess.run(['node', node_script, chart_data_tmp, chart_dir], check=True)

    generate_chartjs_data(data, cfg['charts']['data'])

    # Provide chart image paths to the template
    cfg['charts']['images'] = chart_paths

    html_path = render_html(data, cfg)

    pdf_path = html_to_pdf(html_path, cfg['output']['pdf'])

    print(f'Successfully generated PDF report at {pdf_path}')


if __name__ == '__main__':
    main()
