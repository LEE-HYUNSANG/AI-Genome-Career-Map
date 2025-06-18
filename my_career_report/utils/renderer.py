# File: utils/renderer.py
import os
from jinja2 import Environment, FileSystemLoader


def render_html(data, cfg):
    """Render the report HTML using Jinja2."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')
    html = template.render(**data, styles=cfg['styles'], charts=cfg['charts'])
    output_path = cfg['output']['html']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path
