# chaekim.dev — personal portfolio

Static site for Chae Kim: MBA candidate at UC Berkeley Haas, ex-EY AI & Data consultant, IU Informatics.

- `index.html` — home (hero, selected work, playground, experience, about, contact)
- `projects/*.html` — case studies (one file per project)
- `assets/css/style.css` — design tokens + components (light/dark)
- `assets/js/main.js` — theme toggle, mobile nav, filters, scroll reveal
- `assets/img`, `assets/pdf` — media and downloadable deliverables

No build step. Deployed on Vercel (`vercel.json` enables clean URLs so `/projects/luc` serves `projects/luc.html`).

## Local preview

```bash
python3 -m http.server 8080
```

Then open http://localhost:8080. Note: the Python server doesn't do clean URLs, so project links resolve to `/projects/luc.html` on Vercel but need the `.html` locally — use `npx serve .` for parity.

## Updating content

- Add a project: duplicate a file in `projects/`, then add a `.card` in `index.html` with the right `data-cat` (`product`, `engineering`, `design`).
- Resume: drop a PDF at `assets/pdf/resume.pdf` and point the two "Resume" links in `index.html` to it.

## Photo credits

Project thumbnails are from Unsplash (free license): suitcases, sick-day kit, golden retriever, library study group, students with laptop, red house, meditation dock. Case-study imagery is Chae's own work.
