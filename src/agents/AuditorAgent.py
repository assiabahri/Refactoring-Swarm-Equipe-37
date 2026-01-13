import google.generativeai as genai
from typing import Dict, List, Optional
from src.prompts.PromptEngineer import PromptEngineer
from src.utils.logger import log_experiment, ActionType
from .BaseAgent import BaseAgent


class AuditorAgent(BaseAgent):
    """
    Auditor Agent - Analyzes code and creates refactoring plans
    """
   
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.agent_name = "Auditor_Agent"
   
    def analyze_file(self,
                     file_path: str,
                     file_content: str,
                     pylint_result: Optional[Dict] = None) -> Dict:
        """
        Analyze a single file and produce refactoring recommendations.
       
        Args:
            file_path: Path to file
            file_content: Content of the file
            pylint_result: Optional pylint analysis
           
        Returns:
            Dict with 'success', 'analysis', 'raw_response' keys
        """
        # Format prompt
        prompt = self.prompt_engineer.format_auditor_prompt(
            file_path=file_path,
            file_content=file_content,
            pylint_result=pylint_result
        )
       
        print(f"🔍 Auditor analyzing {file_path}...")
       
        # Call LLM
        response = self._call_llm(prompt)
       
        # Parse JSON response
        analysis = self.prompt_engineer.extract_json_from_response(response)
       
        # Extract issues count safely
        issues_found = 0
        if analysis is not None:
            # Try multiple ways to get issues count
            if "issues" in analysis:
                issues_found = len(analysis["issues"])
            elif "total_issues" in analysis:
                issues_found = analysis["total_issues"]
            elif "refactoring_plan" in analysis:
                issues_found = len(analysis["refactoring_plan"])
       
        # Get pylint score safely
        pylint_score = None
        if pylint_result and isinstance(pylint_result, dict):
            pylint_score = pylint_result.get("score")
       
        # Log the interaction
        log_experiment(
            agent_name=self.agent_name,
            model_used=self.model_name,
            action=ActionType.ANALYSIS,
            details={
                "file_analyzed": file_path,
                "input_prompt": prompt,
                "output_response": response,
                "pylint_score": pylint_score,
                "issues_found": issues_found,
                "analysis_success": analysis is not None
            },
            status="SUCCESS" if analysis else "FAILURE"
        )
       
        if analysis:
            print(f"✅ Found {issues_found} issues in {file_path}")
            return {
                "success": True,
                "analysis": analysis,
                "raw_response": response,
                "issues_found": issues_found
            }
        else:
            print(f"❌ Failed to parse analysis for {file_path}")
           
            # Try to extract some information from raw response as fallback
            estimated_issues = 0
            if response and ("error" in response.lower() or "issue" in response.lower()):
                estimated_issues = 1
           
            return {
                "success": False,
                "error": "Failed to parse JSON response from LLM",
                "analysis": None,
                "raw_response": response,
                "issues_found": estimated_issues,
                "partial_data": {
                    "has_syntax_error": "syntax" in response.lower(),
                    "response_preview": response[:200] if response else "Empty response"
                }
            }
   
    def analyze_codebase(self,
                        files_info: List[Dict],
                        pylint_results: List[Dict]) -> Dict:
        """
        Analyze entire codebase and create prioritized refactoring plan.
       
        Args:
            files_info: List of file information
            pylint_results: List of pylint results
           
        Returns:
            Dict with overall analysis and plan
        """
        # Format prompt for directory analysis
        prompt = self.prompt_engineer.format_auditor_prompt_for_directory(
            files_info=files_info,
            pylint_results=pylint_results
        )
       
        print(f"🔍 Auditor analyzing {len(files_info)} files...")
       
        # Call LLM
        response = self._call_llm(prompt)
       
        # Parse response
        analysis = self.prompt_engineer.extract_json_from_response(response)
       
        # Extract file names safely
        file_names = []
        for f in files_info:
            if isinstance(f, dict):
                rel_path = f.get("relative_path", "Unknown")
                file_names.append(rel_path)
       
        # Log
        log_experiment(
            agent_name=self.agent_name,
            model_used=self.model_name,
            action=ActionType.ANALYSIS,
            details={
                "files_analyzed": file_names,
                "total_files": len(files_info),
                "input_prompt": prompt[:500] + "..." if len(prompt) > 500 else prompt,
                "output_response": response[:500] + "..." if len(response) > 500 else response,
                "analysis_success": analysis is not None
            },
            status="SUCCESS" if analysis else "FAILURE"
        )
       
        if analysis:
            print(f"✅ Codebase analysis completed successfully")
            return {
                "success": True,
                "analysis": analysis,
                "raw_response": response,
                "files_analyzed": len(files_info)
            }
        else:
            print(f"❌ Failed to parse codebase analysis")
            return {
                "success": False,
                "error": "Failed to parse JSON response for codebase analysis",
                "analysis": None,
                "raw_response": response,
                "files_analyzed": len(files_info)
            }
   
    def analyze_file_with_fallback(self,
                                 file_path: str,
                                 file_content: str,
                                 pylint_result: Optional[Dict] = None) -> Dict:
        """
        Analyze a file with multiple fallback strategies if JSON parsing fails.
       
        Args:
            file_path: Path to file
            file_content: Content of the file
            pylint_result: Optional pylint analysis
           
        Returns:
            Dict with analysis, even if minimal
        """
        # First try standard analysis
        result = self.analyze_file(file_path, file_content, pylint_result)
       
        # If successful, return as-is
        if result["success"]:
            return result
       
        # If failed, create a minimal analysis from available data
        print(f"⚠️  Using fallback analysis for {file_path}")
       
        # Extract any useful info from pylint result
        issues = []
        if pylint_result and pylint_result.get("success"):
            pylint_issues = pylint_result.get("issues", [])
            for issue in pylint_issues[:5]:  # Top 5 issues
                issues.append({
                    "line": issue.get("line", 1),
                    "type": issue.get("type", "error"),
                    "message": issue.get("message", "Unknown issue"),
                    "priority": "high" if issue.get("type") == "error" else "medium"
                })
       
        # Create minimal refactoring plan
        refactoring_plan = []
        if pylint_result and pylint_result.get("success"):
            score = pylint_result.get("score", 10)
            if score < 8.0:
                refactoring_plan.append({
                    "step": "Fix syntax errors",
                    "rationale": "File has syntax errors preventing analysis",
                    "priority": "critical"
                })
       
        # If we have issues from pylint, add them to plan
        for issue in issues:
            refactoring_plan.append({
                "step": f"Fix {issue['type']} at line {issue['line']}",
                "rationale": issue["message"],
                "priority": issue["priority"]
            })
       
        # Create minimal analysis
        minimal_analysis = {
            "file": file_path,
            "status": "analyzed_with_fallback",
            "issues": issues,
            "refactoring_plan": refactoring_plan,
            "summary": "Analysis generated from pylint results due to LLM parsing failure",
            "total_issues": len(issues)
        }
       
        return {
            "success": True,
            "analysis": minimal_analysis,
            "raw_response": result.get("raw_response", ""),
            "issues_found": len(issues),
            "used_fallback": True
        }