# Relay: from watching to making

An interactive product concept by Chae Kim. Relay bridges a YouTube playlist and a learning notebook with a concrete outcome: a realistic practice plan, source-linked lessons, practical tasks, and a finished project.

This is an independent concept, not affiliated with YouTube, NotebookLM, or Google. It is not a production learning or AI service.

## Run locally

No build, package install, account, API key, or backend required. From the repository root:

```sh
python3 -m http.server 8080
```

Open **http://localhost:8080/demos/relay/index.html**. The case study is at **http://localhost:8080/projects/relay.html**. Use explicit `.html` paths locally; Vercel supports clean portfolio URLs.

Modern evergreen browsers support the native dialog and localStorage APIs used here. Google Fonts is optional; system font fallbacks work without network access. YouTube source links need internet access.

## A two-minute demo

1. Start on Overview. The fictional learner, Jamie, has completed two of five tasks.
2. Import playlist → Use the sample playlist → Create my sample plan. Choose a goal and a weekly time budget. A new sample starts with zero progress.
3. Open a lesson. Watch source on YouTube opens the creator's original video in a new tab. Mark watched, write a note, and open Practice prompts.
4. Complete tasks and switch between All, To do, and Completed. Watching does not complete a task.
5. Open Final project. Enter `https://example.com/my-project` and a reflection of at least 30 characters. Submit to reveal simulated feedback, then download a Markdown summary.
6. Reload to verify saved progress. Reset demo progress restores the original fictional sample.

## What is simulated

- **Playlist import:** validates an HTTPS YouTube `/playlist?list=...` URL, then loads the same curated web-design fixture. It does not fetch metadata, videos, or transcripts. Custom goals personalize the heading; they do not generate a new curriculum. `PL-relay-demo` is an illustrative ID, not a real playlist.
- **Lessons:** original learning prompts reference source videos. Study times are authored estimates, not runtime metadata or verified chapter lengths. Timestamp links are suggested starting points, not transcript citations.
- **Feedback:** transparent deterministic prompts depend on checklist progress and reflection length. No model call, page fetch, code analysis, score, or quality assessment occurs. Rubric weights describe an intended future evaluation, not an assigned grade.
- **Submission:** saves a URL and reflection locally, without uploading anything. No sign-in, shared records, analytics, or server storage is added by this demo.
- **Progress:** tasks are self-assessed, not proof of mastery. The six-hour plan budget includes watching, practice, review, and project iteration.

Sources: [HTML Crash Course](https://www.youtube.com/watch?v=UB1O30fR-EE), [CSS Crash Course](https://www.youtube.com/watch?v=yfoY53QXEnI), and Kevin Powell's [Responsive design made easy](https://www.youtube.com/watch?v=bn-DQCifeQQ). All exercises and interface illustrations are authored for this concept; they are not attributed to those creators.

## Data and accessibility

Progress is stored under `relay-demo-v1` in localStorage for the current origin. Reload retains notes, task states, and draft form values. Reset overwrites only this demo key. Blocked storage falls back to memory for the current visit. Do not enter confidential information on a shared device.

The UI uses semantic navigation, named inputs, native dialog focus trapping and Escape dismissal, visible focus states, live status messages, a skip link, and reduced-motion handling. Layout breakpoints adapt the sidebar and columns for tablet and phone widths. A deployed-browser review verified the primary flow, notes after reload, task filters, draft feedback, export, Escape dismissal, all five routes at 375px, and the plan at 768px. Cross-browser and assistive-technology testing remain before production. See [the illustrated walkthrough](walkthrough.html) for captured screens and the review record.

## Checks

From the repository root:

```sh
node --check demos/relay/relay.js
node --test demos/relay/relay.test.cjs
python3 scripts/build-cases.py --check
```

The six dependency-free interaction tests execute the real application script in a Node VM with a minimal document harness. They verify navigation rendering, import validation, progress, notes, persistence, project validation, simulated feedback, export, and reset. They do not replace real-browser layout, native dialog, or keyboard testing.

## Portfolio integration

- `scripts/build-home.py`: Builds card; regenerate with `python3 scripts/build-home.py`.
- `scripts/build-cases.py`: case-study source; regenerate with `python3 scripts/build-cases.py`.
- `scripts/stamp_shared.py`: native portfolio live-preview registration.
- `scripts/build-llms.py`: discovery entry; regenerate with `python3 scripts/build-llms.py`.
- `assets/img/builds/relay-cover.svg`: authored illustrative cover, not a screenshot.
- `projects/relay.html`: generated case study.

Vercel serves this static directory as part of the existing portfolio deployment. No hosting configuration changes are needed. A pull request may receive an automatic preview if the repository's Vercel integration is enabled. Production updates only after merge.

## Next product experiment

Test whether five learners can go from the sample playlist to their first practice action without help. Then compare a source-only playlist with the same playlist plus practice tasks. Use blind project review and a delayed transfer task to measure applied skill. Completion and return-to-practice are supporting metrics, not substitutes for demonstrated learning. No outcome claims have been measured for this prototype.

## Product review materials

- [Screen-by-screen walkthrough](walkthrough.html): seven captured screens, phone and tablet examples, and observed verification results.
- [PRD](prd.html) and [Markdown source](PRD.md): primary audience, launch use case, requirements, scope, acceptance criteria, proposed success measures, and research plan.
- `screenshots/`: actual browser captures from the repaired deployment on October 30, 2026. Fictional demo data only.

The deployed clean URL is `/demos/relay`. Asset links use absolute `/demos/relay/...` paths so redirects do not break CSS or JavaScript. Serve this folder from the repository root, as shown above.
