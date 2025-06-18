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
  const configuration = {
    type: 'bar',
    data: {
      labels: ['E', 'A', 'C', 'N', 'O'],
      datasets: [{
        label: 'Score',
        data: ['E','A','C','N','O'].map(k => big5[k]),
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 1
      }]
    },
    options: {
      scales: { y: { beginAtZero: true, max: 100 } },
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
