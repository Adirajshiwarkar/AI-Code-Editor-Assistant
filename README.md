# AI Autonomous Coding & Refactoring Assistant

A powerful multi-agent system that autonomously understands, refactors, documents, and improves codebases using OpenAI's LLM.

## Features

### Core Capabilities
- **Code Understanding**: Analyze structure, dependencies, and logic flow
- **Intelligent Refactoring**: Improve readability, reduce complexity, apply best practices
- **Pattern Conversion**: Transform between procedural, OOP, and functional paradigms
- **Async Conversion**: Add async/await patterns where beneficial
- **Test Generation**: Create comprehensive unit and integration tests
- **Documentation**: Generate docstrings, READMEs, and architecture docs
- **Quality Improvements**: Remove dead code, add type hints, improve error handling
- **Bug Detection**: Identify potential issues and suggest fixes

### Multi-Agent Architecture
- **Planner Agent**: Decomposes requests into structured task sequences
- **Analysis Agent**: Inspects code structure, patterns, and dependencies
- **Refactor Agent**: Rewrites code while preserving functionality
- **QA Agent**: Validates changes and checks for errors
- **TestGen Agent**: Generates comprehensive test suites
- **Doc Agent**: Creates professional documentation
- **Reporting Agent**: Summarizes changes and impacts

### Advanced Features
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++, Go
- **Diff Generation**: Clear before/after comparisons
- **Automatic Backups**: Safe file modification with rollback capability
- **Language Detection**: Automatic detection and language-specific rules
- **Structured Reports**: Detailed analysis with change summaries

## Installation

1. **Clone or navigate to the project directory**
```bash
cd "AI code breakdown"
```

2. **Activate the virtual environment**
```bash
source .venv/bin/activate
```

3. **Install dependencies** (if needed)
```bash
pip install -r requirements.txt
```

4. **Set up your OpenAI API key**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Usage

### Basic Syntax
```bash
python main.py <file_or_folder> "<instruction>"
```

### Example Commands

**Refactor a file:**
```bash
python main.py tests/messy_code.py "refactor this file for better readability"
```

**Generate documentation:**
```bash
python main.py src/ "generate comprehensive documentation"
```

**Add type hints:**
```bash
python main.py app.py "add type hints and improve error handling"
```

**Generate tests:**
```bash
python main.py utils.py "create unit tests for all functions"
```

**Convert to async:**
```bash
python main.py api.py "convert synchronous code to async/await"
```

**Optimize performance:**
```bash
python main.py algorithm.py "optimize for performance while maintaining readability"
```

**Split modules:**
```bash
python main.py monolith.py "split this into smaller, focused modules"
```

### Command-Line Options

- `--no-backup`: Disable automatic backup of modified files
- `--dry-run`: Preview changes without applying them (coming soon)
- `--help`: Show all available options

**Example with options:**
```bash
python main.py --no-backup code.py "quick refactor"
```

## Supported Instructions

The system understands natural language instructions like:
- "Refactor this function for readability"
- "Optimize this class for performance"
- "Explain what this repository does"
- "Rewrite this script using modern patterns"
- "Generate documentation for the modules"
- "Create tests for this logic"
- "Improve error-handling in this file"
- "Convert this code to async"
- "Split this monolithic file into smaller modules"
- "Add type hints throughout"
- "Remove dead code and unused imports"

## Project Structure

```
AI code breakdown/
├── main.py                 # CLI entry point
├── coordinator.py          # Orchestrates multi-agent workflow
├── .env                    # API keys (create this)
├── requirements.txt        # Dependencies
├── agents/                 # Specialized AI agents
│   ├── planner.py         # Task decomposition
│   ├── analysis.py        # Code analysis
│   ├── refactor.py        # Code refactoring
│   ├── qa.py              # Quality assurance
│   ├── test_gen.py        # Test generation
│   ├── doc.py             # Documentation
│   └── reporting.py       # Summary reports
├── tools/                  # Utility functions
│   ├── file_ops.py        # File I/O with backup
│   ├── diff_generator.py  # Diff creation
│   └── language_detector.py # Language detection
├── utils/                  # Core utilities
│   └── llm.py             # LLM interface
└── tests/                  # Test files
    └── messy_code.py      # Example code
```

## How It Works

1. **Input**: You provide a file/folder and an instruction
2. **Planning**: Planner Agent breaks down the request into tasks
3. **Execution**: Specialized agents execute tasks in sequence:
   - Analysis Agent examines the code
   - Refactor Agent improves the code
   - QA Agent validates changes
   - TestGen Agent creates tests (if requested)
   - Doc Agent generates documentation (if requested)
4. **Reporting**: System generates a comprehensive report
5. **Output**: Modified files (with backups) and detailed report

## Safety Features

- **Automatic Backups**: Original files are backed up before modification
- **Functionality Preservation**: QA Agent validates that refactoring preserves behavior
- **Diff Generation**: See exactly what changed
- **Rollback Capability**: Restore from backups if needed

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies: `openai`, `python-dotenv`

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
Make sure you're using the virtual environment:
```bash
source .venv/bin/activate
```

### "OPENAI_API_KEY environment variable not set"
Create a `.env` file with your API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### "externally-managed-environment" error
Always use the virtual environment instead of system Python:
```bash
source .venv/bin/activate
```

## Examples

### Example 1: Refactor Messy Code
```bash
python main.py tests/messy_code.py "improve code quality and add docstrings"
```

**Output**: Refactored code with proper formatting, docstrings, and a detailed diff showing changes.

### Example 2: Generate Tests
```bash
python main.py utils/helpers.py "generate comprehensive unit tests"
```

**Output**: Complete test file with edge cases and assertions.

### Example 3: Document a Module
```bash
python main.py src/ "create README and architecture documentation"
```

**Output**: Professional documentation explaining the codebase.

## License

This project is for educational and development purposes.

## Contributing

Feel free to extend the system by:
- Adding new agents
- Supporting more languages
- Implementing dry-run mode
- Adding more file operation utilities
