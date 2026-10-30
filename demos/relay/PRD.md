# Relay: turn a YouTube playlist into a skill you can show

**Status:** Discovery hypothesis and interactive concept, not a validated business or production service  
**Owner:** Chae Kim  
**Updated:** October 30, 2026  
**Initial use case:** Build and iterate on a responsive landing page  
**Promise:** “Bring a tutorial playlist. Leave with something you made.”

## 1. Who this is for

**Primary audience:** Early-career professionals and career switchers who already use YouTube coding or design tutorials, have a specific project they want to make, and can reserve 2–6 hours per week. They understand basic computer workflows but struggle to turn guided examples into independent work. Recruit by behavior and intent, not age or job title.

**Launch segment:** A beginner who has saved a web-design tutorial and wants to publish a first landing page for a portfolio, side project, or small business within one to three weeks. A finite, inspectable output makes tasks, feedback, and learning outcomes easier to evaluate than a general “learn anything” promise.

**Illustrative persona, not an interviewed user:** Jamie is a marketing associate exploring product roles. Jamie can follow an HTML/CSS tutorial but loses momentum when the example differs from the project they want to build. Jamie has four hours each week and wants a page they can explain in a portfolio review. The need is a clear next action and feedback, rather than a larger content library.

| Segment | Need | Priority |
| --- | --- | --- |
| Career switcher or early-career builder with a saved tutorial and a concrete artifact | Translate explanation into a small plan and finish something independently | Primary |
| Working professional learning a bounded skill for an immediate task | Fit practice around a weekly time budget | Adjacent, validate after launch |
| Creator helping an audience apply a tutorial | Attach exercises and a project brief to existing material | Later distribution partner |
| Passive viewer, exam crammer, or advanced learner seeking deep technical review | Entertainment, recall, or expert evaluation rather than beginner project practice | Outside the initial segment |

**Qualifying signal:** “I saved a tutorial, tried to make my own version, and got stuck or abandoned it.” A saved playlist alone does not establish demand.

## 2. Problem and evidence

A playlist records learning intent but does not specify the learner’s output, practice sequence, or evidence of progress. A motivated beginner must coordinate video, notes, task planning, and a separate project. The cost is abandoned attempts, repeated tutorial watching, and uncertainty about what to do next.

The supplied concept discussion identifies the opportunity to bridge YouTube and a notebook with action. That is the starting hypothesis. There are no discovery interviews, behavioral analytics, willingness-to-pay data, or measured learning outcomes yet. The fictional prototype and authored exercises demonstrate an experience, not demand or efficacy. We have not established which existing product best solves this need.

**Job to be done:** When I have found a useful tutorial and need to build my own version, help me choose a realistic next exercise, apply the lesson, and improve a finished project so I can demonstrate and explain the skill without the tutorial beside me.

**Discovery before investment:** Interview 8–10 qualifying learners. Ask them to show their most recent abandoned tutorial and actual notes/project files; trace where they stopped. Test whether task selection, time, missing prerequisites, confidence, or feedback is the main barrier. Include learners who already finish tutorials to understand when Relay adds little value.

## 3. Goals and non-goals

**User outcomes:** Start a relevant practice task quickly; complete a bounded project; explain one independent design decision; apply the concept again on a different task.

**Product outcome:** Establish a repeatable “lesson → practice → evidence → revision” loop. Returning to practice is more valuable than accumulating watch time.

**Business hypothesis:** Learners may pay for structured guidance and useful project feedback around freely available content. Validate willingness to pay after demonstrating value; no price or revenue forecast is justified yet. Start as a standalone companion linked from a portfolio or creator exercise. YouTube Premium bundling is a later strategic possibility, not a dependency.

**Non-goals for v1:**

- A general-purpose tutor or universal curriculum generator. Support one validated learning domain first.
- Replacing YouTube search, video hosting, or creator ownership. Preserve attribution and links to originals.
- A full note-taking knowledge base. Notes serve the current task and project.
- Credentials, mastery certification, job placement, or high-stakes grading. A checklist is not proof of competence.
- Social feeds, classroom administration, multi-user review, or monetization infrastructure before the learning loop is validated.

## 4. Experience and user stories

| Step | User story | Observable result |
| --- | --- | --- |
| Import | As a beginner with a saved tutorial, I want to name what I will make and set my available time so that the plan fits my life. | Confirmed source, goal, prerequisites, and estimated effort |
| Plan | As a time-constrained learner, I want to see how lessons contribute to the project so that I know what to do next. | Editable sequence with a practice action after each lesson |
| Workspace | As a learner applying a concept, I want source material, notes, and the task close together so that I can switch from understanding to doing. | Source-linked notes and a task with a clear definition of done |
| Practice | As a learner who gets stuck, I want to attempt, revise, or flag a task so that progress reflects what I can do. | Attempt/evidence distinct from watched/completed status |
| Submit | As a portfolio builder, I want to submit a draft and explain my decisions so that feedback has context. | Saved, consented submission with a rubric and revision path |
| Feedback | As a learner revising a draft, I want specific evidence and one next improvement so that I can act and try again. | Bounded feedback, uncertainty label, and a next action |
| Recovery | As a learner with an unavailable source or incomplete draft, I want an honest explanation and a recoverable next step. | No invented source content or lost work |

**Screen walkthrough:** Overview → Import → Learning plan → Video workspace → Tasks → Project submission → Feedback. The accompanying walkthrough illustrates this path using screenshots of the prototype. Mobile supports review, note capture, and task management; producing code may require another tool and a larger screen.

## 5. Requirements and acceptance criteria

### P0: minimum useful pilot

| Requirement | Acceptance criteria | Dependencies / limits |
| --- | --- | --- |
| Confirm source and goal | Given a supported public playlist, importing shows retrieved title, creator, available lessons, and unavailable items before confirmation. Unsupported, private, empty, or failed retrieval produces a retry/change-source path. | Engineering: authorized metadata access and quota handling; creator attribution review |
| Calibrate the plan | Given a goal, starting level, and 2/4/6-hour budget, the learner sees an effort breakdown, prerequisites, output, and editable sequence. A change in time recomputes the calendar estimate without changing the required learning output. | Learning designer validates the first domain; estimates labeled as estimates |
| Connect video to practice | Each task links to a verified source or explicitly authored exercise. Missing transcripts disable source-derived claims. Notes persist through navigation and reload. | Engineering: permitted video embedding or external-link fallback; transcript availability |
| Separate consumption and application | Marking a video watched never completes a task. Each task has a definition of done and accepts a short evidence note or artifact link; learner can undo, flag a blocker, and resume. | Design and learning design define states; analytics records attempts, not mastery |
| Submit and revise | Learner can save a draft before all tasks are complete, provide a link and reflection, see what is shared, and revise after feedback. Invalid URLs fail with a useful message and preserve draft fields. | Engineering: persistence and safe artifact access; explicit consent before remote evaluation |
| Bounded feedback | Every substantive assessment identifies supporting evidence or says it cannot evaluate. No fabricated grade if a page is unavailable. Separate deterministic checks, model suggestions, and human assessment. Give at least one concrete next action. | Engineering + learning design: evaluation rubric and benchmark set |
| Recover safely and accessibly | Keyboard-only flow works; labels, focus order, errors, and contrast are checked. At 375px and 768px controls remain usable without page-level horizontal scrolling. Reload retains work; blocked storage gives a truthful limitation. | Browser QA; WCAG 2.2 AA target subject to audit |
| Preserve attribution and control | Keep creator/source links visible. Do not train on, republish, or expose learner artifacts by default. Learner can export/delete their own work. | Privacy, creator-policy, and security review before real integrations |

**Current prototype boundary:** URL validation loads a fixed web-design fixture. Time budget changes the duration estimate, not the curriculum. Source videos open externally. Task completion is self-reported. Project URL and reflection stay in localStorage. Feedback is deterministic and labeled simulated. No metadata retrieval, model inference, artifact evaluation, cloud storage, or source-grounded assessment is implemented.

### P1: after the loop works

Adaptive task difficulty based on a first independent attempt; “I’m stuck” hints tied to the source; a revised plan after missed sessions; revision history and feedback resolution; optional cross-device sync; creator-authored exercise packs. Prioritize based on observed failure points in the pilot.

### P2: later

Other skill domains, peer/expert review, creator revenue share, YouTube-native distribution, team/classroom workflows, or premium subscriptions. Avoid designing v1 around these assumptions.

## 6. Success measures and experiment

All thresholds below are **proposed pilot decision rules**, not observed results or external benchmarks. Establish baselines and instrument before making claims.

| Measure | Definition / window | Initial decision rule |
| --- | --- | --- |
| Usability | Unassisted success on sample import → first practice task, observed with 5 qualifying learners | At least 4 of 5 succeed; investigate every critical blocker |
| Time to first practice | Median elapsed minutes from plan confirmation to starting a task in the same session, among successful sessions | Under 10 minutes; track abandonment alongside the median |
| Practice activation | Learners who submit evidence for one task within 24h / all learners with a confirmed plan | Hypothesis: at least 50% in a 20–30-person feasibility pilot |
| Project completion | Learners who submit a reviewable draft within 14 days / all randomized learners | Compare arms; do not exclude dropouts or call an inaccessible link complete |
| Applied skill, primary outcome | Blind rubric score on a new transfer task seven days after the learning period | Estimate the between-arm difference and uncertainty; choose a worthwhile effect and power a later study before asserting efficacy |
| Return to practice | Learners who start a second evidence-bearing practice session within seven days / learners who activated | Track directionally; no target until activation baseline is credible |
| Feedback usefulness | Learners who can name and perform one suggested revision / learners receiving feedback | Hypothesis: at least 70%; capture misleading advice separately |

**Experiment:** After usability fixes, run a small feasibility pilot using the same source material, project brief, available time, and starting-skill assessment. Randomly assign source-only versus source plus Relay practice/feedback. Blind assessors to assignment, use the same rubric, and include a delayed transfer task that differs from the tutorial. The pilot tests recruitment, instrumentation, and assessment feasibility; it is not sized to prove a learning lift. Pre-register a larger study after choosing a minimum worthwhile effect and estimating variance.

**Guardrails:** Report source failures, wrong feedback, cost per evaluated draft, draft loss, accessibility blockers, and total time burden. Do not optimize watch minutes. Any serious privacy issue, systematic unsupported assessment, or lost-work defect blocks expansion.

**Proposed events:** `plan_confirmed`, `lesson_opened`, `task_started`, `task_evidence_saved`, `task_blocked`, `draft_submitted`, `feedback_viewed`, `revision_submitted`, `export_completed`. Use identifiers and state transitions, not note or reflection text. No telemetry is added to the current demo.

## 7. Risks and open decisions

| Question / risk | Owner | When needed |
| --- | --- | --- |
| Is the binding problem knowing what to practice, missing prerequisites, or feedback? | Product research | Blocking scope commitment |
| Can we reliably access authorized metadata and usable transcripts for the launch curriculum? | Engineering + policy | Blocking real import |
| What constitutes independent skill at the beginner level, and who validates the rubric? | Learning designer | Blocking efficacy claims |
| How can a learner inspect what a remote evaluator receives and revoke access? | Design + privacy | Blocking remote evaluation |
| How do we prevent arbitrary project URLs from reaching private networks or executing untrusted code? | Engineering security | Blocking artifact fetching; use isolated evaluation and public-address validation |
| Will learners pay, or is creator/institution distribution better? | Product | Non-blocking discovery; test after value delivery |
| Should this live inside YouTube, a notebook, or a standalone companion? | Product + design | Test the standalone loop first; validate context-switch cost |

## 8. Phasing and launch gates

There is no committed launch date or staffing estimate.

1. **Concept and usability:** current prototype, screen walkthrough, 8–10 interviews, then 5 observed usability sessions. Gate: understood value, recoverable flow, and an agreed launch segment.
2. **Curated pilot:** one validated curriculum, real task evidence, saved drafts, and human-reviewed or tightly bounded feedback. Gate: usable flow, validated rubric, consent, privacy controls, and source reliability.
3. **Feasibility experiment:** recruit 20–30 qualifying learners, check instrumentation and blind assessment feasibility, and estimate effort/cost. Gate: sufficient value and operational reliability to justify a powered study.
4. **Broader integration:** authorized import and source-grounded generation only after quality, creator-policy, cost, and security checks. Expand subjects after the first learning loop demonstrates value.

**Positioning to test:** “The next step after a great tutorial: a plan, a project, and a way to improve it.”
