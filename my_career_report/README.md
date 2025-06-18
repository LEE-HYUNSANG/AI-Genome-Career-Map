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
python generate_report.py
```

This will create `dist/report.html` and `dist/report.pdf`.

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

## Chart.js Image Rendering

To create a chart image with Chart.js on Node.js run:

```bash
npm install
node charts/render_big5_chartjs.js
```

This generates `charts/output/big5_chartjs.png` using the data from `data/sample_input.json`.
