import { ChartJSNodeCanvas } from 'chartjs-node-canvas';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function renderInterest(data, outputPath) {
  const width = 600;
  const height = 400;
  const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });
  const interest = data.interest || data;
  const configuration = {
    type: 'radar',
    data: {
      labels: ['R', 'I', 'A', 'S', 'E', 'C'],
      datasets: [{
        label: 'Score',
        data: ['R','I','A','S','E','C'].map(k => interest[k]),
        backgroundColor: 'rgba(54, 162, 235, 0.3)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 2
      }]
    },
    options: {
      scales: { r: { beginAtZero: true, max: 100 } },
      plugins: { title: { display: true, text: 'RIASEC Interest' } }
    }
  };
  const buffer = await chartJSNodeCanvas.renderToBuffer(configuration);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
}

async function main() {
  const dataPath = path.join(__dirname, '../data/sample_input.json');
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  const out = path.join(__dirname, 'output/interest_chartjs.png');
  await renderInterest(data, out);
  console.log('Chart saved to', out);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
