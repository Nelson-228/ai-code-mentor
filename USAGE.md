# AI Code Mentor - CLI Usage Guide

## 🚀 Quick Start

### Basic Analysis (No API Key Required)
```bash
python cli.py your_file.py
```

### With GPT-4 Suggestions (API Key Required)
```bash
python cli.py your_file.py --gpt --api-key "your-openai-api-key"
```

### Output as JSON
```bash
python cli.py your_file.py --json
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `python cli.py file.py` | Basic AST analysis |
| `python cli.py file.py --gpt` | Analysis + GPT-4 suggestions |
| `python cli.py file.py --json` | Output as JSON format |
| `python cli.py file.py --gpt --api-key "key"` | Full analysis with custom API key |

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Set API Key (Optional)
You can set your OpenAI API key in several ways:

**Option A: Environment Variable**
```bash
set OPENAI_API_KEY=your-api-key-here
```

**Option B: Command Line**
```bash
python cli.py file.py --gpt --api-key "your-api-key-here"
```

## 📊 What It Analyzes

### Static Analysis (Always Available)
- ✅ Functions longer than 30 lines
- ✅ Nested loops exceeding 3 levels
- ✅ Cyclomatic complexity
- ✅ Potential infinite loops
- ✅ Code structure issues

### GPT-4 Analysis (Requires API Key)
- 🧠 Improved code suggestions
- ⏱️ Time complexity analysis
- 💾 Space complexity analysis
- 📝 Code explanation
- 💡 Specific improvement suggestions

## 🎯 Example Output

```
============================================================
🤖 AI CODE MENTOR ANALYSIS
============================================================

📁 File: your_file.py
📊 Total Lines: 50
🎯 Complexity Score: 25.0

🔍 Functions Found: 3
  • main_function: 25 lines, complexity 3
  • helper_function: 10 lines, complexity 1

⚠️  Issues Found: 1
  🟡 Line 5: Function 'main_function' is 25 lines long (max: 30)

============================================================
🧠 GPT-4 SUGGESTIONS
============================================================

📝 Explanation:
  This code implements a data processing pipeline...

⏱️  Time Complexity:
  O(n²) - nested loops cause quadratic time complexity

💡 Suggestions:
  1. Consider using list comprehensions
  2. Break down the main function
  3. Add type hints for better readability
```

## 🛠️ Integration with Other Tools

### Use with Any Editor
You can integrate this CLI with any code editor:

**Cursor/VS Code**: Add to tasks.json
**Sublime Text**: Add to build system
**Vim**: Add to .vimrc
**Any Editor**: Run from terminal

### Batch Processing
```bash
# Analyze multiple files
for file in *.py; do
    python cli.py "$file"
done
```

### CI/CD Integration
```bash
# Exit with error if issues found
python cli.py file.py --json | python -c "
import sys, json
data = json.load(sys.stdin)
if data['issues']:
    print('Code quality issues found!')
    sys.exit(1)
"
```

## 🔍 Troubleshooting

### Common Issues

1. **"No module named 'requests'"**
   ```bash
   pip install requests
   ```

2. **"OpenAI API key not provided"**
   - Set environment variable: `set OPENAI_API_KEY=your-key`
   - Or use `--api-key` parameter

3. **"File not found"**
   - Check file path is correct
   - Use absolute path if needed

### Getting Help
```bash
python cli.py --help
```

## 🎉 That's It!

You now have a powerful Python code analysis tool that works without VS Code. Use it in any editor, terminal, or CI/CD pipeline! 