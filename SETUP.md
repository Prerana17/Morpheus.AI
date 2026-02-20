# Setup Guide

Detailed installation, configuration, and troubleshooting guide for the Morpheus Benchmark Runner.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [File Structure](#file-structure)
- [Output Structure](#output-structure)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [System Prompt](#system-prompt)

---

## Prerequisites

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.9+ | Runtime environment |
| Morpheus | 2.0+ | Biological simulation engine |
| pip | Latest | Package management |

### Python Packages

```
anthropic>=0.18.0
pypdf>=3.0.0
python-dotenv>=1.0.0
```

### Morpheus Installation

Morpheus must be installed and accessible from the command line:

| OS | Typical Path |
|----|--------------|
| macOS (Homebrew) | `/opt/homebrew/bin/morpheus-cli` |
| macOS (App) | `/Applications/Morpheus.app/Contents/MacOS/morpheus` |
| Linux | `/usr/local/bin/morpheus` |
| Windows | `C:\Program Files\Morpheus\morpheus.exe` |

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/Morpheus.AI.git
cd Morpheus.AI
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv

# Activate:
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

# Or manually:
pip install anthropic pypdf python-dotenv
```

### Step 4: Verify Morpheus

```bash
morpheus --version

# Or with full path:
/opt/homebrew/bin/morpheus-cli --version
```

---

## Configuration

### API Key

Configure your Anthropic API key using one of these methods:

#### Option 1: Environment Variable (Recommended)

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"
```

#### Option 2: .env File

Create `.env` in the project root:

```env
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

#### Option 3: Direct Configuration

Edit `run_benchmark.py`:

```python
ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"  # Line ~45
```

### Morpheus Path

Configure in `server.py`:

```python
MORPHEUS_BIN = os.getenv("MORPHEUS_BIN", "/opt/homebrew/bin/morpheus-cli")
```
### MCP-tools Path

Configure in `claude_desktop_config.json`:

```
"morpheus-mcp": {
      "command": "/Users/username/path_to_your_mcp_project/.venv/bin/python",
      "args": [
        "/Users/username/path_to_your_mcp_project/server.py"
      ],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "info"
      }
    }
  },
```

### Model Selection

Configure in `run_benchmark.py`:

```python
MODEL_NAME = "claude-sonnet-4-5/6-20250929"  # Line ~55
```

**Available models:**

| Model | Description |
|-------|-------------|
| `claude-sonnet-4-20250514` | Fast, capable (recommended) |
| `claude-sonnet-4-5/6-20250929` | Latest Sonnet 4.5 |
| `claude-opus-4.5/6-20250514` | Most capable (slower, expensive) |

### Other Settings

| Setting | Location | Default | Description |
|---------|----------|---------|-------------|
| `PAPERS_DIR` | run_benchmark.py | `./papers` | Directory containing PDFs |
| `MAX_PAPERS` | run_benchmark.py | `10` | Maximum papers to process |
| `MAX_ITERATIONS_PER_PAPER` | run_benchmark.py | `25` | Max iterations per paper |
| `RUNS_ROOT` | server.py | `./runs` | Output directory |

---

## File Structure

### Project Layout

```
morpheus-benchmark-runner/
├── server.py                 # MCP tool functions
├── run_benchmark.py          # Autonomous agent runner
├── requirements.txt          # Dependencies
├── .env                      # API key (optional)
├── README.md                 # Overview
├── SETUP.md                  # This file
│
├── references/               # Reference XML files
│   ├── CPM/
│   │   ├── CellSorting.xml
│   │   ├── CellMigration.xml
│   │   └── ...
│   ├── PDE/
│   ├── ODE/
│   ├── Multiscale/
│   └── Miscellaneous/
│
└── papers/                   # Input PDFs
    ├── paper1.pdf
    └── ...
```

---

## Output Structure

Each processed paper creates a run directory:

```
runs/
└── 20260129_183548_03941a64/     # timestamp_uuid
    ├── paper.txt                  # Extracted PDF text
    ├── model.xml                  # Generated MorpheusML
    ├── model.xml.out              # Morpheus stdout
    ├── model.xml.err              # Morpheus stderr
    ├── stdout.log                 # Execution log
    ├── stderr.log                 # Error log
    ├── model_graph.dot            # Dependency graph
    ├── evaluation.json            # Scoring results
    │
    ├── *.png                      # Visualization outputs
    └── *.csv                      # Data outputs
```

### Evaluation Report Example

```
============================================================
MORPHEUS EVALUATION REPORT
============================================================
Run ID: 20260129_183548_03941a64
Timestamp: 2026-01-29T18:40:15

TOTAL SCORE: 7 / 7 (100.0%)

------------------------------------------------------------
SCORING BREAKDOWN:
------------------------------------------------------------

1. XML/Stderr Errors: 0 (Score: 0)
2. Model Graph: Present (Score: 1/1)
3. Time Progression: 101 lines (Score: 3/3)
4. StopTime Match: 1000.0 = 1000.0 (Score: 1/1)
5. Result Files: 249 PNGs, 150 CSVs (Score: 1/1)
6. Bonus (10+ PNGs): Yes (Score: 1/1)

============================================================
```

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Morpheus not found | `command not found` | Set `MORPHEUS_BIN` path in `server.py` |
| Rate limit errors | `429 Too Many Requests` | Automatic retry handles this |
| No PNGs generated | `PNGs: 0` | Gnuplotter validation enforces this |
| API key error | `401 Unauthorized` | Check API key configuration |
| Import error | `ModuleNotFoundError` | Run `pip install -r requirements.txt` |

### Diagnostic Commands

```bash
# Check Morpheus installation
which morpheus
morpheus --version

# Check generated files
ls -la runs/<run_id>/

# Check simulation progress
cat runs/<run_id>/stdout.log | grep "Time:"

# Check for errors
cat runs/<run_id>/stderr.log

# Test XML manually
cd runs/<run_id>/
morpheus --file model.xml
```

### Debug Mode

Enable verbose logging in `run_benchmark.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## API Reference

### MCP Tools (server.py)

#### `pdf_to_morpheus_pipeline(pdf_path: str) -> Dict`

Extracts text from PDF and suggests reference categories.

**Returns:** `{run_id, paper_text, suggested_categories}`

---

#### `list_references(category: Optional[str]) -> Dict`

Lists available reference XML files.

**Parameters:**
- `category` — Filter by category (CPM, PDE, ODE, Multiscale, Miscellaneous)

**Returns:** `{categories, files}`

---

#### `read_reference(category: str, name: str, max_chars: int = 8000) -> Dict`

Loads reference XML content.

**Returns:** `{content, truncated}`

---

#### `generate_xml_from_text(model_xml: str, run_id: str, file_name: str = "model.xml") -> Dict`

Saves generated MorpheusML to run directory.

**Returns:** `{path, success}`

---

#### `run_morpheus(xml_path: str, run_id: str) -> Dict`

Executes Morpheus simulation.

**Returns:** `{success, stdout, stderr, output_files}`

---

#### `auto_fix_and_rerun(run_id: str) -> Dict`

Retrieves error details for failed runs.

**Returns:** `{errors, xml_content, suggestions}`

---

#### `evaluation(run_id: str) -> Dict`

Evaluates and scores run results.

**Returns:** `{score, breakdown, png_count, csv_count}`

---

#### `get_run_summary(run_id: str) -> Dict`

Retrieves run logs and file lists.

**Returns:** `{logs, files, status}`

---

#### `read_file_text(path: str, max_chars: int = 20000) -> Dict`

Reads text file content.

**Returns:** `{content, truncated}`

---

### Benchmark Classes (run_benchmark.py)

#### `PaperProcessor`

Processes individual papers using Claude as AI agent.

#### `BenchmarkRunner`

Orchestrates multi-paper processing and aggregates results.

#### `execute_tool(tool_name: str, tool_input: Dict) -> Dict`

Executes MCP tool functions locally.

---

## System Prompt

The agent behavior is controlled by `SYSTEM_PROMPT` in `run_benchmark.py`:

**Key instructions:**

- **Workflow enforcement** — Steps must be followed in order
- **Reference grounding** — XML must be based on official examples
- **Gnuplotter requirement** — `<Analysis>` section must be included
- **Error handling** — Maximum 2 fix attempts before proceeding
- **Evaluation mandate** — `evaluation()` must always be called
- **Completion signal** — "PAPER_COMPLETE" must be stated when done

---

## Cost Optimization

1. Use `claude-sonnet-4-20250514` for best cost/quality balance
2. Limit `max_chars` for reference reading (default: 8000)
3. Conversation truncation is enabled by default
4. Set appropriate `MAX_ITERATIONS_PER_PAPER` limit

---

## Comparison: Chat vs API

| Aspect | Chat Interface | Python API |
|--------|---------------|------------|
| Interaction | Manual | Fully autonomous |
| Continuity | May stop/pause | Continuous execution |
| Control | Limited | Full programmatic |
| Debugging | Difficult | Easy logging |
| Integration | Single session | CI/CD compatible |
| Scalability | One paper at a time | Batch processing |
| Reproducibility | Difficult | Fully reproducible |

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review [Morpheus documentation](https://morpheus.gitlab.io/)
3. Open an issue on GitHub
