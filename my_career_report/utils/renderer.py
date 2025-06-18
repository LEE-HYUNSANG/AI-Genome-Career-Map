# File: utils/renderer.py
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def render_html(data: dict, cfg: dict) -> str:
    """Render the report HTML using Jinja2 templates."""
    project_root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(project_root / 'templates'))
    template = env.get_template('report.html')
    html = template.render(**data, styles=cfg['styles'], charts=cfg['charts'])
    output_path = cfg['output']['html']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path
