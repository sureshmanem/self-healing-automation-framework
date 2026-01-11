"""
Example Usage of Self-Healing Playwright Framework
Demonstrates how to use SafePage with OpenAIHealer for robust test automation
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from playwright.sync_api import sync_playwright
from self_healing_playwright import OpenAIHealer, SafePage
from dotenv import load_dotenv


def example_basic_usage():
    """
    Basic example showing self-healing click action.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize the OpenAI Healer
    healer = OpenAIHealer(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        temperature=0.2  # Low temperature for deterministic results
    )
    
    # Start Playwright
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Wrap the page with SafePage for self-healing capabilities
        safe_page = SafePage(page=page, healer=healer)
        
        try:
            # Navigate to a website
            safe_page.goto("https://example.com")
            
            # This selector might be outdated or incorrect
            # If it fails, SafePage will automatically heal it
            safe_page.click("#outdated-button-id")
            
            print("✓ Test completed successfully!")
            
        except Exception as e:
            print(f"✗ Test failed: {e}")
        
        finally:
            browser.close()


def example_form_filling():
    """
    Example showing self-healing for form filling operations.
    """
    load_dotenv()
    
    healer = OpenAIHealer(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        safe_page = SafePage(page=page, healer=healer)
        
        try:
            # Navigate to a form page
            safe_page.goto("https://www.example-forms.com/login")
            
            # These selectors will self-heal if they fail
            safe_page.fill("#username", "test_user@example.com")
            safe_page.fill("#password", "secure_password_123")
            safe_page.click("button[type='submit']")
            
            print("✓ Form submitted successfully!")
            
        except Exception as e:
            print(f"✗ Form submission failed: {e}")
        
        finally:
            browser.close()


def example_with_explicit_timeout():
    """
    Example showing custom timeout configuration.
    """
    load_dotenv()
    
    healer = OpenAIHealer()  # Uses environment variables
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Configure SafePage with custom DOM limit
        safe_page = SafePage(page=page, healer=healer, dom_limit=3000)
        
        try:
            safe_page.goto("https://slow-loading-site.com")
            
            # Use custom timeout (10 seconds instead of default 30)
            safe_page.click(".dynamic-button", timeout=10000)
            
            print("✓ Action completed!")
            
        except Exception as e:
            print(f"✗ Action failed: {e}")
        
        finally:
            browser.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Self-Healing Playwright Framework - Example Usage")
    print("=" * 60)
    
    # Run basic example
    print("\n[Example 1] Basic self-healing click")
    print("-" * 60)
    example_basic_usage()
    
    # Uncomment to run other examples:
    # print("\n[Example 2] Form filling with self-healing")
    # print("-" * 60)
    # example_form_filling()
    
    # print("\n[Example 3] Custom timeout configuration")
    # print("-" * 60)
    # example_with_explicit_timeout()
