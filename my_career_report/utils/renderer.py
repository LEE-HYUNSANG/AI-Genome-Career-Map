# File: utils/renderer.py
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def render_html(data: dict, cfg: dict) -> str:
    """Render the report HTML using Jinja2 templates."""
    project_root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(project_root / 'templates'))
    template = env.get_template('report.html')
    # Resolve the CSS path relative to the output HTML so both the browser and
    # WeasyPrint can correctly load the stylesheet.  Without this, the
    # generated HTML contained a broken path (e.g. ``templates/assets/style.css``)
    # which caused the PDF to render without colours or layout.
    style_src = project_root / cfg['styles']['css']
    rel_style = os.path.relpath(style_src, start=os.path.dirname(cfg['output']['html']))
    styles = dict(cfg['styles'])
    styles['css'] = rel_style

    html = template.render(**data, styles=styles, charts=cfg['charts'])
    output_path = cfg['output']['html']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path
