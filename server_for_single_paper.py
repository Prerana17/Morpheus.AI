# Benchmark suite tool

@mcp.tool()
def run_benchmark_suite(
    papers_dir: str = "/Users/prerana/Desktop/morpheus/papers", 
    max_auto_fix_attempts: int = 3
) -> Dict[str, Any]:
    """
    Run the full Morpheus MCP pipeline sequentially on all PDF files
    in a directory. Failures are isolated per paper.

    ALWAYS produces:
    - run folder per paper
    - evaluation.json per paper
    - global benchmark_summary.json
    """

    papers_path = Path(papers_dir).expanduser()
    if not papers_path.exists() or not papers_path.is_dir():
        return {"ok": False, "error": f"Papers directory not found: {papers_dir}"}

    pdf_files = sorted(papers_path.glob("*.pdf"))
    if not pdf_files:
        return {"ok": False, "error": "No PDF files found in papers directory"}

    benchmark_results = []

    for idx, pdf_path in enumerate(pdf_files, start=1):
        paper_result = {
            "paper": pdf_path.name,
            "index": idx,
            "status": "started",
            "run_id": None,
        }

        try:
            # -------------------------------------------------
            # 1. Initialize pipeline
            # -------------------------------------------------
            init_res = pdf_to_morpheus_pipeline(str(pdf_path))
            if not init_res.get("ok"):
                raise RuntimeError(init_res.get("error"))

            run_id = init_res["run_id"]
            paper_result["run_id"] = run_id

            # -------------------------------------------------
            # 2. Attempt Morpheus run (XML expected externally)
            # -------------------------------------------------
            run_xml = _run_dir(run_id) / "model.xml"
            if run_xml.exists():
                run_res = run_morpheus(str(run_xml), run_id)
            else:
                run_res = {
                    "status": "skipped",
                    "message": "model.xml not present; waiting for agent-generated XML"
                }

            # -------------------------------------------------
            # 3. Auto-fix attempt (optional)
            # -------------------------------------------------
            attempts = 0
            while (
                run_res.get("status") == "error"
                and attempts < max_auto_fix_attempts
            ):
                attempts += 1
                auto_fix_and_rerun(run_id)
                run_res = run_morpheus(str(run_xml), run_id)

            paper_result["morpheus_status"] = run_res.get("status", "unknown")

        except Exception as e:
            paper_result["status"] = "pipeline_error"
            paper_result["error"] = str(e)

        finally:
            # -------------------------------------------------
            # 4. Evaluation ALWAYS runs
            # -------------------------------------------------
            if paper_result.get("run_id"):
                eval_res = evaluation(paper_result["run_id"])
                paper_result["evaluation"] = {
                    "total_score": eval_res.get("total_score"),
                    "evaluation_path": eval_res.get("evaluation_path"),
                }
            else:
                paper_result["evaluation"] = None

            paper_result["status"] = "completed"
            benchmark_results.append(paper_result)

    # -------------------------------------------------
    # Global benchmark summary
    # -------------------------------------------------
    summary_path = RUNS_ROOT / "benchmark_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "papers_processed": len(benchmark_results),
                "results": benchmark_results,
            },
            indent=2
        ),
        encoding="utf-8"
    )

    return {
        "ok": True,
        "papers_processed": len(benchmark_results),
        "benchmark_summary": str(summary_path),
        "results": benchmark_results,
        "message": "Benchmark suite completed. All papers processed sequentially."
    }



# whole backup file #




import sys
print("Using Python:", sys.executable, file=sys.stderr)

import os
import re
import json
import uuid
import enum
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
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
MORPHEUS_BIN = os.getenv("MORPHEUS_BIN", "morpheus")

MAX_STDOUT_CHARS = 20000
MAX_STDERR_CHARS = 20000

mcp = FastMCP(
    name="morpheus-mcp",
    host="0.0.0.0",
    port=0,
    stateless_http=True,
)

# -----------------------
# Reference config
# -----------------------
REFERENCES_ROOT = Path(__file__).parent / "references"

REFERENCE_CATEGORIES = {
    "CPM": REFERENCES_ROOT / "CPM",
    "PDE": REFERENCES_ROOT / "PDE",
    "ODE": REFERENCES_ROOT / "ODE",
    "Multiscale": REFERENCES_ROOT / "Multiscale",
    "Miscellaneous": REFERENCES_ROOT / "Miscellaneous",
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
    tiffs = sorted([p.name for p in run_path.rglob("*.tif")])
    dots = sorted([p.name for p in run_path.rglob("*.dot")])
    return {"png": pngs, "csv": csvs, "log": logs, "xml": xmls, "tiff": tiffs, "dot": dots}

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

def _infer_reference_categories_from_text(text: str) -> Dict[str, Any]:
    """
    Infer Morpheus reference categories from paper text.
    Returns both raw scores and selected categories.
    """
    t = text.lower()
    scores = {
        "CPM": 0,
        "PDE": 0,
        "ODE": 0,
        "Multiscale": 0,
    }

    cpm_keywords = [
        "cellular potts", "cpm", "adhesion", "contact energy",
        "volume constraint", "surface constraint", "cell sorting"
    ]
    scores["CPM"] += sum(k in t for k in cpm_keywords)

    pde_keywords = [
        "reaction-diffusion", "diffusion equation", "chemotaxis",
        "morphogen", "concentration field", "gradient"
    ]
    scores["PDE"] += sum(k in t for k in pde_keywords)

    ode_keywords = [
        "ordinary differential equation", "ode",
        "kinetic model", "rate equation", "temporal dynamics"
    ]
    scores["ODE"] += sum(k in t for k in ode_keywords)

    multiscale_keywords = [
        "multiscale", "coupled model", "hybrid model",
        "cell-field interaction", "feedback loop"
    ]
    scores["Multiscale"] += sum(k in t for k in multiscale_keywords)

    selected = [k for k, v in scores.items() if v > 0]
    if not selected:
        selected = ["Miscellaneous"]

    return {
        "scores": scores,
        "selected_categories": selected
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


# -----------------------
# XML Validation Helpers
# -----------------------

def _validate_xml_completeness(xml: str) -> Dict[str, Any]:
    """
    Validate that XML has all required sections for proper Morpheus output.
    Returns validation results with warnings and errors.
    """
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "has_analysis": False,
        "has_gnuplotter": False,
        "has_logger": False,
        "has_model_graph": False,
        "has_time_config": False,
        "has_cell_types": False,
        "has_space": False,
        "graph_generation_ready": False,
    }
    
    # Check basic structure
    if "<MorpheusModel" not in xml:
        results["valid"] = False
        results["errors"].append("Missing <MorpheusModel> root element")
        return results
    
    if "</MorpheusModel>" not in xml:
        results["valid"] = False
        results["errors"].append("Missing </MorpheusModel> closing tag")
        return results
    
    # Check for Space
    if "<Space>" in xml:
        results["has_space"] = True
    else:
        results["warnings"].append("Missing <Space> section - spatial domain not defined")
    
    # Check for Time configuration
    if "<Time>" in xml:
        results["has_time_config"] = True
        if "<StopTime" not in xml:
            results["warnings"].append("Missing <StopTime> - simulation may not run properly")
        if "<SaveInterval" not in xml:
            results["warnings"].append("Missing <SaveInterval> - outputs may not be generated at regular intervals")
    else:
        results["warnings"].append("Missing <Time> section - time configuration not defined")
    
    # Check for CellTypes
    if "<CellTypes>" in xml and "<CellType" in xml:
        results["has_cell_types"] = True
    else:
        results["warnings"].append("Missing <CellTypes> section - no cells defined")
    
    # Check for Analysis section (CRITICAL for graph generation)
    if "<Analysis>" in xml:
        results["has_analysis"] = True
        
        # Check for Gnuplotter (generates PNG graphs)
        if "<Gnuplotter" in xml:
            results["has_gnuplotter"] = True
            # Check for Plot elements
            if "<Plot>" in xml or "<Plot " in xml:
                results["graph_generation_ready"] = True
            else:
                results["warnings"].append("Gnuplotter found but no <Plot> elements - no graphs will be generated")
        else:
            results["warnings"].append("CRITICAL: No <Gnuplotter> in Analysis - NO PNG GRAPHS WILL BE GENERATED")
        
        # Check for Logger (generates CSV data)
        if "<Logger" in xml:
            results["has_logger"] = True
        else:
            results["warnings"].append("No <Logger> in Analysis - no CSV data output")
        
        # Check for ModelGraph
        if "<ModelGraph" in xml:
            results["has_model_graph"] = True
    else:
        results["valid"] = False
        results["errors"].append("CRITICAL: Missing <Analysis> section - NO OUTPUTS WILL BE GENERATED")
        results["errors"].append("You MUST include <Analysis> with <Gnuplotter> and <Logger> for graph generation")
    
    # Final graph readiness check
    if not results["has_gnuplotter"]:
        results["graph_generation_ready"] = False
        results["errors"].append("XML will NOT generate PNG graphs without <Gnuplotter> section")
    
    return results


def _get_analysis_template() -> str:
    """
    Return a template Analysis section that agents can use.
    """
    return '''
    <Analysis>
        <!-- Gnuplotter generates PNG images of the simulation -->
        <Gnuplotter time-step="100" decorate="true">
            <Terminal name="png"/>
            <Plot title="Cell Visualization">
                <Cells value="cell.type" min="0" max="2">
                    <ColorMap>
                        <Color value="0" color="white"/>
                        <Color value="1" color="red"/>
                        <Color value="2" color="blue"/>
                    </ColorMap>
                </Cells>
            </Plot>
        </Gnuplotter>
        
        <!-- Logger generates CSV data files -->
        <Logger time-step="100">
            <Input>
                <Symbol symbol-ref="cellcount"/>
            </Input>
            <Output>
                <TextOutput/>
            </Output>
        </Logger>
        
        <!-- ModelGraph generates DOT file of model structure -->
        <ModelGraph reduced="false" include-tags="#untagged"/>
    </Analysis>
'''


# Evaluation helpers (not MCP tools)
def _count_xml_errors(run_path: Path) -> int:
    err_file = run_path / "model.xml.err"
    if not err_file.exists():
        return 0
    return len([
        line for line in err_file.read_text(errors="ignore").splitlines()
        if line.strip()
    ])


def _extract_times(out_text: str) -> List[float]:
    times = []
    for line in out_text.splitlines():
        if line.startswith("Time:"):
            try:
                times.append(float(line.split("Time:")[1].strip()))
            except Exception:
                continue
    return times


def _extract_stop_time(xml_text: str) -> Optional[float]:
    match = re.search(r"<StopTime\s+value=\"([0-9.]+)\"", xml_text)
    if match:
        return float(match.group(1))
    return None


# -----------------------
# Benchmark State Management
# -----------------------

class PaperState(str, enum.Enum):
    PENDING = "pending"
    PDF_PROCESSED = "pdf_processed"
    REFERENCES_LOADED = "references_loaded"
    XML_GENERATED = "xml_generated"
    MORPHEUS_RUN = "morpheus_run"
    EVALUATED = "evaluated"
    FAILED = "failed"


def _get_benchmark_state_path() -> Path:
    return RUNS_ROOT / "benchmark_state.json"


def _load_benchmark_state() -> Dict[str, Any]:
    state_path = _get_benchmark_state_path()
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {"papers": {}, "current_index": 0}


def _save_benchmark_state(state: Dict[str, Any]) -> None:
    state_path = _get_benchmark_state_path()
    state_path.write_text(json.dumps(state, indent=2))


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
def list_references(category: Optional[str] = None) -> Dict[str, Any]:
    """
    List available Morpheus reference files.
    Optionally filter by category (CPM, PDE, ODE, Multiscale, Miscellaneous).
    """
    results = {}

    categories = (
        {category: REFERENCE_CATEGORIES.get(category)}
        if category
        else REFERENCE_CATEGORIES
    )

    for cat, path in categories.items():
        if not path or not path.exists():
            continue
        results[cat] = sorted([
            p.name for p in path.iterdir()
            if p.is_file() and p.suffix in {".xml", ".txt"}
        ])

    return {
        "ok": True,
        "categories": results
    }


@mcp.tool()
def read_reference(
    category: str,
    name: str,
    max_chars: int = 20000
) -> Dict[str, Any]:
    """
    Read a Morpheus reference document or example XML
    from a specific category folder.
    """
    if category not in REFERENCE_CATEGORIES:
        return {
            "ok": False,
            "error": f"Unknown category: {category}. "
                     f"Valid categories: {list(REFERENCE_CATEGORIES.keys())}"
        }

    refs_dir = REFERENCE_CATEGORIES[category]
    path = (refs_dir / name).resolve()

    if not path.exists() or not path.is_file():
        return {"ok": False, "error": f"Reference not found: {category}/{name}"}

    # Safety: ensure no path traversal
    if refs_dir not in path.parents:
        return {"ok": False, "error": "Invalid reference path"}

    text = _read_text(path, limit=max_chars)
    
    # Also validate the reference to show what sections it has
    validation = _validate_xml_completeness(text)
    
    return {
        "ok": True,
        "category": category,
        "name": name,
        "path": str(path),
        "content": text,
        "reference_has_gnuplotter": validation["has_gnuplotter"],
        "reference_has_logger": validation["has_logger"],
        "reference_has_analysis": validation["has_analysis"],
        "tip": "Copy the <Analysis> section from this reference to ensure graph generation!"
    }


@mcp.tool()
def suggest_references(run_id: str) -> Dict[str, Any]:
    run_path = _run_dir(run_id)
    paper_path = run_path / "paper.txt"

    if not paper_path.exists():
        return {"ok": False, "error": "paper.txt not found for this run"}

    text = _read_text(paper_path, limit=50000)

    inference = _infer_reference_categories_from_text(text)
    scores = inference["scores"]
    categories = inference["selected_categories"]

    available = {
        cat: sorted([
            p.name for p in REFERENCE_CATEGORIES[cat].iterdir()
            if p.is_file()
        ])
        for cat in categories if cat in REFERENCE_CATEGORIES
    }

    # Store metadata
    _write_metadata(run_id, {
        "reference_inference": {
            "scores": scores,
            "selected_categories": categories
        }
    })

    return {
        "ok": True,
        "suggested_categories": categories,
        "scores": scores,
        "available_references": available,
        "message": "Reference categories inferred from paper text.",
        "important": "When loading references, pay attention to the <Analysis> section - you MUST include Gnuplotter for PNG generation!"
    }


@mcp.tool()
def validate_xml(xml_content: str) -> Dict[str, Any]:
    """
    Validate Morpheus XML for completeness before saving.
    Checks for required sections including Analysis/Gnuplotter for graph generation.
    
    Call this BEFORE save_benchmark_xml to ensure your XML will generate outputs.
    """
    xml = _sanitize_xml(xml_content)
    validation = _validate_xml_completeness(xml)
    
    return {
        "ok": validation["valid"],
        "graph_generation_ready": validation["graph_generation_ready"],
        "errors": validation["errors"],
        "warnings": validation["warnings"],
        "sections_found": {
            "Analysis": validation["has_analysis"],
            "Gnuplotter": validation["has_gnuplotter"],
            "Logger": validation["has_logger"],
            "ModelGraph": validation["has_model_graph"],
            "Time": validation["has_time_config"],
            "CellTypes": validation["has_cell_types"],
            "Space": validation["has_space"],
        },
        "analysis_template": _get_analysis_template() if not validation["has_analysis"] else None,
        "message": (
            "XML is ready for graph generation!" 
            if validation["graph_generation_ready"] 
            else "XML is MISSING required sections for graph generation. See errors and use the analysis_template."
        )
    }


@mcp.tool()
def get_analysis_template() -> Dict[str, Any]:
    """
    Get a template Analysis section that you can add to your XML.
    This template includes Gnuplotter, Logger, and ModelGraph configurations
    that are REQUIRED for generating PNG graphs and CSV outputs.
    """
    return {
        "ok": True,
        "template": _get_analysis_template(),
        "explanation": {
            "Gnuplotter": "Generates PNG images at specified time-step intervals. REQUIRED for graphs.",
            "Logger": "Generates CSV data files. Useful for quantitative analysis.",
            "ModelGraph": "Generates DOT file showing model structure.",
        },
        "usage": "Copy this <Analysis> section into your XML before </MorpheusModel>"
    }


@mcp.tool()
def generate_xml_from_text(
    model_xml: str,
    run_id: Optional[str] = None,
    file_name: str = "model.xml"
) -> Dict[str, Any]:
    """
    Save Morpheus XML generated by the agent.
    Performs validation checks including Analysis section for graph generation.
    """
    xml = _sanitize_xml(model_xml)

    if not _looks_like_morpheus_xml(xml):
        return {
            "ok": False,
            "error": "Provided XML does not look like a valid MorpheusModel document"
        }
    
    # Validate XML completeness
    validation = _validate_xml_completeness(xml)
    
    # Save the XML regardless, but include warnings
    result = save_model_xml(
        xml_content=xml,
        run_id=run_id,
        file_name=file_name
    )
    
    if result.get("ok"):
        result["validation"] = validation
        result["graph_generation_ready"] = validation["graph_generation_ready"]
        
        if not validation["has_gnuplotter"]:
            result["critical_warning"] = (
                "XML saved but NO GRAPHS WILL BE GENERATED! "
                "Missing <Gnuplotter> in <Analysis> section. "
                "Use get_analysis_template() and add it to your XML."
            )
        
        if validation["errors"]:
            result["validation_errors"] = validation["errors"]
        if validation["warnings"]:
            result["validation_warnings"] = validation["warnings"]
    
    return result


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

    cmd = [
        MORPHEUS_BIN,
        "--file",
        run_xml.name,
        "--outdir",
        str(run_path),
        "--model-graph",
        "dot"
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
    
    # Check if graphs were actually generated
    png_count = len(outputs.get("png", []))
    csv_count = len(outputs.get("csv", []))

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
        "png_count": png_count,
        "csv_count": csv_count,
        "graphs_generated": png_count > 0,
        "message": (
            f"Morpheus run completed successfully. Generated {png_count} PNG graphs and {csv_count} CSV files."
            if success
            else "Morpheus run failed or timed out"
        ),
        "warning": (
            None if png_count > 0 
            else "NO PNG GRAPHS GENERATED! Check if your XML has <Gnuplotter> in <Analysis> section."
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
    outputs = _list_outputs(run_path)
    
    return {
        "ok": True,
        "run_id": run_id,
        "run_dir": str(run_path),
        "stdout": _read_text(stdout_path, limit=MAX_STDOUT_CHARS),
        "stderr": _read_text(stderr_path, limit=MAX_STDERR_CHARS),
        "outputs": outputs,
        "png_count": len(outputs.get("png", [])),
        "csv_count": len(outputs.get("csv", [])),
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
    
    # Read current XML and validate
    current_xml = _read_text(xml_path)
    validation = _validate_xml_completeness(current_xml)

    return {
        "ok": True,
        "run_id": run_id,
        "xml_path": str(xml_path),
        "current_xml": current_xml,
        "stdout": stdout,
        "stderr": stderr,
        "validation": validation,
        "instruction": (
            "Fix the Morpheus XML based on stderr. "
            "IMPORTANT: Ensure you have <Analysis> with <Gnuplotter> for graph generation! "
            "Return ONLY corrected XML."
        ),
        "analysis_template": _get_analysis_template() if not validation["has_gnuplotter"] else None,
    }


@mcp.tool()
def pdf_to_morpheus_pipeline(pdf_path: str) -> Dict[str, Any]:
    """
    End-to-end initializer:
    PDF → text extraction → reference suggestion.
    Prepares a run for reference-grounded XML generation.
    """
    # Step 1: read PDF
    pdf_res = read_pdf(pdf_path)
    if not pdf_res.get("ok"):
        return pdf_res

    run_id = pdf_res["run_id"]

    # Step 2: suggest relevant reference categories
    ref_suggestions = suggest_references(run_id)
    if not ref_suggestions.get("ok"):
        return ref_suggestions

    return {
        "ok": True,
        "run_id": run_id,
        "run_dir": pdf_res["run_dir"],
        "paper_text": pdf_res["text_path"],
        "suggested_reference_categories": ref_suggestions["suggested_categories"],
        "available_references": ref_suggestions["available_references"],
        "next_steps": [
            "Use list_references(category) to explore examples",
            "Load relevant example XML files using read_reference(category, name)",
            "IMPORTANT: Copy the <Analysis> section from references for graph generation!",
            "Generate Morpheus XML grounded in those examples",
            "Call validate_xml() to check your XML before saving",
            "Call generate_xml_from_text",
            "Then call run_morpheus"
        ],
        "message": (
            "PDF processed successfully. "
            "Relevant Morpheus reference categories have been suggested. "
            "Load example XML files before generating the model."
        ),
    }


@mcp.tool()
def evaluation(run_id: str) -> Dict[str, Any]:
    """
    Evaluate a Morpheus run based on execution artifacts and
    store the results as evaluation.json in the run directory.
    """
    run_path = _run_dir(run_id)

    xml_path = run_path / "model.xml"
    out_path = run_path / "model.xml.out"
    eval_json_path = run_path / "evaluation.json"
    eval_txt_path = run_path / "evaluation.txt"

    score = 0
    breakdown: Dict[str, Any] = {}

    try:
        # -------------------------------------------------
        # 1. XML error penalty (best score = 0)
        # -------------------------------------------------
        error_count = _count_xml_errors(run_path)
        breakdown["xml_error_count"] = error_count
        breakdown["xml_error_penalty"] = -error_count
        score -= error_count

        # -------------------------------------------------
        # 2. Model graph existence check
        # -------------------------------------------------
        graph_files = list(run_path.rglob("model_graph.dot"))
        has_graph = len(graph_files) > 0
        breakdown["model_graph_present"] = has_graph
        breakdown["model_graph_files"] = [str(p.name) for p in graph_files]

        if has_graph:
            score += 1

        # -------------------------------------------------
        # 3. Time-step progression check
        # -------------------------------------------------
        if out_path.exists():
            out_text = out_path.read_text(errors="ignore")
            times = _extract_times(out_text)
        else:
            times = []

        breakdown["time_steps_detected"] = len(times)

        if len(times) > 5:
            score += 1
            breakdown["time_step_score"] = 1
        else:
            breakdown["time_step_score"] = 0

        # -------------------------------------------------
        # 4. Metadata presence check
        # -------------------------------------------------
        meta_path = run_path / "metadata.json"
        has_metadata = meta_path.exists()

        breakdown["metadata_present"] = has_metadata
        if has_metadata:
            score += 1

        # -------------------------------------------------
        # 5. Result file generation check (CRITICAL)
        # -------------------------------------------------
        outputs = _list_outputs(run_path)
        png_files = outputs.get("png", [])
        csv_files = outputs.get("csv", [])
        
        has_png = len(png_files) > 0
        has_csv = len(csv_files) > 0
        has_results = has_png or has_csv

        breakdown["results_generated"] = has_results
        breakdown["png_files"] = png_files
        breakdown["png_count"] = len(png_files)
        breakdown["csv_files"] = csv_files
        breakdown["csv_count"] = len(csv_files)

        if has_results:
            score += 1
        
        # Bonus for having many graphs
        if len(png_files) >= 10:
            score += 1
            breakdown["many_graphs_bonus"] = 1
        else:
            breakdown["many_graphs_bonus"] = 0
        
        # -------------------------------------------------
        # 6. XML Analysis section check
        # -------------------------------------------------
        if xml_path.exists():
            xml_content = xml_path.read_text(errors="ignore")
            validation = _validate_xml_completeness(xml_content)
            breakdown["xml_has_analysis"] = validation["has_analysis"]
            breakdown["xml_has_gnuplotter"] = validation["has_gnuplotter"]
            breakdown["xml_has_logger"] = validation["has_logger"]
            
            if validation["has_gnuplotter"]:
                score += 1
                breakdown["gnuplotter_bonus"] = 1
            else:
                breakdown["gnuplotter_bonus"] = 0
                breakdown["missing_gnuplotter_warning"] = "XML missing Gnuplotter - this is why no graphs were generated!"

    except Exception as e:
        # Capture catastrophic failure without aborting evaluation
        breakdown["evaluation_exception"] = str(e)
        breakdown["evaluation_failed"] = True

    finally:
        # -------------------------------------------------
        # Final evaluation object (ALWAYS CREATED)
        # -------------------------------------------------
        evaluation_result = {
            "run_id": run_id,
            "total_score": score,
            "max_possible_score": 7,  # Updated max score
            "breakdown": breakdown,
            "timestamp": datetime.now().isoformat(),
        }

        eval_json_path.write_text(
            json.dumps(evaluation_result, indent=2),
            encoding="utf-8"
        )

        eval_txt_path.write_text(
            (
                f"Run ID: {run_id}\n"
                f"Total Score: {score}/7\n\n"
                f"XML Errors: {breakdown.get('xml_error_count', 'N/A')}\n"
                f"Model Graph Present: {breakdown.get('model_graph_present', False)}\n"
                f"Time Steps Detected: {breakdown.get('time_steps_detected', 0)}\n"
                f"Metadata Present: {breakdown.get('metadata_present', False)}\n"
                f"Results Generated: {breakdown.get('results_generated', False)}\n"
                f"PNG Count: {breakdown.get('png_count', 0)}\n"
                f"CSV Count: {breakdown.get('csv_count', 0)}\n"
                f"Has Gnuplotter: {breakdown.get('xml_has_gnuplotter', False)}\n"
                f"Many Graphs Bonus: {breakdown.get('many_graphs_bonus', 0)}\n"
            ),
            encoding="utf-8"
        )

    return {
        "ok": True,
        "run_id": run_id,
        "total_score": score,
        "max_possible_score": 7,
        "evaluation_path": str(eval_json_path),
        "evaluation_txt_path": str(eval_txt_path),
        "breakdown": breakdown,
        "message": "Evaluation completed and saved to evaluation.json",
        "graph_warning": (
            None if breakdown.get("png_count", 0) > 0
            else "NO PNG GRAPHS GENERATED! Ensure XML has <Gnuplotter> in <Analysis> section."
        )
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


@mcp.tool()
def run_benchmark_suite(
    papers_dir: str = "/Users/prerana/Desktop/morpheus/papers",
    max_auto_fix_attempts: int = 3
) -> Dict[str, Any]:
    """
    Run the full Morpheus MCP pipeline sequentially on all PDF files
    in a directory. Failures are isolated per paper.

    ALWAYS produces:
    - run folder per paper
    - evaluation.json per paper
    - global benchmark_summary.json
    
    NOTE: This is the OLD batch tool. For better results, use the new
    state-machine based tools: init_benchmark, get_next_paper, etc.
    """

    papers_path = Path(papers_dir).expanduser()
    if not papers_path.exists() or not papers_path.is_dir():
        return {"ok": False, "error": f"Papers directory not found: {papers_dir}"}

    pdf_files = sorted(papers_path.glob("*.pdf"))
    if not pdf_files:
        return {"ok": False, "error": "No PDF files found in papers directory"}

    benchmark_results = []

    for idx, pdf_path in enumerate(pdf_files, start=1):
        paper_result = {
            "paper": pdf_path.name,
            "index": idx,
            "status": "started",
            "run_id": None,
        }

        try:
            # -------------------------------------------------
            # 1. Initialize pipeline
            # -------------------------------------------------
            init_res = pdf_to_morpheus_pipeline(str(pdf_path))
            if not init_res.get("ok"):
                raise RuntimeError(init_res.get("error"))

            run_id = init_res["run_id"]
            paper_result["run_id"] = run_id

            # -------------------------------------------------
            # 2. Attempt Morpheus run (XML expected externally)
            # -------------------------------------------------
            run_xml = _run_dir(run_id) / "model.xml"
            if run_xml.exists():
                run_res = run_morpheus(str(run_xml), run_id)
            else:
                run_res = {
                    "status": "skipped",
                    "message": "model.xml not present; waiting for agent-generated XML"
                }

            # -------------------------------------------------
            # 3. Auto-fix attempt (optional)
            # -------------------------------------------------
            attempts = 0
            while (
                run_res.get("status") == "error"
                and attempts < max_auto_fix_attempts
            ):
                attempts += 1
                auto_fix_and_rerun(run_id)
                run_res = run_morpheus(str(run_xml), run_id)

            paper_result["morpheus_status"] = run_res.get("status", "unknown")

        except Exception as e:
            paper_result["status"] = "pipeline_error"
            paper_result["error"] = str(e)

        finally:
            # -------------------------------------------------
            # 4. Evaluation ALWAYS runs
            # -------------------------------------------------
            if paper_result.get("run_id"):
                eval_res = evaluation(paper_result["run_id"])
                paper_result["evaluation"] = {
                    "total_score": eval_res.get("total_score"),
                    "evaluation_path": eval_res.get("evaluation_path"),
                }
            else:
                paper_result["evaluation"] = None

            paper_result["status"] = "completed"
            benchmark_results.append(paper_result)

    # -------------------------------------------------
    # Global benchmark summary
    # -------------------------------------------------
    summary_path = RUNS_ROOT / "benchmark_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "timestamp": datetime.now().isoformat(),
                "papers_processed": len(benchmark_results),
                "results": benchmark_results,
            },
            indent=2
        ),
        encoding="utf-8"
    )

    return {
        "ok": True,
        "papers_processed": len(benchmark_results),
        "benchmark_summary": str(summary_path),
        "results": benchmark_results,
        "message": "Benchmark suite completed. All papers processed sequentially."
    }


# -----------------------
# NEW: Benchmark Orchestration Tools (State Machine)
# -----------------------

@mcp.tool()
def init_benchmark(papers_dir: str = "/Users/prerana/Desktop/morpheus/papers") -> Dict[str, Any]:
    """
    Initialize benchmark suite - discovers all PDFs and creates state tracker.
    Call this ONCE at the start of a benchmark run.
    
    This is the NEW recommended way to run benchmarks. It creates a state
    machine that tracks progress for each paper.
    """
    papers_path = Path(papers_dir).expanduser()
    if not papers_path.exists():
        return {"ok": False, "error": f"Directory not found: {papers_dir}"}

    pdf_files = sorted(papers_path.glob("*.pdf"))
    if not pdf_files:
        return {"ok": False, "error": "No PDF files found"}

    state = {
        "papers": {
            pdf.name: {
                "path": str(pdf),
                "state": PaperState.PENDING.value,
                "run_id": None,
                "error": None,
                "suggested_categories": [],
                "available_references": {},
            }
            for pdf in pdf_files
        },
        "current_index": 0,
        "total_papers": len(pdf_files),
        "started_at": datetime.now().isoformat(),
    }

    _save_benchmark_state(state)

    return {
        "ok": True,
        "total_papers": len(pdf_files),
        "papers": list(state["papers"].keys()),
        "message": "Benchmark initialized. Call `get_next_paper` to start processing.",
        "critical_reminder": (
            "When generating XML, you MUST include <Analysis> section with <Gnuplotter> "
            "to generate PNG graphs. Use get_analysis_template() if needed."
        )
    }


@mcp.tool()
def get_next_paper() -> Dict[str, Any]:
    """
    Get the next paper that needs processing.
    Returns paper info and what step is needed next.
    
    This is the main orchestration tool - it tells you exactly what to do next.
    """
    state = _load_benchmark_state()

    if not state.get("papers"):
        return {
            "ok": False,
            "error": "No benchmark initialized. Call init_benchmark first."
        }

    for paper_name, paper_info in state["papers"].items():
        paper_state = paper_info["state"]

        if paper_state == PaperState.PENDING.value:
            return {
                "ok": True,
                "paper": paper_name,
                "path": paper_info["path"],
                "current_state": paper_state,
                "next_action": "process_pdf",
                "instruction": f"Call `process_benchmark_paper('{paper_info['path']}')`",
            }

        elif paper_state == PaperState.PDF_PROCESSED.value:
            return {
                "ok": True,
                "paper": paper_name,
                "run_id": paper_info["run_id"],
                "current_state": paper_state,
                "next_action": "load_references",
                "suggested_categories": paper_info.get("suggested_categories", []),
                "available_references": paper_info.get("available_references", {}),
                "instruction": (
                    f"Load references using `read_reference(category, name)` for the suggested categories. "
                    f"PAY ATTENTION to the <Analysis> section in references - you need it for graphs! "
                    f"Then call `mark_references_loaded('{paper_info['run_id']}')`"
                ),
            }

        elif paper_state == PaperState.REFERENCES_LOADED.value:
            run_path = _run_dir(paper_info["run_id"])
            paper_text_path = run_path / "paper.txt"
            paper_text = _read_text(paper_text_path, limit=5000) if paper_text_path.exists() else ""
            
            return {
                "ok": True,
                "paper": paper_name,
                "run_id": paper_info["run_id"],
                "current_state": paper_state,
                "next_action": "generate_xml",
                "paper_text_preview": paper_text,
                "instruction": (
                    "Generate Morpheus XML based on paper text and references you loaded. "
                    "CRITICAL: Your XML MUST include <Analysis> section with <Gnuplotter> for PNG generation! "
                    "Use validate_xml() to check before saving. "
                    f"Then call `save_benchmark_xml(run_id='{paper_info['run_id']}', xml_content=...)`"
                ),
                "analysis_template": _get_analysis_template(),
                "xml_requirements": [
                    "Must have <MorpheusModel> root with version attribute",
                    "Must have <Description>",
                    "Must have <Space> with <Lattice>",
                    "Must have <Time> with <StartTime>, <StopTime>, <SaveInterval>",
                    "Must have <CellTypes> with at least one <CellType>",
                    "MUST have <Analysis> with <Gnuplotter> for PNG graphs!",
                    "Should have <Logger> for CSV output",
                ]
            }

        elif paper_state == PaperState.XML_GENERATED.value:
            return {
                "ok": True,
                "paper": paper_name,
                "run_id": paper_info["run_id"],
                "current_state": paper_state,
                "next_action": "run_morpheus",
                "instruction": f"Call `run_benchmark_morpheus('{paper_info['run_id']}')`",
            }

        elif paper_state == PaperState.MORPHEUS_RUN.value:
            return {
                "ok": True,
                "paper": paper_name,
                "run_id": paper_info["run_id"],
                "current_state": paper_state,
                "next_action": "evaluate",
                "instruction": f"Call `evaluate_benchmark_paper('{paper_info['run_id']}')`",
            }

        # Skip EVALUATED and FAILED papers
        elif paper_state in [PaperState.EVALUATED.value, PaperState.FAILED.value]:
            continue

    # All papers processed
    return {
        "ok": True,
        "all_complete": True,
        "message": "All papers have been processed. Call `get_benchmark_summary` for results.",
    }


@mcp.tool()
def process_benchmark_paper(pdf_path: str) -> Dict[str, Any]:
    """
    Step 1: Process a single paper's PDF and extract text.
    Updates benchmark state.
    """
    state = _load_benchmark_state()
    paper_name = Path(pdf_path).name

    if paper_name not in state["papers"]:
        return {"ok": False, "error": f"Paper not in benchmark: {paper_name}"}

    # Process PDF
    pdf_res = read_pdf(pdf_path)
    if not pdf_res.get("ok"):
        state["papers"][paper_name]["state"] = PaperState.FAILED.value
        state["papers"][paper_name]["error"] = pdf_res.get("error")
        _save_benchmark_state(state)
        return pdf_res

    run_id = pdf_res["run_id"]

    # Suggest references
    ref_res = suggest_references(run_id)

    # Update state
    state["papers"][paper_name]["run_id"] = run_id
    state["papers"][paper_name]["state"] = PaperState.PDF_PROCESSED.value
    state["papers"][paper_name]["suggested_categories"] = ref_res.get("suggested_categories", [])
    state["papers"][paper_name]["available_references"] = ref_res.get("available_references", {})
    _save_benchmark_state(state)

    return {
        "ok": True,
        "paper": paper_name,
        "run_id": run_id,
        "run_dir": pdf_res["run_dir"],
        "text_preview": pdf_res.get("text_preview", "")[:1500],
        "suggested_categories": ref_res.get("suggested_categories", []),
        "available_references": ref_res.get("available_references", {}),
        "next_step": (
            "Load relevant references using read_reference(). "
            "IMPORTANT: Study the <Analysis> section - you'll need <Gnuplotter> for graphs! "
            "Then call mark_references_loaded()"
        ),
    }


@mcp.tool()
def mark_references_loaded(run_id: str) -> Dict[str, Any]:
    """
    Step 2: Mark that references have been loaded for a paper.
    Call this after you've read the relevant reference files.
    """
    state = _load_benchmark_state()

    for paper_name, paper_info in state["papers"].items():
        if paper_info.get("run_id") == run_id:
            state["papers"][paper_name]["state"] = PaperState.REFERENCES_LOADED.value
            _save_benchmark_state(state)
            return {
                "ok": True,
                "paper": paper_name,
                "run_id": run_id,
                "next_step": (
                    "Generate Morpheus XML based on paper and references. "
                    "CRITICAL: Include <Analysis> with <Gnuplotter> for PNG graphs! "
                    "Then call save_benchmark_xml()"
                ),
                "analysis_template": _get_analysis_template(),
            }

    return {"ok": False, "error": f"Run ID not found: {run_id}"}


@mcp.tool()
def save_benchmark_xml(run_id: str, xml_content: str) -> Dict[str, Any]:
    """
    Step 3: Save generated XML for a benchmark paper.
    Validates XML and updates state to XML_GENERATED.
    
    IMPORTANT: Your XML MUST have <Analysis> section with <Gnuplotter> for graph generation!
    """
    state = _load_benchmark_state()

    # Find paper by run_id
    paper_name = None
    for name, info in state["papers"].items():
        if info.get("run_id") == run_id:
            paper_name = name
            break

    if not paper_name:
        return {"ok": False, "error": f"Run ID not found: {run_id}"}

    # Validate XML first
    xml = _sanitize_xml(xml_content)
    validation = _validate_xml_completeness(xml)
    
    # Reject XML without Gnuplotter - this is the key fix!
    if not validation["has_gnuplotter"]:
        return {
            "ok": False,
            "error": "XML REJECTED: Missing <Gnuplotter> in <Analysis> section!",
            "reason": "Without <Gnuplotter>, Morpheus will NOT generate any PNG graphs.",
            "validation": validation,
            "analysis_template": _get_analysis_template(),
            "instruction": (
                "Add the <Analysis> section with <Gnuplotter> to your XML and try again. "
                "Use the analysis_template provided above."
            )
        }

    # Save XML
    save_res = generate_xml_from_text(model_xml=xml_content, run_id=run_id)
    if not save_res.get("ok"):
        state["papers"][paper_name]["state"] = PaperState.FAILED.value
        state["papers"][paper_name]["error"] = save_res.get("error")
        _save_benchmark_state(state)
        return save_res

    state["papers"][paper_name]["state"] = PaperState.XML_GENERATED.value
    state["papers"][paper_name]["xml_path"] = save_res.get("xml_path")
    state["papers"][paper_name]["xml_validation"] = validation
    _save_benchmark_state(state)

    return {
        "ok": True,
        "paper": paper_name,
        "run_id": run_id,
        "xml_path": save_res.get("xml_path"),
        "validation": validation,
        "graph_generation_ready": validation["graph_generation_ready"],
        "next_step": f"Run Morpheus: call run_benchmark_morpheus('{run_id}')",
    }


@mcp.tool()
def run_benchmark_morpheus(run_id: str, max_fix_attempts: int = 3) -> Dict[str, Any]:
    """
    Step 4: Run Morpheus for a benchmark paper with auto-fix attempts.
    """
    state = _load_benchmark_state()

    paper_name = None
    for name, info in state["papers"].items():
        if info.get("run_id") == run_id:
            paper_name = name
            break

    if not paper_name:
        return {"ok": False, "error": f"Run ID not found: {run_id}"}

    run_path = _run_dir(run_id)
    xml_path = run_path / "model.xml"

    if not xml_path.exists():
        return {"ok": False, "error": "model.xml not found - generate XML first"}

    # Run Morpheus
    run_res = run_morpheus(str(xml_path), run_id)

    state["papers"][paper_name]["state"] = PaperState.MORPHEUS_RUN.value
    state["papers"][paper_name]["morpheus_result"] = {
        "status": run_res.get("status"),
        "returncode": run_res.get("returncode"),
        "ok": run_res.get("ok"),
        "png_count": run_res.get("png_count", 0),
        "csv_count": run_res.get("csv_count", 0),
    }
    _save_benchmark_state(state)

    return {
        "ok": run_res.get("ok", False),
        "paper": paper_name,
        "run_id": run_id,
        "status": run_res.get("status"),
        "outputs": run_res.get("outputs", {}),
        "png_count": run_res.get("png_count", 0),
        "csv_count": run_res.get("csv_count", 0),
        "graphs_generated": run_res.get("graphs_generated", False),
        "stdout_preview": run_res.get("stdout", "")[:500],
        "stderr_preview": run_res.get("stderr", "")[:500],
        "next_step": f"Evaluate: call evaluate_benchmark_paper('{run_id}')",
        "warning": run_res.get("warning"),
    }


@mcp.tool()
def evaluate_benchmark_paper(run_id: str) -> Dict[str, Any]:
    """
    Step 5: Run evaluation for a benchmark paper.
    """
    state = _load_benchmark_state()

    paper_name = None
    for name, info in state["papers"].items():
        if info.get("run_id") == run_id:
            paper_name = name
            break

    if not paper_name:
        return {"ok": False, "error": f"Run ID not found: {run_id}"}

    eval_res = evaluation(run_id)

    state["papers"][paper_name]["state"] = PaperState.EVALUATED.value
    state["papers"][paper_name]["evaluation"] = {
        "total_score": eval_res.get("total_score"),
        "max_possible_score": eval_res.get("max_possible_score"),
        "breakdown": eval_res.get("breakdown"),
    }
    _save_benchmark_state(state)

    return {
        "ok": True,
        "paper": paper_name,
        "run_id": run_id,
        "total_score": eval_res.get("total_score"),
        "max_possible_score": eval_res.get("max_possible_score"),
        "breakdown": eval_res.get("breakdown"),
        "next_step": "Call get_next_paper() to process the next paper",
        "graph_warning": eval_res.get("graph_warning"),
    }


@mcp.tool()
def get_benchmark_summary() -> Dict[str, Any]:
    """
    Get summary of entire benchmark run.
    """
    state = _load_benchmark_state()

    if not state.get("papers"):
        return {"ok": False, "error": "No benchmark data found"}

    summary = {
        "total_papers": len(state["papers"]),
        "completed": 0,
        "failed": 0,
        "pending": 0,
        "in_progress": 0,
        "scores": [],
        "total_pngs": 0,
        "total_csvs": 0,
        "papers": [],
    }

    for paper_name, info in state["papers"].items():
        paper_state = info["state"]

        if paper_state == PaperState.EVALUATED.value:
            summary["completed"] += 1
            score = info.get("evaluation", {}).get("total_score", 0)
            summary["scores"].append(score)
            
            # Count outputs
            breakdown = info.get("evaluation", {}).get("breakdown", {})
            summary["total_pngs"] += breakdown.get("png_count", 0)
            summary["total_csvs"] += breakdown.get("csv_count", 0)
            
        elif paper_state == PaperState.FAILED.value:
            summary["failed"] += 1
        elif paper_state == PaperState.PENDING.value:
            summary["pending"] += 1
        else:
            summary["in_progress"] += 1

        summary["papers"].append({
            "name": paper_name,
            "state": paper_state,
            "run_id": info.get("run_id"),
            "score": info.get("evaluation", {}).get("total_score") if paper_state == PaperState.EVALUATED.value else None,
            "png_count": info.get("evaluation", {}).get("breakdown", {}).get("png_count", 0) if paper_state == PaperState.EVALUATED.value else None,
            "error": info.get("error"),
        })

    if summary["scores"]:
        summary["average_score"] = sum(summary["scores"]) / len(summary["scores"])
        summary["max_score"] = max(summary["scores"])
        summary["min_score"] = min(summary["scores"])

    # Save summary
    summary_path = RUNS_ROOT / "benchmark_summary.json"
    summary["timestamp"] = datetime.now().isoformat()
    summary_path.write_text(json.dumps(summary, indent=2))

    return {
        "ok": True,
        **summary,
        "summary_path": str(summary_path),
    }


@mcp.tool()
def get_benchmark_state() -> Dict[str, Any]:
    """
    Get the current state of the benchmark (for debugging/inspection).
    """
    state = _load_benchmark_state()
    return {
        "ok": True,
        "state": state,
    }


@mcp.tool()
def reset_benchmark() -> Dict[str, Any]:
    """
    Reset/clear the benchmark state to start fresh.
    Does NOT delete run folders, only clears the state tracker.
    """
    state_path = _get_benchmark_state_path()
    if state_path.exists():
        state_path.unlink()

    return {
        "ok": True,
        "message": "Benchmark state cleared. Call init_benchmark() to start a new benchmark.",
    }


@mcp.tool()
def retry_failed_paper(paper_name: str) -> Dict[str, Any]:
    """
    Reset a failed paper to PENDING state so it can be reprocessed.
    """
    state = _load_benchmark_state()

    if paper_name not in state["papers"]:
        return {"ok": False, "error": f"Paper not found: {paper_name}"}

    state["papers"][paper_name]["state"] = PaperState.PENDING.value
    state["papers"][paper_name]["error"] = None
    state["papers"][paper_name]["run_id"] = None
    _save_benchmark_state(state)

    return {
        "ok": True,
        "paper": paper_name,
        "message": f"Paper '{paper_name}' reset to PENDING. Call get_next_paper() to process it.",
    }


# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    # stdio is what Claude Desktop expects for local MCP
    mcp.run(transport="stdio")