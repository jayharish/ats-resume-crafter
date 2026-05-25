#!/usr/bin/env python3
"""
compile.py — Compile resume + cover letter to PDF, auto-rename archives.
Run after Claude Code writes the LaTeX files.

Usage:
    python compile.py
    python compile.py --no-open   (skip auto-opening PDFs)

Reads session.json for the friendly archive name (full_name, role, company, date).
Outputs:
    outputs/resume_latest.pdf
    outputs/coverletter_latest.pdf
    outputs/FirstName_LastName_{Role}_{Company}_{Date}.pdf
    outputs/FirstName_LastName_CoverLetter_{Role}_{Company}_{Date}.pdf
"""

import subprocess
import shutil
import sys
import os
import re
import json
from pathlib import Path
from datetime import date

# Force UTF-8 output so Unicode symbols render on any terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT    = Path(__file__).parent
OUTPUTS = ROOT / "outputs"
SESSION = ROOT / "session.json"


# ── Helpers ───────────────────────────────────────────────────────────────────

def find_compiler():
    for cmd in ["pdflatex", "xelatex", "lualatex"]:
        if shutil.which(cmd):
            return cmd
    return None


def clean_for_filename(s: str, max_len: int = 28) -> str:
    """Convert a string to a safe, readable filename segment."""
    s = s.strip()
    s = re.sub(r"[\s/\\&()\-]+", "_", s)
    s = re.sub(r"[^a-zA-Z0-9_]", "", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len]


def name_to_filename_prefix(full_name: str) -> str:
    """'Jane Smith' → 'Jane_Smith_'"""
    if not full_name or full_name.strip() == "First Last":
        return ""
    parts = full_name.strip().split()
    return "_".join(clean_for_filename(p, 20) for p in parts) + "_"


def make_friendly_name(prefix: str, role: str, company: str, applied_date: str,
                       cl: bool = False) -> str:
    """FirstName_LastName_{CoverLetter_}{Role}_{Company}_{YYYY-MM-DD}.pdf"""
    cl_tag = "CoverLetter_" if cl else ""
    return (
        f"{prefix}"
        f"{cl_tag}"
        f"{clean_for_filename(role)}_"
        f"{clean_for_filename(company, max_len=20)}_"
        f"{applied_date}.pdf"
    )


def load_session() -> dict:
    try:
        return json.loads(SESSION.read_text(encoding="utf-8"))
    except Exception:
        return {}


def compile_tex(tex_path: Path, compiler: str) -> tuple[bool, str]:
    """Run compiler twice for proper layout. Returns (success, log_message)."""
    cmd = [
        compiler,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-output-directory", str(tex_path.parent),
        str(tex_path),
    ]
    for _ in range(2):  # Two passes for cross-refs
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

    pdf = tex_path.with_suffix(".pdf")
    if pdf.exists():
        size_kb = round(pdf.stat().st_size / 1024, 1)
        return True, f"  compiled  -> {pdf.name}  ({size_kb} KB)"
    else:
        log = tex_path.with_suffix(".log")
        errs = []
        if log.exists():
            for line in log.read_text(errors="ignore").splitlines():
                if line.startswith("!") or "Error" in line:
                    errs.append(line)
        return False, "  FAILED:\n" + "\n".join(errs[:15])


def archive_pdf(pdf: Path, friendly_name: str) -> str:
    """Copy pdf to a friendly-named archive in the same folder."""
    dest = pdf.parent / friendly_name
    shutil.copy2(pdf, dest)
    size_kb = round(dest.stat().st_size / 1024, 1)
    return f"  archived  -> {dest.name}  ({size_kb} KB)"


def open_pdf(pdf_path: Path) -> None:
    try:
        if sys.platform == "win32":
            os.startfile(str(pdf_path))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(pdf_path)])
        else:
            subprocess.Popen(["xdg-open", str(pdf_path)])
    except Exception:
        pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    auto_open = "--no-open" not in sys.argv

    print("=" * 62)
    print("  ats-resume-crafter -- PDF Compiler")
    print("=" * 62)

    session      = load_session()
    full_name    = session.get("full_name", "")
    role         = session.get("role", "")
    company      = session.get("company", "")
    applied_date = session.get("date_applied", str(date.today()))

    name_prefix = name_to_filename_prefix(full_name)

    if role and company:
        resume_archive = make_friendly_name(name_prefix, role, company, applied_date)
        cl_archive     = make_friendly_name(name_prefix, role, company, applied_date, cl=True)
        print(f"\n  Name     : {full_name or '(not set)'}")
        print(f"  Role     : {role}")
        print(f"  Company  : {company}")
        print(f"  Date     : {applied_date}")
    else:
        resume_archive = None
        cl_archive     = None
        print("\n  WARNING: session.json missing role/company -- skipping friendly rename.")
        print("           Update session.json with 'full_name', 'role', 'company', 'date_applied'.")

    compiler = find_compiler()
    if not compiler:
        print("\n  ERROR: No LaTeX compiler found on PATH.")
        print("  Install MiKTeX -> https://miktex.org/download")
        print("  Or TeX Live    -> https://tug.org/texlive/")
        sys.exit(1)

    print(f"\n  Compiler : {compiler}\n")

    # ── Compile resume ────────────────────────────────────────────
    resume_tex = OUTPUTS / "resume_latest.tex"
    if not resume_tex.exists():
        print(f"  ERROR: {resume_tex} not found -- generate LaTeX first.")
        sys.exit(1)

    print("  [RESUME]")
    ok, msg = compile_tex(resume_tex, compiler)
    print(msg)
    if ok and resume_archive:
        print(archive_pdf(OUTPUTS / "resume_latest.pdf", resume_archive))
    elif not ok:
        print("  Aborting -- fix resume errors first.")
        sys.exit(1)

    # ── Compile cover letter ──────────────────────────────────────
    cl_tex = OUTPUTS / "coverletter_latest.tex"
    if cl_tex.exists():
        print("\n  [COVER LETTER]")
        ok_cl, msg_cl = compile_tex(cl_tex, compiler)
        print(msg_cl)
        if ok_cl and cl_archive:
            print(archive_pdf(OUTPUTS / "coverletter_latest.pdf", cl_archive))
    else:
        print("\n  [COVER LETTER]  coverletter_latest.tex not found -- skipping.")

    print("\n" + "=" * 62)

    if auto_open:
        open_pdf(OUTPUTS / "resume_latest.pdf")

    sys.exit(0)


if __name__ == "__main__":
    main()
