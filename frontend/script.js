let recognition;
let radarInstance = null;
let gaugeInstance = null;
let lastSummary = "";
let typingTimer;
let liveTimeout = null;
let driftInstance = null;

// =====================
// DRIFT GRAPH
// =====================

function renderDriftGraph(value) {

  const ctx = document.getElementById("driftChart").getContext("2d");

  if (driftInstance) driftInstance.destroy();

  driftInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Start", "Mid", "End"],
      datasets: [{
        data: [10, value / 2, value],
        borderColor: "#5f9cff",
        tension: 0.4
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: { min: 0, max: 100 }
      }
    }
  });
}


// =====================
// EXPORT PDF
// =====================

async function exportPDF() {

  const problem = document.getElementById("problem").value;
  const confidence = document.getElementById("confidence").value;
  const stepInputs = document.querySelectorAll("#steps-container textarea");
  const steps = Array.from(stepInputs).map(input => input.value);

  const response = await fetch("http://127.0.0.1:8000/export", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem_statement: problem,
      steps: steps,
      confidence_level: parseInt(confidence)
    })
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "Cognitive_Report.pdf";
  a.click();
}
// =====================
// VOICE INPUT
// =====================

function startVoiceInput() {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Speech Recognition not supported in this browser.");
    return;
  }

  recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";

  recognition.onstart = showListeningIndicator;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    handleVoiceCommand(transcript);
  };

  recognition.start();
}

// =====================
// LIVE AUTO ANALYSIS
// =====================

document.addEventListener("input", () => {
  clearTimeout(liveTimeout);
  liveTimeout = setTimeout(runLiveAnalysis, 1200);
});

async function runLiveAnalysis() {

  const problem = document.getElementById("problem").value;
  const confidence = document.getElementById("confidence").value;
  const stepInputs = document.querySelectorAll("#steps-container textarea");
  const steps = Array.from(stepInputs).map(input => input.value);

  if (!problem || steps.length === 0) return;

  const response = await fetch("http://127.0.0.1:8000/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem_statement: problem,
      steps: steps,
      confidence_level: parseInt(confidence)
    })
  });

  const data = await response.json();

  updateLiveDashboard(data);
}

function updateLiveDashboard(data) {

  const live = document.getElementById("livePreview");

  live.innerHTML = `
    <div class="text-[#5f9cff] font-semibold">
      Live Intelligence:
      ${data.ensemble.cognitive_intelligence_index.toFixed(1)}
    </div>
  `;

  renderDisagreementHeat(data.ensemble.disagreement_index);
}
function handleVoiceCommand(text) {
  const lower = text.toLowerCase();

  if (lower.includes("problem")) {
    document.getElementById("problem").value = text;
  } else {
    addStep();
    const stepInputs = document.querySelectorAll("#steps-container textarea");
    stepInputs[stepInputs.length - 1].value = text;
  }
}

function showListeningIndicator() {
  const results = document.getElementById("results");
  results.innerHTML = `
    <div class="flex items-center space-x-3">
      <div class="w-3 h-3 bg-red-500 rounded-full animate-ping"></div>
      <div class="text-red-400">Listening...</div>
    </div>
  `;
}

// =====================
// ADD STEP
// =====================

function addStep() {
  const container = document.getElementById("steps-container");

  const input = document.createElement("textarea");
  input.className = "w-full p-3 input-dark text-white rounded";
  input.placeholder = "Enter step...";

  container.appendChild(input);
}

// =====================
// MAIN ANALYSIS
// =====================

async function analyze() {

  showLoader();

  const problem = document.getElementById("problem").value;
  const confidence = document.getElementById("confidence").value;
  const stepInputs = document.querySelectorAll("#steps-container textarea");
  const steps = Array.from(stepInputs).map(input => input.value);

  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem_statement: problem,
      steps: steps,
      confidence_level: parseInt(confidence)
    })
  });

  const data = await response.json();

  renderResults(data);
  renderRadar(data);
  renderGauge(data);
  renderReasoningGraph(data);
}


// =====================
// LOADER
// =====================

function showLoader() {
  document.getElementById("results").innerHTML = `
    <div class="loader"></div>
    <p class="text-center mt-4 text-[#813FF1]">
      AI analyzing cognitive structure...
    </p>
  `;
}

// =====================
// RESULTS RENDERING
// =====================

function renderResults(data) {

  lastSummary = data.reasoning_summary || "";

  const results = document.getElementById("results");

  results.innerHTML = `
    ${progressBar("Overall Score", data.overall_cognitive_score)}
    ${progressBar("Completeness", data.step_completeness_score)}
    ${progressBar("Consistency", data.logical_consistency_score)}

    <div>
      <strong class="text-[#813FF1]">Confidence:</strong>
      ${data.confidence_alignment}
    </div>

    <div class="mt-4">
      <strong class="text-[#813FF1]">Cognitive Profile:</strong>
      ${classifyProfile(data)}
    </div>

    <div class="mt-4">
      <strong class="text-[#813FF1]">Risk Index:</strong>
      <span style="color:${getRiskColor(data.cognitive_risk_index)}">
        ${data.cognitive_risk_index}
      </span>
    </div>

    <div class="mt-4">
      <strong class="text-[#813FF1]">Summary:</strong>
      <p id="typingSummary"></p>
    </div>
  `;

  typeText("typingSummary", lastSummary);
}

// =====================
// VOICE OUTPUT
// =====================

function speakAI() {

  if (!lastSummary) return;

  const orb = document.getElementById("aiOrb");
  orb.classList.add("animate-ping");

  const speech = new SpeechSynthesisUtterance(lastSummary);

  speech.onend = () => {
    orb.classList.remove("animate-ping");
  };

  speechSynthesis.speak(speech);
}

// =====================
// RADAR
// =====================

function renderRadar(data) {

  const ctx = document.getElementById("radarChart").getContext("2d");

  if (radarInstance) radarInstance.destroy();

  radarInstance = new Chart(ctx, {
    type: "radar",
    data: {
      labels: [
        "Overall",
        "Completeness",
        "Consistency",
        "Depth",
        "Coherence",
        "Error Sensitivity",
        "Stability"
      ],
      datasets: [{
        data: [
          data.overall_cognitive_score,
          data.step_completeness_score,
          data.logical_consistency_score,
          data.analytical_depth,
          data.structural_coherence,
          data.error_sensitivity,
          data.cognitive_stability_index
        ],
        backgroundColor: "rgba(129,63,241,0.2)",
        borderColor: "#813FF1"
      }]
    },
    options: {
      scales: {
        r: {
          min: 0,
          max: 100,
          pointLabels: { color: "white" },
          grid: { color: "#333" }
        }
      }
    }
  });
}

// =====================
// GAUGE
// =====================

function renderGauge(data) {

  const ctx = document.getElementById("stabilityGauge").getContext("2d");

  if (gaugeInstance) gaugeInstance.destroy();

  gaugeInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      datasets: [{
        data: [data.cognitive_stability_index, 100 - data.cognitive_stability_index],
        backgroundColor: ["#813FF1", "#222"],
        borderWidth: 0
      }]
    },
    options: {
      rotation: -90,
      circumference: 180,
      cutout: "70%",
      plugins: { legend: { display: false } }
    }
  });
}

// =====================
// REASONING GRAPH
// =====================

function renderReasoningGraph(data) {

  const container = document.getElementById("reasoningGraph");
  container.innerHTML = "<h3 class='text-[#813FF1]'>Reasoning Flow</h3>";

  data.reasoning_graph.forEach(step => {
    container.innerHTML += `
      <div class="p-3 rounded border border-gray-700">
        Step ${step.step_number}: ${step.content}
      </div>
    `;
  });
}

// =====================
// MULTI AGENT COMPARISON
// =====================

async function compareAgents() {

  const problem = document.getElementById("problem").value;
  const confidence = document.getElementById("confidence").value;
  const stepInputs = document.querySelectorAll("#steps-container textarea");
  const steps = Array.from(stepInputs).map(input => input.value);

  showCompareLoader();

  const response = await fetch("http://127.0.0.1:8000/compare", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem_statement: problem,
      steps: steps,
      confidence_level: parseInt(confidence)
    })
  });

  const data = await response.json();
  // Complete progress animation
const bar = document.getElementById("compareProgressBar");
if (bar) {
  bar.style.width = "100%";
}
  savePerformance(data.ensemble.cognitive_intelligence_index);

  renderAgentComparison(data);
}

function renderAgentComparison(data) {

  const container = document.getElementById("agentComparison");

  const intelligenceRing = `
<div class="flex justify-center mb-6">
  <div class="relative w-32 h-32">
    <svg class="w-32 h-32 transform -rotate-90">
      <circle cx="64" cy="64" r="54"
              stroke="#333"
              stroke-width="8"
              fill="none"/>
      <circle cx="64" cy="64" r="54"
              stroke="#813FF1"
              stroke-width="8"
              fill="none"
              stroke-dasharray="339"
              stroke-dashoffset="${339 - (339 * data.ensemble.cognitive_intelligence_index / 100)}"
              style="transition:all 1s"/>
    </svg>
    <div class="absolute inset-0 flex items-center justify-center text-xl font-bold text-[#5f9cff]">
      ${data.ensemble.cognitive_intelligence_index.toFixed(0)}
    </div>
  </div>
</div>
`;

  container.innerHTML = intelligenceRing + `
    <div class="glass p-6 rounded-xl space-y-8">

      <h3 class="text-2xl text-[#813FF1]">
        Multi-Agent Cognitive Architecture
      </h3>

      <!-- ENSEMBLE -->
      <div>
        <h4 class="text-[#5f9cff] font-bold">Ensemble Intelligence</h4>
        <p>Cognitive Intelligence Index: 
          ${data.ensemble.cognitive_intelligence_index.toFixed(2)}</p>
        <p>Logical Avg: ${data.ensemble.logical_average.toFixed(2)}</p>
        <p>Creative Avg: ${data.ensemble.creative_average.toFixed(2)}</p>
        <p>Disagreement Index: ${data.ensemble.disagreement_index.toFixed(2)}</p>
        <p>Drift Score: ${data.ensemble.drift_score}</p>
      </div>

      <!-- BIAS -->
      <div>
        <h4 class="text-red-400 font-bold">Bias & Risk Analysis</h4>
        <p>Confirmation Bias: ${data.bias_agent.confirmation_bias_risk}</p>
        <p>Overconfidence Risk: ${data.bias_agent.overconfidence_risk}</p>
        <p>Emotional Reasoning: ${data.bias_agent.emotional_reasoning_score}</p>
        <div class="w-full bg-gray-800 h-3 rounded mt-2">
  <div style="
    width:${data.bias_agent.emotional_reasoning_score}%;
    background: linear-gradient(90deg,#813FF1,#ff4da6);
    height:12px;
    border-radius:6px;
    transition:all 0.8s;">
  </div>
</div>
        <p>Cognitive Risk Index: ${data.bias_agent.cognitive_risk_index}</p>
        <p>Meta Cognition: ${data.bias_agent.meta_cognition_score}</p>
      </div>

      <!-- EXAM MODE -->
      <div>
        <h4 class="text-green-400 font-bold">Exam Simulation</h4>
        <p>Readiness Score: ${data.exam_mode.exam_readiness_score.toFixed(2)}</p>
        <p>Performance Band: ${data.exam_mode.performance_band}</p>
      </div>

      <details>
  <summary class="cursor-pointer text-yellow-400 font-bold">
    AI Mentor Insights
  </summary>
  <div class="mt-3">
    <p><strong>Strengths:</strong></p>
    <ul class="list-disc ml-6">
      ${data.mentor_mode.strengths.map(s => `<li>${s}</li>`).join("")}
    </ul>
    <p class="mt-3"><strong>Improvements:</strong></p>
    <ul class="list-disc ml-6">
      ${data.mentor_mode.improvement_areas.map(s => `<li>${s}</li>`).join("")}
    </ul>
  </div>
</details>

    </div>
  `;
  renderDriftGraph(data.ensemble.drift_score);
}

// =====================
// HELPERS
// =====================

function progressBar(label, value) {
  return `
    <div>
      <p class="text-[#813FF1] font-semibold">${label}: ${value}</p>
      <div class="w-full bg-gray-800 rounded-full h-3">
        <div class="bg-gradient-to-r from-[#813FF1] to-[#5f9cff]
                    h-3 rounded-full transition-all duration-700"
             style="width:${value}%"></div>
      </div>
    </div>
  `;
}

// =====================
// DISAGREEMENT HEAT BAR
// =====================

function renderDisagreementHeat(value) {

  const live = document.getElementById("livePreview");

  let color =
    value > 40 ? "red" :
    value > 20 ? "orange" :
    "lime";

  live.innerHTML += `
    <div class="mt-2 w-full bg-gray-800 h-2 rounded">
      <div style="
        width:${value}%;
        background:${color};
        height:8px;
        border-radius:6px;
        transition:all 0.6s;">
      </div>
    </div>
  `;
}

// =====================
// COMPARE LOADING UI
// =====================

function showCompareLoader() {

  const container = document.getElementById("agentComparison");

  container.innerHTML = `
    <div class="glass p-6 rounded-xl">
      <h3 class="text-xl text-[#813FF1] mb-4">
        Running Multi-Agent Cognitive Simulation...
      </h3>

      <div class="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
        <div id="compareProgressBar"
             class="h-4 bg-gradient-to-r from-[#813FF1] to-[#5f9cff]"
             style="width:0%; transition: width 0.3s ease;">
        </div>
      </div>

      <p class="mt-4 text-sm text-gray-400">
        Logical Agent • Creative Agent • Bias Agent • Mentor Engine
      </p>
    </div>
  `;

  animateCompareProgress();
}

function animateCompareProgress() {

  let width = 0;
  const bar = document.getElementById("compareProgressBar");

  const interval = setInterval(() => {
    if (!bar) {
      clearInterval(interval);
      return;
    }

    width += Math.random() * 12;

    if (width >= 90) {
      width = 90; // stop at 90 until real response comes
      clearInterval(interval);
    }

    bar.style.width = width + "%";
  }, 200);
}

// =====================
// PERFORMANCE TRACKING
// =====================

function savePerformance(score) {
  let history = JSON.parse(localStorage.getItem("cognitiveHistory") || "[]");
  history.push(score);
  localStorage.setItem("cognitiveHistory", JSON.stringify(history));
}

function getRiskColor(value) {
  if (value > 60) return "red";
  if (value > 30) return "orange";
  return "lime";
}

function classifyProfile(data) {

  if (data.cognitive_stability_index > 80)
    return "Structured Strategic Thinker";

  if (data.cognitive_risk_index > 60)
    return "Impulsive Overconfident Solver";

  if (data.error_sensitivity > 50)
    return "High Error-Aware Analyst";

  if (data.analytical_depth > 75)
    return "Deep Logical Processor";

  return "Developing Cognitive Structure";
}

function typeText(id, text) {
  let i = 0;
  const el = document.getElementById(id);
  el.innerHTML = "";

  function typing() {
    if (i < text.length) {
      el.innerHTML += text.charAt(i);
      i++;
      setTimeout(typing, 10);
    }
  }
  typing();
}