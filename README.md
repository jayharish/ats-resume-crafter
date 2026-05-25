# ATS Resume Crafter

> Paste a job description → get a tailored, ATS-optimised LaTeX resume + cover letter in minutes.  
> Powered by Claude AI. Professional sidebar layout. Tracks every application in SQLite.

---

## The problem

ATS (Applicant Tracking Systems) don't read resumes — they scan for keyword density, title match, and section structure. A resume that's brilliant for a human reader can score zero on an ATS and never reach a human at all.

Most people send the same resume everywhere. That's why most applications go nowhere.

## The solution

This project is a personal resume-tailoring agent. You fill in your profile once — your work history, real projects, real metrics, certifications. Then for each application:

1. Paste the job description into Claude Code
2. The agent extracts every keyword the ATS is scanning for
3. Synthesises fresh, ATS-optimised bullets from your real experience
4. Applies the **Title Cascading strategy** — assigns job titles that match the JD's vocabulary across your career history
5. Generates a complete LaTeX resume + cover letter
6. Compiles both to PDF in one command
7. Logs the application to a local SQLite tracker

**You never write a bullet point. You never rename a file. You just paste the JD.**

---

## What makes this different

### Title Cascading (Rule 17)
ATS systems weight title match heavily. This agent reassigns your job titles per application to mirror the JD's title vocabulary — showing a clean, credible career trajectory in exactly the domain being hired for. The most recent role always gets the JD title verbatim. Older roles step down cleanly. Never "Junior", never "Intern".

### 100% Keyword Target (Rule 13)
Every keyword in the JD is extracted into categories (role terms, responsibility phrases, tool names, qualifications, industry terms) before a single bullet is written. The resume is not considered done until every extracted keyword is present in the body — either in experience bullets or the skills section. The ATS score is reported with every output.

### The Perfect Candidate Standard (Rule 15)
Every line passes one test: *"When the hiring team reads this, does it make them think 'this is exactly who we need'?"* No gap language. No hedging. No weak verbs. Every bullet positions you as the person accountable and in charge — not a contributor, not someone who helped.

### Professional sidebar layout
Dark charcoal sidebar (photo, contact, skills, certs, languages) + clean white main column. LaTeX-compiled. Renders as a proper professional document, not a Word template.

---

## Setup

### Prerequisites
- [Claude Code](https://claude.ai/code) (free tier works)
- [MiKTeX](https://miktex.org/download) (LaTeX compiler — Windows) or `texlive` (Mac/Linux)
- Python 3.9+
- A headshot photo (optional, for sidebar)

### Installation

```bash
git clone https://github.com/yourusername/ats-resume-crafter.git
cd ats-resume-crafter
```

No Python dependencies to install — only stdlib used.

### 1. Fill in your profile

Edit **`brain/person.md`** — this is the only file you need to fill in.

Add:
- Your name, contact details, LinkedIn, GitHub, location
- Your work history: company, dates, what you actually did, **real metrics**
- Your signature story (your proudest, most differentiating achievement — appears in every summary)
- Education, certifications, languages
- Technical skills master list

You do **not** need to write resume bullet points. The AI synthesises those fresh for each application from your raw facts in `brain/person.md`.

### 2. Update session.json

Set your `full_name` in `session.json` — this is used to name the output PDFs:

```json
{
  "full_name": "Jane Smith",
  ...
}
```

### 3. Add your photo (optional)

Drop a `photo.jpg` in the `assets/` folder. The resume will include an oval-cropped version in the sidebar header.

### 4. Open in Claude Code

```bash
claude
```

Paste any job description. Claude handles the rest — resume, cover letter, compilation, and logging.

---

## Usage

In a Claude Code session, just paste a job description. The agent will:

1. Extract the JD title, company, location, contract type
2. Build the full ATS keyword list
3. Apply title cascading across your career history
4. Write `outputs/resume_latest.tex` (complete LaTeX)
5. Write `outputs/coverletter_latest.tex`
6. Update `session.json`
7. Run `python compile.py --no-open`
8. Log to `applications.db`
9. Report: ATS match %, call probability %, output filenames

### Manual compilation

```bash
python compile.py          # compile + open PDFs
python compile.py --no-open   # compile only
```

### View application log

```bash
python tracker.py list
python tracker.py view 3   # full details of application #3
python tracker.py status   # update status of an application
```

---

## Project structure

```
ats-resume-crafter/
├── CLAUDE.md                     ← Claude Code instructions (loaded automatically)
├── README.md
├── compile.py                    ← Compiles LaTeX → PDF, auto-renames archives
├── tracker.py                    ← SQLite application tracker
├── session.json                  ← Current iteration, role, company
├── brain/
│   ├── person.md                 ← YOUR PROFILE — fill this in
│   ├── rules.md                  ← ATS strategy + generation rules (18 rules)
│   └── style.md                  ← LaTeX visual/typographic decisions
├── outputs/
│   ├── resume_latest.tex         ← Working resume (overwritten each run)
│   ├── coverletter_latest.tex    ← Working cover letter (overwritten each run)
│   ├── resume_latest.pdf         ← Latest compiled resume
│   └── [archived PDFs]           ← Auto-named: FirstName_LastName_Role_Company_Date.pdf
└── assets/
    └── photo.jpg                 ← Your headshot (not tracked in git)
```

---

## The strategy, in plain English

The brain of this project is `brain/rules.md` — 18 rules that govern every resume generated. The key insight is that getting an interview is a two-stage problem:

**Stage 1 (what this project solves):** Beat the ATS machine. Get your resume in front of a human. This requires keyword density, title match, and section structure — not creativity.

**Stage 2 (yours to own):** Win the interview. That's a human problem. Confidence, preparation, and real experience win there — not the resume.

This project is engineered entirely for Stage 1. Once you're in the room, you're on your own.

---

## Output example

Each run produces:
- `FirstName_LastName_RoleTitle_Company_YYYY-MM-DD.pdf` — tailored resume
- `FirstName_LastName_CoverLetter_RoleTitle_Company_YYYY-MM-DD.pdf` — cover letter

---

## Built with

- [Claude Code](https://claude.ai/code) — AI agent
- [LaTeX / pdflatex](https://miktex.org/) — PDF typesetting
- [paracol](https://ctan.org/pkg/paracol) — sidebar layout
- [eso-pic](https://ctan.org/pkg/eso-pic) — full-height sidebar background
- SQLite — application tracking

---

## License

MIT — do whatever you want with it. If it helps you land interviews, that's the point.
