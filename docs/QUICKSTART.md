# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Clone and Install
```bash
git clone <repository-url>
cd self-healing-automation-framework
make install  # Or: pip install -r requirements.txt && playwright install chromium
```

### Step 2: Configure Azure OpenAI
```bash
cp .env.example .env
```

Edit `.env` file with your credentials:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

### Step 3: Write Your First Self-Healing Test
Create `my_test.py`:

```python
from playwright.sync_api import sync_playwright
from self_healing_playwright import OpenAIHealer, SafePage
from dotenv import load_dotenv

load_dotenv()

# Initialize the healer
healer = OpenAIHealer()

# Use with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Wrap page with self-healing capabilities
    safe_page = SafePage(page=page, healer=healer)
    
    # Navigate and interact - selectors auto-heal if they fail!
    safe_page.goto("https://example.com")
    safe_page.click("#my-button")  # Will heal if selector breaks
    safe_page.fill("#username", "test@example.com")
    
    browser.close()
```

### Step 4: Run Your Test
```bash
python my_test.py
```

## 🎯 Key Features

### Auto-Healing Click
```python
# If this selector breaks, AI will find the correct one
safe_page.click("#old-selector")
# Output: HEALED: replaced '#old-selector' with 'button[data-testid="submit"]'
```

### Auto-Healing Form Fill
```python
safe_page.fill("#email-input", "user@example.com")
# Heals automatically if selector changes
```

### Custom Configuration
```python
# Adjust healing parameters
healer = OpenAIHealer(
    temperature=0.1,      # More deterministic
    max_tokens=300        # Faster responses
)

# Adjust DOM snapshot size
safe_page = SafePage(
    page=page,
    healer=healer,
    dom_limit=3000       # Send more context to AI
)
```

## 🧪 Run Examples
```bash
make run-example
# Or: python examples/example_usage.py
```

## ✅ Run Tests
```bash
make test
# Or: python -m pytest tests/ -v
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [examples/example_usage.py](examples/example_usage.py) for more patterns
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. Explore extending SafePage with more self-healing methods

## 🆘 Common Issues

**Issue**: Import errors
```bash
# Solution: Make sure you're in the project directory
cd self-healing-automation-framework
python3 -c "from self_healing_playwright import OpenAIHealer, SafePage"
```

**Issue**: Playwright not installed
```bash
# Solution: Install browsers
playwright install chromium
```

**Issue**: Azure OpenAI errors
```bash
# Solution: Check your .env file has correct credentials
cat .env
```

## 💡 Pro Tips

1. **Lower temperature** (0.1-0.3) for more consistent healing
2. **Monitor API costs** - each healing call uses tokens
3. **Use descriptive selectors** to help AI understand context
4. **Review healing logs** to identify flaky selectors
5. **Cache healed selectors** in production (future feature)

Happy Testing! 🎉
