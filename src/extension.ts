import * as vscode from 'vscode';
import { PythonAnalyzer } from '../models/analyzer';
import { GPTService } from './services/gptService';
import { CodeAnalysisProvider } from './providers/codeAnalysisProvider';

export function activate(context: vscode.ExtensionContext) {
    console.log('AI Code Mentor extension is now active!');

    // Initialize services
    const gptService = new GPTService();
    const analyzer = new PythonAnalyzer();
    const analysisProvider = new CodeAnalysisProvider(analyzer, gptService);

    // Register commands
    const analyzeCommand = vscode.commands.registerCommand('ai-code-mentor.analyzeCode', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'python') {
            vscode.window.showWarningMessage('Please open a Python file to analyze.');
            return;
        }

        try {
            const document = editor.document;
            const code = document.getText();
            const analysis = await analysisProvider.analyzeCode(code, document.fileName);
            
            // Show analysis results in a new panel
            await showAnalysisResults(analysis);
        } catch (error) {
            vscode.window.showErrorMessage(`Analysis failed: ${error}`);
        }
    });

    const suggestionsCommand = vscode.commands.registerCommand('ai-code-mentor.getSuggestions', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.document.languageId !== 'python') {
            vscode.window.showWarningMessage('Please open a Python file to get suggestions.');
            return;
        }

        try {
            const document = editor.document;
            const selection = editor.selection;
            const code = document.getText(selection) || document.getText();
            
            const suggestions = await analysisProvider.getSuggestions(code, document.fileName);
            await showSuggestions(suggestions);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to get suggestions: ${error}`);
        }
    });

    // Register real-time analysis on document changes
    const documentChangeListener = vscode.workspace.onDidChangeTextDocument(async (event) => {
        if (event.document.languageId === 'python') {
            // Debounce rapid changes
            setTimeout(async () => {
                try {
                    const analysis = await analysisProvider.analyzeCode(
                        event.document.getText(), 
                        event.document.fileName
                    );
                    
                    // Update diagnostics
                    updateDiagnostics(analysis, event.document);
                } catch (error) {
                    console.error('Real-time analysis failed:', error);
                }
            }, 1000);
        }
    });

    context.subscriptions.push(analyzeCommand, suggestionsCommand, documentChangeListener);
}

async function showAnalysisResults(analysis: any) {
    const panel = vscode.window.createWebviewPanel(
        'aiCodeMentorAnalysis',
        'AI Code Mentor - Analysis Results',
        vscode.ViewColumn.One,
        {}
    );

    panel.webview.html = getAnalysisWebviewContent(analysis);
}

async function showSuggestions(suggestions: any) {
    const panel = vscode.window.createWebviewPanel(
        'aiCodeMentorSuggestions',
        'AI Code Mentor - GPT-4 Suggestions',
        vscode.ViewColumn.Two,
        {}
    );

    panel.webview.html = getSuggestionsWebviewContent(suggestions);
}

function getAnalysisWebviewContent(analysis: any): string {
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI Code Mentor Analysis</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; }
                .issue { margin: 10px 0; padding: 10px; border-left: 4px solid #ff6b6b; background: #f8f9fa; }
                .warning { border-left-color: #ffd93d; }
                .info { border-left-color: #6bcf7f; }
            </style>
        </head>
        <body>
            <h1>Code Analysis Results</h1>
            <div id="results">
                ${JSON.stringify(analysis, null, 2)}
            </div>
        </body>
        </html>
    `;
}

function getSuggestionsWebviewContent(suggestions: any): string {
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI Code Mentor Suggestions</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; }
                .suggestion { margin: 15px 0; padding: 15px; border: 1px solid #e1e5e9; border-radius: 6px; }
                .code-block { background: #f6f8fa; padding: 10px; border-radius: 4px; font-family: 'Monaco', monospace; }
            </style>
        </head>
        <body>
            <h1>GPT-4 Code Suggestions</h1>
            <div id="suggestions">
                ${JSON.stringify(suggestions, null, 2)}
            </div>
        </body>
        </html>
    `;
}

function updateDiagnostics(analysis: any, document: vscode.TextDocument) {
    // Implementation for real-time diagnostics
    // This would create vscode.Diagnostic objects and update them
    console.log('Updating diagnostics for:', document.fileName);
}

export function deactivate() {
    console.log('AI Code Mentor extension deactivated');
} 