const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(__dirname + "/relay.js", "utf8");
function harness(saved, blocked = false) {
  const elements = new Map(),
    listeners = {},
    windowListeners = {},
    store = new Map(saved ? [["relay-demo-v1", saved]] : []),
    downloads = [];
  function element(id) {
    if (!elements.has(id))
      elements.set(id, {
        value: "",
        textContent: "",
        innerHTML: "",
        dataset: {},
        classList: { add() {}, remove() {}, toggle() {} },
        focus() {},
        scrollIntoView() {},
        showModal() {
          this.open = true;
        },
        close() {
          this.open = false;
        },
      });
    return elements.get(id);
  }
  const nav = ["overview", "plan", "workspace", "tasks", "project"].map(
    (id) => ({
      dataset: { nav: id },
      classList: { toggle() {} },
      setAttribute() {},
      removeAttribute() {},
    }),
  );
  const location = { hash: "" };
  const document = {
    querySelector: element,
    querySelectorAll: () => nav,
    addEventListener: (t, f) => (listeners[t] = f),
    createElement: () => ({
      click() {
        downloads.push(this.download);
      },
    }),
  };
  const context = vm.createContext({
    document,
    location,
    localStorage: {
      getItem: (k) => {
        if (blocked) throw Error("blocked");
        return store.get(k) || null;
      },
      setItem: (k, v) => {
        if (blocked) throw Error("blocked");
        store.set(k, v);
      },
    },
    window: {
      addEventListener: (t, f) => (windowListeners[t] = f),
      scrollTo() {},
    },
    URL,
    Blob,
    matchMedia: () => ({ matches: true }),
    setTimeout: () => 0,
    clearTimeout() {},
  });
  vm.runInContext(source, context);
  return {
    element,
    store,
    downloads,
    run: (code) => vm.runInContext(code, context),
    route: (r) => {
      location.hash = "#" + r;
      windowListeners.hashchange();
    },
    click: (data) => {
      const el = {
        ...data,
        dataset: data.dataset || {},
        hasAttribute: (k) => !!data[k],
      };
      listeners.click({ target: { closest: () => el } });
    },
    input: (id, value) => {
      const el = element("#" + id);
      el.id = id;
      el.value = value;
      listeners.input({ target: el });
    },
    check: (i, checked) =>
      listeners.change({ target: { dataset: { task: String(i) }, checked } }),
    html: () => element("#main").innerHTML,
  };
}
test("five routes, fallback, and independently tracked watching", () => {
  const h = harness();
  assert.match(h.html(), /Your next chapter/);
  for (const route of ["plan", "workspace", "tasks", "project"]) {
    h.route(route);
    assert.ok(h.html().length > 1000);
  }
  h.route("unknown");
  assert.match(h.html(), /Your next chapter/);
  h.route("workspace");
  h.click({ id: "watched" });
  assert.equal(h.run("state.watched.includes(1)"), true);
  assert.equal(h.run("state.done.length"), 2);
});
test("strict playlist validation, custom goal escaping, and schedule", () => {
  const h = harness();
  h.element("#playlist-url").value =
    "https://youtube.com.evil.test/playlist?list=abc";
  h.element("#learning-goal").value = "Build <script>oops</script>";
  h.element("#hours").value = "2";
  h.element("#level").value = "I'm new to this";
  h.element("#import-form").onsubmit({ preventDefault() {} });
  assert.match(h.element("#import-error").textContent, /HTTPS YouTube/);
  assert.equal(h.run("state.imported"), false);
  h.element("#playlist-url").value =
    "https://www.youtube.com/playlist?list=demo";
  h.element("#import-form").onsubmit({ preventDefault() {} });
  h.route("plan");
  assert.equal(h.run("state.done.length"), 0);
  assert.match(h.html(), /3 weeks/);
  assert.match(h.html(), /&lt;script&gt;/);
  assert.doesNotMatch(h.html(), /<script>oops/);
  assert.match(h.html(), /Custom playlist content has not been fetched/);
});
test("tasks, filters, notes, and persisted reload", () => {
  const h = harness();
  h.route("tasks");
  h.check(2, true);
  assert.equal(h.run("state.done.length"), 3);
  h.check(2, false);
  assert.equal(h.run("state.done.length"), 2);
  h.click({ dataset: { filter: "done" } });
  assert.doesNotMatch(h.html(), /id="task-2"/);
  h.route("workspace");
  h.input("notes", "<b>Use a flexible grid</b>");
  const reloaded = harness(h.store.get("relay-demo-v1"));
  reloaded.route("workspace");
  assert.match(reloaded.html(), /&lt;b&gt;Use a flexible grid/);
});
test("submission validation, transparent feedback, export, and reset", () => {
  const h = harness();
  h.route("project");
  h.element("#project-url").value = "javascript:alert(1)";
  h.element("#reflection").value =
    "This reflection is long enough for validation.";
  h.element("#project-form").onsubmit({ preventDefault() {} });
  assert.equal(h.run("state.submitted"), false);
  assert.match(h.element("#project-error").textContent, /http/);
  h.element("#project-url").value = "https://example.com/project";
  h.element("#project-form").onsubmit({ preventDefault() {} });
  assert.equal(h.run("state.submitted"), true);
  assert.match(h.html(), /SIMULATED FEEDBACK/);
  assert.match(h.html(), /has not visited your URL/);
  h.click({ id: "export" });
  assert.deepEqual(h.downloads, ["relay-project-summary.md"]);
  h.element("#reset").onclick();
  assert.equal(h.run("state.submitted"), false);
  assert.equal(h.run("state.done.length"), 2);
});
test("malformed storage and denied storage preserve a usable demo", () => {
  assert.match(harness("{bad").html(), /Your next chapter/);
  const h = harness(null, true);
  h.route("tasks");
  h.check(2, true);
  assert.equal(h.run("state.done.length"), 3);
  assert.match(h.element("#toast").textContent, /Progress updated/);
});

// Vercel cleanUrls removes /index.html and the trailing slash. Asset URLs must
// still resolve inside the demo directory at the canonical deployed URL.
test("assets resolve after Vercel clean URL redirects", () => {
  const html = fs.readFileSync(__dirname + "/index.html", "utf8");
  const base = "https://portfolio.example/demos/relay";
  for (const asset of ["relay.css", "relay.js"]) {
    const match = html.match(new RegExp('(?:href|src)="([^"]*' + asset.replace(".", "\\.") + ')"'));
    assert.ok(match, asset + " is referenced");
    assert.equal(new URL(match[1], base).pathname, "/demos/relay/" + asset);
  }
});
