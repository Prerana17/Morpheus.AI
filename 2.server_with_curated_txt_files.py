import sys
print("Using Python:", sys.executable, file=sys.stderr)

import os
import re
import json
import uuid
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from pypdf import PdfReader

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# -----------------------
# Config
# -----------------------
RUNS_ROOT = Path(os.getenv("MORPHEUS_RUNS_DIR", "/Users/prerana/Desktop/morpheus")).expanduser()
RUNS_ROOT.mkdir(parents=True, exist_ok=True)

# If Morpheus isn't in PATH, set MORPHEUS_BIN in env:
# /Applications/Morpheus.app/Contents/MacOS/morpheus-cli
MORPHEUS_BIN = os.getenv("MORPHEUS_BIN", "/Applications/Morpheus.app/Contents/MacOS/morpheus")

MAX_STDOUT_CHARS = 20000
MAX_STDERR_CHARS = 20000

mcp = FastMCP(
    name="morpheus-mcp",
    host="0.0.0.0",
    port=0,
    stateless_http=True,
)

# -----------------------
# Reference documents (consolidated)
# -----------------------
REFERENCE_DOCS = {
    "model_repository": Path(__file__).parent / "model_repository.txt",
    "model_template": Path(__file__).parent / "model_template.txt",
    "morpheusml_doc": Path(__file__).parent / "morpheusml_doc.txt",
}


# -----------------------
# Helpers
# -----------------------
def _looks_like_morpheus_xml(xml: str) -> bool:
    return (
        "<MorpheusModel" in xml
        and "</MorpheusModel>" in xml
        and "version=" in xml
    )

def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _new_run_id() -> str:
    return f"{_now_stamp()}_{uuid.uuid4().hex[:8]}"

def _run_dir(run_id: str) -> Path:
    d = RUNS_ROOT / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", errors="ignore")

def _read_text(path: Path, limit: int = 20000) -> str:
    if not path.exists():
        return ""
    txt = path.read_text(encoding="utf-8", errors="ignore")
    return txt[:limit]

def _sanitize_xml(xml: str) -> str:
    # remove common markdown fences if agent accidentally includes them
    xml = xml.strip()
    xml = re.sub(r"^\s*```xml\s*", "", xml, flags=re.IGNORECASE)
    xml = re.sub(r"\s*```\s*$", "", xml)
    return xml.strip()

def _list_outputs(run_path: Path) -> Dict[str, List[str]]:
    pngs = sorted([p.name for p in run_path.rglob("*.png")])
    csvs = sorted([p.name for p in run_path.rglob("*.csv")])
    logs = sorted([p.name for p in run_path.rglob("*.log")])
    xmls = sorted([p.name for p in run_path.rglob("*.xml")])
    return {"png": pngs, "csv": csvs, "log": logs, "xml": xmls}

def _run_cmd(cmd: List[str], cwd: Path) -> Dict[str, Any]:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout or "",
        "stderr": proc.stderr or "",
    }


def _write_metadata(run_id: str, data: Dict[str, Any]) -> None:
    run_path = _run_dir(run_id)
    meta_path = run_path / "metadata.json"

    if meta_path.exists():
        existing = json.loads(meta_path.read_text())
    else:
        existing = {}

    existing.update(data)
    meta_path.write_text(json.dumps(existing, indent=2))



def _count_xml_errors(run_path: Path) -> int:
    """
    Count the number of errors in model.xml.err file.
    Returns 0 if file doesn't exist or is empty.
    """
    err_path = run_path / "model.xml.err"
    
    if not err_path.exists():
        return 0
    
    err_text = err_path.read_text(errors="ignore").strip()
    
    if not err_text:
        return 0
    
    # Count error lines - each non-empty line is considered an error
    # You can adjust this logic based on actual error format
    error_lines = [line for line in err_text.split('\n') if line.strip()]
    
    # Also count specific error patterns
    error_patterns = [
        r'\[ERROR\]',
        r'\[FATAL\]',
        r'Error:',
        r'error:',
        r'Exception',
    ]
    
    error_count = 0
    for line in error_lines:
        for pattern in error_patterns:
            if re.search(pattern, line):
                error_count += 1
                break
        else:
            # If no specific pattern matched but line exists, still count it
            if line.strip():
                error_count += 1
    
    return error_count if error_count > 0 else len(error_lines)


def _check_model_graph(run_path: Path) -> Tuple[bool, List[str]]:
    """
    Check if model_graph.dot file exists in the run directory.
    Returns (exists: bool, list of found files).
    """
    graph_files = list(run_path.rglob("model_graph.dot"))
    has_graph = len(graph_files) > 0
    return has_graph, [str(p.name) for p in graph_files]


def _count_time_lines(out_path: Path) -> Tuple[int, List[float]]:
    """
    Count lines starting with "Time: " in model.xml.out AFTER "model is up".
    Returns (count, list of time values).
    
    The structure has 101 lines for a complete run:
    - Start Time: <0.0>
    - End Time: <StopTime>
    - 100 intervals = 101 lines starting with "Time: "
    """
    if not out_path.exists():
        return 0, []
    
    out_text = out_path.read_text(errors="ignore")
    lines = out_text.split('\n')
    
    # Find "model is up" marker to start counting after simulation begins
    model_up_index = -1
    for i, line in enumerate(lines):
        if "model is up" in line.lower():
            model_up_index = i
            break
    
    # Extract time values from lines after "model is up"
    time_values = []
    time_pattern = re.compile(r'^Time:\s*<?([\d.eE+-]+)>?', re.IGNORECASE)
    
    start_index = model_up_index + 1 if model_up_index >= 0 else 0
    
    for line in lines[start_index:]:
        match = time_pattern.match(line.strip())
        if match:
            try:
                time_val = float(match.group(1))
                time_values.append(time_val)
            except ValueError:
                continue
    
    return len(time_values), time_values


def _calculate_time_score(time_line_count: int) -> int:
    """
    Calculate score based on number of Time: lines.
    
    Scoring:
    - ==0:   score +0
    - ==1:   score +1
    - >1 and <101: score +2
    - ==101: score +3
    """
    if time_line_count == 0:
        return 0
    elif time_line_count == 1:
        return 1
    elif time_line_count > 1 and time_line_count < 101:
        return 2
    elif time_line_count >= 101:
        return 3
    else:
        return 0


def _extract_stop_time(xml_path: Path) -> Optional[float]:
    """
    Extract StopTime value from model.xml.
    Returns None if not found.
    """
    if not xml_path.exists():
        return None
    
    xml_text = xml_path.read_text(errors="ignore")
    
    # Pattern to match <StopTime value="X"/> or <StopTime>X</StopTime>
    patterns = [
        r'<StopTime\s+value\s*=\s*["\']?([\d.eE+-]+)["\']?\s*/?>',
        r'<StopTime[^>]*>([\d.eE+-]+)</StopTime>',
        r'stop_time\s*=\s*["\']?([\d.eE+-]+)["\']?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, xml_text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    
    return None


def _check_stop_time_match(stop_time: Optional[float], time_values: List[float], tolerance: float = 1e-6) -> bool:
    """
    Check if the last simulation time matches the StopTime.
    Returns True if they match within tolerance.
    """
    if stop_time is None or not time_values:
        return False
    
    last_time = time_values[-1]
    return abs(stop_time - last_time) < tolerance


def _list_outputs(run_path: Path) -> Dict[str, List[str]]:
    """
    List output files (png, csv) in the run directory.
    Returns dict with file types as keys and list of filenames as values.
    """
    outputs = {
        "png": [],
        "csv": [],
        "other": []
    }
    
    for ext, key in [(".png", "png"), (".csv", "csv")]:
        files = list(run_path.rglob(f"*{ext}"))
        outputs[key] = [str(f.name) for f in files]
    
    return outputs


# -----------------------
# MCP Tools
# -----------------------

@mcp.tool()
def read_pdf(pdf_path: str, run_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Read a PDF file and extract text.
    Saves extracted text into run folder as paper.txt
    """
    pdf_file = Path(pdf_path).expanduser()
    if not pdf_file.exists():
        return {"ok": False, "error": f"PDF not found: {pdf_path}"}

    if run_id is None:
        run_id = _new_run_id()

    run_path = _run_dir(run_id)

    reader = PdfReader(str(pdf_file))
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            continue

    full_text = "\n\n".join(text_parts).strip()
    if not full_text:
        return {"ok": False, "error": "No text could be extracted from PDF"}

    txt_path = run_path / "paper.txt"
    _write_text(txt_path, full_text)

    return {
        "ok": True,
        "run_id": run_id,
        "run_dir": str(run_path),
        "pdf_path": str(pdf_file),
        "text_path": str(txt_path),
        "text_preview": full_text[:2000],
    }
    
@mcp.tool()
def read_reference_doc(
    name: str,
    max_chars: int = 20000
) -> Dict[str, Any]:
    """
    Read a consolidated Morpheus reference document.

    Valid names:
    - model_repository
    - model_template
    - morpheusml_doc
    """
    if name not in REFERENCE_DOCS:
        return {
            "ok": False,
            "error": f"Unknown reference document: {name}. "
                     f"Valid options: {list(REFERENCE_DOCS.keys())}"
        }

    path = REFERENCE_DOCS[name]

    if not path.exists():
        return {"ok": False, "error": f"Reference file not found: {path}"}

    content = _read_text(path, limit=max_chars)

    return {
        "ok": True,
        "name": name,
        "path": str(path),
        "content": content,
    }

@mcp.tool()
def generate_xml_from_text(
    model_xml: str,
    run_id: Optional[str] = None,
    file_name: str = "model.xml"
) -> Dict[str, Any]:
    """
    Save Morpheus XML generated by the agent.
    Performs basic sanity checks before saving.
    """
    xml = _sanitize_xml(model_xml)

    if not _looks_like_morpheus_xml(xml):
        return {
            "ok": False,
            "error": "Provided XML does not look like a valid MorpheusModel document"
        }

    return save_model_xml(
        xml_content=xml,
        run_id=run_id,
        file_name=file_name
    )

@mcp.tool()
def create_run() -> Dict[str, Any]:
    """Create a new run folder and return run_id and paths."""
    run_id = _new_run_id()
    run_path = _run_dir(run_id)
    return {
        "run_id": run_id,
        "run_dir": str(run_path),
        "runs_root": str(RUNS_ROOT),
    }

@mcp.tool()
def save_model_xml(xml_content: str, run_id: Optional[str] = None, file_name: str = "model.xml") -> Dict[str, Any]:
    """Save model XML into the run folder. Returns file path."""
    xml_content = _sanitize_xml(xml_content)
    if not xml_content:
        return {"ok": False, "error": "xml_content is empty. Refusing to write empty XML."}

    if run_id is None:
        run_id = _new_run_id()

    run_path = _run_dir(run_id)
    xml_path = run_path / file_name
    _write_text(xml_path, xml_content)

    return {
        "ok": True,
        "run_id": run_id,
        "run_dir": str(run_path),
        "xml_path": str(xml_path),
        "file_name": file_name,
    }

@mcp.tool()
def run_morpheus(xml_path: str, run_id: Optional[str] = None) -> Dict[str, Any]:
    """
    GUARANTEED Morpheus execution:
    - runs morpheus model.xml
    - captures stdout/stderr
    - waits for completion
    - writes logs
    - never blocks MCP
    """

    xml_file = Path(xml_path).expanduser()
    if not xml_file.exists():
        return {"ok": False, "error": f"XML file not found: {xml_path}"}

    # Infer run_id safely
    if run_id is None:
        run_id = xml_file.parent.name

    run_path = _run_dir(run_id)

    # Ensure model.xml is inside run folder
    run_xml = run_path / "model.xml"
    if xml_file.resolve() != run_xml.resolve():
        shutil.copy2(xml_file, run_xml)

    stdout_path = run_path / "stdout.log"
    stderr_path = run_path / "stderr.log"

    # ABSOLUTE CLI PATH REQUIRED
    morpheus_bin = MORPHEUS_BIN

    cmd = [
        MORPHEUS_BIN,
        "--file",
        run_xml.name,
        "--outdir",
        str(run_path),
    #    "--model-graph",
    #    "dot"
    ]


    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(run_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ.copy(),
        )

        try:
            stdout, stderr = proc.communicate(timeout=600)  # 10 min hard cap
            timed_out = False
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            timed_out = True

    except Exception as e:
        _write_text(stderr_path, str(e))
        return {
            "ok": False,
            "status": "launch_error",
            "error": str(e),
            "run_id": run_id,
        }

    _write_text(stdout_path, stdout)
    _write_text(stderr_path, stderr)

    outputs = _list_outputs(run_path)

    success = (proc.returncode == 0) and not timed_out

    return {
        "ok": success,
        "status": "success" if success else "error",
        "timed_out": timed_out,
        "returncode": proc.returncode,
        "run_id": run_id,
        "run_dir": str(run_path),
        "xml_path": str(run_xml),
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
        "stdout": stdout[:MAX_STDOUT_CHARS],
        "stderr": stderr[:MAX_STDERR_CHARS],
        "outputs": outputs,
        "message": (
            "Morpheus run completed successfully"
            if success
            else "Morpheus run failed or timed out"
        ),
    }


@mcp.tool()
def run_xml_once(xml_content: str) -> Dict[str, Any]:
    """
    Convenience: create run folder, save xml, run Morpheus.
    Returns logs and outputs.
    """
    saved = save_model_xml(xml_content=xml_content)
    if not saved.get("ok"):
        return saved
    return run_morpheus(xml_path=saved["xml_path"], run_id=saved["run_id"])

@mcp.tool()
def get_run_summary(run_id: str) -> Dict[str, Any]:
    """Return logs and output file lists for a run."""
    run_path = _run_dir(run_id)
    stdout_path = run_path / "stdout.log"
    stderr_path = run_path / "stderr.log"
    return {
        "ok": True,
        "run_id": run_id,
        "run_dir": str(run_path),
        "stdout": _read_text(stdout_path, limit=MAX_STDOUT_CHARS),
        "stderr": _read_text(stderr_path, limit=MAX_STDERR_CHARS),
        "outputs": _list_outputs(run_path),
    }

@mcp.tool()
def read_file_text(path: str, max_chars: int = 20000) -> Dict[str, Any]:
    """Read any text file (logs, csv preview)."""
    p = Path(path).expanduser()
    if not p.exists():
        return {"ok": False, "error": f"File not found: {path}"}
    return {"ok": True, "path": str(p), "text": _read_text(p, limit=max_chars)}

@mcp.tool()
def auto_fix_and_rerun(run_id: str) -> Dict[str, Any]:
    """
    If Morpheus failed, return logs and XML so the agent can fix it.
    After agent fixes XML, this tool re-runs Morpheus.
    """
    run_path = _run_dir(run_id)
    xml_path = run_path / "model.xml"

    if not xml_path.exists():
        return {"ok": False, "error": "model.xml not found in run folder"}

    stderr = _read_text(run_path / "stderr.log")
    stdout = _read_text(run_path / "stdout.log")

    return {
        "ok": True,
        "run_id": run_id,
        "xml_path": str(xml_path),
        "stdout": stdout,
        "stderr": stderr,
        "instruction": (
            "Fix the Morpheus XML based on stderr. "
            "Return ONLY corrected XML."
        ),
    }

@mcp.tool()
def pdf_to_morpheus_pipeline(pdf_path: str) -> Dict[str, Any]:
    """
    PDF → text extraction.
    Reference documents are always available globally.
    """
    pdf_res = read_pdf(pdf_path)
    if not pdf_res.get("ok"):
        return pdf_res

    return {
        "ok": True,
        "run_id": pdf_res["run_id"],
        "run_dir": pdf_res["run_dir"],
        "paper_text": pdf_res["text_path"],
        "available_reference_docs": list(REFERENCE_DOCS.keys()),
        "next_steps": [
            "Read model_template for safe XML skeletons",
            "Read morpheusml_doc for valid tags and constraints",
            "Read model_repository for known modeling patterns",
            "Generate Morpheus XML",
            "Call generate_xml_from_text",
            "Then call run_morpheus"
        ],
        "message": (
            "PDF processed successfully. "
            "Use consolidated reference documents to guide model generation."
        ),
    }


# Evaluation tool new

@mcp.tool()
def evaluation(run_id: str) -> Dict[str, Any]:
    """
    Evaluate a Morpheus run based on execution artifacts and
    store the results as evaluation.json in the run directory.
    
    Scoring Criteria:
    1. XML errors in model.xml.err or stderr.log: negative score per error (best = 0)
    2. model_graph.dot exists: +1
    3. Time step progression (graduated scoring):
       - 0 lines:     +0
       - 1-10 lines:  +1
       - 11-50 lines: +2
       - 51+ lines:   +3
    4. StopTime matches last Time in output: +1
    5. Result files (png/csv) generated: +1
    6. BONUS: Many results generated (10+ PNGs): +1
    
    Maximum possible score: 7 (with 0 errors)
    """
    run_path = _run_dir(run_id)

    xml_path = run_path / "model.xml"
    stdout_path = run_path / "stdout.log"      # ← FIXED: Use stdout.log
    stderr_path = run_path / "stderr.log"      # ← FIXED: Use stderr.log
    eval_json_path = run_path / "evaluation.json"
    eval_txt_path = run_path / "evaluation.txt"

    score = 0
    breakdown: Dict[str, Any] = {}

    try:
        # -------------------------------------------------
        # 1. XML error penalty (best score = 0)
        #    Check stderr.log for errors
        # -------------------------------------------------
        error_count = 0
        if stderr_path.exists():
            stderr_content = stderr_path.read_text(errors="ignore").strip()
            if stderr_content:
                # Count error lines
                error_lines = [l for l in stderr_content.split('\n') if l.strip()]
                error_count = len(error_lines)
        
        breakdown["xml_error_count"] = error_count
        breakdown["xml_error_penalty"] = -error_count
        breakdown["stderr_file_exists"] = stderr_path.exists()
        score -= error_count

        # -------------------------------------------------
        # 2. Model graph existence check (+1 if exists)
        # -------------------------------------------------
        has_graph, graph_files = _check_model_graph(run_path)
        breakdown["model_graph_present"] = has_graph
        breakdown["model_graph_files"] = graph_files

        if has_graph:
            score += 1
            breakdown["model_graph_score"] = 1
        else:
            breakdown["model_graph_score"] = 0

        # -------------------------------------------------
        # 3. Time-step progression check (graduated scoring)
        #    Count lines starting with "Time:" in stdout.log
        # -------------------------------------------------
        time_line_count = 0
        time_values = []
        
        if stdout_path.exists():
            stdout_content = stdout_path.read_text(errors="ignore")
            # Find "model is up" marker
            model_up_idx = stdout_content.lower().find("model is up")
            if model_up_idx >= 0:
                # Only look at content after "model is up"
                after_model_up = stdout_content[model_up_idx:]
            else:
                after_model_up = stdout_content
            
            # Count Time: lines
            time_pattern = re.compile(r'Time:\s*<?(\d+\.?\d*)', re.IGNORECASE)
            for match in time_pattern.finditer(after_model_up):
                try:
                    time_values.append(float(match.group(1)))
                    time_line_count += 1
                except ValueError:
                    continue
        
        # Calculate time score with adjusted thresholds
        if time_line_count == 0:
            time_score = 0
        elif time_line_count <= 10:
            time_score = 1
        elif time_line_count <= 50:
            time_score = 2
        else:
            time_score = 3
        
        breakdown["time_lines_count"] = time_line_count
        breakdown["time_score"] = time_score
        breakdown["time_values_sample"] = time_values[:5] if time_values else []
        breakdown["last_time_value"] = time_values[-1] if time_values else None
        breakdown["stdout_file_exists"] = stdout_path.exists()
        
        score += time_score

        # -------------------------------------------------
        # 4. StopTime consistency check (+1 if matches)
        # -------------------------------------------------
        stop_time = _extract_stop_time(xml_path)
        last_time = time_values[-1] if time_values else None
        
        # Check if last time matches stop time (with tolerance)
        stop_time_match = False
        if stop_time is not None and last_time is not None:
            stop_time_match = abs(stop_time - last_time) < 1.0
        
        breakdown["stop_time"] = stop_time
        breakdown["last_simulation_time"] = last_time
        breakdown["stop_time_match"] = stop_time_match

        if stop_time_match:
            score += 1
            breakdown["stop_time_score"] = 1
        else:
            breakdown["stop_time_score"] = 0

        # -------------------------------------------------
        # 5. Result file generation check (+1 if png or csv exists)
        # -------------------------------------------------
        outputs = _list_outputs(run_path)
        png_count = len(outputs.get("png", []))
        csv_count = len(outputs.get("csv", []))
        has_png = png_count > 0
        has_csv = csv_count > 0
        has_results = has_png or has_csv

        breakdown["results_generated"] = has_results
        breakdown["has_png_files"] = has_png
        breakdown["has_csv_files"] = has_csv
        breakdown["png_files"] = outputs.get("png", [])[:20]  # Limit to first 20 for display
        breakdown["csv_files"] = outputs.get("csv", [])
        breakdown["png_count"] = png_count
        breakdown["csv_count"] = csv_count

        if has_results:
            score += 1
            breakdown["results_score"] = 1
        else:
            breakdown["results_score"] = 0

        # -------------------------------------------------
        # 6. BONUS: Many results generated (+1 if 10+ PNGs)
        # -------------------------------------------------
        if png_count >= 10:
            score += 1
            breakdown["bonus_many_results"] = 1
        else:
            breakdown["bonus_many_results"] = 0

    except Exception as e:
        breakdown["evaluation_exception"] = str(e)
        breakdown["evaluation_failed"] = True

    finally:
        # -------------------------------------------------
        # Calculate maximum possible score
        # -------------------------------------------------
        max_score = 7  # 0 errors + 1 graph + 3 time + 1 stoptime + 1 results + 1 bonus
        
        # -------------------------------------------------
        # Final evaluation object
        # -------------------------------------------------
        evaluation_result = {
            "run_id": run_id,
            "total_score": score,
            "max_possible_score": max_score,
            "score_percentage": round((score / max_score) * 100, 2) if max_score > 0 else 0,
            "breakdown": breakdown,
            "timestamp": datetime.now().isoformat(),
        }

        eval_json_path.write_text(
            json.dumps(evaluation_result, indent=2),
            encoding="utf-8"
        )

        # Create human-readable summary
        eval_txt_path.write_text(
            (
                f"{'='*60}\n"
                f"MORPHEUS EVALUATION REPORT\n"
                f"{'='*60}\n"
                f"Run ID: {run_id}\n"
                f"Timestamp: {datetime.now().isoformat()}\n"
                f"\n"
                f"TOTAL SCORE: {score} / {max_score} ({round((score / max_score) * 100, 2) if max_score > 0 else 0}%)\n"
                f"\n"
                f"{'-'*60}\n"
                f"SCORING BREAKDOWN:\n"
                f"{'-'*60}\n"
                f"\n"
                f"1. XML/Stderr Errors (penalty, best=0):\n"
                f"   - Error count: {breakdown.get('xml_error_count', 'N/A')}\n"
                f"   - Score: {breakdown.get('xml_error_penalty', 0)}\n"
                f"\n"
                f"2. Model Graph (model_graph.dot):\n"
                f"   - Present: {breakdown.get('model_graph_present', False)}\n"
                f"   - Files: {breakdown.get('model_graph_files', [])}\n"
                f"   - Score: {breakdown.get('model_graph_score', 0)} / 1\n"
                f"\n"
                f"3. Time Step Progression (from stdout.log):\n"
                f"   - Time lines count: {breakdown.get('time_lines_count', 0)}\n"
                f"   - Scoring: 0->+0, 1-10->+1, 11-50->+2, 51+->+3\n"
                f"   - Score: {breakdown.get('time_score', 0)} / 3\n"
                f"\n"
                f"4. StopTime Match:\n"
                f"   - StopTime in XML: {breakdown.get('stop_time', 'N/A')}\n"
                f"   - Last simulation time: {breakdown.get('last_simulation_time', 'N/A')}\n"
                f"   - Match: {breakdown.get('stop_time_match', False)}\n"
                f"   - Score: {breakdown.get('stop_time_score', 0)} / 1\n"
                f"\n"
                f"5. Result Files Generated:\n"
                f"   - PNG files: {breakdown.get('png_count', 0)}\n"
                f"   - CSV files: {breakdown.get('csv_count', 0)}\n"
                f"   - Score: {breakdown.get('results_score', 0)} / 1\n"
                f"\n"
                f"6. BONUS - Many Results (10+ PNGs):\n"
                f"   - Score: {breakdown.get('bonus_many_results', 0)} / 1\n"
                f"\n"
                f"{'='*60}\n"
            ),
            encoding="utf-8"
        )

    return {
        "ok": True,
        "run_id": run_id,
        "total_score": score,
        "max_possible_score": max_score,
        "score_percentage": round((score / max_score) * 100, 2) if max_score > 0 else 0,
        "evaluation_json_path": str(eval_json_path),
        "evaluation_txt_path": str(eval_txt_path),
        "breakdown": breakdown,
        "message": "Evaluation completed and saved to evaluation.json and evaluation.txt",
    }



@mcp.tool()
def run_full_pipeline(
    pdf_path: str,
    model_xml: Optional[str] = None
) -> Dict[str, Any]:
    """
    Full end-to-end pipeline:
    PDF → references → XML save → Morpheus run → evaluation (ALWAYS)
    """

    run_id = None
    morpheus_result = None
    eval_result = None

    try:
        # 1. PDF → text
        pdf_res = read_pdf(pdf_path)
        if not pdf_res.get("ok"):
            raise RuntimeError(pdf_res.get("error"))

        run_id = pdf_res["run_id"]

        # 2. Suggest references
        suggest_references(run_id)

        # 3. Save XML if provided
        if model_xml:
            save_res = generate_xml_from_text(
                model_xml=model_xml,
                run_id=run_id
            )
            if not save_res.get("ok"):
                raise RuntimeError(save_res.get("error"))

            # 4. Run Morpheus
            morpheus_result = run_morpheus(
                xml_path=save_res["xml_path"],
                run_id=run_id
            )
        else:
            morpheus_result = {
                "status": "skipped",
                "message": "No XML provided, Morpheus not run"
            }

    except Exception as e:
        morpheus_result = {
            "status": "pipeline_error",
            "error": str(e)
        }

    finally:
        # 5. EVALUATION ALWAYS RUNS
        if run_id:
            eval_result = evaluation(run_id)
        else:
            eval_result = {
                "ok": False,
                "error": "No run_id created, evaluation skipped"
            }

    return {
        "ok": True,
        "run_id": run_id,
        "morpheus": morpheus_result,
        "evaluation": eval_result,
        "message": "Pipeline finished. Evaluation executed regardless of failures."
    }

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    # stdio is what Claude Desktop expects for local MCP
    mcp.run(transport="stdio")
