import google.generativeai as genai
from typing import Dict, List, Optional
from src.prompts.PromptEngineer import PromptEngineer
from src.utils.logger import log_experiment, ActionType
from .BaseAgent import BaseAgent

class FixerAgent(BaseAgent):
    """
    Fixer Agent - Applies refactoring changes to code
    """
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.agent_name = "Fixer_Agent"
    
    def fix_file(self,
                 file_path: str,
                 file_content: str,
                 refactoring_plan: List[Dict],
                 previous_errors: Optional[List[str]] = None) -> Dict:
        """
        Fix a file according to refactoring plan.
        
        Args:
            file_path: Path to file to fix
            file_content: Current file content
            refactoring_plan: List of refactoring steps
            previous_errors: Optional errors from previous attempts
            
        Returns:
            Dict with 'success', 'fixed_code', 'summary' keys
        """
        # Format prompt
        prompt = self.prompt_engineer.format_fixer_prompt(
            file_path=file_path,
            file_content=file_content,
            refactoring_plan=refactoring_plan,
            previous_errors=previous_errors
        )
        
        print(f"🔧 Fixer working on {file_path}...")
        
        # Call LLM
        response = self._call_llm(prompt)
        
        # The response should be the fixed code (not JSON for fixer)
        # But we'll try to extract JSON if it's wrapped
        fixed_code = response.strip()
        
        # Remove code block markers if present
        if fixed_code.startswith("```python"):
            fixed_code = fixed_code[9:]
        elif fixed_code.startswith("```"):
            fixed_code = fixed_code[3:]
        
        if fixed_code.endswith("```"):
            fixed_code = fixed_code[:-3]
        
        fixed_code = fixed_code.strip()
        
        # Log the interaction
        log_experiment(
            agent_name=self.agent_name,
            model_used=self.model_name,
            action=ActionType.FIX,
            details={
                "file_fixed": file_path,
                "input_prompt": prompt,
                "output_response": response,
                "refactoring_steps": len(refactoring_plan),
                "had_previous_errors": bool(previous_errors)
            },
            status="SUCCESS"
        )
        
        return {
            "success": True,
            "fixed_code": fixed_code,
            "raw_response": response
        }
    
    def fix_from_test_errors(self,
                           file_path: str,
                           file_content: str,
                           test_output: str,
                           test_statistics: Dict) -> Dict:
        """
        Fix file based on test failure output.
        
        Args:
            file_path: Path to file
            file_content: Current content
            test_output: Pytest output
            test_statistics: Test stats
            
        Returns:
            Dict with fixed code
        """
        # Format prompt
        prompt = self.prompt_engineer.format_fixer_prompt_from_test_errors(
            file_path=file_path,
            file_content=file_content,
            test_output=test_output,
            test_statistics=test_statistics
        )
        
        print(f"🔧 Fixer addressing test failures in {file_path}...")
        
        # Call LLM
        response = self._call_llm(prompt)
        
        # Extract code
        fixed_code = response.strip()
        if fixed_code.startswith("```python"):
            fixed_code = fixed_code[9:]
        elif fixed_code.startswith("```"):
            fixed_code = fixed_code[3:]
        if fixed_code.endswith("```"):
            fixed_code = fixed_code[:-3]
        fixed_code = fixed_code.strip()
        
        # Log
        log_experiment(
            agent_name=self.agent_name,
            model_used=self.model_name,
            action=ActionType.FIX,
            details={
                "file_fixed": file_path,
                "input_prompt": prompt,
                "output_response": response,
                "tests_failed": test_statistics.get("failed", 0)
            },
            status="SUCCESS"
        )
        
        return {
            "success": True,
            "fixed_code": fixed_code,
            "raw_response": response
        }