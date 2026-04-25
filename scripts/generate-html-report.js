const fs = require('fs');
const path = require('path');

const DEFAULT_INPUT_PATH = path.join(__dirname, '..', 'artifacts', 'generated', 'evaluation-results.json');
const DEFAULT_OUTPUT_PATH = path.join(__dirname, '..', 'artifacts', 'generated', 'evaluation-results.html');

function parseArgs(argv) {
    const args = {};

    for (let index = 0; index < argv.length; index += 1) {
        const token = argv[index];
        const next = argv[index + 1];

        if (token === '--input' && next) {
            args.input = next;
            index += 1;
        } else if (token === '--output' && next) {
            args.output = next;
            index += 1;
        }
    }

    return args;
}

const cliArgs = parseArgs(process.argv.slice(2));
const resultsPath = path.resolve(cliArgs.input || DEFAULT_INPUT_PATH);
const htmlPath = path.resolve(cliArgs.output || DEFAULT_OUTPUT_PATH);
const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));

const getPromptName = (prompt) => {
    if (!prompt || typeof prompt.label !== 'string') {
        return 'unknown-prompt';
    }

    const label = prompt.label;
    const labelParts = label.split('/');
    return labelParts[labelParts.length - 1] || label;
};

const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

const formatLatency = (latencyMs) => {
    if (!Number.isFinite(latencyMs)) {
        return 'n/a';
    }

    return `${Math.round(latencyMs)}ms`;
};

const getResultLatency = (result) => Number(result?.latencyMs ?? result?.response?.latencyMs ?? NaN);

const promptSummaries = results.results.prompts.map((prompt) => {
    const promptResults = results.results.results.filter((result) => result.prompt?.raw === prompt.raw);
    const totalLatencyMs = promptResults.reduce((acc, result) => acc + getResultLatency(result), 0);
    const totalTokens = promptResults.reduce((acc, result) => acc + Number(result?.response?.tokenUsage?.total ?? 0), 0);

    return {
        prompt,
        promptResults,
        averageLatencyMs: promptResults.length > 0 ? totalLatencyMs / promptResults.length : NaN,
        totalTokens,
    };
});

const totalTokens = promptSummaries.reduce((acc, item) => acc + item.totalTokens, 0);
const totalLatencyMs = results.results.results.reduce((acc, result) => acc + getResultLatency(result), 0);
const averageLatencyMs = results.results.results.length > 0
    ? totalLatencyMs / results.results.results.length
    : NaN;

const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Evaluation Report</title>
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
        <h1>Prompt Evaluation Report</h1>
        <p>Benefit Start Date Extraction Benchmark</p>
        <p>Executed at: ${new Date(results.results.timestamp).toLocaleString('en-US')}</p>
    </div>

    <div class="summary">
        <h2>Evaluation Summary</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">${results.results.prompts.length}</div>
                <div class="stat-label">Prompts Tested</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${results.results.results.length}</div>
                <div class="stat-label">Test Cases</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${totalTokens}</div>
                <div class="stat-label">Tokens Used</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${formatLatency(averageLatencyMs)}</div>
                <div class="stat-label">Average Latency</div>
            </div>
        </div>
    </div>

    ${promptSummaries.map(({ prompt, promptResults, averageLatencyMs, totalTokens }, index) => `
    <div class="prompt-section">
        <div class="prompt-header">
            Prompt ${index + 1}: ${escapeHtml(getPromptName(prompt))}
        </div>
        <div class="prompt-content">
            <div class="prompt-text">${escapeHtml(prompt.raw)}</div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value ${prompt.metrics.score === 1 ? 'pass' : 'fail'}">${Math.round(prompt.metrics.score * 100)}%</div>
                    <div class="metric-label">Success Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${totalTokens}</div>
                    <div class="metric-label">Total Tokens</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${formatLatency(averageLatencyMs)}</div>
                    <div class="metric-label">Average Latency</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${prompt.metrics.testPassCount}</div>
                    <div class="metric-label">Tests Passed</div>
                </div>
            </div>

            <div class="test-results">
                <h4>Test Results</h4>
                ${promptResults.map((result, testIndex) => `
                <div class="test-case">
                    <div class="test-header">Test ${testIndex + 1}</div>
                    <div class="test-content">
                        <strong>Description:</strong> ${escapeHtml(result.testCase?.description || 'n/a')}<br>
                        <strong>Category:</strong> ${escapeHtml(result.testCase?.metadata?.category || 'n/a')}<br>
                        <strong>Input:</strong> ${escapeHtml((result.vars.text_blob || '').substring(0, 140))}${(result.vars.text_blob || '').length > 140 ? '...' : ''}<br>
                        <strong>Output:</strong> "${escapeHtml(result.response.output)}"<br>
                        <strong>Expected:</strong> ${escapeHtml(result.vars.expected_date || 'n/a')}<br>
                        <strong>Latency:</strong> ${formatLatency(getResultLatency(result))}<br>
                        <strong>Status:</strong> <span class="${result.success ? 'pass' : 'fail'}">${result.success ? 'PASS' : 'FAIL'}</span>
                    </div>
                </div>
                `).join('')}
            </div>
        </div>
    </div>
    `).join('')}

    <div class="footer">
        <p>Automatically generated from promptfoo output at ${new Date().toLocaleString('en-US')}</p>
        <p>Evaluation ID: ${results.evalId}</p>
    </div>
</body>
</html>
`;

fs.mkdirSync(path.dirname(htmlPath), { recursive: true });
fs.writeFileSync(htmlPath, html);

console.log(`HTML report generated at: ${htmlPath}`);
