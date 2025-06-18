import { ChartJSNodeCanvas } from 'chartjs-node-canvas';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function renderCharts(dataPath, outDir) {
  const width = 600;
  const height = 400;
  const canvas = new ChartJSNodeCanvas({ width, height, chartCallback: (Chart) => { Chart.defaults.font.size = 24; } });
  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });

  const big5Codes = ['E','A','C','N','O'];
  const big5Labels = ['외향성','친화성','성실성','신경성','개방성'];
  const big5Scores = big5Codes.map(k => data.big5[k]);
  const big5Norm = big5Codes.map(k => (data.big5_norm || {})[k]);
  let config = {
    type: 'radar',
    data: {
      labels: big5Labels,
      datasets: [
        {
          label: 'Your Score',
          data: big5Scores,
          backgroundColor: 'rgba(54, 162, 235, 0.3)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 2
        },
        {
          label: 'Global Norm',
          data: big5Norm,
          backgroundColor: 'rgba(255, 99, 132, 0.1)',
          borderColor: 'rgb(255, 99, 132)',
          borderWidth: 2
        }
      ]
    },
    options: { scales: { r: { beginAtZero: true, max: 100 } } }
  };
  let buffer = await canvas.renderToBuffer(config);
  fs.writeFileSync(path.join(outDir, 'big5.png'), buffer);

  const interestCodes = ['R','I','A','S','E','C'];
  const interestLabels = ['현실형','탐구형','예술형','사회형','기업형','관습형'];
  const interestScores = interestCodes.map(k => data.interest[k]);
  config = {
    type: 'bar',
    data: { labels: interestLabels, datasets: [{ label: 'Score', data: interestScores }] },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
  };
  buffer = await canvas.renderToBuffer(config);
  fs.writeFileSync(path.join(outDir, 'interest.png'), buffer);

  const valuesCodes = ['A','I','Rec','Rel','S','W'];
  const valuesLabels = ['능력발휘','자율성','보상','안정성','사회적 인정','워라밸'];
  const valuesScores = valuesCodes.map(k => data.values[k]);
  config = {
    type: 'radar',
    data: { labels: valuesLabels, datasets: [{ label: 'Score', data: valuesScores }] },
    options: { scales: { r: { beginAtZero: true, max: 100 } } }
  };
  buffer = await canvas.renderToBuffer(config);
  fs.writeFileSync(path.join(outDir, 'values.png'), buffer);

  const aiCodes = ['EU','TS','CE','AO','SE','CB','ER'];
  const aiLabels = ['AI 이해','프롬프트','검증','도구 적용','학습','협업','윤리'];
  const aiScores = aiCodes.map(k => data.ai[k]);
  config = {
    type: 'radar',
    data: { labels: aiLabels, datasets: [{ label: 'Score', data: aiScores }] },
    options: { scales: { r: { beginAtZero: true, max: 100 } } }
  };
  buffer = await canvas.renderToBuffer(config);
  fs.writeFileSync(path.join(outDir, 'ai.png'), buffer);

  const techLabels = data.tech.map(t => t.name);
  const techScores = data.tech.map(t => t.score);
  config = {
    type: 'bar',
    data: { labels: techLabels, datasets: [{ label: 'Score', data: techScores }] },
    options: { indexAxis: 'y', scales: { x: { beginAtZero: true, max: 100 } } }
  };
  buffer = await canvas.renderToBuffer(config);
  fs.writeFileSync(path.join(outDir, 'tech.png'), buffer);

  const softLabels = data.soft.map(t => t.name);
  const softScores = data.soft.map(t => t.score);
  config = {
    type: 'bar',
    data: { labels: softLabels, datasets: [{ label: 'Score', data: softScores }] },
    options: { indexAxis: 'y', scales: { x: { beginAtZero: true, max: 100 } } }
  };
  buffer = await canvas.renderToBuffer(config);
  fs.writeFileSync(path.join(outDir, 'soft.png'), buffer);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [dataPath, outDir] = process.argv.slice(2);
  renderCharts(dataPath, outDir).catch(err => { console.error(err); process.exit(1); });
}
