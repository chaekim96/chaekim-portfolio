"use strict";
const KEY = "relay-demo-v1";
const lessons = [
  {
    title: "Think in boxes, not pages",
    topic: "HTML structure & semantic landmarks",
    duration: 18,
    video: "UB1O30fR-EE",
    creator: "Traversy Media",
    chapter: "HTML Crash Course",
    seconds: 720,
  },
  {
    title: "Make the layout work for you",
    topic: "CSS Grid, Flexbox & visual hierarchy",
    duration: 24,
    video: "yfoY53QXEnI",
    creator: "Traversy Media",
    chapter: "CSS Crash Course",
    seconds: 1680,
  },
  {
    title: "Design for the small screen first",
    topic: "Responsive layouts & breakpoints",
    duration: 21,
    video: "bn-DQCifeQQ",
    creator: "Kevin Powell",
    chapter: "Responsive design made easy",
    seconds: 0,
  },
  {
    title: "Make every interaction count",
    topic: "Forms, focus states & accessibility",
    duration: 19,
    video: "UB1O30fR-EE",
    creator: "Traversy Media",
    chapter: "HTML Crash Course",
    seconds: 2520,
  },
];
const tasks = [
  {
    title: "Sketch the content hierarchy",
    detail: "Write one headline, one call to action, and three benefits.",
    time: "15 min",
    lesson: 0,
  },
  {
    title: "Build your semantic page structure",
    detail: "Use header, main, section, and footer landmarks.",
    time: "25 min",
    lesson: 0,
  },
  {
    title: "Build a responsive hero section",
    detail: "Use Grid or Flexbox. Check your layout at 375px and 1280px.",
    time: "35 min",
    lesson: 1,
  },
  {
    title: "Make the page work on mobile",
    detail: "Stack content, resize typography, and check for overflow.",
    time: "30 min",
    lesson: 2,
  },
  {
    title: "Test keyboard and form interactions",
    detail: "Tab through every control and label each form field.",
    time: "20 min",
    lesson: 3,
  },
];
const fresh = () => ({
  done: [0, 1],
  watched: [0],
  lesson: 1,
  notes: {},
  goal: "Build a responsive landing page",
  hours: 4,
  level: "I'm new to this",
  imported: false,
  url: "",
  projectUrl: "",
  reflection: "",
  submitted: false,
});
let state = fresh(),
  storageAvailable = true,
  filter = "all",
  noteTab = "notes",
  toastTimer;
try {
  const s = JSON.parse(localStorage.getItem(KEY));
  if (s && Array.isArray(s.done) && Array.isArray(s.watched))
    state = {
      ...fresh(),
      ...s,
      done: s.done.filter((n) => Number.isInteger(n) && n >= 0 && n < 5),
      watched: s.watched.filter((n) => Number.isInteger(n) && n >= 0 && n < 4),
      lesson: Number.isInteger(s.lesson) && lessons[s.lesson] ? s.lesson : 1,
      notes: s.notes && typeof s.notes === "object" ? s.notes : {},
      hours: [2, 4, 6].includes(s.hours) ? s.hours : 4,
    };
} catch {
  storageAvailable = false;
}
const $ = (s) => document.querySelector(s);
const esc = (s) =>
  String(s).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
function toast(s) {
  $("#toast").textContent = s;
  $("#toast").classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $("#toast").classList.remove("show"), 3500);
}
function save() {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    storageAvailable = false;
    toast("Storage unavailable. Progress lasts for this visit.");
  }
}
const pct = () => Math.round((state.done.length / 5) * 100);
const btn = (href, label, cls = "") =>
  `<a class="button ${cls}" href="${href}">${label}</a>`;
const intro = (eyebrow, title, subtitle) =>
  `<div class="intro"><div><div class="eyebrow">${eyebrow}</div><h1>${title}</h1><p>${subtitle}</p></div><span class="date">A LITTLE PROGRESS, EVERY DAY.</span></div>`;
const visual = () =>
  `<div class="path-visual" aria-hidden="true"><div class="window"><div class="window-bar"><i></i><i></i><i></i></div><div class="window-grid"><b>Good ideas.<br>Better websites.</b><span></span></div></div><div class="design-label">design.<br>build.<br>repeat. ↗</div></div>`;
function overview() {
  return `${intro("FROM WATCHING TO MAKING", "Your next chapter starts here.", "A little less “watch later.” A little more “look what I made.”")}
<section class="hero"><div class="hero-copy"><span class="tag">WATCH IT. TRY IT. MAKE IT YOURS.</span><h2>You have the playlist.<br>Now build the skill.</h2><p>Turn the videos you love into a plan you can follow, one small project at a time.</p><button class="button primary" data-import>Turn a playlist into a plan ↗</button></div><div class="hero-art" aria-hidden="true"><div class="art-card"><div class="art-top"><span>YOUR NEXT CHAPTER</span><span>↗</span></div><h3>Ideas become<br>things you can do.</h3><div class="art-lines"><span class="check">✓</span> Find something worth learning</div><div class="art-lines"><span class="check">✓</span> Put it into practice</div><div class="art-lines"><span class="check">↗</span> Make something of your own</div></div><div class="floating"><span>✦</span> Small steps. Real skills.</div></div></section>
<div class="stats"><div class="stat"><strong>01</strong><span>learning path<br>in motion</span></div><div class="stat"><strong>${state.done.length}<small style="font-size:14px;color:#909486"> / 5</small></strong><span>practical tasks<br>completed</span></div><div class="stat"><strong>${pct()}%</strong><span>of your project<br>practice complete</span></div></div>
<div class="section-head"><h2>Keep the momentum.</h2><a href="#plan">View learning plan ↗</a></div><div class="columns"><article class="card path-card">${visual()}<div class="path-info"><span class="eyebrow">YOUR ACTIVE LEARNING PATH</span><h3 style="margin-top:9px">${esc(state.goal)}</h3><p>4 curated lessons · ${Math.ceil(6 / state.hours)} weeks · Beginner friendly</p><div class="progress-label"><span>${state.done.length} of 5 practice tasks complete</span><strong>${pct()}%</strong></div><div class="progress"><div style="width:${pct()}%"></div></div><div class="path-bottom"><div class="avatars"><b>TM</b><b>KP</b>Learn from 2 creators</div>${btn("#workspace", "Continue learning →", "small")}</div></div></article><article class="card next-card"><span class="eyebrow">UP NEXT · PUT IT INTO PRACTICE</span><h3>${esc(tasks.find((_, i) => !state.done.includes(i))?.title || "Your project is ready for its next chapter.")}</h3><p>Close the gap between understanding a lesson and using it. Your next task is a small piece of your final project.</p><div class="source"><b>▷</b> Based on your web-design learning path</div><div class="time">◷ 25–35 minutes of focused making</div>${btn(state.done.length === 5 ? "#project" : "#tasks", state.done.length === 5 ? "Submit your project ↗" : "Open my tasks ↗", "ghost")}</article></div>`;
}
function plan() {
  const weeks = Math.ceil(6 / state.hours);
  return `${intro("YOUR LEARNING PLAN", "A playlist. With a finish line.", "Every lesson moves you toward a responsive landing page you can show.")}<div class="banner"><strong>Your goal:</strong> ${esc(state.goal)}<br>${state.hours} hours per week · ${weeks} weeks · ${esc(state.level)}${state.imported ? "<br>Sample plan loaded. Custom playlist content has not been fetched." : ""}</div><div class="plan-layout"><div>${[
    0, 1,
  ]
    .map(
      (w) =>
        `<section class="card week"><div class="week-heading"><span class="week-num">0${w + 1}</span><div><h3>${w === 0 ? "Start with structure" : "Make it work everywhere"}</h3><p>Phase ${w + 1} of 2 · ${w === 0 ? "Watch 42 min · Practice 75 min" : "Watch 40 min · Practice 50 min"}</p></div></div>${lessons
          .slice(w * 2, w * 2 + 2)
          .map((l, j) => {
            const i = w * 2 + j;
            return `<div class="lesson"><span class="lesson-number">${state.watched.includes(i) ? "✓" : i + 1}</span><div class="lesson-text"><h4>${l.title}</h4><small>${l.duration} min suggested study · ${l.creator}</small></div><button class="button small" data-lesson="${i}">${state.watched.includes(i) ? "Revisit" : "Open"} →</button></div>`;
          })
          .join("")}</section>`,
    )
    .join(
      "",
    )}<p class="notice">Curated demo: lessons and exercises are original learning prompts. Source links point to creator videos. No transcripts or AI summaries were retrieved. Six hours includes practice, review, and project work; the schedule is an estimate.</p></div><aside class="card project-mini"><span class="eyebrow">THE THING YOU'LL MAKE</span><h3>One page.<br>Entirely yours.</h3><p>A responsive landing page for an idea you care about. You pick the product. We help you get it across the finish line.</p><ul><li>Clear headline & call to action</li><li>Responsive content layout</li><li>Accessible interaction states</li><li>A shareable project link</li></ul>${btn("#project", "See the project brief ↗", "primary")}</aside></div>`;
}
function workspace() {
  const l = lessons[state.lesson];
  return `${intro("LESSON " + (state.lesson + 1) + " OF 4", "Watch with a purpose.", l.topic)}<div class="workspace"><div><div class="video"><span class="eyebrow">CURATED SOURCE · ${l.creator.toUpperCase()}</span><h2>${l.title}</h2><a class="button" target="_blank" rel="noopener noreferrer" href="https://www.youtube.com/watch?v=${l.video}&t=${l.seconds}s">▷ Watch source on YouTube ↗</a><small>Opens the original creator video · ${l.duration} min suggested study</small></div><div class="video-caption"><div><h3>${l.chapter}</h3><div class="source"><b>▷</b> ${l.creator} · Source-linked learning</div></div><button class="button small" id="watched">${state.watched.includes(state.lesson) ? "✓ Watched · mark unwatched" : "Mark as watched"}</button></div><div class="card"><div class="tabs" aria-label="Learning resources">${[
    ["notes", "My notes"],
    ["takeaways", "Practice prompts"],
    ["chapters", "All lessons"],
  ]
    .map(
      ([id, label]) =>
        `<button data-note-tab="${id}" aria-pressed="${noteTab === id}">${label}</button>`,
    )
    .join(
      "",
    )}</div>${noteTab === "notes" ? `<label for="notes">What do you want to remember?<textarea id="notes" placeholder="Try: Use a two-column grid on desktop, then stack the hero on mobile…">${esc(state.notes[state.lesson] || "")}</textarea></label><button id="save-notes" class="button small">Save note</button><span class="source" style="display:inline;margin-left:12px">Saved in this browser</span>` : noteTab === "takeaways" ? `<div class="note"><strong>Try it without the tutorial.</strong><br>Explain ${esc(l.topic.toLowerCase())} in your own words. Then use it in your project.</div><div class="note">What changes at 375px? Which element should the visitor notice first? Can someone reach your call to action using a keyboard?</div><p class="notice">Authored demo prompts, not a transcript or AI summary.</p>` : lessons.map((x, i) => `<div class="lesson"><div class="lesson-text"><h4>${i + 1}. ${x.title}</h4><small>${x.creator}</small></div><button class="button small" data-lesson="${i}">Open →</button></div>`).join("")}</div></div><aside class="card workspace-side"><div><span class="eyebrow">NOW, MAKE IT STICK</span><h3>${tasks.find((t) => t.lesson === state.lesson).title}</h3><p>Use this lesson in your own landing page. Aim for a working first version.</p><div class="criteria"><strong>Your definition of done</strong>✓ A clear visual hierarchy<br>✓ A layout that adapts to mobile<br>✓ A decision you can explain</div></div><div><div class="notice">Learning happens when you try. Watching and completing tasks are tracked separately.</div>${btn("#tasks", "Go to practice tasks →", "primary")}<p><a href="#plan">← Back to the full plan</a></p></div></aside></div>`;
}
function taskView() {
  const list = tasks
    .map((t, i) => ({ ...t, i }))
    .filter(
      (t) =>
        filter === "all" ||
        (filter === "done"
          ? state.done.includes(t.i)
          : !state.done.includes(t.i)),
    );
  return `${intro("SMALL STEPS. REAL SKILLS.", "Make the learning yours.", "Five practical tasks. One project that gets better with every lesson.")}<div class="stats"><div class="stat"><strong>${state.done.length}</strong><span>completed</span></div><div class="stat"><strong>${5 - state.done.length}</strong><span>ready to try</span></div><div class="stat"><strong>${pct()}%</strong><span>practice complete</span></div></div><div class="filter-row" aria-label="Filter tasks">${["all", "open", "done"].map((f) => `<button class="button small" data-filter="${f}" aria-pressed="${filter === f}">${f === "all" ? "All tasks" : f === "open" ? "To do" : "Completed"}</button>`).join("")}</div><section class="card">${list.length ? list.map((t) => `<div class="task-row ${state.done.includes(t.i) ? "done" : ""}"><input type="checkbox" id="task-${t.i}" data-task="${t.i}" ${state.done.includes(t.i) ? "checked" : ""}><label for="task-${t.i}"><span>${t.title}</span><small>${t.detail}</small></label><a class="pill" href="#workspace" data-task-source="${t.lesson}" aria-label="Open lesson ${t.lesson + 1}">${t.time} ↗</a></div>`).join("") : '<div class="empty">Nothing here yet. Every small step counts.</div>'}</section><div class="section-head"><p class="source">Checking a task records your self-assessment.</p>${btn("#project", "Ready to share your project? ↗", "primary")}</div>`;
}
function feedback() {
  return state.submitted
    ? `<div class="feedback-heading"><span class="eyebrow">YOUR NEXT ITERATION</span><span class="check">✓</span></div><h3 style="margin-top:20px">Draft saved. Keep making.</h3><p>Your project and reflection are saved in this browser. They have not been uploaded or reviewed.</p><p class="notice">SIMULATED FEEDBACK · Rule-based prompts use checklist progress and reflection length. Relay has not visited your URL or assessed its quality.</p><div class="feedback-item"><strong>01 · ${state.done.includes(2) ? "Put your hero to the test" : "Start with the hero"}</strong><p>${state.done.includes(2) ? "Ask a friend to look at your page for five seconds. Can they say what it offers and what to do next?" : "Finish the hero task. Write one headline and one primary action before refining the visual style."}</p></div><div class="feedback-item"><strong>02 · Check the edges</strong><p>${state.done.includes(3) ? "Recheck at 375px, 768px, and 1280px. Try a longer headline to catch fragile layouts." : "Complete the mobile task, then check for horizontal scrolling and cramped controls at 375px."}</p></div><div class="feedback-item"><strong>03 · Explain the tradeoff</strong><p>${state.reflection.trim().length < 120 ? "Expand your reflection: name one design decision, an alternative you considered, and how you tested the result." : "Turn your reflection into evidence: add a before/after screenshot and explain what your next test would measure."}</p></div><button class="button small" id="export" style="margin-top:20px">Download project summary ↓</button>`
    : `<span class="eyebrow">FEEDBACK THAT MOVES YOU FORWARD</span><h3 style="margin-top:20px">A draft is a great place to start.</h3><p>Share a project link and a short reflection to reveal an example of how actionable feedback could work.</p><div class="note"><strong>Specific over generic.</strong><br>“Test your hero at 375px” is a next step. “Looks good” isn't.</div><div class="note"><strong>Progress over perfection.</strong><br>Submit early, make one change, and try again.</div><p class="notice">This prototype uses a local checklist. A production version would need source-grounded evaluation, user consent, and clear limits on feedback confidence.</p>`;
}
function project() {
  return `${intro("THE FINISH LINE IS A STARTING POINT.", "Make something worth sharing.", "A small, finished project says more than another completed playlist.")}<div class="project-layout"><section class="card"><span class="eyebrow">YOUR FINAL PROJECT</span><h3 style="margin-top:14px">Launch a landing page.</h3><p>Choose a product, a cause, or a side project. Build one responsive page that explains its value and invites a visitor to act.</p>${[
    ["Clarity & content hierarchy", 30],
    ["Responsive layout", 30],
    ["Accessibility & interaction", 25],
    ["Reflection on design choices", 15],
  ]
    .map(
      ([s, n]) =>
        `<div class="rubric"><span>${s}</span><strong>${n}%</strong></div>`,
    )
    .join(
      "",
    )}<div class="notice">${state.done.length}/5 practice tasks complete. Submit a draft at any point. Feedback is an illustrative checklist, not an evaluation of your website.</div><form id="project-form"><label for="project-url">Project URL<input id="project-url" type="url" placeholder="https://your-project.example" value="${esc(state.projectUrl)}" required></label><label for="reflection">What did you build, and what would you improve?<textarea id="reflection" minlength="30" maxlength="3000" placeholder="Describe your layout choices, what you tested, and one thing you want feedback on…" required>${esc(state.reflection)}</textarea></label><p id="project-error" class="error" role="alert"></p><button class="button primary" type="submit">${state.submitted ? "Update draft & feedback" : "Submit draft & see sample feedback"} ↗</button></form></section><aside class="card" id="feedback">${feedback()}</aside></div>`;
}
function render() {
  const route = location.hash.slice(1) || "overview",
    views = { overview, plan, workspace, tasks: taskView, project },
    active = views[route] ? route : "overview";
  $("#main").innerHTML = views[active]();
  $("#breadcrumb").textContent = {
    overview: "Overview",
    plan: "Learning plan",
    workspace: "Video workspace",
    tasks: "My tasks",
    project: "Final project",
  }[active];
  document.querySelectorAll("[data-nav]").forEach((a) => {
    a.classList.toggle("active", a.dataset.nav === active);
    if (a.dataset.nav === active) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  $("#task-count").textContent = 5 - state.done.length;
  const form = $("#project-form");
  if (form) form.onsubmit = submitProject;
}
function validHttp(s) {
  try {
    const u = new URL(s);
    return (
      ["http:", "https:"].includes(u.protocol) && !u.username && !u.password
    );
  } catch {
    return false;
  }
}
function submitProject(e) {
  e.preventDefault();
  const url = $("#project-url").value.trim(),
    reflection = $("#reflection").value.trim();
  if (!validHttp(url) || reflection.length < 30) {
    $("#project-error").textContent =
      "Use an http(s) project URL and at least 30 characters of reflection.";
    return;
  }
  Object.assign(state, { projectUrl: url, reflection, submitted: true });
  save();
  render();
  $("#feedback").scrollIntoView({
    behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
      ? "instant"
      : "smooth",
    block: "nearest",
  });
  toast("Draft saved locally. Sample feedback is ready.");
}
document.addEventListener("click", (e) => {
  const el = e.target.closest("button,a");
  if (!el) return;
  if (el.hasAttribute("data-import")) {
    $("#import-error").textContent = "";
    $("#import-dialog").showModal();
  }
  if (el.dataset.lesson !== undefined) {
    state.lesson = Number(el.dataset.lesson);
    save();
    if (location.hash === "#workspace") render();
    else location.hash = "workspace";
  }
  if (el.dataset.taskSource !== undefined) {
    state.lesson = Number(el.dataset.taskSource);
    save();
    if (location.hash === "#workspace") render();
  }
  if (el.dataset.filter) {
    filter = el.dataset.filter;
    render();
    $(`[data-filter="${filter}"]`).focus();
  }
  if (el.dataset.noteTab) {
    noteTab = el.dataset.noteTab;
    render();
    $(`[data-note-tab="${noteTab}"]`).focus();
  }
  if (el.id === "watched") {
    const i = state.lesson;
    state.watched = state.watched.includes(i)
      ? state.watched.filter((n) => n !== i)
      : [...state.watched, i];
    save();
    render();
  }
  if (el.id === "save-notes") {
    state.notes[state.lesson] = $("#notes").value;
    save();
    toast("Note saved. Your next idea is waiting.");
  }
  if (el.id === "export") exportSummary();
});
document.addEventListener("change", (e) => {
  if (e.target.dataset.task !== undefined) {
    const i = Number(e.target.dataset.task);
    state.done = e.target.checked
      ? [...new Set([...state.done, i])]
      : state.done.filter((n) => n !== i);
    save();
    render();
    const next = $("#task-" + i);
    if (next) next.focus();
    toast("Progress updated. One step at a time.");
  }
});
document.addEventListener("input", (e) => {
  if (e.target.id === "notes") state.notes[state.lesson] = e.target.value;
  else if (e.target.id === "project-url") state.projectUrl = e.target.value;
  else if (e.target.id === "reflection") state.reflection = e.target.value;
  else return;
  save();
});
$("#close-import").onclick = () => $("#import-dialog").close();
$("#sample").onclick = () => {
  $("#import-error").textContent = "";
  $("#playlist-url").value =
    "https://www.youtube.com/playlist?list=PL-relay-demo";
  $("#learning-goal").value = "Build a responsive landing page";
  $("#playlist-url").focus();
};
$("#import-form").onsubmit = (e) => {
  e.preventDefault();
  let u;
  try {
    u = new URL($("#playlist-url").value.trim());
  } catch {}
  if (
    !u ||
    !["youtube.com", "www.youtube.com", "m.youtube.com"].includes(u.hostname) ||
    u.protocol !== "https:" ||
    u.pathname !== "/playlist" ||
    !u.searchParams.get("list")
  ) {
    $("#import-error").textContent =
      "Use an HTTPS YouTube playlist URL with a list parameter, or load the sample.";
    return;
  }
  const goal = $("#learning-goal").value.trim();
  if (!goal) {
    $("#import-error").textContent = "Add a learning goal.";
    return;
  }
  state = {
    ...fresh(),
    done: [],
    watched: [],
    lesson: 0,
    goal,
    hours: Number($("#hours").value),
    level: $("#level").value,
    url: u.href,
    imported: true,
  };
  save();
  $("#import-dialog").close();
  if (location.hash === "#plan") render();
  else location.hash = "plan";
  toast("Your curated sample plan is ready.");
};
$("#reset").onclick = () => {
  state = fresh();
  filter = "all";
  save();
  render();
  toast("Demo reset to the original sample.");
};
function exportSummary() {
  const text = `# Relay project summary\n\nGoal: ${state.goal}\nProject: ${state.projectUrl}\n\n## Reflection\n${state.reflection}\n\n## Practice checklist\n${tasks.map((t, i) => `- [${state.done.includes(i) ? "x" : " "}] ${t.title}`).join("\n")}\n\nFeedback is simulated; no website or project was evaluated.\n`;
  const url = URL.createObjectURL(new Blob([text], { type: "text/markdown" })),
    a = document.createElement("a");
  a.href = url;
  a.download = "relay-project-summary.md";
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
window.addEventListener("hashchange", () => {
  render();
  $("#main").focus({ preventScroll: true });
  window.scrollTo(0, 0);
});
render();
if (!storageAvailable) toast("Storage unavailable. This visit still works.");
