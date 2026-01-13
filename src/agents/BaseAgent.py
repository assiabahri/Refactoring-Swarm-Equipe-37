import google.generativeai as genai
from typing import Dict, List, Optional
from src.prompts.PromptEngineer import PromptEngineer
from src.utils.logger import log_experiment, ActionType
 

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize base agent with API configuration.
        
        Args:
            api_key: Google API key
            model_name: Gemini model to use
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        self.prompt_engineer = PromptEngineer(prompts_dir="src/prompts")
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with a prompt.
        
        Args:
            prompt: Formatted prompt string
            
        Returns:
            LLM response text
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ LLM call failed: {str(e)}")
            return f"ERROR: {str(e)}"
