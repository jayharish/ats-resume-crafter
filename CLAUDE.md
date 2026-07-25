# ATS Resume Crafter — Claude Code Instructions

## What this project is

An agentic resume-tailoring system. The user pastes a job description → you generate a tailored LaTeX resume + cover letter → compile to PDF → log to tracker.

**North star:** 100 applications/day, zero manual intervention after the JD is pasted.

---

## ALWAYS READ FIRST

Before doing anything, read these files in order:

1. `brain/rules.md` — 19 rules governing every resume generation. **Non-negotiable.**
2. `brain/person.md` — the user's master profile. Source of truth for all facts and metrics.
3. `brain/style.md` — LaTeX visual/typographic decisions.
4. `session.json` — current iteration and last output state.

---

## When the user pastes a job description

Follow **Rule 0** exactly (full workflow in `brain/rules.md`):

1. **Classify & Plan** — extract title, company, location; apply Rule 17 title cascade; build ATS keyword list
2. **Write `outputs/resume_latest.tex`** — complete .tex file, gold standard layout (Rule 18)
3. **Write `outputs/coverletter_latest.tex`** — complete cover letter .tex
4. **Update `session.json`** — increment iteration, set role/company/date/full_name
5. **Compile** — `python compile.py --no-open`
6. **Log** — insert into `applications.db` (direct DB insert, not interactive tracker.py)
7. **Report** — ATS match %, call probability %, both output filenames, PDF sizes

---

## Key rules to remember

- **Rule 17 (Title Cascading):** Most recent role gets the exact JD title verbatim; older roles step down. Never "Junior" or "Intern".
- **Rule 13 (ATS):** Target 100% keyword match. Bold all JD keywords. Mirror exact JD terminology.
- **Rule 15 (Perfect Candidate):** Every line must make the hiring team think "this is exactly who we need." No gap language, no hedging.
- **Rule 3 (Impact-First Bullets):** Lead with the outcome and its metric. Tool jargon does NOT go in bullets — it lives in the sidebar Skills block.
- **Rule 7 (Skills):** ONE consolidated, categorised **Technical Skills** block in the sidebar via `\sideskill{Category}{items}`. No per-role skills lines, no last-page skills block.
- **Rule 9 (LaTeX):** `\raggedright` mandatory. Brace all color commands. `\mainsection` not `\section` (titlesec + paracol incompatible). `\sideskill` groups are unbreakable minipages. Title cells are ragged-right X columns.
- **Rule 16 (Dates):** Employment dates come from `brain/person.md` only — never from any other file.
- **Rule 18 (Layout):** Gold standard is locked — navy sidebar + azure accents + optional company logos + Selected Projects section. Do not change it unless the user explicitly asks.
- **Rule 19 (Fast-Learnable Tools):** A JD-named tool that is adjacent to real skills and genuinely fast to learn may be added to the Skills block by name. Credentials (degrees, certs, awards) are NEVER invented.

---

## Gold standard layout (Rule 18 — locked)

- **Left sidebar:** deep navy `RGB(22,36,60)`, 29.5% width, eso-pic background `0.327\paperwidth` — photo, name, cascaded title, contact, optional differentiator section, **Technical Skills** (all tool jargon), certifications, languages, industries
- **Right column:** soft off-white `RGB(248,250,252)`, `\small` body text — Summary → Education → Experience → **Selected Projects** → Achievements
- **Accents:** azure three-tier — `azure RGB(70,128,196)` primary, `azuredeep RGB(40,88,148)` on light, `azurebright RGB(120,176,240)` on navy. Sidebar text is white/off-white only.
- **Company logos (optional):** `\explentry`/`\edulentry`/`\achieveentry` reserve an 11mm logo column; `assets/logo_<name>.png` files fill it; missing files degrade gracefully via `\IfFileExists`.
- **Selected Projects:** 5–6 `\projectentry{Name}{-- Type tag}{Impact}` rows after Experience — bold name + azure italic type tag + one-line impact, spanning the whole career.
- `\columnratio{0.295}`, `\setlength{\columnsep}{14pt}`
- Entry titles: role line 1 (bold left, dates right), company line 2 (italic left, location right) — ragged-right X columns so wrapped titles never justify-stretch.
- The full macro set lives in `outputs/resume_latest.tex` — regenerate content, reuse the macros.

---

## Compilation

```bash
python compile.py --no-open
```

Reads `session.json` → compiles both .tex files → creates friendly-named PDF archives.  
Archive pattern: `FirstName_LastName_Role_Company_YYYY-MM-DD.pdf`

If pdflatex not found: ensure MiKTeX (Windows) or TeX Live/MacTeX (Mac/Linux) is installed and on PATH.  
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

---

## End of every session

When the user wraps up, remind them to commit and push so their fork stays in sync across devices:

```
git add -A
git commit -m "v{N}: {Role} -- {Company} ({date})"
git push
```
