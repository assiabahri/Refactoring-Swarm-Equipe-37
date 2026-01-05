"""
Toolsmith Module - Internal API for Refactoring Swarm
Provides secure, sandboxed tools for agent operations
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import ast


class SecurityError(Exception):
    """Raised when a security violation is detected"""
    pass


class ToolsmithAPI:
    """
    Main API class providing secure tools for agents.
    All file operations are sandboxed to prevent unauthorized access.
    """
    
    def __init__(self, sandbox_root: str):
        """
        Initialize the Toolsmith API with a sandbox root directory.
        
        Args:
            sandbox_root: Absolute path to the sandbox directory
        """
        self.sandbox_root = Path(sandbox_root).resolve()
        self.backup_dir = self.sandbox_root / ".backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    # ==================== SECURITY LAYER ====================
    
    def _validate_path(self, file_path: str) -> Path:
        """
        Validate that a path is within the sandbox.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Resolved Path object
            
        Raises:
            SecurityError: If path is outside sandbox
        """
        try:
            resolved = Path(file_path).resolve()
            
            # Check if path is within sandbox
            if not str(resolved).startswith(str(self.sandbox_root)):
                raise SecurityError(
                    f"Access denied: {file_path} is outside sandbox {self.sandbox_root}"
                )
            
            return resolved
        except Exception as e:
            raise SecurityError(f"Path validation failed: {str(e)}")
    
    def _create_backup(self, file_path: Path) -> str:
        """
        Create a backup of a file before modification.
        
        Args:
            file_path: Path to file to backup
            
        Returns:
            Path to backup file
        """
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            shutil.copy2(file_path, backup_path)
            return str(backup_path)
        return None
    
    # ==================== FILE OPERATIONS ====================
    
    def read_file(self, file_path: str) -> Dict:
        """
        Safely read a file from the sandbox.
        
        Args:
            file_path: Path to file to read
            
        Returns:
            Dict with 'success', 'content', 'error' keys
        """
        try:
            validated_path = self._validate_path(file_path)
            
            if not validated_path.exists():
                return {
                    "success": False,
                    "content": None,
                    "error": f"File not found: {file_path}"
                }
            
            with open(validated_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "error": None,
                "path": str(validated_path),
                "size": len(content)
            }
        except SecurityError as e:
            return {"success": False, "content": None, "error": str(e)}
        except Exception as e:
            return {"success": False, "content": None, "error": f"Read error: {str(e)}"}
    
    def write_file(self, file_path: str, content: str, create_backup: bool = True) -> Dict:
        """
        Safely write content to a file in the sandbox.
        
        Args:
            file_path: Path to file to write
            content: Content to write
            create_backup: Whether to create backup before writing
            
        Returns:
            Dict with 'success', 'backup_path', 'error' keys
        """
        try:
            validated_path = self._validate_path(file_path)
            
            # Create backup if file exists
            backup_path = None
            if create_backup and validated_path.exists():
                backup_path = self._create_backup(validated_path)
            
            # Ensure parent directory exists
            validated_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            with open(validated_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "path": str(validated_path),
                "backup_path": backup_path,
                "error": None
            }
        except SecurityError as e:
            return {"success": False, "backup_path": None, "error": str(e)}
        except Exception as e:
            return {"success": False, "backup_path": None, "error": f"Write error: {str(e)}"}
    
    def list_python_files(self, directory: str = None) -> Dict:
        """
        List all Python files in the sandbox or a subdirectory.
        
        Args:
            directory: Subdirectory to search (None for root)
            
        Returns:
            Dict with 'success', 'files', 'error' keys
        """
        try:
            if directory:
                search_path = self._validate_path(directory)
            else:
                search_path = self.sandbox_root
            
            if not search_path.exists():
                return {"success": False, "files": [], "error": "Directory not found"}
            
            python_files = []
            for py_file in search_path.rglob("*.py"):
                # Skip backup directory
                if ".backups" not in py_file.parts:
                    python_files.append({
                        "path": str(py_file),
                        "relative_path": str(py_file.relative_to(self.sandbox_root)),
                        "size": py_file.stat().st_size
                    })
            
            return {
                "success": True,
                "files": python_files,
                "count": len(python_files),
                "error": None
            }
        except SecurityError as e:
            return {"success": False, "files": [], "error": str(e)}
        except Exception as e:
            return {"success": False, "files": [], "error": f"List error: {str(e)}"}
    
    # ==================== PYLINT INTERFACE ====================
    
    def run_pylint(self, file_path: str) -> Dict:
        """
        Run Pylint static analysis on a Python file.
        
        Args:
            file_path: Path to Python file to analyze
            
        Returns:
            Dict with analysis results including score and issues
        """
        try:
            validated_path = self._validate_path(file_path)
            
            if not validated_path.exists():
                return {"success": False, "error": "File not found"}
            
            # Run pylint with JSON output
            result = subprocess.run(
                ['pylint', str(validated_path), '--output-format=json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse JSON output
            issues = []
            if result.stdout:
                try:
                    issues = json.loads(result.stdout)
                except json.JSONDecodeError:
                    pass
            
            # Extract score from stderr (pylint prints score there)
            score = self._extract_pylint_score(result.stderr)
            
            # Categorize issues
            categorized = {
                "error": [i for i in issues if i.get("type") == "error"],
                "warning": [i for i in issues if i.get("type") == "warning"],
                "convention": [i for i in issues if i.get("type") == "convention"],
                "refactor": [i for i in issues if i.get("type") == "refactor"]
            }
            
            return {
                "success": True,
                "file": str(validated_path),
                "score": score,
                "issues": issues,
                "categorized": categorized,
                "total_issues": len(issues),
                "error": None
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Pylint execution timeout"}
        except SecurityError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Pylint error: {str(e)}"}
    
    def _extract_pylint_score(self, stderr_output: str) -> Optional[float]:
        """
        Extract the Pylint score from stderr output.
        
        Args:
            stderr_output: Standard error output from pylint
            
        Returns:
            Float score or None if not found
        """
        import re
        match = re.search(r'Your code has been rated at ([\d.]+)/10', stderr_output)
        if match:
            return float(match.group(1))
        return None
    
    def run_pylint_on_directory(self, directory: str = None) -> Dict:
        """
        Run Pylint on all Python files in a directory.
        
        Args:
            directory: Directory to analyze (None for sandbox root)
            
        Returns:
            Dict with aggregated results
        """
        files_result = self.list_python_files(directory)
        if not files_result["success"]:
            return files_result
        
        results = []
        total_score = 0
        analyzed_count = 0
        
        for file_info in files_result["files"]:
            pylint_result = self.run_pylint(file_info["path"])
            if pylint_result["success"] and pylint_result["score"] is not None:
                results.append(pylint_result)
                total_score += pylint_result["score"]
                analyzed_count += 1
        
        avg_score = total_score / analyzed_count if analyzed_count > 0 else 0
        
        return {
            "success": True,
            "results": results,
            "average_score": avg_score,
            "files_analyzed": analyzed_count,
            "error": None
        }
    
    # ==================== PYTEST INTERFACE ====================
    
    def run_pytest(self, target_path: str = None, verbose: bool = True) -> Dict:
        """
        Run pytest on a file or directory.
        
        Args:
            target_path: Path to test file/directory (None for sandbox root)
            verbose: Whether to use verbose output
            
        Returns:
            Dict with test results
        """
        try:
            if target_path:
                validated_path = self._validate_path(target_path)
            else:
                validated_path = self.sandbox_root
            
            if not validated_path.exists():
                return {"success": False, "error": "Test target not found"}
            
            # Build pytest command
            cmd = ['pytest', str(validated_path), '--json-report', '--json-report-file=none']
            if verbose:
                cmd.append('-v')
            
            # Run pytest
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.sandbox_root)
            )
            
            # Parse results
            passed = result.returncode == 0
            output = result.stdout + result.stderr
            
            # Extract test statistics
            stats = self._parse_pytest_output(output)
            
            return {
                "success": True,
                "passed": passed,
                "output": output,
                "statistics": stats,
                "exit_code": result.returncode,
                "error": None if passed else "Tests failed"
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "passed": False, "error": "Pytest execution timeout"}
        except SecurityError as e:
            return {"success": False, "passed": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "passed": False, "error": f"Pytest error: {str(e)}"}
    
    def _parse_pytest_output(self, output: str) -> Dict:
        """
        Parse pytest output to extract statistics.
        
        Args:
            output: Pytest output string
            
        Returns:
            Dict with test statistics
        """
        import re
        
        stats = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "total": 0
        }
        
        # Look for summary line like "5 passed, 2 failed in 1.23s"
        match = re.search(r'(\d+) passed', output)
        if match:
            stats["passed"] = int(match.group(1))
        
        match = re.search(r'(\d+) failed', output)
        if match:
            stats["failed"] = int(match.group(1))
        
        match = re.search(r'(\d+) error', output)
        if match:
            stats["errors"] = int(match.group(1))
        
        match = re.search(r'(\d+) skipped', output)
        if match:
            stats["skipped"] = int(match.group(1))
        
        stats["total"] = sum([stats["passed"], stats["failed"], stats["errors"]])
        
        return stats
    
    # ==================== SYNTAX VALIDATION ====================
    
    def validate_python_syntax(self, file_path: str) -> Dict:
        """
        Validate Python syntax without executing the code.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dict with validation results
        """
        try:
            validated_path = self._validate_path(file_path)
            
            read_result = self.read_file(str(validated_path))
            if not read_result["success"]:
                return read_result
            
            # Try to parse the AST
            try:
                ast.parse(read_result["content"])
                return {
                    "success": True,
                    "valid": True,
                    "error": None
                }
            except SyntaxError as e:
                return {
                    "success": True,
                    "valid": False,
                    "error": {
                        "type": "SyntaxError",
                        "message": str(e),
                        "line": e.lineno,
                        "offset": e.offset
                    }
                }
        except SecurityError as e:
            return {"success": False, "valid": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "valid": False, "error": f"Validation error: {str(e)}"}
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def get_sandbox_info(self) -> Dict:
        """
        Get information about the sandbox environment.
        
        Returns:
            Dict with sandbox statistics
        """
        python_files = self.list_python_files()
        
        return {
            "sandbox_root": str(self.sandbox_root),
            "python_files_count": python_files.get("count", 0),
            "backup_dir": str(self.backup_dir),
            "exists": self.sandbox_root.exists()
        }
    
    def restore_from_backup(self, backup_path: str, target_path: str) -> Dict:
        """
        Restore a file from backup.
        
        Args:
            backup_path: Path to backup file
            target_path: Target path to restore to
            
        Returns:
            Dict with operation result
        """
        try:
            validated_backup = self._validate_path(backup_path)
            validated_target = self._validate_path(target_path)
            
            if not validated_backup.exists():
                return {"success": False, "error": "Backup file not found"}
            
            shutil.copy2(validated_backup, validated_target)
            
            return {
                "success": True,
                "restored_to": str(validated_target),
                "error": None
            }
        except SecurityError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Restore error: {str(e)}"}


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Initialize API with sandbox
    api = ToolsmithAPI(sandbox_root="/path/to/sandbox")
    
    # Example: Read a file
    result = api.read_file("buggy_code/example.py")
    if result["success"]:
        print(f"File content: {result['content'][:100]}...")
    
    # Example: Run Pylint
    pylint_result = api.run_pylint("buggy_code/example.py")
    if pylint_result["success"]:
        print(f"Pylint score: {pylint_result['score']}/10")
        print(f"Total issues: {pylint_result['total_issues']}")
    
    # Example: Run tests
    test_result = api.run_pytest("tests/")
    if test_result["success"]:
        print(f"Tests passed: {test_result['passed']}")
        print(f"Statistics: {test_result['statistics']}")
    
    # Example: Write corrected code
    corrected_code = "def hello():\n    print('Hello, World!')\n"
    write_result = api.write_file("buggy_code/example.py", corrected_code)
    if write_result["success"]:
        print(f"File written with backup: {write_result['backup_path']}")