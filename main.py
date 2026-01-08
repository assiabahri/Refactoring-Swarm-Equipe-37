import os
from dotenv import load_dotenv
from src.ToolsmithAPI import ToolsmithAPI
from src.utils.logger import log_experiment, ActionType 

def main():
    # -------------------------------
    # Step 0: Load API key
    # -------------------------------
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"✅ API_KEY loaded: {api_key[:4]}***")
    else:
        print("❌ API_KEY not found in .env")

    # -------------------------------
    # Step 1: Set sandbox folder
    # -------------------------------
    sandbox_folder = r"C:\Users\DELL\Refactoring-Swarm-Equipe-37\sandbox"
    api = ToolsmithAPI(sandbox_root=sandbox_folder)

    """
    # -------------------------------
    # Step 2: List all Python files
    # -------------------------------
    files_result = api.list_python_files()
    if files_result["success"]:
        print("\n📂 Python files found:")
        for f in files_result["files"]:
            print(f" - {f['relative_path']}")
    else:
        print("❌ Failed to list files:", files_result.get("error"))
        return

    # -------------------------------
    # Step 3: Check syntax and run pylint
    # -------------------------------
    print("\n🔍 Checking syntax and running pylint...")
    for f in files_result["files"]:
        path = f["path"]

        # Syntax check
        syntax_result = api.validate_python_syntax(path)
        if syntax_result["success"] and not syntax_result["valid"]:
            err = syntax_result["error"]
            print(f"❌ Syntax error in {f['relative_path']} | Line {err['line']}: {err['message']}")
        else:
            print(f"✅ Syntax valid: {f['relative_path']}")

        # Pylint check
        pylint_result = api.run_pylint(path)
        if pylint_result["success"]:
            score = pylint_result['score'] if pylint_result['score'] is not None else "N/A"
            print(f"📄 {f['relative_path']} | Score: {score} | Issues: {pylint_result['total_issues']}")
        else:
            print(f"❌ Pylint failed on {f['relative_path']} | Error: {pylint_result.get('error')}")
    """

    # Read a file
    print("--> reading a file :")
    result = api.read_file("buggy_1.py")
    if result["success"]:
        file_content = result['content']
        print(f"File content: {file_content[:100]}...")
        
        # LOG: File reading and analysis
        log_experiment(
            agent_name="Main_Agent",
            model_used="gemini-2.5-flash",
            action=ActionType.ANALYSIS,
            details={
                "file_analyzed": "buggy_1.py",
                "input_prompt": "Analyze the Python file buggy_1.py for potential issues",
                "output_response": f"File read successfully. Content length: {len(file_content)} characters. Content: {file_content[:200]}",
                "file_size": result.get('size', 0),
                "file_path": result.get('path', '')
            },
            status="SUCCESS"
        )
    else:
        print(f"❌ Failed to read file: {result.get('error')}")
        
        # LOG: Failed file reading
        log_experiment(
            agent_name="Main_Agent",
            model_used="gemini-2.5-flash",
            action=ActionType.ANALYSIS,
            details={
                "file_analyzed": "buggy_1.py",
                "input_prompt": "Analyze the Python file buggy_1.py for potential issues",
                "output_response": f"Failed to read file: {result.get('error')}",
                "error": result.get('error')
            },
            status="FAILURE"
        )
        return

     #  Run Pylint
    print("--> pylint on a buggy file :")
    pylint_result = api.run_pylint("buggy_1.py")

    if pylint_result["success"]:
        print(f"Pylint score: {pylint_result['score']}/10")
        print(f"Total issues: {pylint_result['total_issues']}")
    
        # LOG: Pylint analysis
        log_experiment(
            agent_name="Main_Agent",
            model_used="gemini-2.5-flash",
            action=ActionType.ANALYSIS,
            details={
                "file_analyzed": "buggy_1.py",
                "input_prompt": "Run static code analysis using Pylint on buggy_1.py to identify code quality issues",
                "output_response": f"Pylint analysis completed. Score: {pylint_result['score']}/10. Total issues: {pylint_result['total_issues']}. Issues breakdown: {pylint_result.get('categorized', {})}",
                "pylint_score": pylint_result['score'],
                "total_issues": pylint_result['total_issues'],
                "categorized_issues": pylint_result.get('categorized', {}),
                "issues_detail": pylint_result.get('issues', [])
            },
            status="SUCCESS"
        )
    else:
        print(f"❌ Pylint failed: {pylint_result.get('error')}")
        
        # LOG: Pylint failure
        log_experiment(
            agent_name="Main_Agent",
            model_used="gemini-2.5-flash",
            action=ActionType.ANALYSIS,
            details={
                "file_analyzed": "buggy_1.py",
                "input_prompt": "Run static code analysis using Pylint on buggy_1.py to identify code quality issues",
                "output_response": f"Pylint analysis failed: {pylint_result.get('error')}",
                "error": pylint_result.get('error')
            },
            status="FAILURE"
        )

    # Run tests
    print("--> pytest on a test file :")
    test_result = api.run_pytest("test_buggy_1.py")
    if test_result["success"]:
        print(f"Tests passed: {test_result['passed']}")
        print(f"Statistics: {test_result['statistics']}")
    
        # LOG: Test execution
        log_experiment(
            agent_name="Main_Agent",
            model_used="gemini-2.5-flash",
            action=ActionType.DEBUG,
            details={
                "test_file": "test_buggy_1.py",
                "input_prompt": "Execute pytest on test_buggy_1.py to verify code correctness",
                "output_response": test_result.get('output', 'Tests executed'),
                "tests_passed": test_result['passed'],
                "statistics": test_result['statistics'],
                "exit_code": test_result.get('exit_code', 0)
            },
            status="SUCCESS" if test_result['passed'] else "FAILURE"
        )
    else:
        print(f"❌ Pytest failed: {test_result.get('error')}")
        
        # LOG: Test execution failure
        log_experiment(
            agent_name="Main_Agent",
            model_used="gemini-2.5-flash",
            action=ActionType.DEBUG,
            details={
                "test_file": "test_buggy_1.py",
                "input_prompt": "Execute pytest on test_buggy_1.py to verify code correctness",
                "output_response": f"Pytest execution failed: {test_result.get('error')}",
                "error": test_result.get('error')
            },
            status="FAILURE"
        )
    """

    # Write corrected code
    corrected_code = "def hello():\n    print('Hello, World!')\n"
    write_result = api.write_file("sandbox/buggy_1.py", corrected_code)
    if write_result["success"]:
        print(f"File written with backup: {write_result['backup_path']}")
    else:
        print(f"Write failed: {write_result.get('error')}")
    """
    """
    # -------------------------------
    # Step 4: Run pytest on sandbox
    # -------------------------------
    print("\n🧪 Running tests in sandbox...")
    test_result = api.run_pytest(target_path=sandbox_folder)
    if test_result["success"]:
        print(f"Tests passed: {test_result['passed']}")
        print(f"Statistics: {test_result['statistics']}")
    else:
        print(f"❌ Pytest failed | Error: {test_result.get('error')}")
        print(test_result.get("output"))

    """    
if __name__ == "__main__":
    main()
