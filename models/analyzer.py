#!/usr/bin/env python3
"""
Python AST Analyzer for AI Code Mentor VS Code Extension
Analyzes Python code for code quality issues and provides structured feedback.
"""

import ast
import json
import sys
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class CodeIssue:
    """Represents a code quality issue found during analysis."""
    line: int
    column: int
    severity: str  # 'error', 'warning', 'info'
    message: str
    issue_type: str
    suggestion: Optional[str] = None


@dataclass
class FunctionInfo:
    """Information about a function in the code."""
    name: str
    line_start: int
    line_end: int
    line_count: int
    complexity: int
    nested_loops: int
    issues: List[CodeIssue]


@dataclass
class AnalysisResult:
    """Complete analysis result for a Python file."""
    file_path: str
    total_lines: int
    functions: List[FunctionInfo]
    issues: List[CodeIssue]
    complexity_score: float
    suggestions: List[str]


class PythonAnalyzer:
    """Main analyzer class that uses AST to analyze Python code."""
    
    def __init__(self, max_function_lines: int = 30, max_nested_loops: int = 3):
        self.max_function_lines = max_function_lines
        self.max_nested_loops = max_nested_loops
        self.issues: List[CodeIssue] = []
        self.functions: List[FunctionInfo] = []
    
    def analyze_code(self, code: str, file_path: str = "unknown") -> AnalysisResult:
        """
        Analyze Python code and return structured analysis results.
        
        Args:
            code: Python source code as string
            file_path: Path to the file being analyzed
            
        Returns:
            AnalysisResult with all findings
        """
        self.issues = []
        self.functions = []
        
        try:
            tree = ast.parse(code)
            self._analyze_ast(tree, code)
            
            return AnalysisResult(
                file_path=file_path,
                total_lines=len(code.splitlines()),
                functions=self.functions,
                issues=self.issues,
                complexity_score=self._calculate_complexity_score(),
                suggestions=self._generate_suggestions()
            )
        except SyntaxError as e:
            # Handle syntax errors
            self.issues.append(CodeIssue(
                line=e.lineno or 1,
                column=e.offset or 1,
                severity='error',
                message=f"Syntax error: {e.msg}",
                issue_type='syntax_error'
            ))
            return AnalysisResult(
                file_path=file_path,
                total_lines=len(code.splitlines()),
                functions=[],
                issues=self.issues,
                complexity_score=0.0,
                suggestions=["Fix syntax errors before analysis"]
            )
    
    def _analyze_ast(self, tree: ast.AST, code: str) -> None:
        """Recursively analyze AST nodes."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._analyze_function(node, code)
            elif isinstance(node, (ast.For, ast.While)):
                self._analyze_loop(node)
    
    def _analyze_function(self, node: ast.FunctionDef, code: str) -> None:
        """Analyze a function definition."""
        lines = code.splitlines()
        function_code = '\n'.join(lines[node.lineno - 1:node.end_lineno])
        
        # Count lines in function
        line_count = node.end_lineno - node.lineno + 1
        
        # Analyze nested loops
        nested_loops = self._count_nested_loops(node)
        
        # Calculate complexity (simplified)
        complexity = self._calculate_function_complexity(node)
        
        # Check for issues
        function_issues = []
        
        if line_count > self.max_function_lines:
            function_issues.append(CodeIssue(
                line=node.lineno,
                column=node.col_offset,
                severity='warning',
                message=f"Function '{node.name}' is {line_count} lines long (max: {self.max_function_lines})",
                issue_type='long_function',
                suggestion="Consider breaking this function into smaller functions"
            ))
        
        if nested_loops > self.max_nested_loops:
            function_issues.append(CodeIssue(
                line=node.lineno,
                column=node.col_offset,
                severity='warning',
                message=f"Function '{node.name}' has {nested_loops} nested loops (max: {self.max_nested_loops})",
                issue_type='nested_loops',
                suggestion="Consider refactoring to reduce nesting"
            ))
        
        # Add function info
        function_info = FunctionInfo(
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno,
            line_count=line_count,
            complexity=complexity,
            nested_loops=nested_loops,
            issues=function_issues
        )
        
        self.functions.append(function_info)
        self.issues.extend(function_issues)
    
    def _analyze_loop(self, node: ast.AST) -> None:
        """Analyze loop structures."""
        # Check for potential infinite loops
        if isinstance(node, ast.While):
            if not self._has_break_or_return(node):
                self.issues.append(CodeIssue(
                    line=node.lineno,
                    column=node.col_offset,
                    severity='warning',
                    message="While loop without clear exit condition",
                    issue_type='potential_infinite_loop',
                    suggestion="Ensure the loop has a proper exit condition"
                ))
    
    def _count_nested_loops(self, node: ast.AST) -> int:
        """Count nested loops within a function."""
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                count += 1
        return count
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _has_break_or_return(self, node: ast.AST) -> bool:
        """Check if a loop has break or return statements."""
        for child in ast.walk(node):
            if isinstance(child, (ast.Break, ast.Return)):
                return True
        return False
    
    def _calculate_complexity_score(self) -> float:
        """Calculate overall complexity score for the file."""
        if not self.functions:
            return 0.0
        
        total_complexity = sum(f.complexity for f in self.functions)
        avg_complexity = total_complexity / len(self.functions)
        
        # Normalize to 0-100 scale
        return min(100.0, avg_complexity * 10)
    
    def _generate_suggestions(self) -> List[str]:
        """Generate general suggestions based on analysis."""
        suggestions = []
        
        if len(self.functions) == 0:
            suggestions.append("No functions found. Consider adding functions to improve code organization.")
        
        long_functions = [f for f in self.functions if f.line_count > self.max_function_lines]
        if long_functions:
            suggestions.append(f"Consider breaking down {len(long_functions)} long function(s) into smaller, more focused functions.")
        
        complex_functions = [f for f in self.functions if f.complexity > 10]
        if complex_functions:
            suggestions.append(f"Consider simplifying {len(complex_functions)} complex function(s) to improve readability.")
        
        return suggestions


def main():
    """CLI interface for testing the analyzer."""
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <python_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        analyzer = PythonAnalyzer()
        result = analyzer.analyze_code(code, file_path)
        
        # Output as JSON for VS Code extension
        print(json.dumps(asdict(result), indent=2))
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 