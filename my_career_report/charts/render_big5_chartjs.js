import { ChartJSNodeCanvas } from 'chartjs-node-canvas';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function renderBig5(data, outputPath) {
  const width = 600;
  const height = 400;
  const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });
  const big5 = data.big5 || data;
  const LABEL_MAP = { E: '외향성', A: '친화성', C: '성실성', N: '신경성', O: '개방성' };
  const codes = ['E', 'A', 'C', 'N', 'O'];
  const configuration = {
    type: 'polarArea',
    data: {
      labels: codes.map(c => LABEL_MAP[c]),
      datasets: [{
        label: 'Score',
        data: codes.map(c => big5[c]),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: { r: { beginAtZero: true, max: 100 } },
      plugins: { title: { display: true, text: 'BIG-5 Scores' } }
    }
  };
  const buffer = await chartJSNodeCanvas.renderToBuffer(configuration);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
}

async function main() {
  const dataPath = path.join(__dirname, '../data/sample_input.json');
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  const out = path.join(__dirname, 'output/big5_chartjs.png');
  await renderBig5(data, out);
  console.log('Chart saved to', out);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
