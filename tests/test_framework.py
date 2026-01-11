"""
Unit Tests for Self-Healing Playwright Framework
"""
import sys
from pathlib import Path

# Add parent directory to path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from unittest.mock import Mock, patch, MagicMock
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from self_healing_playwright import OpenAIHealer, SafePage


class TestOpenAIHealer(unittest.TestCase):
    """Test cases for OpenAIHealer class"""
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4'
    })
    def test_initialization_with_env_vars(self):
        """Test healer initializes correctly with environment variables"""
        healer = OpenAIHealer()
        self.assertEqual(healer.azure_endpoint, 'https://test.openai.azure.com/')
        self.assertEqual(healer.api_key, 'test-key')
        self.assertEqual(healer.deployment_name, 'gpt-4')
    
    def test_initialization_with_parameters(self):
        """Test healer initializes correctly with explicit parameters"""
        healer = OpenAIHealer(
            azure_endpoint='https://custom.openai.azure.com/',
            api_key='custom-key',
            deployment_name='custom-deployment'
        )
        self.assertEqual(healer.azure_endpoint, 'https://custom.openai.azure.com/')
        self.assertEqual(healer.api_key, 'custom-key')
        self.assertEqual(healer.deployment_name, 'custom-deployment')
    
    @patch.dict('os.environ', {}, clear=True)
    def test_initialization_fails_without_credentials(self):
        """Test healer raises error when credentials missing"""
        with self.assertRaises(ValueError):
            OpenAIHealer()
    
    @patch('self_healing_playwright.openai_healer.AzureOpenAI')
    def test_get_new_selector_success(self, mock_azure_client):
        """Test successful selector correction"""
        # Mock Azure OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = 'button[data-testid="submit"]'
        
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_azure_client.return_value = mock_client_instance
        
        healer = OpenAIHealer(
            azure_endpoint='https://test.openai.azure.com/',
            api_key='test-key',
            deployment_name='gpt-4'
        )
        
        new_selector = healer.get_new_selector(
            old_selector='#old-button',
            dom_chunk='<html><body><button data-testid="submit">Click</button></body></html>',
            error_msg='Timeout exceeded'
        )
        
        self.assertEqual(new_selector, 'button[data-testid="submit"]')
    
    @patch('self_healing_playwright.openai_healer.AzureOpenAI')
    def test_get_new_selector_removes_quotes(self, mock_azure_client):
        """Test that healer removes surrounding quotes from response"""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '"button.submit-btn"'
        
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_response
        mock_azure_client.return_value = mock_client_instance
        
        healer = OpenAIHealer(
            azure_endpoint='https://test.openai.azure.com/',
            api_key='test-key',
            deployment_name='gpt-4'
        )
        
        new_selector = healer.get_new_selector(
            old_selector='#old',
            dom_chunk='<html></html>',
            error_msg='Error'
        )
        
        self.assertEqual(new_selector, 'button.submit-btn')


class TestSafePage(unittest.TestCase):
    """Test cases for SafePage class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_page = Mock()
        self.mock_healer = Mock(spec=OpenAIHealer)
        self.safe_page = SafePage(
            page=self.mock_page,
            healer=self.mock_healer,
            dom_limit=2000
        )
    
    def test_click_success_no_healing(self):
        """Test click succeeds without needing healing"""
        self.mock_page.click = Mock()
        
        self.safe_page.click('#button')
        
        self.mock_page.click.assert_called_once_with('#button', timeout=30000)
        self.mock_healer.get_new_selector.assert_not_called()
    
    def test_click_triggers_healing_on_timeout(self):
        """Test click triggers healing when selector fails"""
        # First call raises timeout, second call succeeds
        self.mock_page.click = Mock(side_effect=[
            PlaywrightTimeoutError('Timeout exceeded'),
            None
        ])
        self.mock_page.content = Mock(return_value='<html><body>content</body></html>')
        self.mock_healer.get_new_selector = Mock(return_value='button.new-selector')
        
        self.safe_page.click('#old-button')
        
        # Verify healing was triggered
        self.mock_healer.get_new_selector.assert_called_once()
        # Verify click was retried with new selector
        self.assertEqual(self.mock_page.click.call_count, 2)
        second_call_args = self.mock_page.click.call_args_list[1]
        self.assertEqual(second_call_args[0][0], 'button.new-selector')
    
    def test_fill_success_no_healing(self):
        """Test fill succeeds without needing healing"""
        self.mock_page.fill = Mock()
        
        self.safe_page.fill('#input', 'test value')
        
        self.mock_page.fill.assert_called_once_with('#input', 'test value', timeout=30000)
        self.mock_healer.get_new_selector.assert_not_called()
    
    def test_fill_triggers_healing_on_timeout(self):
        """Test fill triggers healing when selector fails"""
        self.mock_page.fill = Mock(side_effect=[
            PlaywrightTimeoutError('Timeout exceeded'),
            None
        ])
        self.mock_page.content = Mock(return_value='<html><body>content</body></html>')
        self.mock_healer.get_new_selector = Mock(return_value='input[name="username"]')
        
        self.safe_page.fill('#old-input', 'test data')
        
        self.mock_healer.get_new_selector.assert_called_once()
        self.assertEqual(self.mock_page.fill.call_count, 2)
    
    def test_get_dom_snapshot_limits_content(self):
        """Test DOM snapshot is limited to configured size"""
        long_html = 'a' * 5000
        self.mock_page.content = Mock(return_value=long_html)
        
        snapshot = self.safe_page._get_dom_snapshot()
        
        self.assertEqual(len(snapshot), 2000)
        self.assertEqual(snapshot, 'a' * 2000)
    
    def test_passthrough_methods(self):
        """Test that pass-through methods call underlying page"""
        self.mock_page.goto = Mock()
        self.mock_page.wait_for_selector = Mock()
        self.mock_page.screenshot = Mock()
        self.mock_page.close = Mock()
        
        self.safe_page.goto('https://example.com')
        self.safe_page.wait_for_selector('#element')
        self.safe_page.screenshot(path='test.png')
        self.safe_page.close()
        
        self.mock_page.goto.assert_called_once()
        self.mock_page.wait_for_selector.assert_called_once()
        self.mock_page.screenshot.assert_called_once()
        self.mock_page.close.assert_called_once()
    
    def test_url_property(self):
        """Test URL property returns page URL"""
        self.mock_page.url = 'https://example.com/page'
        
        url = self.safe_page.url
        
        self.assertEqual(url, 'https://example.com/page')


if __name__ == '__main__':
    unittest.main()
