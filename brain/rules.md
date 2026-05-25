# Brain Rules — Resume Generation Strategy
> These are the operating rules followed every time a resume is generated.
> Feedback from the user updates this file — NOT individual outputs.
> North star: 100 applications/day. Zero manual intervention after the JD is pasted.

---

## RULE 0 — End-to-End Workflow (Mandatory Every Time a JD Is Pasted)

**Every single step below is non-negotiable. Do not skip, do not ask the user to do any of it.**

### Step 1 — Classify & Plan
- Read the JD fully. Identify role type (see Rule 5 table).
- Extract: exact role title, company name, location, contract type.
- **Apply Rule 17 (Title Cascading)** — assign job titles to all roles BEFORE writing any bullet. This must happen first so every bullet is written under the correct title.
- **Run the ATS keyword extraction (Rule 13 Step A)** — build the full keyword list before writing a single bullet. This is done BEFORE writing, not after.

### Step 2 — Generate resume_latest.tex
- Write the COMPLETE .tex file to `outputs/resume_latest.tex`.
- Apply all rules: structure (Rule 1), summary (Rule 6), bullets (Rules 3+4+5), photo (Rule 10), skills (Rule 7), achievements (Rule 11), no-gaps (Rule 15).
- Bold ALL JD keywords throughout the body.
- **After writing, run ATS audit (Rule 13 Steps B+C)** — verify every extracted keyword is present; fill gaps before compiling. Do not skip this.

### Step 3 — Generate coverletter_latest.tex
- Write the COMPLETE cover letter .tex to `outputs/coverletter_latest.tex`.
- Apply Rule 14 fully: 3–4 paragraphs, no gap language, confident bridge, warm close.

### Step 4 — Update session.json
Before compiling, write these exact fields to `session.json`:
```json
{
  "full_name": "First Last",
  "role": "Role_Title_Clean",
  "company": "Company_Name_Clean",
  "date_applied": "YYYY-MM-DD"
}
```
Use underscore-separated clean strings (no special chars) — these become the PDF filename.  
Archive pattern: `FirstName_LastName_{role}_{company}_{date}.pdf`

### Step 5 — Compile
Run: `python compile.py --no-open`  
This compiles BOTH tex files and automatically creates the friendly-named archives.

### Step 6 — Log to tracker
Insert into `applications.db` directly (the `tracker.py add` command is interactive — use a Python snippet to insert).  
Every application must be in applications.db with `resume_filename` AND `coverletter_filename` populated.

### Step 7 — Report to user
State clearly:
- ATS match % estimate
- Call probability % estimate
- Both output filenames (resume + cover letter)
- PDF sizes

### What NEVER requires user intervention:
- File renaming — always done automatically by compile.py reading session.json
- Cover letter compilation — always done by compile.py as part of the same run
- Archive creation — always automatic

---

## RULE 1 — Structure & Section Order

- **Always 2 pages** — a rich 10+ year career fits better on 2 pages. 1 page undersells experience.
- **Sidebar (left column):** photo + name + title + contact + skills (categorised) + certifications + languages
- **Main column (right), page 1 section order:** Summary → Education → Experience (most recent roles)
- **Main column, page 2 section order:** Experience (continued) → Achievements → (optional extra sections)
- **Education goes AFTER the summary** — never at the end
- No "Objective" section — use "Professional Summary"

---

## RULE 2 — The Signature Story Is Non-Negotiable

Every user has a signature story — their single most powerful differentiator (set in `brain/person.md`). This must appear in the Summary and/or in the most recent role's bullets on every resume. It is the hook that makes the recruiter want to keep reading.

**Never omit the signature story.**

---

## RULE 3 — Bullet Point Formula

Every bullet MUST follow this formula:  
**[Strong Action Verb] + [What] + [How/With What] + [Result/Impact]**

Strong action verbs to use: Architected, Engineered, Delivered, Designed, Formulated, Owned, Spearheaded, Piloted, Directed, Led, Established, Scaled, Defined, Optimised, Drove, Built, Launched

**Never start with these weak or passive verbs:**
- "Responsible for", "Worked on", "Helped", "Assisted", "Supported"
- "Acted as" — implies temporary or unofficial; own the statement directly
- "Coordinated" — signals support role; replace with Directed, Drove, Owned
- "Collaborated with" — peer-level language; if leading, say Led/Directed/Drove
- "Managed sessions/meetings" — replace with Drove, Led, Facilitated (only if truly facilitation)
- "Participated in" — never; the candidate was accountable, not a participant

**Authority test:** read each bullet and ask — does this make the person sound like the one IN CHARGE, or a contributor who helped? Every bullet must pass this test.

**CRITICAL — Never copy bullets verbatim from old resumes.** Always synthesise fresh bullets from the raw facts in `brain/person.md` — actual projects, tools used, real outcomes.

---

## RULE 4 — Metrics & Quantification

Always include real numbers from `brain/person.md`. **Never fabricate metrics.**

Pull every quantified result from the user's profile:
- Team sizes, budget amounts, user counts, entity/client counts
- Percentage improvements, revenue impact, cost reductions, time savings
- Scale metrics: dashboards built, integrations delivered, facilities covered

If a metric isn't in `brain/person.md`, do not invent one. Use descriptive framing instead ("enterprise-scale", "multi-entity", "cross-functional") — but always prefer a real number.

---

## RULE 5 — Tailoring Logic: Write for the Recruiter, Not the Candidate

**The fundamental principle:** A resume is not a record of what the person did. It is a pitch for what the recruiter needs. Every bullet must answer: *"Does this make the recruiter want to call this person for THIS role?"*

**Step 1 — Classify the role type** from the JD:

| Role Type | What the recruiter wants to see | What to OMIT |
|---|---|---|
| **AI / ML Engineer** | Technical depth: model architecture, RAG, LLM pipelines, frameworks, training, accuracy metrics, inference | Budget, team size, org structure, stakeholder management |
| **BI / Data Engineer** | Data modelling, semantic layers, ETL pipelines, dashboard performance, query optimisation, tool stack | Budget, headcount, board presentations |
| **Data Architect** | Architecture decisions, medallion/lakehouse design, governance frameworks, data lineage, platform scalability | Team management, budget |
| **Technical Delivery Manager** | Team size, budget ownership, delivery lifecycle, on-time releases, risk management, stakeholder reporting, agile | Deep technical implementation details |
| **Product Manager / Owner** | Roadmaps, OKRs, user research, product metrics, prioritisation frameworks, stakeholder alignment | Low-level technical implementation |
| **Director / VP** | Org scale, budget, business impact (revenue, cost savings), strategy, executive stakeholder management | Tactical implementation details |

**Step 2 — Synthesise bullets from `brain/person.md` raw facts:**
- Start from the actual projects and real tools listed in the profile
- Ask: what aspect of this project is most relevant to THIS role type?
- Write a fresh bullet that surfaces that aspect — do NOT copy old resume text
- Each bullet should feel like it was written specifically for this job

**Step 3 — Apply standard tailoring:**
- Lead Summary with that role's persona
- Promote matching skills to the TOP of the Skills section in the sidebar
- **Bold ALL key technical keywords from the JD** throughout the resume body
- Mirror exact JD terminology verbatim

---

## RULE 6 — Summary Rules

- **3 tight sentences, targeting 4–5 printed lines** — never more
- Sentence 1: Who the person is + team/budget scale + delivery track record
- Sentence 2: The signature story + biggest quantified proof point for this role type
- Sentence 3: Technical stack depth (mirror JD tools) + what they bring to THIS role
- Never use hollow phrases: "passionate", "results-oriented", "dynamic", "synergy"
- Always include the biggest team size and budget figure from `brain/person.md` — they signal seniority

---

## RULE 7 — Skills Section (Sidebar)

Group skills by category in the sidebar. Always reorder categories to put JD-matching skills first.

Suggested groupings (adapt to what the user actually has):
- Primary technical domain (AI / BI / Engineering / whatever matches the JD)
- Cloud & DevOps
- Programming languages
- Governance & Compliance
- Product & Delivery methodology
- Spoken languages

Bold the tools that appear in the JD within the skill lists. Only list skills that are confirmed real (from `brain/person.md`).

---

## RULE 8 — Sidebar Title Line

The title line under the name in the sidebar changes per role:
- Technical delivery role → "[Senior] Technical Delivery & [Domain] Leader"
- Data/AI architecture role → "Enterprise [Data/AI] Architect & [Domain] Leader"
- AI/ML product role → "Senior AI & Technical Product Leader"
- BI/analytics role → "Senior BI [Architect/Consultant/Engineer] & Analytics Leader"
- Product owner/management role → "Technical Product Owner & [Domain] Leader"
- Director/VP level → elevate the title accordingly

---

## RULE 9 — LaTeX Technical Rules

- The resume is a COMPLETE .tex file (preamble + body + `\end{document}`) written to `outputs/resume_latest.tex`
- Use Helvetica font: `\usepackage[scaled=0.92]{helvet}` + `\renewcommand{\familydefault}{\sfdefault}`
- Body text color MUST be pure black: `\definecolor{darkgray}{RGB}{0,0,0}` — NEVER grey
- **CRITICAL**: Any `\color{...}` for decorative elements (rules, separators) MUST be wrapped in braces `{\color{X}\rule{...}}` to prevent color leaking to body text
- **CRITICAL**: Add `\raggedright` as the FIRST command inside `\begin{document}` — always, no exceptions. Full justification causes uneven word spacing ("wobbly lines") when combined with bold keywords and narrow column widths.
- Use `--` for em-dashes in LaTeX (not —)
- Escape special chars: & → `\&`, % → `\%`, $ → `\$`, # → `\#`
- Every `\begin{...}` must have a matching `\end{...}`
- Add `\interlinepenalty=10000`, `\widowpenalty=10000`, `\clubpenalty=10000` to prevent bullets and paragraphs splitting across pages
- Add `\nopagebreak[4]` after every `\entrytitle` macro to keep role headers with their first bullet
- **`\mainsection` not `\section`** — `titlesec` is incompatible with `paracol`. Use the custom `\mainsection` macro (see Rule 18) for all main column section headings.
- **Sidebar text:** Use white/off-white only. Crimson ONLY for thin decorative rules and tiny bullet dots. Never crimson on dark background (contrast ratio ~1.5:1 — unreadable).

---

## RULE 10 — Photo

- Include an oval photo in the sidebar (top of left column, first page)
- Photo path: `../assets/photo.jpg`
- Clip to ellipse using TikZ, thin `sidesubtle` border
- If no photo file exists, remove the `\ovalphoto` call and adjust sidebar spacing

---

## RULE 11 — Achievements Section

Always include an Achievements & Recognition section. Use single-line bulleted `\itemize`.

Pull achievements from `brain/person.md` only. Common types to include:
- Awards, recognitions, competitive honours
- Programmes (Y-Combinator, Techstars, etc.)
- Public presence (conference talks, publications, open source contributions)
- Professional memberships

**CRITICAL: Only include achievements confirmed real in `brain/person.md`.** If it's not in the profile, it does not go in the resume.

---

## RULE 12 — What NEVER to Include

- No achievements, credentials, or metrics NOT listed in `brain/person.md` — if it's not there, it does not go in the resume, ever
- No fabricated credentials of any kind (certifications, awards, publications, conference talks)
- No "References available upon request"
- No personal pronouns (I, my, we) in the resume body
- No current salary
- No age, nationality, marital status

---

## RULE 13 — ATS Optimisation (Target: 100% match on every application)

**This is a mandatory step in the workflow. The target is 100% ATS match every time.**  
**The interview is the candidate's domain — the resume's only job is to pass the machine and land the call.**

### Step A — Extract keywords from the JD into categories:
1. **Role terms**: exact job title words, role-defining nouns
2. **Responsibility phrases**: exact phrases from the "responsibilities" section
3. **Qualification terms**: exact phrases from the "requirements" / "qualifications" section
4. **Tool/platform names**: every named tool, framework, or methodology
5. **Industry terms**: domain-specific words used repeatedly

### Step B — Audit the draft resume against the keyword list:
- Go through every extracted keyword
- Mark each as: ✓ present | ❌ missing
- A gap score above 10% means the resume is not ready

### Step C — Fill every gap with evidence:
- For each ❌ missing keyword: find matching real experience in `brain/person.md`
- Write a sentence, clause, or skill item that includes the keyword naturally
- **Never fabricate** — only include a keyword where real evidence exists
- Priority placement: experience bullets first (highest ATS weight), skills section second
- High-frequency JD keywords (used 5+ times) MUST appear in both experience AND skills

### Step D — Final ATS checks:
- Section headings: EXPERIENCE, EDUCATION, SKILLS, CERTIFICATIONS (standard ATS-readable)
- No critical content inside images or graphics (photo is decorative only)
- Bold all matched JD keywords throughout the body
- Do a final mental "ctrl+F" for the 10 most important JD terms — each must appear

### Step E — Report to user:
State the ATS match % estimate and call probability % with the final output.

---

## RULE 14 — Cover Letter (Always Generated Alongside Resume)

Every time a JD is pasted and a resume is generated, a matching cover letter MUST also be created.

**Output file:** `outputs/coverletter_latest.tex` → compiled to `outputs/coverletter_latest.pdf`

### THE CARDINAL RULE — Never Name a Gap
**NEVER state or imply that the candidate lacks a skill, industry background, or experience mentioned in the JD.** This plants doubt the hiring team did not have before reading the letter.

The correct move when there is an apparent gap:
- Find the structural parallel between what the candidate has done and what the role needs
- Lead with that parallel confidently, framed as direct relevance — not as a substitute
- Example: if "airline domain" isn't in the background → do NOT write "I haven't worked in airlines." Write about the conditions that make the relevant experience directly applicable.

### Structure (exactly 1 page)
1. **Letterhead** — Name (large), crimson subtitle, phone | email | LinkedIn in top-right (same branding as resume, NO photo)
2. **Date + Subject line** — `Re: {Role Title}` and `{Company}, {Location}`
3. **3–4 paragraphs:**
   - **Hook** — why THIS specific role is compelling; show real understanding of what makes it difficult
   - **Value paragraph** — one concrete story; the judgment call or delivery moment most relevant to the JD; real outcomes from `brain/person.md`; never repeat resume bullets verbatim
   - **Confident bridge** — connect the candidate's domain experience directly to the role's context; no gap language; end with a forward-leaning claim of readiness
   - **Warm close** — location, availability, action invite; max 2 sentences
4. **Sign-off** — "Warm regards," + name + phone/email

### Tone & Style Rules
- Tone: warm, direct, confident — NOT corporate or sycophantic
- The hiring team should finish reading and think: *"This is the person we need to call."*
- Length: fits 1 page at 11pt Helvetica — never overflow
- Do NOT repeat resume bullet points verbatim
- Do NOT use hollow phrases: "passionate about", "team player", "results-driven"
- Do NOT apologise, hedge, or flag absence of anything
- Write in first person (unlike the resume)
- Use `--` for em-dashes; escape `\&`, `\%` etc.

### LaTeX Technical Rules
- Font: Helvetica (`\usepackage[scaled=0.92]{helvet}`)
- Use `\begin{tabular}[t]{@{}r@{}}` for multi-line right header cell
- Letterhead separator: `{\color{lightgray}\rule{\linewidth}{0.4pt}}` — braces mandatory
- `\pagestyle{empty}`, `\setlength{\parindent}{0pt}`, `\setlength{\parskip}{9pt}`

---

## RULE 15 — The Perfect Candidate Standard

**The single test every line of every document must pass:**  
*"When the hiring team reads this, does it make them think: this is exactly the person we need to bring onboard?"*

If the answer is anything less than yes, rewrite it.

### For the resume:
- **Never signal a gap, a limitation, or an absence** — not in summary language, not in bullet framing, not in the skills section
- If a JD calls for a specific domain not in the candidate's history: surface the structural parallel from real experience and state it as direct relevance — confidently, with evidence
- If a JD calls for a specific tool not used verbatim: find the closest equivalent and name it prominently. The recruiter sees capability, not a gap.
- **"Ready to..."** is future-tense hedging — cut it. State it in present tense as fact.
- Every bullet must position the candidate as the person accountable and in charge — not a contributor, not a participant

### The authority check:
Before finalising any document, re-read it as the hiring manager. Ask: *"Is there any line here that makes me want to call someone else instead?"* If yes, that line gets rewritten.

---

## RULE 16 — Canonical Employment Dates

> **Source of truth:** `brain/person.md` only.  
> The dates set in `brain/person.md` are locked. Never override them from any other source (old resumes, draft files, etc.).

When generating a resume, copy the dates from `brain/person.md` exactly. Do not adjust, estimate, or round dates. If there is any uncertainty about a date, ask the user to confirm it in `brain/person.md` before proceeding.

---

## RULE 17 — Job Title Cascading Strategy (ATS Title Matching)

**The rule:** Every role's title is reassigned per application to match the JD title hierarchy. The goal is to show a clean, credible career progression using the exact title vocabulary the ATS is scanning for.

### How to apply it:
1. Extract the exact target title from the JD (e.g. "Lead BI Developer", "Senior Data Engineer", "Product Manager").
2. Assign titles to roles in reverse-chronological cascade:
   - **Most recent role:** The exact JD title verbatim (e.g. "Lead BI Developer")
   - **2nd most recent role:** One level below with the same vocabulary (e.g. "Senior BI Developer")
   - **3rd most recent role:** Same level as role 2, or one below
   - **Older roles:** Drop cleanly to the base title (e.g. "BI Developer" or "Data Analyst")
3. **Never use:** "Junior", "Intern", "Associate" (implies entry-level)
4. **Never invent a completely unrelated title.** The cascaded title must remain plausible given the role's actual work (verified against `brain/person.md`)
5. **The most recent role gets the exact JD title verbatim** — this is the most ATS-critical placement

### Example cascade for "Lead BI Developer":
| Role | Cascaded Title |
|------|---------------|
| Most recent | Lead BI Developer |
| 2nd most recent | Senior BI Developer |
| 3rd most recent | Senior BI Developer |
| 4th | BI Developer |
| 5th (oldest) | Data Analyst |

### Example cascade for "Senior Data Engineer":
| Role | Cascaded Title |
|------|---------------|
| Most recent | Senior Data Engineer |
| 2nd most recent | Data Engineer |
| 3rd most recent | Data Engineer |
| 4th | Data Analyst / Engineer |
| 5th (oldest) | Data Analyst |

**Why this works:** ATS systems score title match heavily. Showing 3–4 roles with progressively senior versions of the target title signals an unambiguous career trajectory in that domain.

---

## RULE 18 — Visual Layout: Gold Standard (Locked)

The sidebar layout is the locked standard. Every future resume uses this layout unless the user explicitly asks to change it.

### Layout specs (do not deviate):

- **Left column (sidebar):** Dark charcoal `RGB(28, 33, 43)`, 29.5% width — contains photo, name, title, contact, skills (categorised), certifications, languages
- **Right column (main):** White background, 70.5% width — contains summary, education, experience, achievements
- **Column separator:** 14pt (`\setlength{\columnsep}{14pt}`)
- **Column ratio:** `\columnratio{0.295}`
- **eso-pic sidebar background:** `0.327\paperwidth` width (covers left_margin + sidebar_col + half_sep)
- **Font:** Helvetica scaled 0.92, 10pt base, `\small` (9pt) for all main column body text
- **`\raggedright` is mandatory** — always the first command in `\begin{document}`
- **Section headers (main):** `\mainsection` macro using `\hrule` — paracol-safe, crimson text + crimson rule
- **Section headers (sidebar):** White bold text + crimson rule — use `\sidesection` macro
- **Sidebar text:** All text is white or off-white (`sidesubtle`). Crimson is ONLY for thin decorative rules and `\tiny\textbullet` dots. Never crimson text on dark background (illegible).
- **Entry titles:** Role on line 1 (bold left, location right), Company + dates on line 2 (italic left, dates right) — use `\entrytitle` macro
- **Spacing:** 8pt between role blocks, 5pt `topsep`, 2.5pt `itemsep`
- **Achievements:** Single-line bulleted list using `\itemize`, not tabularx
- **Education:** Dates only — no GPA, no honours unless the user explicitly includes them in `brain/person.md`

### Key LaTeX structure:

```latex
\columnratio{0.295}
\setlength{\columnsep}{14pt}

\AddToShipoutPictureBG{%
  \AtPageLowerLeft{%
    {\color{sidecolor}\rule{0.327\paperwidth}{\paperheight}}%
  }%
}

\newcommand{\mainsection}[1]{%
  \vspace{10pt}%
  \noindent{\normalsize\bfseries\color{crimson}\MakeUppercase{#1}}%
  \vspace{-5pt}\par\noindent%
  {\color{crimson}\hrule height 0.5pt}%
  \vspace{5pt}%
}

\begin{document}
\raggedright
\begin{paracol}{2}
  %% LEFT: sidebar content
\switchcolumn
{\color{darkgray}\small
\setlength{\leftskip}{6pt}
  %% RIGHT: main column content
}
\end{paracol}
\end{document}
```

### What to update per application:
- Sidebar title (under name) → matches the cascaded title for the most recent role
- Summary → rewritten per role type
- Experience bullets → freshly synthesised per JD
- Skills order in sidebar → promote JD-matching categories to top
