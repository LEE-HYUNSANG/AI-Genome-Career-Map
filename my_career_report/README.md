# my_career_report

This project generates automated career reports using data files and Jinja2 templates.

## Structure

- `config.yaml` – output locations and chart settings
- `data/` – sample input data
- `charts/` – chart rendering modules
- `templates/` – Jinja2 templates and CSS assets
- `utils/` – helper modules for loading data, rendering HTML and exporting PDF

## Install & Run

```bash
pip install -r requirements.txt
npm install --silent
python generate_report.py
```

This will create `dist/report.html` and `dist/report.pdf`.

### Korean fonts

The charts rely on the **Noto Sans CJK** fonts that ship with most Linux
distributions. `generate_report.py` loads this font at runtime so Korean labels
render correctly. If the font is missing, the script falls back to other common
Korean fonts such as NanumGothic or Malgun Gothic when available.

### WeasyPrint dependencies

WeasyPrint relies on external libraries such as **cairo** and **Pango**. On
Linux these are typically available through your package manager (for example
`apt-get install libpangocairo-1.0-0 libcairo2`).

On Windows you must install the bundled dependencies from the
[WeasyPrint documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation).
If you see an error about `libgobject-2.0-0` when running the script, it means
these libraries are missing. Installing the official WeasyPrint binaries or the
MSYS2 packages will resolve the issue.

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/ci.yml` installs dependencies and runs `generate_report.py` on each push. The generated PDF is uploaded as a workflow artifact.

## Chart.js Data

`generate_report.py` now renders Chart.js graphs for the PDF by calling a Node
script. It also exports a JSON file with the data needed for the web version at
`charts/output/chart_data.json`.
