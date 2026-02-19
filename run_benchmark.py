#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MORPHEUS BENCHMARK RUNNER - AUTONOMOUS AGENT               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  This script runs Claude with Morpheus MCP tools entirely from Python.       ║
║  It processes papers ONE AT A TIME, completing each fully before moving on.  ║
║                                                                              ║
║  Usage:                                                                      ║
║      python run_benchmark.py                                                 ║
║      python run_benchmark.py --papers-dir /path/to/papers                    ║
║      python run_benchmark.py --max-papers 10                                 ║
║                                                                              ║
║  Requirements:                                                               ║
║      pip install anthropic pypdf python-dotenv                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from unittest import result

# =============================================================================
#   CONFIGURATION SETTINGS
#   EDIT THE SETTINGS BELOW TO CONFIGURE YOUR BENCHMARK
#
# =============================================================================

# -----------------------------------------------------------------------------
#  API KEY CONFIGURATION
# -----------------------------------------------------------------------------
# Option 1: Set directly here (not recommended for production)
ANTHROPIC_API_KEY = " "  # <-- PUT YOUR API KEY HERE (e.g., "sk-ant-api03-...")

# Option 2: Use environment variable (recommended)
# In terminal: export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Option 3: Use .env file
# Create a file named ".env" in the same directory with:
# ANTHROPIC_API_KEY=sk-ant-api03-...

# -----------------------------------------------------------------------------
#  MODEL CONFIGURATION
# -----------------------------------------------------------------------------
# Available models:
#   - "claude-sonnet-4-20250514" (recommended - fast and capable)
#   - "claude-sonnet-4-5-20250929" (improved version of sonnet-4)
#   - "claude-opus-4-20250514" (most capable but slower and more expensive)
MODEL_NAME = "claude-sonnet-4-5-20250929"

# -----------------------------------------------------------------------------
#  PATHS CONFIGURATION
# -----------------------------------------------------------------------------
# Path to the directory containing your PDF papers
PAPERS_DIR = "/Users/prerana/Desktop/morpheus/papers"  # <-- CHANGE THIS

# Maximum number of papers to process (loop limit)
MAX_PAPERS = 10

# Maximum Claude API iterations per paper (safety limit to prevent infinite loops)
MAX_ITERATIONS_PER_PAPER = 25

# -----------------------------------------------------------------------------
#  SYSTEM PROMPT - EDIT THIS TO CHANGE AGENT BEHAVIOR
# -----------------------------------------------------------------------------
# This prompt tells Claude how to process each paper.
# It is sent fresh for each paper.

# MORPHEUS.AI SYSTEM PROMPT
# Use this in run_benchmark.py SYSTEM_PROMPT variable

SYSTEM_PROMPT = """
You are Morpheus.AI, an expert in biological modeling using MorpheusML v4.

You do NOT execute simulations yourself. 
You interact with Morpheus exclusively through MCP tools.

Your task is to generate VALID, RUNNABLE MorpheusML XML models that produce 
VISUALIZATION GRAPHS (PNG) and DATA OUTPUTS (CSV), grounded in scientific 
papers and official Morpheus example models.

════════════════════════════════════════════════════════════════════════════════
                                 CORE RULES
════════════════════════════════════════════════════════════════════════════════

1. Never invent Morpheus XML tags, attributes, or structures.
2. Always ground your XML in official Morpheus reference examples.
3. Prefer minimal modification of example XML over writing XML from scratch.
4. When uncertain, follow reference XML exactly rather than improvising.
5. When asked for XML output, return ONLY the XML document.
   - No explanations
   - No markdown fences
   - No comments outside XML

════════════════════════════════════════════════════════════════════════════════
                            REQUIRED WORKFLOW
════════════════════════════════════════════════════════════════════════════════

When given a scientific PDF, follow these steps IN ORDER:

┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: INITIALIZE THE PIPELINE                                            │
│  → Call: pdf_to_morpheus_pipeline(pdf_path)                                 │
│  → Save the run_id for all subsequent steps                                 │
│  → Note the suggested_reference_categories and available_references         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: LOAD REFERENCES BEFORE WRITING XML (CRITICAL!)                     │
│  → Call: list_references(category) for suggested categories                 │
│  → Call: read_reference(category, name) for 2-3 relevant examples           │
│                                                                             │
│  -  IMPORTANT: Study the <Analysis> section in EVERY reference!            │
│  -  Copy the <Gnuplotter> and <Logger> structure - you NEED these!         │
│  -  Use reference XML as structural templates                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: GENERATE MORPHEUS XML                                              │
│                                                                             │
│  → Combine reference patterns conservatively                                │
│  → Use biologically meaningful parameters inferred from the paper           │
│  → Ensure the XML is valid MorpheusML v4                                    │
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗  │
│  ║     CRITICAL: YOUR XML MUST INCLUDE <Analysis> SECTION!               ║  │
│  ║                                                                       ║  │
│  ║  WITHOUT <Analysis> = NO GRAPHS = FAILED RUN = SCORE 0                ║  │
│  ║                                                                       ║  │
│  ║  See MANDATORY XML STRUCTURE below!                                   ║  │
│  ╚═══════════════════════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4: SAVE THE MODEL                                                     │
│  → Call: generate_xml_from_text(model_xml, run_id)                          │
│  → Verify xml_path is returned                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 5: EXECUTE THE SIMULATION                                             │
│  → Call: run_morpheus(xml_path, run_id)                                     │
│  → Check the outputs field: should have PNG and CSV files                   │
│  → If PNGs = 0, your XML is MISSING <Gnuplotter>! Fix it!                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 6: ERROR HANDLING (if Morpheus failed or 0 outputs)                   │
│  → Call: auto_fix_and_rerun(run_id)                                         │
│  → Inspect stderr carefully                                                 │
│  → Re-check the SAME reference examples                                     │
│  → Modify the XML minimally to fix the error                                │
│  → ENSURE <Analysis> section with <Gnuplotter> is present!                  │
│  → Re-save and re-run (maximum 2 fix attempts)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 7: RUN EVALUATION (MANDATORY - ALWAYS DO THIS!)                       │
│  → Call: evaluation(run_id)                                                 │
│  → Report the total_score and breakdown                                     │
│  → This step is REQUIRED even if simulation failed                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 8: REPORT COMPLETION                                                  │
│  → State: "Paper [name] completed with score [X]/6"                         │
│  → Report: Number of PNG and CSV files generated                            │
│  → Say exactly: "PAPER_COMPLETE"                                            │
└─────────────────────────────────────────────────────────────────────────────┘

════════════════════════════════════════════════════════════════════════════════
                     MANDATORY XML STRUCTURE FOR OUTPUT GENERATION
════════════════════════════════════════════════════════════════════════════════

Your generated XML MUST follow this structure. Missing sections = FAILURE!

```xml
<MorpheusModel version="4">

    <Description>
        <Title>Your Model Title Based on Paper</Title>
        <Details>Brief description of what the model simulates</Details>
    </Description>

    <Space>
        <Lattice class="square">
            <Size symbol="size" value="200, 200, 0"/>
            <BoundaryConditions>
                <Condition type="periodic" boundary="x"/>
                <Condition type="periodic" boundary="y"/>
            </BoundaryConditions>
        </Lattice>
        <SpaceSymbol symbol="size" name="size"/>
    </Space>

    <Time>
        <StartTime value="0"/>
        <StopTime value="1000"/>           <!-- Adjust based on model needs -->
        <SaveInterval value="10"/>          <!-- Controls output frequency -->
        <RandomSeed value="0"/>
    </Time>

    <CellTypes>
        <CellType name="medium" class="medium"/>
        <CellType name="cells" class="biological">
            <!-- Cell properties: VolumeConstraint, SurfaceConstraint, etc. -->
            <VolumeConstraint target="200" strength="1"/>
            <SurfaceConstraint target="180" mode="aspherity" strength="1"/>
            <!-- Add more constraints/properties as needed from references -->
        </CellType>
    </CellTypes>

    <!-- CPM section if using Cellular Potts Model -->
    <CPM>
        <Interaction>
            <Contact type1="cells" type2="medium" value="12"/>
            <Contact type1="cells" type2="cells" value="6"/>
        </Interaction>
        <MonteCarloSampler stepper="edgelist">
            <MCSDuration value="1"/>
            <Neighborhood>
                <Order>2</Order>
            </Neighborhood>
            <MetropolisKinetics temperature="2"/>
        </MonteCarloSampler>
        <ShapeSurface scaling="norm">
            <Neighborhood>
                <Order>6</Order>
            </Neighborhood>
        </ShapeSurface>
    </CPM>

    <CellPopulations>
        <Population type="cells" size="0">
            <InitCircle mode="random" number-of-cells="25" center="100,100,0" radius="50"/>
        </Population>
    </CellPopulations>

    <!-- ═══════════════════════════════════════════════════════════════════ -->
    <!--  ANALYSIS SECTION - ABSOLUTELY REQUIRED FOR OUTPUT GENERATION!   -->
    <!-- ═══════════════════════════════════════════════════════════════════ -->
    
    <Analysis>
        <!-- Gnuplotter: Generates PNG images - REQUIRED! -->
        <Gnuplotter time-step="10" decorate="true">
            <Terminal name="png"/>
            <Plot title="Cell Simulation">
                <Cells value="cell.type" min="0" max="1">
                    <ColorMap>
                        <Color value="0" color="white"/>
                        <Color value="1" color="red"/>
                    </ColorMap>
                </Cells>
            </Plot>
        </Gnuplotter>
        
        <!-- Logger: Generates CSV data files - REQUIRED! -->
        <Logger time-step="10">
            <Input>
                <Symbol symbol-ref="cellcount"/>
            </Input>
            <Output>
                <TextOutput/>
            </Output>
        </Logger>
        
        <!-- ModelGraph: Generates DOT file of model structure -->
        <ModelGraph include-tags="#untagged" reduced="false" format="dot"/>
    </Analysis>

</MorpheusModel>
```

════════════════════════════════════════════════════════════════════════════════
                        ANALYSIS SECTION CHECKLIST
════════════════════════════════════════════════════════════════════════════════

Before saving your XML, verify you have ALL of these:

  ☐ <Analysis> tag present (wrapper for all output config)
  
  ☐ <Gnuplotter time-step="..."> present with:
      ☐ <Terminal name="png"/>
      ☐ At least one <Plot> with <Cells> or <Field>
      
  ☐ <Logger time-step="..."> present with:
      ☐ <Input> with at least one <Symbol>
      ☐ <Output> with <TextOutput/>
      
  ☐ <ModelGraph/> present

  If ANY of these are missing, Morpheus will generate 0 output files!

════════════════════════════════════════════════════════════════════════════════
                            ERROR HANDLING
════════════════════════════════════════════════════════════════════════════════

If Morpheus fails OR generates 0 PNG/CSV files:

1. Call auto_fix_and_rerun(run_id) to get error details
2. Check stderr for specific error messages
3. Common fixes:
   - Missing <Analysis> section → Add complete Analysis block
   - Missing symbol reference → Define the symbol in a CellType or Global
   - Invalid tag/attribute → Check reference XML for correct syntax
   - Wrong nesting → Follow reference XML structure exactly
4. Re-check the SAME reference examples you loaded earlier
5. Modify XML minimally - don't rewrite from scratch
6. Re-save with generate_xml_from_text()
7. Re-run with run_morpheus()
8. Maximum 2 fix attempts, then proceed to evaluation

════════════════════════════════════════════════════════════════════════════════
                               PRIORITIES
════════════════════════════════════════════════════════════════════════════════

Priority 1: Generate OUTPUT FILES (PNG graphs and CSV data)
            → This requires <Analysis> with <Gnuplotter> and <Logger>
            
Priority 2: Morpheus correctness (XML must run without errors)
            → Follow reference XML structure exactly
            
Priority 3: Faithfulness to reference examples
            → Minimal modifications to working templates
            
Priority 4: Biological realism from the paper
            → Adjust parameters to match paper's biology

  NEVER sacrifice Priority 1 or 2 for Priority 4!
  A running model with graphs is better than a "realistic" model that fails!

════════════════════════════════════════════════════════════════════════════════
                           SUCCESS CRITERIA
════════════════════════════════════════════════════════════════════════════════

A successful run produces:
  ✓ model.xml that Morpheus can execute
  ✓ Multiple PNG graph files (10-100+ depending on simulation length)
  ✓ CSV data files with logged values
  ✓ model_graph.dot file
  ✓ Evaluation score of 4-6 out of 7

If you get 0 PNG files, your XML is WRONG - go back and add <Gnuplotter>!

════════════════════════════════════════════════════════════════════════════════
                              START NOW
════════════════════════════════════════════════════════════════════════════════

Begin by calling pdf_to_morpheus_pipeline() with the provided PDF path.
Follow ALL steps in order. Say "PAPER_COMPLETE" only after evaluation is done.
"""
# =============================================================================
# PATHS CONFIGURATION
# =============================================================================

import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# -----------------------------------------------------------------------------
# Import MCP tool functions from server.py
# -----------------------------------------------------------------------------
# Make sure server.py is in the same directory or adjust the import path

try:
    from server import (
        # Core pipeline tools
        pdf_to_morpheus_pipeline,
        read_pdf,
        suggest_references,
        
        # Reference tools
        list_references,
        read_reference,
        
        # XML tools
        generate_xml_from_text,
        save_model_xml,
        
        # Execution tools
        run_morpheus,
        run_xml_once,
        
        # Utility tools
        auto_fix_and_rerun,
        get_run_summary,
        read_file_text,
        create_run,
        
        # Evaluation
        evaluation,
        
        # Full pipeline (optional)
        run_full_pipeline,
    )
    print("✓ Successfully imported tools from server.py")
except ImportError as e:
    print(f"✗ Error importing from server.py: {e}")
    print("\nMake sure server.py is in the same directory as this script.")
    print("Or update the import statement to match your file location.")
    sys.exit(1)


# -----------------------------------------------------------------------------
# Tool Definitions for Claude API
# -----------------------------------------------------------------------------

TOOLS = [
    {
        "name": "pdf_to_morpheus_pipeline",
        "description": "STEP 1: Initialize processing for a PDF paper. Extracts text and suggests reference categories. Returns run_id for subsequent steps.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pdf_path": {
                    "type": "string",
                    "description": "Full path to the PDF file"
                }
            },
            "required": ["pdf_path"]
        }
    },
    {
        "name": "list_references",
        "description": "List available Morpheus reference XML files. Use to discover examples before loading them.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category to filter: CPM, PDE, ODE, Multiscale, or Miscellaneous. Leave empty for all."
                }
            },
            "required": []
        }
    },
    {
        "name": "read_reference",
        "description": "STEP 2: Load a reference XML file. IMPORTANT: Study the <Analysis> section for graph generation config!",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category: CPM, PDE, ODE, Multiscale, or Miscellaneous"
                },
                "name": {
                    "type": "string",
                    "description": "Filename of the reference (e.g., 'CellSorting.xml')"
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum characters to read (default: 8000 to save tokens)"
                }
            },
            "required": ["category", "name"]
        }
    },
    {
        "name": "generate_xml_from_text",
        "description": "STEP 3: Save your generated Morpheus XML. The XML MUST include <Analysis> with <Gnuplotter> for PNG generation!",
        "input_schema": {
            "type": "object",
            "properties": {
                "model_xml": {
                    "type": "string",
                    "description": "Complete MorpheusModel XML content. Must include <Analysis> section with <Gnuplotter>!"
                },
                "run_id": {
                    "type": "string",
                    "description": "Run ID from pdf_to_morpheus_pipeline"
                },
                "file_name": {
                    "type": "string",
                    "description": "Filename (default: model.xml)"
                }
            },
            "required": ["model_xml", "run_id"]
        }
    },
    {
        "name": "run_morpheus",
        "description": "STEP 4: Execute Morpheus simulation. Check 'outputs' in response for generated PNG/CSV files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "xml_path": {
                    "type": "string",
                    "description": "Path to the model.xml file"
                },
                "run_id": {
                    "type": "string",
                    "description": "Run ID for this paper"
                }
            },
            "required": ["xml_path"]
        }
    },
    {
        "name": "auto_fix_and_rerun",
        "description": "STEP 5 (if needed): Get error details when Morpheus fails. Returns stderr and current XML for fixing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "string",
                    "description": "Run ID of the failed run"
                }
            },
            "required": ["run_id"]
        }
    },
    {
        "name": "evaluation",
        "description": "STEP 6 (MANDATORY): Evaluate the Morpheus run. Generates evaluation.json and evaluation.txt with scores. ALWAYS call this!",
        "input_schema": {
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "string",
                    "description": "Run ID to evaluate"
                }
            },
            "required": ["run_id"]
        }
    },
    {
        "name": "get_run_summary",
        "description": "Get summary of a run including logs and output file lists.",
        "input_schema": {
            "type": "object",
            "properties": {
                "run_id": {
                    "type": "string",
                    "description": "Run ID to summarize"
                }
            },
            "required": ["run_id"]
        }
    },
    {
        "name": "read_file_text",
        "description": "Read any text file (logs, CSV, etc.) for inspection.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Full path to the file"
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum characters to read (default: 20000)"
                }
            },
            "required": ["path"]
        }
    },
]


# -----------------------------------------------------------------------------
# Tool Executor - Maps tool names to actual Python functions
# -----------------------------------------------------------------------------

def execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool by name with the given input.
    Returns the result as a dictionary.
    """
    tool_map = {
        "pdf_to_morpheus_pipeline": pdf_to_morpheus_pipeline,
        "list_references": list_references,
        "read_reference": read_reference,
        "generate_xml_from_text": generate_xml_from_text,
        "run_morpheus": run_morpheus,
        "auto_fix_and_rerun": auto_fix_and_rerun,
        "evaluation": evaluation,
        "get_run_summary": get_run_summary,
        "read_file_text": read_file_text,
    }
    
    if tool_name not in tool_map:
        return {"ok": False, "error": f"Unknown tool: {tool_name}"}
    
    try:
        func = tool_map[tool_name]
        # Filter out None values and call function
        filtered_input = {k: v for k, v in tool_input.items() if v is not None}
        
        # Limit max_chars for reference reading to save tokens
        if tool_name == "read_reference" and "max_chars" not in filtered_input:
            filtered_input["max_chars"] = 8000
        if tool_name == "read_file_text" and "max_chars" not in filtered_input:
            filtered_input["max_chars"] = 5000
        
        # Check if model.xml has Gnuplotter BEFORE running Morpheus
        if tool_name == "run_morpheus":
            xml_path = filtered_input.get("xml_path", "")
            if xml_path and Path(xml_path).exists():
                xml_content = Path(xml_path).read_text()
                if "<Gnuplotter" not in xml_content:
                    return {
                        "ok": False,
                        "error": "XML REJECTED: Missing <Gnuplotter> in <Analysis> section! Add it and try again."
                    }
        
        result = func(**filtered_input)
        return result
    except Exception as e:
        import traceback
        return {
            "ok": False, 
            "error": f"Tool execution failed: {str(e)}",
            "traceback": traceback.format_exc()
        }
# -----------------------------------------------------------------------------
# Paper Processor - Handles ONE paper at a time
# -----------------------------------------------------------------------------

class PaperProcessor:
    """
    Processes a single paper using Claude as the AI agent.
    Runs an agentic loop until the paper is complete or max iterations reached.
    """
    
    def __init__(self, api_key: str, model: str = MODEL_NAME):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.messages: List[Dict[str, Any]] = []
        self.max_iterations = MAX_ITERATIONS_PER_PAPER
        
    def process_paper(self, pdf_path: str, paper_index: int, total_papers: int) -> Dict[str, Any]:
        """
        Process a single paper completely.
        Returns result with status, score, and outputs.
        """
        paper_name = Path(pdf_path).name
        
        print(f"\n{'='*70}")
        print(f"   PROCESSING PAPER {paper_index}/{total_papers}: {paper_name}")
        print(f"{'='*70}")
        
        # Initial message with PDF path
        self.messages = [
            {
                "role": "user",
                "content": f"Process this paper completely: {pdf_path}\n\nFollow ALL steps in order. Say 'PAPER_COMPLETE' only after evaluation is done."
            }
        ]
        
        result = {
            "paper": paper_name,
            "pdf_path": pdf_path,
            "status": "started",
            "run_id": None,
            "score": None,
            "max_score": 7,
            "png_count": 0,
            "csv_count": 0,
            "iterations": 0,
            "error": None,
        }
        
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            result["iterations"] = iteration
            
            print(f"\n  [Iteration {iteration}/{self.max_iterations}]")
            
            try:
                # Truncate conversation to reduce tokens (keep first + last 6 messages)
                if len(self.messages) > 8:
                    self.messages = self.messages[:1] + self.messages[-6:]
                    print(f"    [Truncated conversation to {len(self.messages)} messages]")
                
                # Call Claude API
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=8192,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=self.messages
                )
                
                # Check for completion signal in text
                response_text = self._extract_text(response.content)
                
                if "PAPER_COMPLETE" in response_text.upper():
                    print(f"  ✓ Paper marked as COMPLETE by agent")
                    result["status"] = "completed"
                    break
                
                # Handle different stop reasons
                if response.stop_reason == "end_turn":
                    # Claude finished without tool use - might be done or need prompting
                    print(f"  Agent says: {response_text[:200]}...")
                    
                    # Add response to messages
                    self.messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    
                    # Prompt to continue or confirm completion
                    self.messages.append({
                        "role": "user",
                        "content": "Have you completed ALL steps including evaluation? If yes, say 'PAPER_COMPLETE'. If not, continue with the next step."
                    })
                    
                elif response.stop_reason == "tool_use":
                    # Claude wants to use tools - execute them
                    tool_results = self._handle_tool_use(response, result)
                    
                    # Add assistant response and tool results to conversation
                    self.messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    self.messages.append({
                        "role": "user",
                        "content": tool_results
                    })
                    
                else:
                    print(f"  ⚠ Unexpected stop reason: {response.stop_reason}")
                    break
                
                # Add delay between iterations to avoid rate limits
                time.sleep(5)
                    
            except anthropic.APIStatusError as e:
                if e.status_code == 429:
                    print(f"  ⏳ Rate limit (429). Waiting 90 seconds...")
                    time.sleep(90)
                    continue  # Retry same iteration
                print(f"  ✗ API Status Error ({e.status_code}): {e}")
                result["status"] = "api_error"
                result["error"] = str(e)
                # Try to run evaluation anyway if we have a run_id
                if result["run_id"]:
                    print(f"  → Running evaluation despite error...")
                    try:
                        eval_result = evaluation(result["run_id"])
                        if eval_result.get("ok"):
                            result["score"] = eval_result.get("total_score")
                            result["status"] = "partial"
                            print(f"  ← Evaluation: {result['score']}/7")
                    except:
                        pass
                break
                
            except anthropic.APIError as e:
                print(f"  ✗ API Error: {e}")
                result["status"] = "api_error"
                result["error"] = str(e)
                # Try to run evaluation anyway if we have a run_id
                if result["run_id"]:
                    print(f"  → Running evaluation despite error...")
                    try:
                        eval_result = evaluation(result["run_id"])
                        if eval_result.get("ok"):
                            result["score"] = eval_result.get("total_score")
                            result["status"] = "partial"
                            print(f"  ← Evaluation: {result['score']}/7")
                    except:
                        pass
                break
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                result["status"] = "error"
                result["error"] = str(e)
                import traceback
                traceback.print_exc()
                break
        
        if iteration >= self.max_iterations:
            print(f"  ⚠ Max iterations ({self.max_iterations}) reached")
            result["status"] = "max_iterations"
        
        # FORCE EVALUATION if we have a run_id but no score
        if result["run_id"] and result["score"] is None:
            print(f"\n  → Force running evaluation for run_id: {result['run_id']}")
            try:
                eval_result = evaluation(result["run_id"])
                if eval_result.get("ok"):
                    result["score"] = eval_result.get("total_score")
                    result["max_score"] = eval_result.get("max_possible_score", 7)
                    
                    # Also get output counts from evaluation breakdown
                    breakdown = eval_result.get("breakdown", {})
                    result["png_count"] = breakdown.get("png_count", result["png_count"])
                    result["csv_count"] = breakdown.get("csv_count", result["csv_count"])
                    
                    print(f"  ← Evaluation: {result['score']}/{result['max_score']}")
                    print(f"  ← PNGs: {result['png_count']}, CSVs: {result['csv_count']}")
            except Exception as e:
                print(f"  ✗ Evaluation failed: {e}")
        
        # Print paper result summary
        print(f"\n  {'─'*60}")
        print(f"  Paper Result: {result['status'].upper()}")
        print(f"  Score: {result['score']}/{result['max_score']}" if result['score'] else "  Score: Not evaluated")
        print(f"  PNGs: {result['png_count']}, CSVs: {result['csv_count']}")
        print(f"  Iterations: {result['iterations']}")
        print(f"  {'─'*60}")
        
        return result
    
    def _extract_text(self, content: List) -> str:
        """Extract text from response content blocks."""
        texts = []
        for block in content:
            if hasattr(block, 'text'):
                texts.append(block.text)
        return "\n".join(texts)
    
    def _handle_tool_use(self, response, result: Dict) -> List[Dict]:
        """
        Handle tool use requests from Claude.
        Executes tools and returns results.
        """
        tool_results = []
        
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_use_id = block.id
                
                # Log tool call (truncate long inputs)
                input_str = json.dumps(tool_input)
                if len(input_str) > 100:
                    input_str = input_str[:100] + "..."
                print(f"    → Calling: {tool_name}")
                
                # Execute the tool
                tool_result = execute_tool(tool_name, tool_input)
                
                # Track important results
                if tool_name == "pdf_to_morpheus_pipeline" and tool_result.get("ok"):
                    result["run_id"] = tool_result.get("run_id")
                    print(f"    ← run_id: {result['run_id']}")
                    
                elif tool_name == "run_morpheus":
                    if tool_result.get("ok"):
                        outputs = tool_result.get("outputs", {})
                        result["png_count"] = len(outputs.get("png", []))
                        result["csv_count"] = len(outputs.get("csv", []))
                        print(f"    ← Success! PNGs: {result['png_count']}, CSVs: {result['csv_count']}")
                    else:
                        # Show actual error details
                        error_msg = tool_result.get('error') or tool_result.get('message') or 'Unknown'
                        stderr_preview = tool_result.get('stderr', '')[:200]
                        print(f"    ← Failed: {error_msg[:80]}")
                        if stderr_preview:
                            print(f"    ← stderr: {stderr_preview}")
                    
                elif tool_name == "evaluation":
                    if tool_result.get("ok"):
                        result["score"] = tool_result.get("total_score")
                        result["max_score"] = tool_result.get("max_possible_score", 7)
        
                # Get actual file counts from evaluation breakdown
                        breakdown = tool_result.get("breakdown", {})
                        result["png_count"] = breakdown.get("png_count", 0)
                        result["csv_count"] = breakdown.get("csv_count", 0)

                        print(f"    ← Evaluation: {result['score']}/{result['max_score']} | PNGs: {result['png_count']}, CSVs: {result['csv_count']}")
                    else:
                        print(f"    ← Evaluation failed")
                
                elif tool_name == "generate_xml_from_text":
                    if tool_result.get("ok"):
                        print(f"    ← XML saved to: {tool_result.get('xml_path', 'unknown')}")
                    else:
                        print(f"    ← XML save failed: {tool_result.get('error', '')[:25]}")
                
                else:
                    # Generic result logging
                    status = "✓" if tool_result.get("ok") else "✗"
                    print(f"    ← {status}")
                
                # Add to results
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": json.dumps(tool_result)
                })
        
        return tool_results


# -----------------------------------------------------------------------------
# Benchmark Runner - Processes ALL papers one by one
# -----------------------------------------------------------------------------

class BenchmarkRunner:
    """
    Runs the complete benchmark on multiple papers.
    Processes papers ONE AT A TIME, collecting results.
    """
    
    def __init__(self, api_key: str, papers_dir: str, max_papers: int = MAX_PAPERS, model: str = MODEL_NAME):
        self.api_key = api_key
        self.papers_dir = Path(papers_dir).expanduser()
        self.max_papers = max_papers
        self.model = model
        self.results: List[Dict[str, Any]] = []
        
    def discover_papers(self) -> List[Path]:
        """Find all PDF files in the papers directory."""
        if not self.papers_dir.exists():
            raise FileNotFoundError(f"Papers directory not found: {self.papers_dir}")
        
        papers = sorted(self.papers_dir.glob("*.pdf"))
        return papers[:self.max_papers]  # Limit to max_papers
    
    def run(self) -> Dict[str, Any]:
        """
        Run the complete benchmark.
        Returns summary with all results.
        """
        start_time = datetime.now()
        
        print("\n" + "═"*70)
        print("   MORPHEUS BENCHMARK RUNNER")
        print("═"*70)
        print(f"  Papers directory: {self.papers_dir}")
        print(f"  Model: {self.model}")
        print(f"  Max papers: {self.max_papers}")
        print(f"  Max iterations per paper: {MAX_ITERATIONS_PER_PAPER}")
        print("═"*70)
        
        # Discover papers
        papers = self.discover_papers()
        
        if not papers:
            print("\n  ✗ No PDF files found!")
            return {"status": "error", "error": "No PDF files found"}
        
        print(f"\n   Found {len(papers)} PDF files:")
        for i, p in enumerate(papers, 1):
            print(f"    {i}. {p.name}")
        
        # Process each paper ONE AT A TIME
        for i, pdf_path in enumerate(papers, 1):
            print(f"\n\n{'#'*70}")
            print(f"#  STARTING PAPER {i} OF {len(papers)}")
            print(f"{'#'*70}")
            
            # Create a fresh processor for each paper
            processor = PaperProcessor(api_key=self.api_key, model=self.model)
            
            # Process this paper completely
            result = processor.process_paper(
                pdf_path=str(pdf_path),
                paper_index=i,
                total_papers=len(papers)
            )
            
            # Save result
            self.results.append(result)
            
            # Brief pause between papers to avoid rate limits
            if i < len(papers):
                print(f"\n  ⏳ Waiting 60 seconds before next paper...")
                time.sleep(60)
        
        # Calculate summary statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        completed = sum(1 for r in self.results if r["status"] == "completed")
        scores = [r["score"] for r in self.results if r["score"] is not None]
        total_pngs = sum(r["png_count"] for r in self.results)
        total_csvs = sum(r["csv_count"] for r in self.results)
        
        summary = {
            "status": "completed",
            "timestamp": end_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "duration_formatted": f"{int(duration//60)}m {int(duration%60)}s",
            "model": self.model,
            "total_papers": len(papers),
            "completed_papers": completed,
            "failed_papers": len(papers) - completed,
            "total_pngs_generated": total_pngs,
            "total_csvs_generated": total_csvs,
            "scores": {
                "average": round(sum(scores) / len(scores), 2) if scores else 0,
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 0,
                "all": scores,
            },
            "results": self.results,
        }
        
        # Print summary
        self._print_summary(summary)
        
        # Save summary to JSON file
        summary_path = self.papers_dir.parent / "benchmark_results.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"\n   Results saved to: {summary_path}")
        
        return summary
    
    def _print_summary(self, summary: Dict):
        """Print a formatted summary of the benchmark results."""
        print("\n\n" + "═"*70)
        print("   BENCHMARK SUMMARY")
        print("═"*70)
        print(f"  Total papers processed: {summary['total_papers']}")
        print(f"  Successfully completed: {summary['completed_papers']}")
        print(f"  Failed/Incomplete: {summary['failed_papers']}")
        print(f"  Total PNGs generated: {summary['total_pngs_generated']}")
        print(f"  Total CSVs generated: {summary['total_csvs_generated']}")
        print(f"  Average score: {summary['scores']['average']}/7")
        print(f"  Duration: {summary['duration_formatted']}")
        print("═"*70)
        
        print("\n  Individual Results:")
        print("  " + "─"*66)
        print(f"  {'Paper':<40} {'Status':<12} {'Score':<8} {'PNGs':<6}")
        print("  " + "─"*66)
        
        for r in summary["results"]:
            status = "✓ Done" if r["status"] == "completed" else f"✗ {r['status'][:8]}"
            score_str = f"{r['score']}/7" if r["score"] is not None else "N/A"
            paper_short = r['paper'][:38] + ".." if len(r['paper']) > 40 else r['paper']
            print(f"  {paper_short:<40} {status:<12} {score_str:<8} {r['png_count']:<6}")
        
        print("  " + "─"*66)


# -----------------------------------------------------------------------------
# Main Entry Point
# -----------------------------------------------------------------------------

def main():
    """Main entry point for the benchmark runner."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run Morpheus benchmark autonomously using Claude API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_benchmark.py
  python run_benchmark.py --papers-dir /path/to/papers
  python run_benchmark.py --max-papers 5
  python run_benchmark.py --model claude-opus-4-20250514
        """
    )
    parser.add_argument(
        "--papers-dir",
        type=str,
        default=PAPERS_DIR,
        help=f"Directory containing PDF papers (default: {PAPERS_DIR})"
    )
    parser.add_argument(
        "--max-papers",
        type=int,
        default=MAX_PAPERS,
        help=f"Maximum number of papers to process (default: {MAX_PAPERS})"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=MODEL_NAME,
        help=f"Claude model to use (default: {MODEL_NAME})"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Anthropic API key (overrides config and env var)"
    )
    
    args = parser.parse_args()
    
    # Get API key with priority: CLI arg > Config > Environment
    api_key = args.api_key or ANTHROPIC_API_KEY or os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("\n" + "="*70)
        print("   ERROR: No API key provided!")
        print("="*70)
        print("\n  Set your Anthropic API key using one of these methods:\n")
        print("  1. Edit ANTHROPIC_API_KEY at the top of this script")
        print("  2. Set environment variable:")
        print('     export ANTHROPIC_API_KEY="sk-ant-api03-..."')
        print("  3. Create a .env file with:")
        print('     ANTHROPIC_API_KEY=sk-ant-api03-...')
        print("  4. Pass via command line:")
        print('     python run_benchmark.py --api-key "sk-ant-api03-..."')
        print("\n" + "="*70)
        sys.exit(1)
    
    # Use model from CLI args (defaults to MODEL_NAME from config)
    model_to_use = args.model
    
    # Verify papers directory exists
    papers_path = Path(args.papers_dir).expanduser()
    if not papers_path.exists():
        print(f"\n   ERROR: Papers directory not found: {args.papers_dir}")
        sys.exit(1)
    
    # Count PDFs
    pdf_count = len(list(papers_path.glob("*.pdf")))
    if pdf_count == 0:
        print(f"\n   ERROR: No PDF files found in {args.papers_dir}")
        sys.exit(1)
    
    print(f"\n  Found {pdf_count} PDF files")
    print(f"  Will process up to {args.max_papers} papers")
    
    # Create and run the benchmark
    runner = BenchmarkRunner(
        api_key=api_key,
        papers_dir=args.papers_dir,
        max_papers=args.max_papers,
        model=model_to_use
    )
    
    try:
        summary = runner.run()
        
        # Exit with appropriate code
        if summary.get("failed_papers", 0) == 0:
            print("\n   Benchmark completed successfully!")
            sys.exit(0)
        else:
            print(f"\n   Benchmark completed with {summary['failed_papers']} failures")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n  Interrupted by user (Ctrl+C)")
        print("  Partial results may have been saved.")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n   FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# -----------------------------------------------------------------------------
# Run the script
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()