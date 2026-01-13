import google.generativeai as genai
from typing import Dict, List, Optional
from src.prompts.PromptEngineer import PromptEngineer
from src.utils.logger import log_experiment, ActionType
from .BaseAgent import BaseAgent
class JudgeAgent(BaseAgent):
    """
    Judge Agent - Evaluates test results and decides if refactoring is complete
    """
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.agent_name = "Judge_Agent"
    
    def evaluate_tests(self,
                      test_output: str,
                      test_statistics: Dict,
                      previous_score: Optional[float] = None,
                      current_score: Optional[float] = None) -> Dict:
        """
        Evaluate test results and code quality.
        
        Args:
            test_output: Full pytest output
            test_statistics: Test statistics
            previous_score: Previous pylint score
            current_score: Current pylint score
            
        Returns:
            Dict with 'success', 'verdict', 'tests_passed', 'errors' keys
        """
        # Format prompt
        prompt = self.prompt_engineer.format_judge_prompt(
            test_output=test_output,
            test_statistics=test_statistics,
            previous_score=previous_score,
            current_score=current_score
        )
        
        print(f"⚖️  Judge evaluating test results...")
        
        # Call LLM
        response = self._call_llm(prompt)
        
        # Parse JSON response
        evaluation = self.prompt_engineer.extract_json_from_response(response)
        
        # Log
        log_experiment(
            agent_name=self.agent_name,
            model_used=self.model_name,
            action=ActionType.DEBUG,
            details={
                "input_prompt": prompt,
                "output_response": response,
                "tests_passed": test_statistics.get("passed", 0),
                "tests_failed": test_statistics.get("failed", 0),
                "quality_improvement": (current_score - previous_score) 
                if (previous_score is not None and current_score is not None) 
                else None
            },
            status="SUCCESS" if evaluation else "FAILURE"
        )
        
        if evaluation:
            tests_passed = evaluation.get("tests_passed", False)
            print(f"{'✅' if tests_passed else '❌'} Judge verdict: {'PASS' if tests_passed else 'NEEDS MORE WORK'}")
            
            return {
                "success": True,
                "verdict": evaluation,
                "tests_passed": tests_passed,
                "errors": evaluation.get("errors", []),
                "raw_response": response
            }
        else:
            print(f"❌ Failed to parse judge evaluation")
            return {
                "success": False,
                "error": "Failed to parse JSON response",
                "raw_response": response
            }
    
    def should_continue(self, evaluation: Dict) -> bool:
        """
        Determine if the refactoring loop should continue.
        
        Args:
            evaluation: Evaluation dict from evaluate_tests
            
        Returns:
            True if should continue fixing, False if complete
        """
        if not evaluation.get("success"):
            return True  # Continue if evaluation failed
        
        return not evaluation.get("tests_passed", False)
