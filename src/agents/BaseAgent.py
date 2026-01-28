import google.generativeai as genai
from typing import Dict, List, Optional
from src.prompts.PromptEngineer import PromptEngineer
from src.utils.logger import log_experiment, ActionType
from groq import Groq
 

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initialize base agent with API configuration.
        
        Args:
            api_key: Google API key
            model_name: Gemini model to use
        """
        self.client = Groq(api_key=api_key)
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Groq API call failed: {str(e)}")
            return f"ERROR: {str(e)}"