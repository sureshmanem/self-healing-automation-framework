"""
SafePage Module
Self-healing Playwright Page wrapper with automatic selector correction
"""
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from .openai_healer import OpenAIHealer


class SafePage:
    """
    A wrapper around Playwright's Page object that adds self-healing capabilities.
    When selectors fail, it automatically attempts to find corrected selectors using AI.
    """
    
    def __init__(self, page: Page, healer: OpenAIHealer, dom_limit: int = 2000):
        """
        Initialize SafePage with a Playwright Page and OpenAI Healer.
        
        Args:
            page: Playwright Page object to wrap
            healer: OpenAIHealer instance for selector correction
            dom_limit: Maximum characters of DOM to send to LLM (default: 2000)
        """
        self.page = page
        self.healer = healer
        self.dom_limit = dom_limit
    
    def _get_dom_snapshot(self) -> str:
        """
        Capture a snapshot of the current page's HTML content.
        
        Returns:
            str: Limited portion of the page HTML
        """
        try:
            full_html = self.page.content()
            return full_html[:self.dom_limit]
        except Exception as e:
            return f"<error capturing DOM: {str(e)}>"
    
    def click(self, selector: str, timeout: float = 30000, **kwargs) -> None:
        """
        Click an element with self-healing capability.
        
        If the initial selector fails, automatically requests a corrected selector
        from the AI healer and retries the click operation.
        
        Args:
            selector: CSS selector, text selector, or other Playwright selector
            timeout: Maximum time to wait for element in milliseconds (default: 30000)
            **kwargs: Additional keyword arguments to pass to page.click()
        
        Raises:
            Exception: If both original and healed selectors fail
        """
        try:
            # First attempt: use the original selector
            self.page.click(selector, timeout=timeout, **kwargs)
            
        except PlaywrightTimeoutError as e:
            # Selector failed - initiate self-healing
            error_msg = str(e)
            print(f"[HEALING] Original selector failed: {selector}")
            print(f"[HEALING] Error: {error_msg}")
            
            # Get DOM snapshot
            dom_chunk = self._get_dom_snapshot()
            
            # Request corrected selector from AI
            try:
                new_selector = self.healer.get_new_selector(
                    old_selector=selector,
                    dom_chunk=dom_chunk,
                    error_msg=error_msg
                )
                
                print(f"[HEALING] AI suggested new selector: {new_selector}")
                
                # Retry with the new selector
                self.page.click(new_selector, timeout=timeout, **kwargs)
                
                # Success!
                print(f"HEALED: replaced '{selector}' with '{new_selector}'")
                
            except Exception as healing_error:
                # Healing failed
                raise Exception(
                    f"Self-healing failed. Original selector: '{selector}', "
                    f"Suggested selector: '{new_selector}', "
                    f"Error: {str(healing_error)}"
                )
        
        except Exception as e:
            # Some other error occurred
            raise Exception(f"Click failed for selector '{selector}': {str(e)}")
    
    def fill(self, selector: str, value: str, timeout: float = 30000, **kwargs) -> None:
        """
        Fill an input element with self-healing capability.
        
        Args:
            selector: CSS selector, text selector, or other Playwright selector
            value: Text to fill into the input
            timeout: Maximum time to wait for element in milliseconds (default: 30000)
            **kwargs: Additional keyword arguments to pass to page.fill()
        
        Raises:
            Exception: If both original and healed selectors fail
        """
        try:
            # First attempt: use the original selector
            self.page.fill(selector, value, timeout=timeout, **kwargs)
            
        except PlaywrightTimeoutError as e:
            # Selector failed - initiate self-healing
            error_msg = str(e)
            print(f"[HEALING] Original selector failed: {selector}")
            print(f"[HEALING] Error: {error_msg}")
            
            # Get DOM snapshot
            dom_chunk = self._get_dom_snapshot()
            
            # Request corrected selector from AI
            try:
                new_selector = self.healer.get_new_selector(
                    old_selector=selector,
                    dom_chunk=dom_chunk,
                    error_msg=error_msg
                )
                
                print(f"[HEALING] AI suggested new selector: {new_selector}")
                
                # Retry with the new selector
                self.page.fill(new_selector, value, timeout=timeout, **kwargs)
                
                # Success!
                print(f"HEALED: replaced '{selector}' with '{new_selector}'")
                
            except Exception as healing_error:
                # Healing failed
                raise Exception(
                    f"Self-healing failed. Original selector: '{selector}', "
                    f"Suggested selector: '{new_selector}', "
                    f"Error: {str(healing_error)}"
                )
        
        except Exception as e:
            # Some other error occurred
            raise Exception(f"Fill failed for selector '{selector}': {str(e)}")
    
    def goto(self, url: str, **kwargs):
        """Navigate to a URL (pass-through to underlying page)."""
        return self.page.goto(url, **kwargs)
    
    def wait_for_selector(self, selector: str, **kwargs):
        """Wait for a selector (pass-through to underlying page)."""
        return self.page.wait_for_selector(selector, **kwargs)
    
    def locator(self, selector: str, **kwargs):
        """Get a locator (pass-through to underlying page)."""
        return self.page.locator(selector, **kwargs)
    
    @property
    def url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    def screenshot(self, **kwargs):
        """Take a screenshot (pass-through to underlying page)."""
        return self.page.screenshot(**kwargs)
    
    def close(self):
        """Close the page (pass-through to underlying page)."""
        return self.page.close()
