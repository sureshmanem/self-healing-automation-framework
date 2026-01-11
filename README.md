# Self-Healing Playwright Automation Framework

A Python framework that adds self-healing capabilities to Playwright test automation using Azure OpenAI. When UI elements are not found, the framework automatically asks an LLM for corrected selectors and retries actions.

## 🎯 Features

- **Self-Healing Selectors**: Automatically fixes broken selectors using AI
- **Azure OpenAI Integration**: Leverages GPT models for intelligent selector correction
- **Playwright Sync API**: Built on standard Playwright synchronous API
- **Easy Integration**: Simple wrapper around existing Playwright code
- **Multiple Actions**: Supports click, fill, and more operations
- **Detailed Logging**: Clear feedback on healing attempts and outcomes

## 📋 Requirements

- Python 3.10+
- Azure OpenAI account with deployed model
- Playwright browser drivers

## 🚀 Installation

### Method 1: Using pip (Development Mode)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd self-healing-automation-framework
```

2. **Install the package**:
```bash
# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Or install just the package
pip install -e .
```

3. **Install Playwright browsers**:
```bash
playwright install chromium
```

4. **Configure Azure OpenAI credentials**:
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### Method 2: Using Make (Recommended)

```bash
# Clone and navigate to the repository
git clone <repository-url>
cd self-healing-automation-framework

# Install everything with one command
make install

# Or install with development dependencies
make install-dev

# Configure credentials
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

### Method 3: Using requirements.txt

```bash
pip install -r requirements.txt
playwright install chromium
# Edit .env with your Azure OpenAI credentials
```

## ⚙️ Configuration

Create a `.env` file with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

## 📖 Usage

### Basic Example

```python
from playwright.sync_api import sync_playwright
from self_healing_playwright import OpenAIHealer, SafePage

# Initialize the healer
healer = OpenAIHealer()

# Create Playwright browser and wrap page
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    safe_page = SafePage(page=page, healer=healer)
    
    # Navigate and interact - selectors will self-heal if they fail
    safe_page.goto("https://example.com")
    safe_page.click("#button-id")  # Will heal if selector fails
    safe_page.fill("#input-field", "test data")
```

### Advanced Configuration

```python
# Custom healer configuration
healer = OpenAIHealer(
    azure_endpoint="https://your-endpoint.openai.azure.com/",
    api_key="your-api-key",
    deployment_name="gpt-4",
    temperature=0.2,  # Lower = more deterministic
    max_tokens=500
)

# Custom SafePage configuration
safe_page = SafePage(
    page=page,
    healer=healer,
    dom_limit=3000  # Amount of DOM to send to LLM
)

# Use with custom timeouts
safe_page.click(".dynamic-button", timeout=10000)
```

## 🏗️ Architecture

### Components

1. **OpenAIHealer** (`openai_healer.py`)
   - Initializes Azure OpenAI client
   - Contains `get_new_selector()` method
### Components

1. **OpenAIHealer** ([self_healing_playwright/openai_healer.py](self_healing_playwright/openai_healer.py))
   - Initializes Azure OpenAI client
   - Contains `get_new_selector()` method
   - Sends descriptive prompts to LLM
   - Returns corrected selectors

2. **SafePage** ([self_healing_playwright/safe_page.py](self_healing_playwright/safe_page.py))
   - Wraps Playwright Page object
   - Implements self-healing actions (click, fill, etc.)
   - Catches TimeoutErrors
   - Captures DOM snapshots
   - Retries with healed selectors

### Project Structure

```
self-healing-automation-framework/
├── self_healing_playwright/    # Main package
│   ├── __init__.py            # Package initialization
│   ├── openai_healer.py       # OpenAIHealer class
│   └── safe_page.py           # SafePage wrapper class
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_framework.py      # Comprehensive test suite
├── examples/                   # Usage examples
│   └── example_usage.py       # Example scripts
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── Makefile                   # Common commands
├── README.md                  # This file
├── pyproject.toml            # Modern Python packaging
├── requirements.txt           # Dependencies
├── setup.cfg                  # Tool configurations
└── setup.py                   # Package setup
```

### Workflow

```
1. SafePage.click(selector) called
          ↓
2. Try standard Playwright click
          ↓
3. TimeoutError caught? → NO → Success ✓
          ↓ YES
4. Capture DOM snapshot (limited to 2000 chars)
          ↓
5. Call OpenAIHealer.get_new_selector(old, dom, error)
          ↓
6. Retry click with new selector
          ↓
7. Success? → YES → Print "HEALED: replaced {old} with {new}"
          ↓ NO
8. Raise exception with details
```

## 📝 Example Output

```
[HEALING] Original selector failed: #old-button-id
[HEALING] Error: Timeout 30000ms exceeded...
[HEALING] AI suggested new selector: button[data-testid="submit-btn"]
HEALED: replaced '#old-button-id' with 'button[data-testid="submit-btn"]'
```

## 🧪 Running Tests and Examples

### Run Tests

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run tests with coverage report
make test-coverage

# Or use pytest directly
python -m pytest tests/
python -m pytest tests/ -v
python -m pytest tests/ --cov=self_healing_playwright
```

### Run Examples

```bash
# Using Make
make run-example

# Or directly
python examples/example_usage.py
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Clean build artifacts
make clean
```

## 🔒 Best Practices

1. **Environment Variables**: Always use `.env` files for credentials, never commit them
2. **DOM Limit**: Keep `dom_limit` reasonable (2000-5000 chars) to manage API costs
3. **Temperature**: Use low temperature (0.1-0.3) for more consistent selector suggestions
4. **Error Handling**: Always wrap automation in try-except blocks
5. **Logging**: Review healing logs to identify patterns in broken selectors

## 🛠️ Extending the Framework

Add more self-healing methods to [SafePage](self_healing_playwright/safe_page.py):

```python
def hover(self, selector: str, timeout: float = 30000, **kwargs) -> None:
    """Hover with self-healing capability."""
    try:
        self.page.hover(selector, timeout=timeout, **kwargs)
    except PlaywrightTimeoutError as e:
        # Add healing logic similar to click()
        pass
```

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines on contributing to the project.

## 📊 Limitations

- **API Costs**: Each healing attempt calls Azure OpenAI (monitor usage)
- **DOM Size**: Limited DOM snapshot may miss context for complex pages
- **Healing Success Rate**: Depends on DOM structure and LLM accuracy
- **Performance**: Healing adds latency (typically 2-5 seconds per attempt)

## 🤝 Contributing

Contributions welcome! Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

Areas for improvement:
- Add more self-healing methods (hover, select, etc.)
- Implement selector caching to reduce API calls
- Add metrics and success rate tracking
- Support for async Playwright API

## � Documentation

Comprehensive documentation is available in the [docs/](docs/) directory:
- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Codebase organization
- [Organization Summary](docs/ORGANIZATION_SUMMARY.md) - Workspace organization details

## �📄 License

MIT License - feel free to use in your projects!

## 🆘 Troubleshooting

**Issue**: `ValueError: Azure OpenAI endpoint must be provided`
- **Solution**: Ensure `.env` file exists with correct credentials

**Issue**: Healing always fails
- **Solution**: Increase `dom_limit` or check if element exists in captured DOM

**Issue**: High API costs
- **Solution**: Implement selector caching or reduce healing attempts

## 📚 Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Self-Healing Test Automation Patterns](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
