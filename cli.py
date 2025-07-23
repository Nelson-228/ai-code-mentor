#!/usr/bin/env python3
"""
AI Code Mentor CLI - Command Line Interface
Use this to analyze Python code without VS Code
"""

import sys
import json
import argparse
import os
from models.analyzer import PythonAnalyzer
import requests

def colorize(text, color="green", use_colors=True):
    """Colorize text using ANSI escape codes"""
    if not use_colors:
        return text
    
    colors = {
        "green": "\033[32m",
        "red": "\033[31m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def build_parser():
    """Build and return the argument parser"""
    parser = argparse.ArgumentParser(description='AI Code Mentor CLI - Analyze Python code')
    parser.add_argument('file', help='Python file to analyze')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--gpt', action='store_true', help='Get GPT-4 suggestions')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--color', choices=['auto', 'always', 'never'], default='auto', 
                       help='Colorize output (default: auto)')
    return parser

class AICodeMentorCLI:
    def __init__(self, openai_api_key=None):
        self.analyzer = PythonAnalyzer()
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
    
    def analyze_file(self, file_path):
        """Analyze a Python file and return results"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            result = self.analyzer.analyze_code(code, file_path)
            return result
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            return None
        except Exception as e:
            print(f"Error analyzing file: {e}")
            return None
    
    def get_gpt_suggestions(self, code, context=""):
        """Get GPT-4 suggestions for code"""
        if not self.openai_api_key:
            print("Warning: No OpenAI API key provided. Skipping GPT suggestions.")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""
Please analyze this Python code and provide:

1. **Improved Code**: A cleaner, more efficient version of the code
2. **Time Complexity**: O() notation and explanation
3. **Space Complexity**: O() notation and explanation  
4. **What the code is doing**: Clear explanation of the code's purpose and logic
5. **Suggestions**: 2-3 specific improvements for code quality, readability, or performance

Code to analyze:
```python
{code}
```

{context}

Please format your response as JSON with the following structure:
{{
    "improvedCode": "your improved code here",
    "timeComplexity": "O(n) - explanation",
    "spaceComplexity": "O(1) - explanation", 
    "explanation": "what the code does",
    "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}}
"""
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert Python code reviewer and mentor. Provide clear, actionable feedback with code examples."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return self.parse_gpt_response(content)
            else:
                print(f"Error calling OpenAI API: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting GPT suggestions: {e}")
            return None
    
    def parse_gpt_response(self, response):
        """Parse GPT response and extract JSON"""
        try:
            json_match = response.find('{')
            if json_match != -1:
                json_str = response[json_match:]
                parsed = json.loads(json_str)
                return {
                    "improvedCode": parsed.get("improvedCode", "No improved code provided"),
                    "timeComplexity": parsed.get("timeComplexity", "Not analyzed"),
                    "spaceComplexity": parsed.get("spaceComplexity", "Not analyzed"),
                    "explanation": parsed.get("explanation", "No explanation provided"),
                    "suggestions": parsed.get("suggestions", [])
                }
        except Exception as e:
            print(f"Warning: Failed to parse GPT response: {e}")
        
        return {
            "improvedCode": "Unable to parse improved code from response",
            "timeComplexity": "Not analyzed",
            "spaceComplexity": "Not analyzed",
            "explanation": response,
            "suggestions": ["Review the response manually for suggestions"]
        }
    
    def print_analysis(self, analysis_result):
        """Print analysis results in a nice format"""
        if not analysis_result:
            return
        
        print("\n" + "="*60)
        print("🤖 AI CODE MENTOR ANALYSIS")
        print("="*60)
        
        print(f"\n📁 File: {analysis_result.file_path}")
        print(f"📊 Total Lines: {analysis_result.total_lines}")
        print(f"🎯 Complexity Score: {analysis_result.complexity_score:.1f}")
        
        if analysis_result.functions:
            print(f"\n🔍 Functions Found: {len(analysis_result.functions)}")
            for func in analysis_result.functions:
                print(f"  • {func.name}: {func.line_count} lines, complexity {func.complexity}")
        
        if analysis_result.issues:
            print(f"\n⚠️  Issues Found: {len(analysis_result.issues)}")
            for issue in analysis_result.issues:
                severity_icon = "🔴" if issue.severity == "error" else "🟡" if issue.severity == "warning" else "🔵"
                print(f"  {severity_icon} Line {issue.line}: {issue.message}")
                if issue.suggestion:
                    print(f"     💡 Suggestion: {issue.suggestion}")
        
        if analysis_result.suggestions:
            print(f"\n💡 General Suggestions:")
            for suggestion in analysis_result.suggestions:
                print(f"  • {suggestion}")
    
    def print_gpt_suggestions(self, gpt_result):
        """Print GPT suggestions in a nice format"""
        if not gpt_result:
            return
        
        print("\n" + "="*60)
        print("🧠 GPT-4 SUGGESTIONS")
        print("="*60)
        
        print(f"\n📝 Explanation:")
        print(f"  {gpt_result['explanation']}")
        
        print(f"\n⏱️  Time Complexity:")
        print(f"  {gpt_result['timeComplexity']}")
        
        print(f"\n💾 Space Complexity:")
        print(f"  {gpt_result['spaceComplexity']}")
        
        if gpt_result['suggestions']:
            print(f"\n💡 Suggestions:")
            for i, suggestion in enumerate(gpt_result['suggestions'], 1):
                print(f"  {i}. {suggestion}")
        
        if gpt_result['improvedCode'] and gpt_result['improvedCode'] != "Unable to parse improved code from response":
            print(f"\n✨ Improved Code:")
            print("```python")
            print(gpt_result['improvedCode'])
            print("```")

def main():
    parser = build_parser()
    args = parser.parse_args()
    
    # Determine if we should use colors
    use_colors = (args.color == 'always' or 
                  (args.color == 'auto' and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()))
    
    if args.verbose:
        print(colorize("Verbose mode enabled", "green", use_colors))
    
    # Initialize CLI
    cli = AICodeMentorCLI(args.api_key)
    
    # Analyze file
    analysis = cli.analyze_file(args.file)
    
    if not analysis:
        sys.exit(1)
    
    if args.json:
        # Output as JSON
        print(json.dumps(analysis, indent=2, default=lambda x: x.__dict__))
    else:
        # Print formatted results
        cli.print_analysis(analysis)
        
        # Get GPT suggestions if requested
        if args.gpt:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read()
            gpt_result = cli.get_gpt_suggestions(code, f"Analyzing file: {args.file}")
            cli.print_gpt_suggestions(gpt_result)

if __name__ == "__main__":
    main() 