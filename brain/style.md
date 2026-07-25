# Style Guide — Visual & Typographic Decisions

---

## Font
- **Primary font:** Helvetica (sans-serif) via `\usepackage[scaled=0.92]{helvet}` + `\renewcommand{\familydefault}{\sfdefault}`
- **Why Helvetica:** Uniform stroke width — no hairline serifs — renders true black at all sizes. Serif fonts (Palatino, Charter, Computer Modern) have thin strokes that appear grey/light at 10pt.
- **Body size:** 10pt base, `\small` (9pt) for main-column body text
- **Name in sidebar:** `\fontsize{13}{16}` bold white, centred
- **Section headers (main):** `\normalsize\bfseries` in deep azure, uppercase via `\MakeUppercase`

---

## Colors (Azure palette — the gold standard)

| Role | Name | RGB |
|---|---|---|
| Primary accent | `azure` | 70, 128, 196 |
| Main-column headers/rules/bullets | `azuredeep` | 40, 88, 148 |
| Sidebar rules/dots (on navy) | `azurebright` | 120, 176, 240 |
| Sidebar background | `sidecolor` | 22, 36, 60 |
| Sidebar text | `sidetext` | 224, 230, 238 |
| Sidebar muted text | `sidesubtle` | 158, 174, 196 |
| Sidebar links | `sidelinkblue` | 130, 185, 245 |
| Page background | `mainbg` | 248, 250, 252 |
| Body text | `darkgray` | 16, 20, 26 |
| Meta (dates, company, location) | `medgray` | 92, 98, 106 |
| Light rule | `lightgray` | 205, 212, 222 |
| Links (main) | `linkblue` | 40, 88, 148 |

- The palette is swappable as a set, but keep the three-tier accent structure: primary / deep-on-light / bright-on-dark.
- **Body text is near-black — never grey.**
- **CRITICAL bug to avoid:** Any `\color{X}` for decorative elements MUST be wrapped in braces `{\color{X}\rule{...}}` — an unbraced `\color{}` leaks and turns ALL subsequent text that color.
- **Contrast rule:** Sidebar text is white/off-white only. Accent colour on the dark sidebar is reserved for thin rules and `\tiny\textbullet` dots — accent-coloured *text* on navy is unreadable.

---

## Sidebar Layout (top to bottom)
1. Oval photo — TikZ ellipse clip, thin `azurebright` border, `../assets/photo.jpg` (skipped automatically if absent)
2. Name (bold white) + cascaded title (bright azure, uppercase, `\scriptsize`)
3. Contact — phone, email, LinkedIn, GitHub, city (`\sidecontact` rows, links in `sidelinkblue`)
4. Optional differentiator section (e.g. "Current AI Research & Practice") — delete if unused
5. **Skills** — ONE consolidated block of ~6 `\sideskill{Category}{items}` groups (Rule 7)
6. Certifications (`\sidecertitem` rows)
7. Languages (`\sidelangitem` rows)
8. Industries (`\sidecertitem` rows)

**Orphan control:** each `\sideskill` group is an unbreakable minipage — the category label can never be stranded at a page bottom. `\sidesection` headings end lines with `\\*`.

---

## Company Logos (optional)
- Experience, education, and achievement entries reserve an **11mm logo column** left of the text (`\logocol`), with a 3pt gap (`\logogap`).
- Files: `assets/logo_<name>.png` (or `.jpg`) — e.g. `logo_company1.png`. Experience/education logos render 11mm tall; achievement icons 6mm.
- Missing logo files degrade to blank reserved space — text alignment never shifts, compilation never breaks.
- Logos are excluded from git along with all other images in `assets/`.

---

## Spacing
- **Margins:** top 0.55in, bottom 0.55in, left 0.50in, right 0.60in
- **Main sections:** `\mainsection` = 9pt above, 5pt below the rule
- **Between role blocks:** `\vspace{6pt}`
- **Bullet list:** itemsep=2pt, parsep=0pt, topsep=3pt
- **Sidebar skill groups:** 6.5pt between `\sideskill` minipages
- **Education entries:** 6pt between

---

## Page Layout (2 pages — fill both)
**Page 1:**
- Sidebar: photo → name/title → contact → (optional differentiator) → Skills (start)
- Main: Professional Summary (3 sentences, 4–5 lines) → Education (2 entries) → Experience (most recent role + start of second)

**Page 2:**
- Sidebar: Skills (rest) → Certifications → Languages → Industries
- Main: Experience continued → Selected Projects (5–6 `\projectentry` rows) → Achievements & Recognition

**Page break behaviour:**
- NO forced `\newpage` mid-experience — let LaTeX flow naturally
- `\interlinepenalty=10000` — no bullet splits across pages; whole bullet moves to next page
- `\widowpenalty=10000`, `\clubpenalty=10000` — no orphan lines
- `\nopagebreak[4]` after every `\explentry` — role header never stranded without its first bullet
- Page 2 must reach the bottom margin — add real bullets from `brain/person.md` if it trails off (Rule 1)

---

## Skimmability — Bold Keywords
**Bold ALL key technical terms from the JD** in the resume body using `\textbf{}`:
- Tool names the JD uses (in the sidebar skills and, for deeply technical roles, inline)
- Key phrases the JD repeats: "end-to-end delivery", "agile delivery", "CI/CD", etc.
- The biggest impact numbers can also be bolded
- Do NOT over-bold — only JD-matching terms and the biggest metrics

---

## Certifications (what to show)
Show ONLY the certifications listed in `brain/person.md`. Never add a certification that is not in the profile — certifications are credentials, and Rules 12/19 hard-block invented credentials.

---

## Compilation
- Run: `python compile.py --no-open` from the project root
- Compiler: `pdflatex` (MiKTeX on Windows, TeX Live / MacTeX on Mac/Linux)
- Output: `outputs/resume_latest.pdf` + `outputs/coverletter_latest.pdf` + friendly-named archives
- Windows, if PATH not refreshed: `$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")`

---

## Cover Letter Style
The cover letter is a separate 1-page document, compiled from `outputs/coverletter_latest.tex`.

**Visual branding:**
- Same Helvetica font, same deep azure accent, same link colour as the resume
- Letterhead: name (18pt bold) + azure subtitle + 2-line contact top-right (no photo)
- Thin light-grey rule beneath letterhead (ALWAYS in braces to prevent color leak)
- `\parskip{9pt}` for natural paragraph rhythm; no `\parindent`

**LaTeX structure gotchas:**
- Multi-line right cell in letterhead tabularx: use `\begin{tabular}[t]{@{}r@{}}` nested inside the cell — do NOT use `\\` inside a `{...}` group in a tabular
- After a `\\` line break, never start the next line with a literal `[` — LaTeX parses it as an optional argument. Use `\newline` instead.

**Content philosophy:**
- Write in first person (unlike the resume)
- Complement the resume — never duplicate bullet points
- Lead with genuine understanding of what makes the specific role difficult
- One concrete story per letter — the judgment call or delivery moment most relevant to the JD
- **Never name a gap.** Never write "I haven't worked in X." Find the structural parallel in real experience and state it as direct relevance — confidently, with evidence
- The reader should finish the letter thinking: *"This is the person we need to call."*
- Warm close: availability + location + open invitation, ≤2 sentences

**Archive filename pattern:** `FirstName_LastName_CoverLetter_{Role}_{Company}_{YYYY-MM-DD}.pdf`
