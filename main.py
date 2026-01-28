"""
Main Entry Point for Refactoring Swarm
Orchestrates the complete workflow: Auditor -> Fixer -> Judge loop
Location: main.py (root of project)
"""

import os
import argparse
from dotenv import load_dotenv
from pathlib import Path
import traceback

# Import Toolsmith API
from src.ToolsmithAPI import ToolsmithAPI
 

# Import Agents
from src.agents.AuditorAgent import AuditorAgent
from src.agents.FixerAgent import FixerAgent
from src.agents.JudgeAgent import JudgeAgent

# Import Logging
from src.utils.logger import log_experiment, ActionType


class RefactoringOrchestrator:
    """
    Main orchestrator that coordinates the refactoring workflow.
    
    Workflow:
    1. Auditor analyzes all files and creates refactoring plan
    2. For each file:
        a. Fixer applies refactoring plan
        b. Judge runs tests and validates
        c. If tests fail, loop back to Fixer with errors
        d. Repeat until tests pass or max iterations reached
    """
    
    def __init__(self, api_key: str, target_dir: str, max_iterations: int = 10):
        """
        Initialize the orchestrator.
        
        Args:
            api_key: Google Gemini API key
            target_dir: Directory containing code to refactor
            max_iterations: Max iterations per file
        """
        self.target_dir = target_dir
        self.max_iterations = max_iterations
        
        # Initialize tools and agents
        self.tools = ToolsmithAPI(sandbox_root=target_dir)
        self.auditor = AuditorAgent(api_key=api_key)
        self.fixer = FixerAgent(api_key=api_key)
        self.judge = JudgeAgent(api_key=api_key)
        
        # State tracking
        self.files_processed = []
        self.total_iterations = 0
    
    def run(self):
        """Execute the complete refactoring workflow"""
        print("=" * 70)
        print("🐝 REFACTORING SWARM STARTED")
        print("=" * 70)
        print(f"📁 Target Directory: {self.target_dir}")
        print(f"🔄 Max Iterations: {self.max_iterations}")
        print()
        
        try:
            # Phase 1: Discovery & Analysis
            files_to_fix = self.phase_1_discovery()
            
            if not files_to_fix:
                print("✅ No files need refactoring!")
                return
            
            # Phase 2: Refactoring Loop
            self.phase_2_refactoring_loop(files_to_fix)
            
            # Phase 3: Final Validation
            self.phase_3_final_validation()
            
            print("\n" + "=" * 70)
            print("🎉 REFACTORING SWARM COMPLETED")
            print("=" * 70)
            print(f"📊 Files processed: {len(self.files_processed)}")
            print(f"🔄 Total iterations: {self.total_iterations}")
            print(f"📄 Logs: logs/experiment_data.json")
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {str(e)}")
            traceback.print_exc()
            log_experiment(
                agent_name="Orchestrator",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "error": str(e),
                    "input_prompt": "System orchestration",
                    "output_response": f"Critical error occurred: {str(e)}"
                },
                status="FAILURE"
            )
    
    def phase_1_discovery(self):
        """
        Phase 1: Discover files and run initial analysis.
        
        Returns:
            List of files that need refactoring
        """
        print("─" * 70)
        print("📋 PHASE 1: DISCOVERY & ANALYSIS")
        print("─" * 70)
        
        # Step 1: List all Python files
        print("\n🔍 Discovering Python files...")
        files_result = self.tools.list_python_files()
        
        if not files_result["success"]:
            print(f"❌ Failed to list files: {files_result.get('error')}")
            return []
        
        files = files_result["files"]
        print(f"✅ Found {len(files)} Python files")
        
        # Step 2: Run Pylint on each file
        print("\n🔬 Running static analysis...")
        pylint_results = []
        
        for file_info in files:
            file_path = file_info["path"]
            rel_path = file_info["relative_path"]
            
            # Skip test files for now (they'll be used for validation)
            if "test_" in rel_path or "/tests/" in rel_path:
                print(f"⏭️  Skipping test file: {rel_path}")
                continue
            
            # Run pylint
            pylint_result = self.tools.run_pylint(file_path)
            
            if pylint_result["success"]:
                score = pylint_result.get("score")
                issues = pylint_result.get("total_issues", 0)
                score_str = f"{score:>4.1f}" if score is not None else "N/A"
                print(f"📄 {rel_path:<40} | Score: {score_str}/10 | Issues: {issues:>3}")
                
                pylint_results.append({
                    "file_info": file_info,
                    "pylint_result": pylint_result
                })
            else:
                print(f"⚠️  {rel_path:<40} | Pylint failed")
        
        # Step 3: Auditor creates refactoring plan
        print("\n🔍 Auditor creating refactoring plan...")
        
        files_to_fix = []
        for item in pylint_results:
            file_info = item["file_info"]
            pylint_result = item["pylint_result"]
            
            # Only fix files with low scores or many issues
            score = pylint_result.get("score", 10)
            issues = pylint_result.get("total_issues", 0)
            if score is None:
                score = 10
            
            if score < 8.0 or issues > 5:
                # Read file content
                read_result = self.tools.read_file(file_info["path"])
                if not read_result["success"]:
                    continue
                
                # Auditor analyzes
                analysis_result = self.auditor.analyze_file_with_fallback(
                    file_path=file_info["relative_path"],
                    file_content=read_result["content"],
                    pylint_result=pylint_result
                )

                if analysis_result["success"] and analysis_result["analysis"] is not None:
                    files_to_fix.append({
                        "file_info": file_info,
                        "pylint_result": pylint_result,
                        "analysis": analysis_result["analysis"],
                        "initial_score": score,
                        "used_fallback": analysis_result.get("used_fallback", False)
                    })
                
                    plan_steps = len(analysis_result["analysis"].get("refactoring_plan", []))
                    fallback_note = " (fallback)" if analysis_result.get("used_fallback") else ""
                    print(f"  ✅ {file_info['relative_path']}: {plan_steps} refactoring steps{fallback_note}")
        
        print(f"\n📊 Summary: {len(files_to_fix)} files need refactoring")
        return files_to_fix
    
    def phase_2_refactoring_loop(self, files_to_fix):
        """
        Phase 2: Apply refactoring with self-healing loop.
        
        Args:
            files_to_fix: List of files with analysis
        """
        print("\n" + "─" * 70)
        print("🔧 PHASE 2: REFACTORING LOOP")
        print("─" * 70)
        
        for idx, file_data in enumerate(files_to_fix, 1):
            file_info = file_data["file_info"]
            file_path = file_info["path"]
            rel_path = file_info["relative_path"]
            analysis = file_data["analysis"]
            initial_score = file_data["initial_score"]
            
            print(f"\n[{idx}/{len(files_to_fix)}] 🔧 Fixing {rel_path}")
            print("─" * 70)
            
            iteration = 0
            test_errors = None
            
            # Self-healing loop
            while iteration < self.max_iterations:
                iteration += 1
                self.total_iterations += 1
                
                print(f"\n  🔄 Iteration {iteration}/{self.max_iterations}")
                
                # Read current file content
                read_result = self.tools.read_file(file_path)
                if not read_result["success"]:
                    print(f"  ❌ Cannot read file: {read_result['error']}")
                    break
                
                current_content = read_result["content"]
                
                # Fixer applies refactoring
                if test_errors:
                    # Use test errors to guide fixing
                    fix_result = self.fixer.fix_from_test_errors(
                        file_path=rel_path,
                        file_content=current_content,
                        test_output=test_errors["output"],
                        test_statistics=test_errors["statistics"]
                    )
                else:
                    # Use refactoring plan
                    fix_result = self.fixer.fix_file(
                        file_path=rel_path,
                        file_content=current_content,
                        refactoring_plan=analysis.get("refactoring_plan", [])
                    )
                
                if not fix_result["success"]:
                    print(f"  ❌ Fixer failed")
                    break
                
                # Write fixed code
                fixed_code = fix_result["fixed_code"]
                write_result = self.tools.write_file(file_path, fixed_code)
                
                if not write_result["success"]:
                    print(f"  ❌ Failed to write file: {write_result['error']}")
                    break
                
                print(f"  ✏️  Code updated (backup: {Path(write_result['backup_path']).name})")
                
                # Validate syntax
                syntax_check = self.tools.validate_python_syntax(file_path)
                if not syntax_check["valid"]:
                    print(f"  ⚠️  Syntax error: {syntax_check['error']['message']}")
                    test_errors = {
                        "output": f"Syntax error at line {syntax_check['error']['line']}",
                        "statistics": {"passed": 0, "failed": 1, "total": 1}
                    }
                    continue
                
                # Run tests
                test_result = self.tools.run_pytest()
                stats = test_result.get("statistics", {})
                
                print(f"  🧪 Tests: {stats.get('passed', 0)} passed, {stats.get('failed', 0)} failed")
                
                # Judge evaluates
                current_pylint = self.tools.run_pylint(file_path)
                current_score = current_pylint.get("score") if current_pylint.get("success") else None
                
                evaluation = self.judge.evaluate_tests(
                    test_output=test_result.get("output", ""),
                    test_statistics=stats,
                    previous_score=initial_score,
                    current_score=current_score
                )
                
                # Check if we're done
                if evaluation.get("tests_passed", False):
                    print(f"  ✅ SUCCESS! Tests passing.")
                    if current_score is not None and initial_score is not None:
                        improvement = current_score - initial_score
                        print(f"  📊 Quality: {initial_score:.1f} → {current_score:.1f} ({improvement:+.1f})")
                    elif current_score is not None:
                        print(f"  📊 Quality: {current_score:.1f}/10")
                    self.files_processed.append(rel_path)
                    break
                else:
                    # Tests failed - prepare for next iteration
                    print(f"  ⚠️  Tests failed, retrying...")
                    test_errors = {
                        "output": test_result.get("output", "Unknown error"),
                        "statistics": stats
                    }
            
            else:
                # Max iterations reached
                print(f"  ⚠️  Max iterations reached for {rel_path}")
    
    def phase_3_final_validation(self):
        """Phase 3: Run final validation on all files"""
        print("\n" + "─" * 70)
        print("🏁 PHASE 3: FINAL VALIDATION")
        print("─" * 70)
        
        # Run all tests
        print("\n🧪 Running full test suite...")
        final_tests = self.tools.run_pytest()
        
        if final_tests["success"]:
            stats = final_tests.get("statistics", {})
            print(f"  Tests: {stats.get('passed', 0)} passed, {stats.get('failed', 0)} failed")
            
            if final_tests["passed"]:
                print("  ✅ All tests PASSED!")
            else:
                print("  ⚠️  Some tests still failing")
        else:
            print(f"  ❌ Test execution failed: {final_tests.get('error')}")
        
        # Get final quality scores
        print("\n📊 Final code quality:")
        final_analysis = self.tools.run_pylint_on_directory()
        
        if final_analysis["success"]:
            avg_score = final_analysis.get("average_score", 0)
            print(f"  Average Pylint Score: {avg_score:.2f}/10")
        
        # Log final state
        log_experiment(
            agent_name="Orchestrator",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "phase": "final_validation",
                "input_prompt": "Final validation of all refactored code",
                "output_response": f"Tests passed: {final_tests.get('passed', False)}, Average score: {final_analysis.get('average_score', 0):.2f}",
                "tests_passed": final_tests.get("passed", False),
                "average_score": final_analysis.get("average_score", 0),
                "files_processed": self.files_processed,
                "total_iterations": self.total_iterations
            },
            status="SUCCESS" if final_tests.get("passed", False) else "PARTIAL"
        )


def main():
    """Main entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Refactoring Swarm - Automated Code Quality Improvement"
    )
    parser.add_argument(
        "--target_dir",
        required=True,
        help="Directory containing code to refactor"
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=10,
        help="Maximum iterations per file (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in .env file")
        print("Please create a .env file with your API key:")
        print("GROQ_API_KEY=your_key_here")
        return 1
    
    # Validate target directory
    if not os.path.exists(args.target_dir):
        print(f"❌ ERROR: Directory '{args.target_dir}' does not exist")
        return 1
    
    # Run orchestrator
    orchestrator = RefactoringOrchestrator(
        api_key=api_key,
        target_dir=args.target_dir,
        max_iterations=args.max_iterations
    )
    
    orchestrator.run()
    
    return 0


if __name__ == "__main__":
    exit(main())