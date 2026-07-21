const STORAGE_KEY = "story-review-decisions-v1";
const state = { data: null, activePanelId: null, decisions: loadDecisions() };

function loadDecisions() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; } catch { return {}; }
}
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, (character) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "'":"&#39;", '"':"&quot;" })[character]);
}
function saveDecisions() { localStorage.setItem(STORAGE_KEY, JSON.stringify(state.decisions)); }
function decisionFor(panelId) { return state.decisions[panelId] || { decision: "pending", comment: "" }; }

function renderMetrics() {
  const evaluation = state.data.evaluation;
  const approved = Object.values(state.decisions).filter((item) => item.decision === "approved").length;
  const metrics = [
    ["Foundation score", evaluation.quality_score, "Before human approvals"],
    ["Source validity", `${Math.round(evaluation.source_validity_rate * 100)}%`, "Exact source offsets"],
    ["Source coverage", `${Math.round(evaluation.source_coverage_rate * 100)}%`, "Story text represented"],
    ["Blocking findings", evaluation.blocking_findings, "Must resolve"],
    ["Approved locally", approved, `of ${state.data.panels.length} panels`],
  ];
  document.querySelector("#metrics").innerHTML = metrics.map(([label,value,note]) => `<article class="metric"><span>${label}</span><strong>${value}</strong><small>${note}</small></article>`).join("");
}

function renderList() {
  const reviewed = Object.values(state.decisions).filter((item) => item.decision !== "pending").length;
  document.querySelector("#progress").textContent = `${reviewed} / ${state.data.panels.length}`;
  document.querySelector("#panel-list").innerHTML = state.data.panels.map((panel) => {
    const decision = decisionFor(panel.panelId).decision;
    return `<button class="panel-link ${panel.panelId === state.activePanelId ? "active" : ""}" data-panel="${panel.panelId}"><span class="number">${panel.order}</span><span><strong>${escapeHtml(panel.sceneId)}</strong><small>${escapeHtml(panel.shot.replaceAll("_", " "))}</small></span><i class="status-dot ${decision === "request_changes" ? "changes" : decision}"></i></button>`;
  }).join("");
}

function renderDetail() {
  const panel = state.data.panels.find((item) => item.panelId === state.activePanelId);
  const review = decisionFor(panel.panelId);
  document.querySelector("#panel-detail").innerHTML = `
    <p class="eyebrow">PANEL ${panel.order} · ${escapeHtml(panel.panelId)}</p>
    <h2>${escapeHtml(panel.storyPurpose)}</h2>
    <div class="detail-grid">
      <section class="source-card"><h3>Source evidence</h3><small>Offsets ${panel.sourceOffsets[0]}–${panel.sourceOffsets[1]}</small><blockquote>${escapeHtml(panel.sourceExcerpt)}</blockquote></section>
      <section class="direction-card"><h3>Production direction</h3><div class="meta-list"><div><span>Scene</span><strong>${escapeHtml(panel.sceneId)}</strong></div><div><span>Characters</span><strong>${escapeHtml(panel.characterIds.join(", ") || "None")}</strong></div><div><span>Location</span><strong>${escapeHtml(panel.locationId || "None")}</strong></div><div><span>Camera</span><strong>${escapeHtml(panel.shot)} / ${escapeHtml(panel.cameraAngle)}</strong></div></div><h3>Continuity constraints</h3><ul class="constraints">${panel.continuityConstraints.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>
    </div>
    <section class="decision-box"><h3>Human decision</h3><div class="decision-actions"><button class="approve" data-decision="approved">Approve</button><button class="changes" data-decision="request_changes">Request changes</button><button class="reject" data-decision="rejected">Reject</button></div><textarea id="review-comment" placeholder="Explain the decision or required correction…">${escapeHtml(review.comment)}</textarea></section>`;
}

function render() { renderMetrics(); renderList(); renderDetail(); }

document.querySelector("#panel-list").addEventListener("click", (event) => {
  const button = event.target.closest("[data-panel]");
  if (!button) return;
  state.activePanelId = button.dataset.panel;
  render();
});
document.querySelector("#panel-detail").addEventListener("click", (event) => {
  const decision = event.target.dataset.decision;
  if (!decision) return;
  state.decisions[state.activePanelId] = { decision, comment: document.querySelector("#review-comment").value.trim(), reviewedAt: new Date().toISOString() };
  saveDecisions(); render();
});
document.querySelector("#reset").addEventListener("click", () => { state.decisions = {}; saveDecisions(); render(); });
document.querySelector("#export").addEventListener("click", () => {
  const payload = { schemaVersion:"1.0", projectId:state.data.project.id, exportedAt:new Date().toISOString(), decisions:state.decisions };
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:"application/json"}));
  const link = Object.assign(document.createElement("a"),{href:url,download:"story-review-decisions.json"}); link.click(); URL.revokeObjectURL(url);
});

state.data = await fetch("data.json").then((response) => response.json());
state.activePanelId = state.data.panels[0].panelId;
document.querySelector("#project-label").textContent = `${state.data.project.title} · ${state.data.project.author}`;
render();
