# Style Guide — Visual & Typographic Decisions

---

## Font

- **Primary font:** Helvetica (sans-serif) via `\usepackage[scaled=0.92]{helvet}` + `\renewcommand{\familydefault}{\sfdefault}`
- **Why Helvetica:** Uniform stroke width — no hairline serifs — renders true black at all sizes. Serif fonts (Palatino, Charter, Computer Modern) have thin strokes that appear grey/light at 10pt.
- **Body size:** 10pt base; `\small` (9pt) for all main column body text
- **Name in sidebar:** `\fontsize{13}{16}` bold
- **Section headers:** `\normalsize\bfseries` in crimson, uppercase via `\MakeUppercase`

---

## Colors

- **Body text (main column):** Pure black `RGB(0, 0, 0)` — NEVER use grey for body text
- **Sidebar background:** Dark charcoal `RGB(28, 33, 43)`
- **Sidebar body text:** Off-white `RGB(230, 230, 230)`
- **Sidebar subtle text (name subtitle, dates, categories):** `RGB(175, 182, 196)`
- **Sidebar links:** `RGB(120, 185, 245)`
- **Section rules and bullet dots:** Crimson `RGB(165, 28, 48)`
- **Meta info in main column (dates, company names, locations):** Dark grey `RGB(90, 90, 90)`
- **Header separator rule:** Light grey `RGB(210, 210, 210)`
- **Links (main column):** Deep blue `RGB(0, 50, 110)`

**CRITICAL bug to avoid:** Any `\color{X}` for decorative elements MUST be wrapped in braces `{\color{X}\rule{...}}` — an unbraced `\color{}` leaks and turns ALL subsequent body text that color.

**Contrast rule:** Never use crimson text on the dark charcoal sidebar background. Crimson on charcoal is ~1.5:1 contrast ratio — completely illegible. Sidebar headings and labels must be white or `sidesubtle`.

---

## Sidebar Layout

```
┌─────────────────┬──────────────────────────────────────────┐
│  [oval photo]   │  Professional Summary                    │
│                 │  ───────────────────────────────────────  │
│  Name           │  Education                               │
│  Title          │  ───────────────────────────────────────  │
│                 │  Experience                              │
│  CONTACT        │                                          │
│  ───────        │  Most Recent Role                        │
│  phone          │  Company         Location                │
│  email          │  • Bullet 1                              │
│  linkedin       │  • Bullet 2                              │
│  github         │                                          │
│                 │  Second Role                             │
│  SKILLS         │  Company         Location                │
│  ───────        │  • Bullet 1                              │
│  Category       │                                          │
│  • Skill        │  ...continued...                         │
│  • Skill        │                                          │
│                 │  Achievements                            │
│  CERTIFICATIONS │  ───────────────────────────────────────  │
│  ───────────── │  • Item                                  │
│  • Cert         │  • Item                                  │
│                 │                                          │
│  LANGUAGES      │                                          │
│  ───────────── │                                          │
│  English Native │                                          │
└─────────────────┴──────────────────────────────────────────┘
```

---

## Spacing

- **Page margins:** top 0.55in, bottom 0.55in, left 0.50in, right 0.60in
- **Between role blocks:** `\vspace{8pt}`
- **Bullet list:** `itemsep=2.5pt`, `parsep=0pt`, `topsep=4pt`
- **Between education entries:** `\vspace{6pt}`

---

## Sidebar Width Math

The eso-pic background must cover exactly the sidebar column without bleeding into the main column or leaving a gap:

```
left_margin (0.50in = 12.7mm)
+ sidebar_col (0.295 × (textwidth − columnsep) = 0.295 × 178.4mm ≈ 52.6mm)
+ half_sep (14pt / 2 ≈ 2.5mm)
= ~67.8mm → 67.8 / 210mm = 0.323 → round up to 0.327\paperwidth
```

**Use `0.327\paperwidth`** — do not change this unless the column ratio or margins change.

---

## Key Macros

```latex
%% Sidebar section header
\newcommand{\sidesection}[1]{%
  \vspace{8pt}%
  {\color{white}\footnotesize\bfseries\MakeUppercase{#1}}\\[-2pt]%
  {\color{crimson}\rule{\linewidth}{0.35pt}}\\[4pt]%
}

%% Sidebar skill category label
\newcommand{\sideskillcat}[1]{%
  \vspace{5pt}%
  {\color{white}\footnotesize\bfseries #1}\\[2pt]%
}

%% Sidebar skill item
\newcommand{\sideskillitem}[1]{%
  \hspace{5pt}{\color{crimson}\tiny\textbullet}\enspace{\color{sidesubtle}\footnotesize #1}\\[2.5pt]%
}

%% Main column section heading (paracol-safe — do NOT use \section)
\newcommand{\mainsection}[1]{%
  \vspace{10pt}%
  \noindent{\normalsize\bfseries\color{crimson}\MakeUppercase{#1}}%
  \vspace{-5pt}\par\noindent%
  {\color{crimson}\hrule height 0.5pt}%
  \vspace{5pt}%
}

%% Entry title: role line 1, company+dates line 2
\newcommand{\entrytitle}[4]{%
  \noindent
  \begin{tabularx}{\linewidth}{@{}X r@{}}
    \textbf{#1} & \textcolor{medgray}{\small #4}\\[1pt]
    \textcolor{medgray}{\small\itshape #2} & \textcolor{medgray}{\small #3}
  \end{tabularx}%
  \nopagebreak[4]%
}
```

---

## Page Flow

- NO forced `\newpage` mid-experience — let LaTeX flow naturally with paracol
- `\interlinepenalty=10000` — no bullet splits across pages
- `\widowpenalty=10000`, `\clubpenalty=10000` — no orphan lines
- `\nopagebreak[4]` after every `\entrytitle` — role header never stranded without first bullet

---

## Bullet Points

```latex
\setlist[itemize]{
  leftmargin = 1.2em,
  itemsep    = 2.5pt,
  parsep     = 0pt,
  topsep     = 4pt,
  label      = {\textcolor{crimson}{\small\textbullet}},
}
```

Crimson bullet dots only — not crimson text.

---

## Cover Letter Style

**Visual branding:**
- Same Helvetica font, same crimson accent, same link color as the resume
- Letterhead: name (18pt bold) + crimson subtitle + 2-line contact top-right (no photo)
- Thin light-grey rule beneath letterhead (ALWAYS in braces to prevent color leak)
- `\parskip{9pt}` for natural paragraph rhythm; no `\parindent`

**Letterhead structure:**
```latex
\begin{tabularx}{\linewidth}{@{}X r@{}}
  {\fontsize{18}{22}\selectfont\bfseries Name} &
  \begin{tabular}[t]{@{}r@{}}
    {\footnotesize phone | email}\\[-1pt]
    {\footnotesize linkedin}
  \end{tabular}\\[-2pt]
  {\small\bfseries\color{crimson} Title} &
  {\footnotesize Location}
\end{tabularx}
```

Use `\begin{tabular}[t]{@{}r@{}}` for the multi-line right cell — do NOT use `\\` inside a `{...}` group, it causes brace mismatch errors.

---

## Compilation

```bash
python compile.py            # compile + open PDFs
python compile.py --no-open  # compile only
```

Compiler: `pdflatex` via MiKTeX (Windows) or TeX Live (Mac/Linux).

If pdflatex not found on Windows:
```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
```
