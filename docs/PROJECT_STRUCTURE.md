# Project Structure

## Overview
```
self-healing-automation-framework/
├── 📦 self_healing_playwright/    # Main Python package
│   ├── __init__.py               # Package exports: OpenAIHealer, SafePage
│   ├── openai_healer.py          # Azure OpenAI integration for selector healing
│   └── safe_page.py              # Self-healing Playwright Page wrapper
│
├── 🧪 tests/                      # Test suite
│   ├── __init__.py               # Test package marker
│   └── test_framework.py         # Comprehensive unit tests (12 tests)
│
├── 📚 examples/                   # Usage examples
│   └── example_usage.py          # Multiple example scenarios
│
├── 📄 Configuration Files
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Git ignore patterns
│   ├── pyproject.toml            # Modern Python project metadata
│   ├── setup.py                  # Package installation script
│   ├── setup.cfg                 # Tool configurations (pytest, flake8, mypy)
│   ├── requirements.txt          # Python dependencies
│   └── Makefile                  # Common development commands
│
└── 📖 Documentation
    ├── README.md                 # Complete project documentation
    ├── QUICKSTART.md             # 5-minute setup guide
    ├── CONTRIBUTING.md           # Contribution guidelines
    └── LICENSE                   # MIT License

Hidden files (development):
├── .env                          # Your local credentials (not in git)
├── .venv/                        # Virtual environment (not in git)
├── __pycache__/                  # Python cache (not in git)
└── .pytest_cache/                # Pytest cache (not in git)
```

## Package Structure

### `self_healing_playwright/` - Main Package
The core package that provides self-healing capabilities.

**`__init__.py`**
- Exports public API: `OpenAIHealer`, `SafePage`
- Version information: `__version__ = "1.0.0"`

**`openai_healer.py`** (152 lines)
- `OpenAIHealer` class
- Azure OpenAI client initialization
- `get_new_selector(old_selector, dom_chunk, error_msg)` method
- Intelligent prompt engineering for QA context
- Environment variable support

**`safe_page.py`** (179 lines)
- `SafePage` class - Playwright Page wrapper
- Self-healing methods:
  - `click(selector, **kwargs)` - Auto-healing click
  - `fill(selector, value, **kwargs)` - Auto-healing form fill
- Pass-through methods: `goto()`, `wait_for_selector()`, `screenshot()`, etc.
- DOM snapshot capture with configurable limits
- Detailed healing logs

### `tests/` - Test Suite
Comprehensive unit tests with mocking.

**`test_framework.py`** (202 lines, 12 tests)
- `TestOpenAIHealer` (5 tests)
  - Environment variable initialization
  - Parameter-based initialization  
  - Credential validation
  - Selector correction
  - Response cleaning
  
- `TestSafePage` (7 tests)
  - Click without healing
  - Click with healing trigger
  - Fill without healing
  - Fill with healing trigger
  - DOM snapshot limits
  - Pass-through methods
  - URL property

**Test Coverage**: All critical paths tested with mocks

### `examples/` - Usage Examples
Real-world usage patterns.

**`example_usage.py`** (142 lines)
- `example_basic_usage()` - Simple self-healing click
- `example_form_filling()` - Form automation with healing
- `example_with_explicit_timeout()` - Custom configuration
- Ready-to-run with proper error handling

## File Purposes

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Production dependencies (playwright, openai, python-dotenv) |
| `pyproject.toml` | Modern Python packaging metadata (PEP 621) |
| `setup.py` | Package installation and distribution |
| `setup.cfg` | Tool configurations (pytest, flake8, mypy, coverage) |
| `.env.example` | Template for Azure OpenAI credentials |
| `.gitignore` | Files to exclude from version control |
| `Makefile` | Developer convenience commands |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete documentation, architecture, usage |
| `QUICKSTART.md` | 5-minute setup guide for quick start |
| `CONTRIBUTING.md` | Development setup, code style, PR process |
| `LICENSE` | MIT License |

## Import Paths

### For Application Code
```python
from self_healing_playwright import OpenAIHealer, SafePage
```

### For Tests (with sys.path modification)
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from self_healing_playwright import OpenAIHealer, SafePage
```

### For Examples
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from self_healing_playwright import OpenAIHealer, SafePage
```

## Development Workflow

### Using Makefile
```bash
make help           # Show all available commands
make install        # Install dependencies
make install-dev    # Install with dev dependencies
make test           # Run tests
make test-verbose   # Run tests with verbose output
make test-coverage  # Run tests with coverage report
make lint           # Run flake8
make format         # Run black
make clean          # Clean build artifacts
make run-example    # Run example script
```

### Manual Commands
```bash
# Install
pip install -e .
pip install -e ".[dev]"

# Test
python -m pytest tests/
python -m pytest tests/ -v
python -m pytest tests/ --cov=self_healing_playwright

# Run examples
python examples/example_usage.py

# Code quality
black self_healing_playwright/ tests/ examples/
flake8 self_healing_playwright/ tests/ examples/
```

## Key Design Decisions

1. **Package Name**: `self_healing_playwright` (snake_case for Python packages)
2. **Module Organization**: Separate concerns (healer vs page wrapper)
3. **Import Strategy**: Absolute imports with `__init__.py` exports
4. **Test Location**: Separate `tests/` directory with `sys.path` manipulation
5. **Examples Location**: Separate `examples/` directory for clarity
6. **Configuration**: Multiple approaches (pyproject.toml, setup.py, setup.cfg) for compatibility
7. **Documentation**: Multi-level (README, QUICKSTART, CONTRIBUTING) for different audiences

## Dependencies

### Production
- `playwright>=1.47.0` - Browser automation
- `openai>=1.54.0` - Azure OpenAI SDK
- `python-dotenv>=1.0.0` - Environment variable management

### Development (Optional)
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking

## File Statistics
- Total Python files: 6
- Total lines of code: ~680
- Test coverage: 12 comprehensive tests
- Documentation: 4 markdown files
- Configuration: 6 config files

## Version Information
- Package Version: 1.0.0
- Python Requirement: >=3.10
- Status: Beta / Production-Ready
