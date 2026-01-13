"""
Prompt Engineer Module
Manages system prompts for all agents and formats them with context
Location: src/utils/prompts.py
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class PromptEngineer:
    """
    Manages and formats prompts for the Refactoring Swarm agents.
    Loads prompt templates from files and injects context dynamically.
    """
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize the Prompt Engineer.
        
        Args:
            prompts_dir: Directory containing prompt template files
        """
        self.prompts_dir = Path(prompts_dir)
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all prompt templates from files"""
        template_files = {
            "auditor": "auditor_prompt.txt",
            "fixer": "fixer_prompt.txt",
            "judge": "judge_prompt.txt"
        }
        
        for agent_name, filename in template_files.items():
            filepath = self.prompts_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.templates[agent_name] = f.read()
                print(f"✅ Loaded {agent_name} prompt template")
            else:
                print(f"⚠️  Warning: {filename} not found at {filepath}")
                self.templates[agent_name] = ""
    
    # ==================== AUDITOR PROMPTS ====================
    
    def format_auditor_prompt(self, 
                             file_path: str, 
                             file_content: str,
                             pylint_result: Optional[Dict] = None) -> str:
        """
        Format the Auditor prompt with file context.
        
        Args:
            file_path: Path to the file being analyzed
            file_content: Content of the file
            pylint_result: Optional pylint analysis results
            
        Returns:
            Formatted prompt string ready to send to LLM
        """
        base_prompt = self.templates.get("auditor", "")
        
        # Build context section
        context = f"""
FILE PATH: {file_path}

FILE CONTENT:
```python
{file_content}
```
"""
        
        # Add pylint results if available
        if pylint_result and pylint_result.get("success"):
            score = pylint_result.get("score", "N/A")
            issues = pylint_result.get("categorized", {})
            
            context += f"""

PYLINT ANALYSIS:
- Current Score: {score}/10
- Errors: {len(issues.get('error', []))}
- Warnings: {len(issues.get('warning', []))}
- Conventions: {len(issues.get('convention', []))}
- Refactor suggestions: {len(issues.get('refactor', []))}

TOP ISSUES:
"""
            # Add top 5 issues
            all_issues = pylint_result.get("issues", [])
            for i, issue in enumerate(all_issues[:5], 1):
                context += f"{i}. Line {issue.get('line', '?')}: {issue.get('message', 'Unknown')}\n"
        
        # Combine base prompt with context
        full_prompt = f"{base_prompt}\n\n{context}\n\nProvide your analysis as JSON:"
        
        return full_prompt
    
    def format_auditor_prompt_for_directory(self,
                                           files_info: List[Dict],
                                           pylint_results: List[Dict]) -> str:
        """
        Format Auditor prompt for analyzing multiple files.
        
        Args:
            files_info: List of file information dicts
            pylint_results: List of pylint results for each file
            
        Returns:
            Formatted prompt for directory-level analysis
        """
        base_prompt = self.templates.get("auditor", "")
        
        context = "CODEBASE ANALYSIS:\n\n"
        
        # Add summary of each file
        for file_info, pylint_result in zip(files_info, pylint_results):
            file_path = file_info.get("relative_path", "Unknown")
            score = pylint_result.get("score", "N/A") if pylint_result.get("success") else "N/A"
            total_issues = pylint_result.get("total_issues", 0) if pylint_result.get("success") else 0
            
            context += f"""
FILE: {file_path}
- Pylint Score: {score}/10
- Total Issues: {total_issues}
- Size: {file_info.get('size', 0)} bytes
"""
        
        full_prompt = f"{base_prompt}\n\n{context}\n\nProvide a prioritized refactoring plan as JSON:"
        
        return full_prompt
    
    # ==================== FIXER PROMPTS ====================
    
    def format_fixer_prompt(self,
                           file_path: str,
                           file_content: str,
                           refactoring_plan: List[Dict],
                           previous_errors: Optional[List[str]] = None) -> str:
        """
        Format the Fixer prompt with refactoring instructions.
        
        Args:
            file_path: Path to file to fix
            file_content: Current content of the file
            refactoring_plan: List of refactoring steps from Auditor
            previous_errors: Optional list of errors from previous attempts
            
        Returns:
            Formatted prompt for code fixing
        """
        base_prompt = self.templates.get("fixer", "")
        
        # Build context
        context = f"""
FILE TO FIX: {file_path}

CURRENT CODE:
```python
{file_content}
```

REFACTORING PLAN:
"""
        
        # Add refactoring steps
        for i, step in enumerate(refactoring_plan, 1):
            context += f"{i}. {step.get('step', 'Fix issues')}\n"
            if 'rationale' in step:
                context += f"   Rationale: {step['rationale']}\n"
        
        # Add previous errors if this is a retry
        if previous_errors:
            context += "\n\nPREVIOUS ATTEMPT ERRORS:\n"
            for error in previous_errors:
                context += f"- {error}\n"
            context += "\nPlease fix these errors in addition to the refactoring plan.\n"
        
        context += """

IMPORTANT:
- Return ONLY the fixed code, no explanations or markdown
- Ensure all syntax errors are corrected
- Follow PEP 8 style guidelines
- Add proper docstrings where missing
- Fix all issues mentioned in the plan

Provide the complete fixed code:
"""
        
        full_prompt = f"{base_prompt}\n\n{context}"
        
        return full_prompt
    
    def format_fixer_prompt_from_test_errors(self,
                                            file_path: str,
                                            file_content: str,
                                            test_output: str,
                                            test_statistics: Dict) -> str:
        """
        Format Fixer prompt based on test failure output.
        
        Args:
            file_path: Path to file that failed tests
            file_content: Current file content
            test_output: Pytest output with errors
            test_statistics: Test statistics dict
            
        Returns:
            Formatted prompt for fixing test failures
        """
        base_prompt = self.templates.get("fixer", "")
        
        context = f"""
FILE TO FIX: {file_path}

CURRENT CODE:
```python
{file_content}
```

TEST RESULTS:
- Tests Passed: {test_statistics.get('passed', 0)}
- Tests Failed: {test_statistics.get('failed', 0)}
- Errors: {test_statistics.get('errors', 0)}

TEST OUTPUT:
```
{test_output}
```

TASK:
Analyze the test failures and fix the code to make all tests pass.
Focus on:
1. Logic errors causing test failures
2. Missing functionality
3. Edge cases not handled

Provide the complete fixed code:
"""
        
        full_prompt = f"{base_prompt}\n\n{context}"
        
        return full_prompt
    
    # ==================== JUDGE PROMPTS ====================
    
    def format_judge_prompt(
        self,
        test_output: str,
        test_statistics: Dict,
        previous_score: Optional[float] = None,
        current_score: Optional[float] = None
    ) -> str:
        """
        Format the Judge prompt with test results.
        """
        base_prompt = self.templates.get("judge", "")

        context = f"""
    TEST EXECUTION RESULTS:

    STATISTICS:
    - Tests Passed: {test_statistics.get('passed', 0)}
    - Tests Failed: {test_statistics.get('failed', 0)}
    - Errors: {test_statistics.get('errors', 0)}
    - Total Tests: {test_statistics.get('total', 0)}
    """

        # ===== SAFE SCORE HANDLING =====
        if previous_score is not None and current_score is not None:
            improvement = current_score - previous_score
            context += f"""
    CODE QUALITY METRICS:
    - Previous Pylint Score: {previous_score}/10
    - Current Pylint Score: {current_score}/10
    - Improvement: {improvement:+.2f} points
    """
        elif current_score is not None:
            # First iteration: no previous score
            context += f"""
    CODE QUALITY METRICS:
    - Current Pylint Score: {current_score}/10
    - Previous Pylint Score: N/A
    - Improvement: N/A
    """
        else:
            # No score at all (rare)
            context += """
    CODE QUALITY METRICS:
    - Pylint Score: N/A
    - Previous Pylint Score: N/A
    - Improvement: N/A
    """

        context += f"""

    TEST OUTPUT:


```
{test_output}
```


    TASK:
    Evaluate whether the refactoring is complete and successful.
    Analyze:
    1. Are all tests passing?
    2. If not, what are the critical errors?
    3. Is the code ready for production?

    Provide your evaluation as JSON:
    """
        
        full_prompt = f"{base_prompt}\n\n{context}"
        
        return full_prompt
    
    # ==================== UTILITY METHODS ====================
    
    def minimize_prompt_tokens(self, prompt: str, max_lines: int = 100) -> str:
        """
        Minimize prompt size by truncating long code sections.
        
        Args:
            prompt: Full prompt string
            max_lines: Maximum lines to keep in code blocks
            
        Returns:
            Truncated prompt
        """
        # Split into lines
        lines = prompt.split('\n')
        
        # If prompt is short enough, return as-is
        if len(lines) <= max_lines:
            return prompt
        
        # Keep first part and last part
        half = max_lines // 2
        truncated = lines[:half] + ["\n... [CODE TRUNCATED FOR BREVITY] ...\n"] + lines[-half:]
        
        return '\n'.join(truncated)
    
    def extract_json_from_response(self, response: str) -> Optional[Dict]:
        """
        Extract JSON from LLM response, handling markdown code blocks.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        # Remove markdown code blocks if present
        cleaned = response.strip()
        
        # Remove ```json and ``` markers
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        cleaned = cleaned.strip()
        
        # Try to parse JSON
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Response was: {cleaned[:200]}...")
            return None
    
    def get_template(self, agent_name: str) -> str:
        """
        Get raw template for an agent.
        
        Args:
            agent_name: Name of agent (auditor, fixer, judge)
            
        Returns:
            Template string
        """
        return self.templates.get(agent_name, "")
    
    def reload_templates(self):
        """Reload all templates from disk (useful for prompt iteration)"""
        self.templates.clear()
        self._load_templates()
        print("🔄 Prompt templates reloaded")

