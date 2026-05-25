#!/usr/bin/env python3
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
"""
tracker.py — Job Application Tracker
Manages SQLite database of all job applications.

Usage:
    python tracker.py add      — log a new application (interactive)
    python tracker.py list     — show all applications
    python tracker.py status   — update status of an application
    python tracker.py view 3   — view full details of application #3
    python tracker.py save     — save current resume_latest.pdf with a friendly name
"""

import sqlite3
import os
import re
import json
import shutil
from pathlib import Path
from datetime import date

ROOT    = Path(__file__).parent
DB_PATH = ROOT / "applications.db"
OUTPUTS = ROOT / "outputs"
SESSION = ROOT / "session.json"


# ── DB Setup ──────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            date_applied         TEXT    NOT NULL,
            company              TEXT    NOT NULL,
            role                 TEXT    NOT NULL,
            location             TEXT,
            contract_type        TEXT    DEFAULT 'Permanent',
            resume_filename      TEXT,
            resume_path          TEXT,
            coverletter_filename TEXT,
            jd_text              TEXT,
            ats_score            INTEGER,
            call_probability     INTEGER,
            status               TEXT    DEFAULT 'Applied',
            notes                TEXT,
            created_at           TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cols = [row[1] for row in conn.execute("PRAGMA table_info(applications)").fetchall()]
    if "coverletter_filename" not in cols:
        conn.execute("ALTER TABLE applications ADD COLUMN coverletter_filename TEXT")
    conn.commit()
    conn.close()


# ── Naming ────────────────────────────────────────────────────────────────────

def load_full_name() -> str:
    """Read full_name from session.json, fall back to empty string."""
    try:
        data = json.loads(SESSION.read_text(encoding="utf-8"))
        name = data.get("full_name", "").strip()
        if name and name != "First Last":
            return name
    except Exception:
        pass
    return ""


def clean(s: str, max_len: int = 30) -> str:
    s = s.strip()
    s = re.sub(r"[\s/\\&()\-]+", "_", s)
    s = re.sub(r"[^a-zA-Z0-9_]", "", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:max_len]


def name_prefix() -> str:
    """Returns 'First_Last_' or empty string if name not set."""
    full_name = load_full_name()
    if not full_name:
        return ""
    parts = full_name.split()
    return "_".join(clean(p, 20) for p in parts) + "_"


def make_filename(role: str, company: str, applied_date: str, prefix: str = "") -> str:
    """{FirstName}_{LastName}_{prefix}{Role}_{Company}_{YYYY-MM-DD}.pdf"""
    return f"{name_prefix()}{prefix}{clean(role, 30)}_{clean(company, 20)}_{applied_date}.pdf"


def save_resume(role: str, company: str, applied_date: str) -> str | None:
    """Copy resume_latest.pdf to a friendly-named archive."""
    src = OUTPUTS / "resume_latest.pdf"
    if not src.exists():
        print("  No resume_latest.pdf found — run compile.py first.")
        return None
    filename = make_filename(role, company, applied_date)
    dest = OUTPUTS / filename
    shutil.copy2(src, dest)
    print(f"  Resume saved      → {dest.name}")
    return filename


def save_coverletter(role: str, company: str, applied_date: str) -> str | None:
    """Copy coverletter_latest.pdf to a friendly-named archive."""
    src = OUTPUTS / "coverletter_latest.pdf"
    if not src.exists():
        print("  No coverletter_latest.pdf found — compile cover letter first.")
        return None
    filename = make_filename(role, company, applied_date, prefix="CoverLetter_")
    dest = OUTPUTS / filename
    shutil.copy2(src, dest)
    print(f"  Cover letter saved → {dest.name}")
    return filename


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_add():
    print("\n── Add New Application ─────────────────────────────")
    company       = input("  Company name     : ").strip()
    role          = input("  Role / Title     : ").strip()
    location      = input("  Location         : ").strip() or "Not specified"
    contract_type = input("  Type [Permanent/Contract/Freelance] (Enter=Permanent): ").strip() or "Permanent"
    applied_date  = input(f"  Date applied     [{date.today()}]: ").strip() or str(date.today())
    ats_score     = input("  ATS score (0-100, Enter to skip): ").strip() or None
    call_prob     = input("  Call probability % (Enter to skip): ").strip() or None
    notes         = input("  Notes            : ").strip()

    print("\n  Paste job description below.")
    print("  Type END on a new line when done:")
    jd_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        jd_lines.append(line)
    jd_text = "\n".join(jd_lines)

    resume_filename = save_resume(role, company, applied_date)
    resume_path     = str(OUTPUTS / resume_filename) if resume_filename else None
    cl_filename     = save_coverletter(role, company, applied_date)

    conn = get_db()
    conn.execute("""
        INSERT INTO applications
            (date_applied, company, role, location, contract_type,
             resume_filename, resume_path, coverletter_filename,
             jd_text, ats_score, call_probability, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (applied_date, company, role, location, contract_type,
          resume_filename, resume_path, cl_filename,
          jd_text or None,
          int(ats_score) if ats_score else None,
          int(call_prob)  if call_prob  else None,
          notes or None))
    conn.commit()
    row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()

    print(f"\n  ✓ Application #{row_id} logged for {role} @ {company}")
    print(f"    Resume      : {resume_filename or 'not saved'}")
    print(f"    Cover letter: {cl_filename or 'not saved'}")
    print(f"    Status      : Applied\n")


def cmd_list():
    conn = get_db()
    rows = conn.execute("""
        SELECT id, date_applied, company, role, contract_type,
               status, ats_score, call_probability, resume_filename
        FROM applications ORDER BY date_applied DESC
    """).fetchall()
    conn.close()

    if not rows:
        print("\n  No applications logged yet. Run: python tracker.py add\n")
        return

    print(f"\n{'ID':>3}  {'Date':<12} {'Company':<22} {'Role':<30} {'Type':<12} {'Status':<14} {'ATS':>4} {'Call%':>6}")
    print("─" * 105)
    for r in rows:
        ats  = f"{r['ats_score']}%"  if r['ats_score']        else "—"
        prob = f"{r['call_probability']}%" if r['call_probability'] else "—"
        print(f"{r['id']:>3}  {r['date_applied']:<12} {r['company']:<22} {r['role']:<30} "
              f"{r['contract_type']:<12} {r['status']:<14} {ats:>4} {prob:>6}")
    print(f"\n  {len(rows)} application(s) total.\n")


def cmd_status():
    cmd_list()
    try:
        row_id = int(input("  Enter application ID to update: ").strip())
    except ValueError:
        print("  Invalid ID."); return

    print("\n  Status options:")
    statuses = ["Applied", "Screening Call", "Interview Scheduled",
                "Interview Done", "Offer Received", "Offer Accepted",
                "Rejected", "Withdrawn", "No Response"]
    for i, s in enumerate(statuses, 1):
        print(f"    {i}. {s}")

    try:
        choice = int(input("  Choose (1-9): ").strip())
        new_status = statuses[choice - 1]
    except (ValueError, IndexError):
        print("  Invalid choice."); return

    notes = input("  Add a note (Enter to skip): ").strip()

    conn = get_db()
    if notes:
        conn.execute("""
            UPDATE applications
            SET status = ?, notes = COALESCE(notes || ' | ', '') || ?
            WHERE id = ?
        """, (new_status, notes, row_id))
    else:
        conn.execute("UPDATE applications SET status = ? WHERE id = ?",
                     (new_status, row_id))
    conn.commit()
    conn.close()
    print(f"\n  ✓ Application #{row_id} updated → {new_status}\n")


def cmd_view(row_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (row_id,)
    ).fetchone()
    conn.close()

    if not row:
        print(f"\n  No application with ID {row_id}\n"); return

    print(f"""
── Application #{row['id']} ──────────────────────────────────────────
  Company       : {row['company']}
  Role          : {row['role']}
  Location      : {row['location']}
  Type          : {row['contract_type']}
  Date Applied  : {row['date_applied']}
  Status        : {row['status']}
  ATS Score     : {f"{row['ats_score']}%" if row['ats_score'] else '—'}
  Call Prob.    : {f"{row['call_probability']}%" if row['call_probability'] else '—'}
  Resume file   : {row['resume_filename'] or '—'}
  Cover letter  : {row['coverletter_filename'] or '—'}
  Notes         : {row['notes'] or '—'}
  Logged at     : {row['created_at']}

── Job Description ───────────────────────────────────────────────────
{row['jd_text'] or '(not saved)'}
──────────────────────────────────────────────────────────────────────
""")


def cmd_save():
    """Save resume_latest.pdf with a friendly name without a full add."""
    role    = input("  Role / Title  : ").strip()
    company = input("  Company name  : ").strip()
    applied = input(f"  Date [{date.today()}]: ").strip() or str(date.today())
    save_resume(role, company, applied)
    save_coverletter(role, company, applied)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    init_db()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"

    if cmd == "add":
        cmd_add()
    elif cmd == "list":
        cmd_list()
    elif cmd == "status":
        cmd_status()
    elif cmd == "view":
        if len(sys.argv) < 3:
            print("Usage: python tracker.py view <id>"); return
        cmd_view(int(sys.argv[2]))
    elif cmd == "save":
        cmd_save()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
