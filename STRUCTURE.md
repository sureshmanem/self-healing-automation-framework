# Self-Healing Playwright Automation Framework
# Clean Folder Structure

```
self-healing-automation-framework/
│
├── 📦 self_healing_playwright/    # Main Python package (source code)
│   ├── __init__.py               # Package initialization & exports
│   ├── openai_healer.py          # Azure OpenAI integration
│   └── safe_page.py              # Self-healing Page wrapper
│
├── 🧪 tests/                      # Test suite
│   ├── __init__.py               # Test package marker
│   └── test_framework.py         # Unit tests (12 tests)
│
├── 📚 examples/                   # Usage examples
│   └── example_usage.py          # Example scenarios
│
├── 📖 docs/                       # Documentation
│   ├── README.md                 # Documentation index
│   ├── QUICKSTART.md             # 5-minute setup guide
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── PROJECT_STRUCTURE.md      # Detailed structure
│   └── ORGANIZATION_SUMMARY.md   # Organization summary
│
├── 📄 Configuration Files
│   ├── pyproject.toml            # Modern Python packaging (PEP 621)
│   ├── setup.py                  # Package setup script
│   ├── setup.cfg                 # Tool configurations
│   ├── requirements.txt          # Dependencies
│   ├── .env.example              # Environment template (create .env from this)
│   ├── .gitignore                # Git ignore patterns
│   └── Makefile                  # Developer commands
│
├── 📋 Documentation Files (Root)
│   ├── README.md                 # Main project documentation
│   └── LICENSE                   # MIT License
│
└── 🚫 Excluded from Git (.gitignore)
    ├── .env                      # Your credentials (not committed)
    ├── .venv/                    # Virtual environment
    ├── __pycache__/              # Python cache
    ├── .pytest_cache/            # Pytest cache
    ├── *.egg-info/               # Build artifacts
    └── dist/, build/             # Distribution files
```

## Directory Purpose

### Source Code
- **`self_healing_playwright/`** - Core framework code, importable as a package

### Testing
- **`tests/`** - All test files, run with `make test` or `pytest tests/`

### Examples
- **`examples/`** - Real-world usage examples, run with `make run-example`

### Documentation
- **`docs/`** - All documentation files organized in one place
- **Root docs** - Essential files (README, LICENSE) stay at root for visibility

### Configuration
- **Root level** - All config files at root for tool discovery

## Import Structure

```python
# Clean, professional imports
from self_healing_playwright import OpenAIHealer, SafePage
```

## Common Commands

```bash
# Installation
make install          # Install dependencies
make install-dev      # Install with dev tools

# Testing
make test            # Run all tests
make test-coverage   # With coverage report

# Development
make format          # Format code
make lint            # Check code quality
make clean           # Clean cache files
make clean-all       # Deep clean including .venv

# Running
make run-example     # Run example script
make docs            # Open documentation

# Help
make help            # Show all commands
```

## File Organization Principles

1. **Separation of Concerns**: Source, tests, examples, docs in separate directories
2. **Discoverability**: README and LICENSE at root for GitHub visibility
3. **Convention**: Follows Python packaging best practices (PEP 517/518/621)
4. **Clean Root**: No source files in root, everything organized in subdirectories
5. **Documentation Hub**: All docs in `docs/` folder with index

## Benefits

✅ **Professional Structure** - Follows industry standards
✅ **Easy Navigation** - Clear directory purposes
✅ **Installable Package** - Can be installed with `pip install -e .`
✅ **Clean Imports** - Simple, clean import statements
✅ **Maintainable** - Easy to find and modify files
✅ **CI/CD Ready** - Standard structure for automation
✅ **Documentation Hub** - All docs organized in one place

## Next Steps

1. Keep source code in `self_healing_playwright/`
2. Add tests to `tests/`
3. Add examples to `examples/`
4. Update docs in `docs/`
5. Configuration files stay at root
6. Never commit `.env` or cache files
