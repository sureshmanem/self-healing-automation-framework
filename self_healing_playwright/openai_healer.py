"""
OpenAI Healer Module
Self-healing selector repair using Azure OpenAI
"""
import os
from typing import Optional
from openai import AzureOpenAI


class OpenAIHealer:
    """
    A self-healing assistant that uses Azure OpenAI to suggest corrected selectors
    when UI elements are not found in Playwright automation.
    """
    
    def __init__(
        self,
        azure_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = "2024-02-15-preview",
        deployment_name: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.2,
        max_tokens: int = 500
    ):
        """
        Initialize the OpenAI Healer with Azure OpenAI credentials.
        
        Args:
            azure_endpoint: Azure OpenAI endpoint URL (defaults to AZURE_OPENAI_ENDPOINT env var)
            api_key: Azure OpenAI API key (defaults to AZURE_OPENAI_API_KEY env var)
            api_version: API version for Azure OpenAI
            deployment_name: Deployment name (defaults to AZURE_OPENAI_DEPLOYMENT env var)
            model: Model name (fallback if deployment_name not provided)
            temperature: Controls randomness (0-1, lower is more deterministic)
            max_tokens: Maximum tokens in response
        """
        self.azure_endpoint = azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.api_version = api_version
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        if not self.azure_endpoint:
            raise ValueError(
                "Azure OpenAI endpoint must be provided via parameter or "
                "AZURE_OPENAI_ENDPOINT environment variable"
            )
        
        if not self.api_key:
            raise ValueError(
                "Azure OpenAI API key must be provided via parameter or "
                "AZURE_OPENAI_API_KEY environment variable"
            )
        
        if not self.deployment_name:
            raise ValueError(
                "Azure OpenAI deployment name must be provided via parameter or "
                "AZURE_OPENAI_DEPLOYMENT environment variable"
            )
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
    
    def get_new_selector(
        self,
        old_selector: str,
        dom_chunk: str,
        error_msg: str
    ) -> str:
        """
        Request a corrected selector from Azure OpenAI based on the failed selector,
        DOM snapshot, and error message.
        
        Args:
            old_selector: The selector that failed to locate the element
            dom_chunk: A portion of the page's HTML DOM
            error_msg: The error message from Playwright
        
        Returns:
            str: A new selector suggested by the LLM
        
        Raises:
            Exception: If the API call fails or returns invalid response
        """
        # Construct a detailed prompt for the LLM
        system_prompt = """Act as a Senior QA Engineer and Playwright expert.
Your job is to analyze failed selectors and suggest corrected ones based on the DOM structure.

Rules:
- Return ONLY the corrected selector string, nothing else
- Prefer CSS selectors or text-based selectors
- Ensure the selector is specific and unlikely to match multiple elements
- Consider common issues: dynamic IDs, changed class names, restructured DOM
- Use Playwright-specific selectors when appropriate (text=, role=, etc.)
"""
        
        user_prompt = f"""The following selector FAILED:
Selector: {old_selector}

Error Message:
{error_msg}

DOM Snapshot (partial):
{dom_chunk}

Analyze the DOM and provide a corrected selector that would likely work.
Return ONLY the selector string."""
        
        try:
            # Call Azure OpenAI API
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract the new selector from response
            new_selector = response.choices[0].message.content.strip()
            
            # Clean up the response (remove quotes if LLM wrapped it)
            new_selector = new_selector.strip('"\'`')
            
            return new_selector
            
        except Exception as e:
            raise Exception(f"Failed to get new selector from Azure OpenAI: {str(e)}")
