const API_BASE_URL = window.location.origin;

let currentMessageResult = null;
let currentUrlResult = null;

document.addEventListener('DOMContentLoaded', function() {
    initCounters();
    
    if (document.getElementById('messageForm')) {
        document.getElementById('messageForm').addEventListener('submit', analyzeMessage);
    }
    
    if (document.getElementById('urlForm')) {
        document.getElementById('urlForm').addEventListener('submit', scanUrl);
    }
    
    if (document.getElementById('historyList')) {
        loadHistory();
    }
});

function initCounters() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    });
}

async function analyzeMessage(e) {
    e.preventDefault();
    
    const message = document.getElementById('messageInput').value.trim();
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('analyzeBtnText');
    const btnSpinner = document.getElementById('analyzeBtnSpinner');
    const results = document.getElementById('messageResults');
    const errorAlert = document.getElementById('messageErrorAlert');
    
    results.classList.add('d-none');
    errorAlert.classList.add('d-none');
    
    analyzeBtn.disabled = true;
    btnText.textContent = '🔄 Analyzing...';
    btnSpinner.classList.remove('d-none');
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze_message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze message');
        }
        
        if (data.success) {
            currentMessageResult = {
                type: 'message',
                content: message,
                analysis: data.analysis,
                timestamp: new Date().toISOString()
            };
            displayMessageResults(data.analysis);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        errorAlert.textContent = error.message;
        errorAlert.classList.remove('d-none');
    } finally {
        analyzeBtn.disabled = false;
        btnText.textContent = '🔍 Analyze Message';
        btnSpinner.classList.add('d-none');
    }
}

function displayMessageResults(analysis) {
    const results = document.getElementById('messageResults');
    const verdict = analysis.final_verdict;
    const ml = analysis.ml_prediction;
    const rules = analysis.rules;
    const triggers = analysis.psychology_triggers;
    
    const verdictAlert = document.getElementById('messageVerdictAlert');
    verdictAlert.className = `alert alert-${verdict.verdict}`;
    document.getElementById('messageVerdictLabel').textContent = verdict.label;
    document.getElementById('messageVerdictRecommendation').textContent = verdict.recommendation;
    document.getElementById('messageRiskScore').textContent = verdict.risk_score;
    
    const mlPrediction = document.getElementById('messageMlPrediction');
    mlPrediction.textContent = ml.prediction.toUpperCase();
    mlPrediction.className = `badge ${ml.prediction === 'phishing' ? 'bg-danger' : 'bg-success'}`;
    
    document.getElementById('messageMlConfidence').textContent = ml.confidence;
    document.getElementById('messagePhishingProb').textContent = ml.phishing_probability;
    document.getElementById('messageSafeProb').textContent = ml.safe_probability;
    
    const phishingBar = document.getElementById('messagePhishingBar');
    phishingBar.style.width = `${ml.phishing_probability}%`;
    phishingBar.textContent = `${ml.phishing_probability}%`;
    
    const rulesContent = document.getElementById('messageRulesContent');
    if (rules.length === 0) {
        rulesContent.innerHTML = '<p class="text-muted mb-0">✓ No rule violations detected</p>';
    } else {
        rulesContent.innerHTML = rules.map(rule => `
            <div class="rule-item ${rule.severity}">
                <strong>${rule.rule}</strong>
                <p class="mb-0 mt-1">${rule.detail}</p>
                <small class="text-muted">Severity: ${rule.severity.toUpperCase()}</small>
            </div>
        `).join('');
    }
    
    const triggersContent = document.getElementById('messageTriggersContent');
    if (triggers.length === 0) {
        triggersContent.innerHTML = '<p class="text-muted mb-0">✓ No psychological manipulation detected</p>';
    } else {
        triggersContent.innerHTML = triggers.map(trigger => `
            <div class="trigger-item">
                <strong>${trigger.type}</strong>
                <p class="mb-1 mt-1">${trigger.description}</p>
                <small class="text-muted">Tactic: ${trigger.tactic}</small>
            </div>
        `).join('');
    }
    
    results.classList.remove('d-none');
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function scanUrl(e) {
    e.preventDefault();
    
    const url = document.getElementById('urlInput').value.trim();
    const scanBtn = document.getElementById('scanBtn');
    const btnText = document.getElementById('scanBtnText');
    const btnSpinner = document.getElementById('scanBtnSpinner');
    const results = document.getElementById('urlResults');
    const errorAlert = document.getElementById('urlErrorAlert');
    
    results.classList.add('d-none');
    errorAlert.classList.add('d-none');
    
    scanBtn.disabled = true;
    btnText.textContent = '🔄 Scanning...';
    btnSpinner.classList.remove('d-none');
    
    try {
        const response = await fetch(`${API_BASE_URL}/scan_url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to scan URL');
        }
        
        if (data.success) {
            currentUrlResult = {
                type: 'url',
                content: url,
                analysis: data.analysis,
                timestamp: new Date().toISOString()
            };
            displayUrlResults(data.analysis);
        } else {
            throw new Error(data.error || 'Scan failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        errorAlert.textContent = error.message;
        errorAlert.classList.remove('d-none');
    } finally {
        scanBtn.disabled = false;
        btnText.textContent = '🔍 Scan URL';
        btnSpinner.classList.add('d-none');
    }
}

function displayUrlResults(analysis) {
    const results = document.getElementById('urlResults');
    const verdict = analysis.final_verdict;
    const ml = analysis.ml_prediction;
    const checks = analysis.checks;
    
    const verdictAlert = document.getElementById('urlVerdictAlert');
    verdictAlert.className = `alert alert-${verdict.verdict}`;
    document.getElementById('urlVerdictLabel').textContent = verdict.label;
    document.getElementById('urlVerdictRecommendation').textContent = verdict.recommendation;
    document.getElementById('urlRiskScore').textContent = verdict.risk_score;
    
    document.getElementById('urlScannedUrl').textContent = analysis.url;
    
    const checksContent = document.getElementById('urlChecksContent');
    checksContent.innerHTML = checks.map(check => `
        <div class="check-item ${check.status}">
            <strong>${check.check}</strong>
            <p class="mb-0 mt-1">${check.message}</p>
        </div>
    `).join('');
    
    const mlPrediction = document.getElementById('urlMlPrediction');
    mlPrediction.textContent = ml.prediction.toUpperCase();
    mlPrediction.className = `badge ${ml.prediction === 'phishing' ? 'bg-danger' : 'bg-success'}`;
    
    document.getElementById('urlMlConfidence').textContent = ml.confidence;
    document.getElementById('urlPhishingProb').textContent = ml.phishing_probability;
    document.getElementById('urlSafeProb').textContent = ml.safe_probability;
    
    const phishingBar = document.getElementById('urlPhishingBar');
    phishingBar.style.width = `${ml.phishing_probability}%`;
    phishingBar.textContent = `${ml.phishing_probability}%`;
    
    results.classList.remove('d-none');
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function saveToHistory(type) {
    const result = type === 'message' ? currentMessageResult : currentUrlResult;
    
    if (!result) {
        alert('No scan result to save');
        return;
    }
    
    let history = JSON.parse(localStorage.getItem('phishShieldHistory') || '[]');
    
    history.unshift(result);
    
    if (history.length > 50) {
        history = history.slice(0, 50);
    }
    
    localStorage.setItem('phishShieldHistory', JSON.stringify(history));
    
    alert('✓ Scan saved to history!');
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem('phishShieldHistory') || '[]');
    const historyList = document.getElementById('historyList');
    const emptyState = document.getElementById('emptyState');
    
    let dangerCount = 0;
    let warningCount = 0;
    let safeCount = 0;
    
    if (history.length === 0) {
        emptyState.classList.remove('d-none');
        historyList.innerHTML = '';
    } else {
        emptyState.classList.add('d-none');
        
        historyList.innerHTML = history.map((item, index) => {
            const verdict = item.analysis.final_verdict;
            const date = new Date(item.timestamp);
            const formattedDate = date.toLocaleString();
            
            if (verdict.verdict === 'danger') dangerCount++;
            else if (verdict.verdict === 'warning') warningCount++;
            else safeCount++;
            
            const preview = item.content.substring(0, 100) + (item.content.length > 100 ? '...' : '');
            
            return `
                <div class="history-item ${verdict.verdict}">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <span class="badge bg-${verdict.verdict === 'danger' ? 'danger' : verdict.verdict === 'warning' ? 'warning text-dark' : 'success'} me-2">
                                ${item.type === 'message' ? '📨 Message' : '🔗 URL'}
                            </span>
                            <span class="badge bg-${verdict.verdict === 'danger' ? 'danger' : verdict.verdict === 'warning' ? 'warning text-dark' : 'success'}">
                                ${verdict.label}
                            </span>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteHistoryItem(${index})">🗑️</button>
                    </div>
                    <p class="mb-2"><strong>${preview}</strong></p>
                    <div class="row">
                        <div class="col-md-6">
                            <small class="text-muted">
                                Risk Score: <strong>${verdict.risk_score}/100</strong>
                            </small>
                        </div>
                        <div class="col-md-6 text-end">
                            <small class="text-muted">${formattedDate}</small>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    document.getElementById('totalScans').textContent = history.length;
    document.getElementById('dangerScans').textContent = dangerCount;
    document.getElementById('warningScans').textContent = warningCount;
    document.getElementById('safeScans').textContent = safeCount;
}

function deleteHistoryItem(index) {
    if (!confirm('Delete this scan from history?')) return;
    
    let history = JSON.parse(localStorage.getItem('phishShieldHistory') || '[]');
    history.splice(index, 1);
    localStorage.setItem('phishShieldHistory', JSON.stringify(history));
    loadHistory();
}

function clearHistory() {
    if (!confirm('Are you sure you want to clear all scan history? This cannot be undone.')) return;
    
    localStorage.removeItem('phishShieldHistory');
    loadHistory();
}
