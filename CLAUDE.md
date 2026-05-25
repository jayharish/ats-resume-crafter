# ATS Resume Crafter — Claude Code Instructions

## What this project is

An agentic resume-tailoring system. The user pastes a job description → you generate a tailored LaTeX resume + cover letter → compile to PDF → log to tracker.

**North star:** 100 applications/day, zero manual intervention after the JD is pasted.

---

## ALWAYS READ FIRST

Before doing anything, read these files in order:

1. `brain/rules.md` — 18 rules governing every resume generation. **Non-negotiable.**
2. `brain/person.md` — the user's master profile. Source of truth for all facts and metrics.
3. `brain/style.md` — LaTeX visual/typographic decisions.
4. `session.json` — current iteration and last output state.

---

## When the user pastes a job description

Follow **Rule 0** exactly (full workflow in `brain/rules.md`):

1. **Classify & Plan** — extract title, company, location; apply Rule 17 title cascade; build ATS keyword list
2. **Write `outputs/resume_latest.tex`** — complete .tex file, sidebar layout (Rule 18 gold standard)
3. **Write `outputs/coverletter_latest.tex`** — complete cover letter .tex
4. **Update `session.json`** — increment iteration, set role/company/date/full_name
5. **Compile** — `python compile.py --no-open`
6. **Log** — insert into `applications.db` (direct DB insert, not interactive tracker.py)
7. **Report** — ATS match %, call probability %, both output filenames, PDF sizes

---

## Key rules to remember

- **Rule 17 (Title Cascading):** DOH-equivalent (most recent) gets exact JD title; older roles step down. Never "Junior" or "Intern".
- **Rule 13 (ATS):** Target 100% keyword match. Bold all JD keywords. Mirror exact JD terminology.
- **Rule 15 (Perfect Candidate):** Every line must make the hiring team think "this is exactly who we need." No gap language, no hedging.
- **Rule 9 (LaTeX):** `\raggedright` mandatory. Brace all color commands. `\mainsection` not `\section` (titlesec + paracol incompatible).
- **Rule 18 (Layout):** Sidebar layout is locked. Do not change it unless the user explicitly asks.

---

## LaTeX sidebar layout (gold standard — Rule 18)

```latex
%% Two-column sidebar
\columnratio{0.295}
\setlength{\columnsep}{14pt}

%% Sidebar background (eso-pic, calibrated width)
\AddToShipoutPictureBG{%
  \AtPageLowerLeft{%
    {\color{sidecolor}\rule{0.327\paperwidth}{\paperheight}}%
  }%
}

%% Paracol-safe section heading (DO NOT use \section — titlesec+paracol incompatible)
\newcommand{\mainsection}[1]{%
  \vspace{10pt}%
  \noindent{\normalsize\bfseries\color{crimson}\MakeUppercase{#1}}%
  \vspace{-5pt}\par\noindent%
  {\color{crimson}\hrule height 0.5pt}%
  \vspace{5pt}%
}

\begin{document}
\raggedright   %% ALWAYS first — prevents wobbly word spacing
\begin{paracol}{2}
  %% LEFT SIDEBAR — dark charcoal, white text
\switchcolumn
  %% RIGHT MAIN COLUMN — white bg, \small body text
\end{paracol}
\end{document}
```

**Sidebar:** charcoal `RGB(28,33,43)`, white headings, crimson rules + bullet dots only  
**Main column:** pure black body text, crimson section headings + rules

---

## Compilation

```bash
python compile.py --no-open
```

Reads `session.json` → compiles both .tex files → creates friendly-named PDF archives.  
Archive pattern: `FirstName_LastName_Role_Company_YYYY-MM-DD.pdf`

If pdflatex not found: ensure MiKTeX is installed and on PATH.  
Windows PATH refresh: `$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")`

---

## Logging to tracker

The `tracker.py add` command is interactive — insert directly into SQLite instead:

```python
import sqlite3
from pathlib import Path

ROOT = Path(r"<project_root>")
conn = sqlite3.connect(ROOT / "applications.db")
conn.execute("""
    INSERT INTO applications
        (date_applied, company, role, location, contract_type,
         resume_filename, resume_path, coverletter_filename,
         ats_score, call_probability, notes)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
""", ("<date>", "<company>", "<role>", "<location>", "Permanent",
      "<resume_fn>", "<resume_path>", "<cl_fn>",
      <ats_score>, <call_prob>, "<notes>"))
conn.commit()
conn.close()
```

---

## session.json schema

```json
{
  "iteration": 1,
  "full_name": "First Last",
  "brain_version": 1,
  "feedback_log": ["v1: ..."],
  "last_job_title": "Role -- Company",
  "last_output": "outputs/resume_latest.tex",
  "role": "Role_Title_Clean",
  "company": "Company_Name_Clean",
  "date_applied": "YYYY-MM-DD"
}
```

`role` and `company` use underscores, no special characters — these become the PDF filename segments.
