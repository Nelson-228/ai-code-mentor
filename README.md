# AI Code Mentor

A VS Code extension that provides real-time Python coding feedback using GPT-4 and static code analysis.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Compile Extension**
   ```bash
   npm run compile
   ```

3. **Set OpenAI API Key**
   - Open VS Code Settings
   - Search for "AI Code Mentor"
   - Add your OpenAI API key

4. **Test the Extension**
   - Open a Python file
   - Use Command Palette: `AI Code Mentor: Analyze Current File`
   - Or: `AI Code Mentor: Get GPT-4 Suggestions`

## ✨ Features

- **AST-based Code Analysis**: Identifies nested loops, long functions, and complexity issues
- **GPT-4 Integration**: AI-powered code suggestions and explanations
- **Real-time Feedback**: Live analysis as you code
- **Complexity Analysis**: Time/space complexity breakdown
- **Code Improvements**: Specific suggestions for better code quality

## 📁 Project Structure

```
ai-code-mentor/
├── src/                    # Extension logic (TypeScript)
│   ├── extension.ts       # Main extension entry point
│   ├── services/          # External service integrations
│   └── providers/         # Data providers
├── models/                # Python AST parser and analysis
├── docs/                  # Documentation and screenshots
└── logs/                  # Development logs
```

## 🛠️ Development

```bash
# Watch for changes during development
npm run watch

# Run tests
npm test

# Lint code
npm run lint
```

## 📖 Documentation

See [docs/README.md](docs/README.md) for detailed documentation.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.