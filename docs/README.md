# AI Code Mentor - VS Code Extension

Real-time Python coding feedback using GPT-4 and static code analysis.

## Features

### 🚀 MVP Features

1. **Inline Python Code Analysis**
   - AST-based analysis to flag nested loops or functions > 30 lines
   - Real-time code quality assessment
   - Complexity scoring and suggestions

2. **GPT-4 Code Suggestions**
   - Popup or sidebar with intelligent code recommendations
   - Improved code examples with explanations
   - Time/space complexity analysis
   - Clear explanations of what the code does

3. **Real-time Feedback**
   - Live analysis as you type
   - Instant suggestions for code improvements
   - Context-aware recommendations

## Architecture

```
ai-code-mentor/
├── src/                    # Extension logic (TypeScript)
│   ├── extension.ts       # Main extension entry point
│   ├── services/          # External service integrations
│   │   └── gptService.ts  # OpenAI GPT-4 integration
│   └── providers/         # Data providers
│       └── codeAnalysisProvider.ts
├── models/                # Python AST parser and analysis
│   └── analyzer.py        # Python code analyzer
├── docs/                  # Documentation and screenshots
└── logs/                  # Development logs
```

## Setup

### Prerequisites

- Node.js 16+
- Python 3.8+
- VS Code 1.74+
- OpenAI API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Compile TypeScript:
   ```bash
   npm run compile
   ```
4. Set your OpenAI API key in VS Code settings:
   ```json
   {
     "aiCodeMentor.openaiApiKey": "your-api-key-here"
   }
   ```

### Development

```bash
# Watch for changes
npm run watch

# Run tests
npm test

# Lint code
npm run lint
```

## Usage

### Commands

- `AI Code Mentor: Analyze Current File` - Run full analysis on current Python file
- `AI Code Mentor: Get GPT-4 Suggestions` - Get AI-powered suggestions for selected code

### Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `aiCodeMentor.openaiApiKey` | `""` | OpenAI API Key for GPT-4 access |
| `aiCodeMentor.maxFunctionLines` | `30` | Maximum lines allowed in a function |
| `aiCodeMentor.maxNestedLoops` | `3` | Maximum nested loops allowed |

## GPT-4 Prompt Structure

The extension sends structured prompts to GPT-4 requesting:

1. **Improved Code** - Cleaner, more efficient version
2. **Time Complexity** - O() notation and explanation
3. **Space Complexity** - O() notation and explanation
4. **Code Explanation** - What the code does
5. **Suggestions** - 2-3 specific improvements

## Python AST Analysis

The analyzer checks for:

- Functions longer than 30 lines
- Nested loops exceeding 3 levels
- Potential infinite loops
- Cyclomatic complexity
- Code structure issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 