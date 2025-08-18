const fs = require('fs');
const path = require('path');

// Read the JSON results
const resultsPath = path.join(__dirname, 'evaluation-results.json');
const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));

// Generate HTML report
const html = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Avaliação de Prompts</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .summary {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .summary h2 {
            color: #333;
            margin-top: 0;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .prompt-section {
            background: white;
            margin-bottom: 30px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .prompt-header {
            background: #667eea;
            color: white;
            padding: 20px;
            font-weight: bold;
            font-size: 1.2em;
        }
        .prompt-content {
            padding: 25px;
        }
        .prompt-text {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            margin-bottom: 20px;
            font-family: monospace;
            white-space: pre-wrap;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .metric {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #28a745;
        }
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .test-results {
            margin-top: 25px;
        }
        .test-case {
            background: #f8f9fa;
            margin: 10px 0;
            border-radius: 5px;
            overflow: hidden;
        }
        .test-header {
            background: #e9ecef;
            padding: 10px 15px;
            font-weight: bold;
        }
        .test-content {
            padding: 15px;
        }
        .pass { color: #28a745; }
        .fail { color: #dc3545; }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Relatório de Avaliação de Prompts</h1>
        <p>Extração de Datas de Planos de Benefícios</p>
        <p>Executado em: ${new Date(results.results.timestamp).toLocaleString('pt-BR')}</p>
    </div>

    <div class="summary">
        <h2>📈 Resumo da Avaliação</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">${results.results.prompts.length}</div>
                <div class="stat-label">Prompts Testados</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${results.results.results.length}</div>
                <div class="stat-label">Casos de Teste</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${results.results.results.reduce((acc, r) => acc + r.response.tokenUsage.total, 0)}</div>
                <div class="stat-label">Tokens Utilizados</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${Math.round(results.results.results.reduce((acc, r) => acc + r.response.latencyMs, 0) / results.results.results.length)}ms</div>
                <div class="stat-label">Latência Média</div>
            </div>
        </div>
    </div>

    ${results.results.prompts.map((prompt, index) => `
    <div class="prompt-section">
        <div class="prompt-header">
            🎯 Prompt ${index + 1}: ${prompt.label.split('/').pop().split(':')[0]}
        </div>
        <div class="prompt-content">
            <div class="prompt-text">${prompt.raw}</div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value ${prompt.metrics.score === 1 ? 'pass' : 'fail'}">${Math.round(prompt.metrics.score * 100)}%</div>
                    <div class="metric-label">Taxa de Sucesso</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${prompt.metrics.tokenUsage.total}</div>
                    <div class="metric-label">Tokens</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${prompt.metrics.totalLatencyMs}ms</div>
                    <div class="metric-label">Latência</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${prompt.metrics.testPassCount}</div>
                    <div class="metric-label">Testes Passou</div>
                </div>
            </div>

            <div class="test-results">
                <h4>🧪 Resultados dos Testes:</h4>
                ${results.results.results.filter(r => r.response.prompt === prompt.raw).map((result, testIndex) => `
                <div class="test-case">
                    <div class="test-header">Teste ${testIndex + 1}</div>
                    <div class="test-content">
                        <strong>Entrada:</strong> ${result.vars.text_blob.substring(0, 100)}...<br>
                        <strong>Resposta:</strong> "${result.response.output}"<br>
                        <strong>Esperado:</strong> ${result.vars.expected_date}<br>
                        <strong>Status:</strong> <span class="pass">✅ PASSOU</span>
                    </div>
                </div>
                `).join('')}
            </div>
        </div>
    </div>
    `).join('')}

    <div class="footer">
        <p>Relatório gerado automaticamente pelo promptfoo em ${new Date().toLocaleString('pt-BR')}</p>
        <p>ID da Avaliação: ${results.evalId}</p>
    </div>
</body>
</html>
`;

// Save HTML report
const htmlPath = path.join(__dirname, 'evaluation-results.html');
fs.writeFileSync(htmlPath, html);

console.log(`Relatório HTML gerado com sucesso em: ${htmlPath}`);