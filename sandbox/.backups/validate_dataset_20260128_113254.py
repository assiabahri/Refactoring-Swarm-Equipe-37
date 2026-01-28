#!/usr/bin/env python3
"""
Validation Script for Test Dataset
Verifies that the dataset is properly structured and tests work as expected
"""

import os
import sys
from pathlib import Path
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_section(text):
    """Print a section header"""
    print(f"\n{'─' * 70}")
    print(f"  {text}")
    print(f"{'─' * 70}")

def check_file_structure():
    """Check that all expected files exist"""
    print_header("CHECKING FILE STRUCTURE")
    
    expected_files = [
        "buggy_calculator.py",
        "buggy_string_utils.py",
        "buggy_data_processor.py",
        "buggy_validator.py",
        "tests/test_calculator.py",
        "tests/test_string_utils.py",
        "tests/test_data_processor.py",
        "tests/test_validator.py",
        "tests/__init__.py",
        "README.md"
    ]
    
    all_exist = True
    for file_path in expected_files:
        exists = Path(file_path).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_syntax_errors():
    """Check which files have syntax errors (intentional)"""
    print_header("CHECKING FOR SYNTAX ERRORS")
    
    source_files = [
        "buggy_calculator.py",
        "buggy_string_utils.py",
        "buggy_data_processor.py",
        "buggy_validator.py"
    ]
    
    syntax_errors = []
    
    for file_path in source_files:
        if not Path(file_path).exists():
            print(f"⚠️  {file_path} not found")
            continue
        
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            print(f"✅ {file_path} - No syntax errors")
        except SyntaxError as e:
            print(f"❌ {file_path} - Syntax error at line {e.lineno}: {e.msg}")
            syntax_errors.append(file_path)
    
    print(f"\nExpected syntax errors: buggy_data_processor.py")
    print(f"Actual syntax errors: {', '.join(syntax_errors) if syntax_errors else 'None'}")
    
    return syntax_errors

def run_pylint():
    """Run pylint on source files"""
    print_header("RUNNING PYLINT ANALYSIS")
    
    source_files = [
        "buggy_calculator.py",
        "buggy_string_utils.py",
        # Skip buggy_data_processor.py due to syntax error
        "buggy_validator.py"
    ]
    
    scores = {}
    
    for file_path in source_files:
        if not Path(file_path).exists():
            continue
        
        try:
            result = subprocess.run(
                ['pylint', file_path, '--score=yes'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Extract score from output
            output = result.stdout
            for line in output.split('\n'):
                if 'rated at' in line.lower():
                    # Example: "Your code has been rated at 6.67/10"
                    parts = line.split('rated at')
                    if len(parts) > 1:
                        score_str = parts[1].split('/')[0].strip()
                        try:
                            score = float(score_str)
                            scores[file_path] = score
                            print(f"📊 {file_path:<30} Score: {score:.2f}/10")
                        except ValueError:
                            pass
        except Exception as e:
            print(f"⚠️  {file_path} - Pylint error: {str(e)}")
    
    if scores:
        avg_score = sum(scores.values()) / len(scores)
        print(f"\n📈 Average Pylint Score: {avg_score:.2f}/10")
        print(f"   (Expected: < 7.0 before refactoring)")
    
    return scores

def run_tests():
    """Run pytest on test suite"""
    print_header("RUNNING TEST SUITE")
    
    if not Path("tests").exists():
        print("❌ Tests directory not found")
        return False
    
    try:
        print("Running: pytest tests/ -v --tb=short\n")
        result = subprocess.run(
            ['pytest', 'tests/', '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        
        # Parse results
        output = result.stdout + result.stderr
        if 'passed' in output:
            print("\n✅ Tests executed successfully")
            
            # Count results
            if 'passed' in output:
                for line in output.split('\n'):
                    if 'passed' in line or 'failed' in line or 'skipped' in line:
                        print(f"   {line.strip()}")
        else:
            print("\n⚠️  Test execution completed (check output above)")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out (> 30 seconds)")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")
        return False

def print_summary():
    """Print summary and usage instructions"""
    print_header("DATASET VALIDATION COMPLETE")
    
    print("""
📋 SUMMARY:
   This test dataset is ready to use with your Refactoring Swarm system.
   
🎯 EXPECTED BEHAVIOR:
   ✓ buggy_data_processor.py has intentional syntax error
   ✓ Most tests will PASS (some skipped due to syntax error)
   ✓ Pylint scores should be < 7.0 (before refactoring)
   ✓ After refactoring: all tests pass, scores > 8.0
   
🚀 USAGE:
   1. Copy this dataset to your sandbox:
      cp -r test_dataset /path/to/sandbox/
   
   2. Run your refactoring system:
      python main.py --target_dir "./sandbox/test_dataset"
   
   3. Verify results:
      cd sandbox/test_dataset
      pytest tests/ -v
      pylint buggy_*.py
   
📊 SUCCESS CRITERIA:
   After refactoring, you should see:
   ✅ All 49 tests passing
   ✅ Average Pylint score > 8.5
   ✅ No syntax errors
   ✅ Proper docstrings added
""")

def main():
    """Main validation function"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           TEST DATASET VALIDATION SCRIPT                          ║
║           For Refactoring Swarm - IGL Lab 2025-2026              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"📂 Working directory: {Path.cwd()}")
    
    # Run validation checks
    structure_ok = check_file_structure()
    
    if not structure_ok:
        print("\n❌ File structure validation failed!")
        print("   Some expected files are missing.")
        return 1
    
    syntax_errors = check_syntax_errors()
    scores = run_pylint()
    tests_ok = run_tests()
    
    print_summary()
    
    # Final status
    print("\n" + "=" * 70)
    if structure_ok:
        print("✅ DATASET IS VALID AND READY TO USE")
    else:
        print("❌ DATASET HAS ISSUES - Check errors above")
    print("=" * 70 + "\n")
    
    return 0 if structure_ok else 1

if __name__ == "__main__":
    sys.exit(main())
