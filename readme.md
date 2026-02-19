restore venv

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
 

# Morpheus Benchmark Runner

An autonomous pipeline for processing scientific papers and generating Morpheus biological simulations using Claude AI with MCP (Model Context Protocol) tools.

---


## Overview

The Morpheus Benchmark Runner enables Claude AI to be run with MCP tools entirely from Python code without any chat interface. This approach is known as **agentic tool use** with the Anthropic API.

Scientific papers (PDFs) are processed automatically, and corresponding Morpheus XML models are generated, executed, and evaluated. The entire pipeline is handled autonomously by Claude, with results including visualization graphs (PNGs) and data files (CSVs) being produced for each paper.

### What is Morpheus?

Morpheus is a modeling and simulation environment for multicellular systems biology. It is used for creating computational models of biological processes such as cell migration, tissue development, and pattern formation. Models are defined using MorpheusML, an XML-based modeling language.

### What is MCP?

The Model Context Protocol (MCP) is a standardized way to connect AI models to external tools and data sources. In this project, MCP tools are implemented as Python functions that Claude can call to interact with the Morpheus simulation environment.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MORPHEUS BENCHMARK RUNNER                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐      ┌─────────────────┐      ┌───────────────────┐   │
│  │   Claude    │      │   Tool Request  │      │   MCP Functions   │   │
│  │    API      │─────▶│   (tool_use)    │─────▶│   (server.py)     │   │
│  │             │◀─────│   Tool Result   │◀─────│                   │   │
│  └─────────────┘      └─────────────────┘      └───────────────────┘   │
│         │                                               │               │
│         │                                               ▼               │
│         │                                      ┌───────────────────┐   │
│         │                                      │     Morpheus      │   │
│         │                                      │    Simulator      │   │
│         │                                      └───────────────────┘   │
│         │                                               │               │
│         ▼                                               ▼               │
│  ┌─────────────┐                               ┌───────────────────┐   │
│  │  Benchmark  │                               │  Output Files     │   │
│  │   Results   │                               │  (PNG, CSV, XML)  │   │
│  └─────────────┘                               └───────────────────┘   │
│                                                                         │
│  The loop is repeated until completion is signaled by Claude            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Process Flow

1. The Claude API is called with tool definitions provided
2. A `tool_use` request is returned by Claude specifying which tool to execute
3. The requested tool is executed locally (MCP functions from `server.py`)
4. The `tool_result` is sent back to Claude
5. Steps 2-4 are repeated until "PAPER_COMPLETE" is signaled by Claude
6. The next paper is processed (steps 1-5 are repeated)
7. A final benchmark summary is generated upon completion of all papers

---

## Features

- **Autonomous Processing**: Papers are processed without manual intervention
- **Reference-Grounded Generation**: XML models are generated based on official Morpheus examples
- **Automatic Error Recovery**: Failed simulations are automatically diagnosed and fixed (up to 2 attempts)
- **Comprehensive Evaluation**: Each run is scored based on multiple criteria
- **Rate Limit Handling**: API rate limits are handled automatically with exponential backoff
- **Conversation Truncation**: Token usage is optimized by truncating long conversations
- **JSON Output**: Results are saved in structured JSON format for further analysis
- **Gnuplotter Validation**: XML is validated to ensure graph generation is properly configured

---

## Prerequisites

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.9+ | Runtime environment |
| Morpheus | 2.0+ | Biological simulation engine |
| pip | Latest | Package management |

### Python Packages

The following packages are required:

```
anthropic>=0.18.0
pypdf>=3.0.0
python-dotenv>=1.0.0
```

### Morpheus Installation

Morpheus must be installed and accessible from the command line. The installation path varies by operating system:

| OS | Typical Path |
|----|--------------|
| macOS (Homebrew) | `/opt/homebrew/bin/morpheus-cli` |
| macOS (App) | `/Applications/Morpheus.app/Contents/MacOS/morpheus` |
| Linux | `/usr/local/bin/morpheus` |
| Windows | `C:\Program Files\Morpheus\morpheus.exe` |

---

## Installation

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd morpheus-benchmark-runner
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install anthropic pypdf python-dotenv
```

### Step 4: Verify Morpheus Installation

```bash
# Check if Morpheus is accessible
morpheus --version

# Or with full path
/opt/homebrew/bin/morpheus-cli --version
```

---

## Configuration

### API Key

The Anthropic API key must be configured using one of the following methods:

#### Option 1: Environment Variable (Recommended)

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"
```

#### Option 2: .env File

A `.env` file can be created in the project directory:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

#### Option 3: Direct Configuration

The API key can be set directly in `run_benchmark.py`:

```python
ANTHROPIC_API_KEY = "sk-ant-api03-your-key-here"  # Line ~45
```

### Morpheus Path

The Morpheus binary path is configured in `server.py`:

```python
MORPHEUS_BIN = os.getenv("MORPHEUS_BIN", "/opt/homebrew/bin/morpheus-cli")
```

### Model Selection

The Claude model can be configured in `run_benchmark.py`:

```python
MODEL_NAME = "claude-sonnet-4.5-20250514"  # Line ~55
```

Available models:
- `claude-sonnet-4-20250514` - Recommended (fast, capable)
- `claude-sonnet-4-5-20250929` - Latest Sonnet 4.5
- `claude-opus-4-20250514` - Most capable (slower, more expensive)

### Other Settings

| Setting | Location | Default | Description |
|---------|----------|---------|-------------|
| `PAPERS_DIR` | run_benchmark.py | `/Users/prerana/Desktop/morpheus/papers` | Directory containing PDF papers |
| `MAX_PAPERS` | run_benchmark.py | `10` | Maximum papers to process |
| `MAX_ITERATIONS_PER_PAPER` | run_benchmark.py | `25` | Maximum Claude iterations per paper |
| `RUNS_ROOT` | server.py | `/Users/prerana/Desktop/morpheus` | Output directory for runs |

---

## File Structure

### Project Structure

```
morpheus-benchmark-runner/
├── server.py                 # MCP tool functions
├── run_benchmark.py          # Autonomous agent runner
├── .env                      # API key configuration (optional)
├── README.md                 # This documentation
│
├── references/               # Reference XML files (required)
│   ├── CPM/                  # Cellular Potts Model examples
│   │   ├── CellSorting.xml
│   │   ├── CellMigration.xml
│   │   └── ...
│   ├── PDE/                  # Partial Differential Equation examples
│   ├── ODE/                  # Ordinary Differential Equation examples
│   ├── Multiscale/           # Multiscale model examples
│   └── Miscellaneous/        # Other examples
│
└── papers/                   # Input PDF papers
    ├── paper1.pdf
    ├── paper2.pdf
    └── ...
```

### Output Structure

For each processed paper, a run directory is created:

```
/Users/prerana/Desktop/morpheus/
├── 20260129_183548_03941a64/           # Run directory (timestamp_uuid)
│   ├── paper.txt                        # Extracted text from PDF
│   ├── model.xml                        # Generated Morpheus model
│   ├── metadata.json                    # Run metadata
│   ├── stdout.log                       # Morpheus stdout output
│   ├── stderr.log                       # Morpheus stderr output
│   ├── model_graph.dot                  # Model dependency graph
│   ├── evaluation.json                  # Evaluation results (JSON)
│   ├── evaluation.txt                   # Evaluation results (human-readable)
│   ├── logger.csv                       # Data output from Logger
│   ├── plot-1_00000.png                 # Visualization frame 1
│   ├── plot-1_00010.png                 # Visualization frame 2
│   └── ...                              # Additional output files
│
├── 20260129_184542_f876ef8f/           # Another run directory
│   └── ...
│
└── benchmark_results.json               # Overall benchmark summary
```

---

## Usage

### Basic Usage

The benchmark is executed by running:

```bash
python run_benchmark.py
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--papers-dir` | Directory containing PDF papers | Value in config |
| `--max-papers` | Maximum number of papers to process | `10` |
| `--model` | Claude model to be used | `claude-sonnet-4.5-20250514` |
| `--api-key` | Anthropic API key (overrides env var) | None |

### Examples

Process all papers with default settings:
```bash
python run_benchmark.py
```

Process papers from a specific directory:
```bash
python run_benchmark.py --papers-dir /path/to/papers
```

Limit processing to 10 papers:
```bash
python run_benchmark.py --max-papers 10
```

Use a different Claude model:
```bash
python run_benchmark.py --model claude-sonnet-4-5-20250929
```

Combine multiple options:
```bash
python run_benchmark.py --papers-dir /path/to/papers --max-papers 3 --model claude-opus-4-20250514
```

---

## Workflow

### Per-Paper Processing Workflow

For each paper, the following steps are executed by Claude:

```
┌─────────────────────────────────────────────────────────────┐
│                    PAPER PROCESSING WORKFLOW                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1: PDF Initialization                                 │
│  └── pdf_to_morpheus_pipeline() is called                   │
│  └── Text is extracted from the PDF                         │
│  └── Reference categories are suggested                     │
│                                                             │
│  STEP 2: Reference Loading                                  │
│  └── list_references() is called to discover examples       │
│  └── read_reference() is called for 2-3 relevant examples   │
│  └── <Analysis> sections are studied for graph config       │
│                                                             │
│  STEP 3: XML Generation                                     │
│  └── Morpheus XML is generated based on paper + references  │
│  └── <Gnuplotter> must be included for PNG generation       │
│  └── generate_xml_from_text() is called to save XML         │
│                                                             │
│  STEP 4: Simulation Execution                               │
│  └── XML is validated for <Gnuplotter> presence             │
│  └── run_morpheus() is called to execute simulation         │
│  └── PNG and CSV files are generated                        │
│                                                             │
│  STEP 5: Error Handling (if needed)                         │
│  └── auto_fix_and_rerun() is called to get error details    │
│  └── XML is corrected based on stderr                       │
│  └── Maximum 2 fix attempts are made                        │
│                                                             │
│  STEP 6: Evaluation                                         │
│  └── evaluation() is called to score the run                │
│  └── evaluation.json and evaluation.txt are generated       │
│                                                             │
│  STEP 7: Completion                                         │
│  └── "PAPER_COMPLETE" is signaled by Claude                 │
│  └── Next paper processing begins                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### MCP Tools Used

| Tool | Purpose |
|------|---------|
| `pdf_to_morpheus_pipeline` | PDF text extraction and reference suggestion |
| `list_references` | Discovery of available reference XML files |
| `read_reference` | Loading of reference XML content |
| `generate_xml_from_text` | Saving of generated Morpheus XML |
| `run_morpheus` | Execution of Morpheus simulation |
| `auto_fix_and_rerun` | Error diagnosis and recovery |
| `evaluation` | Scoring and evaluation of run results |
| `get_run_summary` | Retrieval of run logs and outputs |
| `read_file_text` | Reading of any text file |

---

## Output

### Benchmark Results JSON

Upon completion, a summary is saved to `benchmark_results.json`:

```json
{
  "benchmark_summary": {
    "model": "claude-sonnet-4-5-20250929",
    "total_papers_processed": 10,
    "successfully_completed": 9,
    "failed_incomplete": 1,
    "total_pngs_generated": 944,
    "total_csvs_generated": 162,
    "average_score": 6.3,
    "max_possible_score": 7,
    "min_score": 0,
    "max_score": 7,
    "duration": "70m 39s",
    "duration_seconds": 4239,
    "success_rate_percent": 90.0,
    "perfect_scores_count": 9
  },
  "individual_results": [
    {
      "index": 1,
      "paper": "1_Szabo2010_clean.pdf",
      "status": "completed",
      "score": 7,
      "max_score": 7,
      "png_count": 249,
      "csv_count": 150
    },
    ...
  ]
}
```

### Console Output

During execution, progress is displayed in the console:

```
══════════════════════════════════════════════════════════════════════
  🚀 MORPHEUS BENCHMARK RUNNER
══════════════════════════════════════════════════════════════════════
  Papers directory: /Users/prerana/Desktop/morpheus/papers
  Model: claude-sonnet-4-5-20250929
  Max papers: 10
  Max iterations per paper: 25
══════════════════════════════════════════════════════════════════════

  📚 Found 10 PDF files:
    1. 1_Szabo2010_clean.pdf
    2. 2_Thapa2024_clean.pdf
    ...

======================================================================
  📄 PROCESSING PAPER 1/10: 1_Szabo2010_clean.pdf
======================================================================

  [Iteration 1/25]
    → Calling: pdf_to_morpheus_pipeline
    ← run_id: 20260129_183548_03941a64

  [Iteration 2/25]
    → Calling: read_reference
    ← ✓

  ...

  ✓ Paper marked as COMPLETE by agent

  ────────────────────────────────────────────────────────────
  Paper Result: COMPLETED
  Score: 7/7
  PNGs: 249, CSVs: 150
  Iterations: 23
  ────────────────────────────────────────────────────────────
```

### Evaluation Report

For each run, an evaluation report is generated:

```
============================================================
MORPHEUS EVALUATION REPORT
============================================================
Run ID: 20260129_183548_03941a64
Timestamp: 2026-01-29T18:40:15.123456

TOTAL SCORE: 7 / 7 (100.0%)

------------------------------------------------------------
SCORING BREAKDOWN:
------------------------------------------------------------

1. XML/Stderr Errors (penalty, best=0):
   - Error count: 0
   - Score: 0

2. Model Graph (model_graph.dot):
   - Present: True
   - Files: ['model_graph.dot']
   - Score: 1 / 1

3. Time Step Progression (from stdout.log):
   - Time lines count: 101
   - Scoring: 0->+0, 1-10->+1, 11-50->+2, 51+->+3
   - Score: 3 / 3

4. StopTime Match:
   - StopTime in XML: 1000.0
   - Last simulation time: 1000.0
   - Match: True
   - Score: 1 / 1

5. Result Files Generated:
   - PNG files: 249
   - CSV files: 150
   - Score: 1 / 1

6. BONUS - Many Results (10+ PNGs):
   - Score: 1 / 1

============================================================
```

---

## Evaluation Criteria

Each run is scored on a scale of 0-7 points:

| Criterion | Points | Description |
|-----------|--------|-------------|
| **XML Errors** | 0 to -N | Negative points for each error in stderr.log |
| **Model Graph** | +1 | model_graph.dot file is present |
| **Time Progression** | +1 to +3 | Simulation time steps completed (1-10: +1, 11-50: +2, 51+: +3) |
| **StopTime Match** | +1 | Last simulation time matches StopTime in XML |
| **Results Generated** | +1 | At least one PNG or CSV file is generated |
| **Bonus: Many Results** | +1 | 10 or more PNG files are generated |

**Maximum Score: 7 points**

### Score Interpretation

| Score | Interpretation |
|-------|----------------|
| 7/7 | Perfect run - all criteria met |
| 5-6/7 | Good run - minor issues |
| 3-4/7 | Partial success - significant issues |
| 1-2/7 | Poor run - major problems |
| 0/7 | Failed run - simulation did not complete |

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Morpheus not found | `morpheus: command not found` | The `MORPHEUS_BIN` path should be set in `server.py` |
| Rate limit errors | `429 Too Many Requests` | Automatic retry is implemented; waiting is handled |
| No PNGs generated | `PNGs: 0` despite success | `<Gnuplotter>` must be present in XML; validation is enforced |
| Wrong output counts | Console shows 0 but files exist | Counts are now taken from evaluation breakdown |
| API key error | `401 Unauthorized` | API key must be set via env var or config |
| Import error | `ModuleNotFoundError` | Dependencies must be installed via pip |

### Diagnostic Commands

Check Morpheus installation:
```bash
which morpheus
morpheus --version
```

Check generated files:
```bash
ls -la /path/to/run_directory/
```

Check stdout for simulation progress:
```bash
cat /path/to/run_directory/stdout.log | grep "Time:"
```

Check for errors:
```bash
cat /path/to/run_directory/stderr.log
```

Test XML manually:
```bash
cd /path/to/run_directory/
morpheus --file model.xml
```

### Debug Mode

Additional logging can be enabled by modifying `run_benchmark.py`:

```python
# Add at the top of the file
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Cost Estimation

### API Usage

For processing 10 papers with approximately 15 iterations each:

| Model | Estimated Cost | Processing Time |
|-------|----------------|-----------------|
| claude-sonnet-4-20250514 | $5-10 | ~60-90 minutes |
| claude-sonnet-4-5-20250929 | $8-15 | ~70-100 minutes |
| claude-opus-4-20250514 | $15-30 | ~90-120 minutes |

### Factors Affecting Cost

- **Paper complexity**: More complex papers require more iterations
- **XML errors**: Error recovery adds additional API calls
- **Reference loading**: Each reference read consumes tokens
- **Rate limiting**: Delays don't add cost but extend duration

### Cost Optimization Tips

1. Use `claude-sonnet-4-20250514` for best cost/quality balance
2. Limit `max_chars` for reference reading (default: 8000)
3. Conversation truncation is enabled by default
4. Set appropriate `MAX_ITERATIONS_PER_PAPER` limit

---

## Comparison with Chat Interface

| Aspect | Claude Chat Interface | Python API Approach |
|--------|----------------------|---------------------|
| **Interaction** | Manual interaction is required | Fully autonomous execution is achieved |
| **Continuity** | Processing may be stopped/paused | Continuous execution until completion |
| **Control** | Limited control is available | Full programmatic control is provided |
| **Debugging** | Debugging is difficult | Easy logging/debugging is supported |
| **Integration** | Single session only | CI/CD and cron job integration is possible |
| **Scalability** | One paper at a time | Batch processing is supported |
| **Reproducibility** | Difficult to reproduce | Fully reproducible runs |
| **Cost Tracking** | Manual tracking required | Automatic tracking via API |

---

## API Reference

### MCP Tools (server.py)

#### `pdf_to_morpheus_pipeline(pdf_path: str) -> Dict`
PDF text extraction and reference category suggestion is performed.

#### `list_references(category: Optional[str]) -> Dict`
Available reference XML files are listed.

#### `read_reference(category: str, name: str, max_chars: int) -> Dict`
Reference XML content is loaded and returned.

#### `generate_xml_from_text(model_xml: str, run_id: str, file_name: str) -> Dict`
Generated Morpheus XML is saved to the run directory.

#### `run_morpheus(xml_path: str, run_id: str) -> Dict`
Morpheus simulation is executed and results are returned.

#### `auto_fix_and_rerun(run_id: str) -> Dict`
Error details are retrieved for failed runs.

#### `evaluation(run_id: str) -> Dict`
Run results are evaluated and scored.

#### `get_run_summary(run_id: str) -> Dict`
Run logs and output file lists are retrieved.

#### `read_file_text(path: str, max_chars: int) -> Dict`
Text file content is read and returned.

### Benchmark Runner (run_benchmark.py)

#### `PaperProcessor`
Individual papers are processed using Claude as the AI agent.

#### `BenchmarkRunner`
Multiple papers are processed and results are aggregated.

#### `execute_tool(tool_name: str, tool_input: Dict) -> Dict`
MCP tool functions are executed locally.

---

## System Prompt

The agent behavior is controlled by the `SYSTEM_PROMPT` in `run_benchmark.py`. Key instructions include:

- **Workflow enforcement**: Steps must be followed in order
- **Reference grounding**: XML must be based on official examples
- **Gnuplotter requirement**: `<Analysis>` section must be included
- **Error handling**: Maximum 2 fix attempts before proceeding
- **Evaluation mandate**: `evaluation()` must always be called
- **Completion signal**: "PAPER_COMPLETE" must be stated when done

The system prompt can be customized to modify agent behavior as needed.


## Acknowledgments

- **Morpheus**: Developed by the Center for Information Services and High Performance Computing (ZIH) at TU Dresden
- **Anthropic**: Claude AI and the Anthropic API
- **MCP**: Model Context Protocol specification
