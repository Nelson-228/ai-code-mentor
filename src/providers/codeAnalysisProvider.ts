import * as vscode from 'vscode';
import { spawn } from 'child_process';
import { GPTService, GPTSuggestion } from '../services/gptService';

export interface AnalysisResult {
    filePath: string;
    totalLines: number;
    functions: any[];
    issues: any[];
    complexityScore: number;
    suggestions: string[];
}

export class CodeAnalysisProvider {
    constructor(
        private analyzer: any, // PythonAnalyzer instance
        private gptService: GPTService
    ) {}

    async analyzeCode(code: string, filePath: string): Promise<AnalysisResult> {
        try {
            // Run Python AST analysis
            const astAnalysis = await this.runPythonAnalyzer(code, filePath);
            
            // Get GPT suggestions for the entire code
            const gptSuggestions = await this.gptService.getSuggestions(code, `Analyzing file: ${filePath}`);
            
            // Combine results
            return {
                ...astAnalysis,
                gptSuggestions: gptSuggestions
            };
        } catch (error) {
            console.error('Code analysis failed:', error);
            throw error;
        }
    }

    async getSuggestions(code: string, filePath: string): Promise<GPTSuggestion> {
        try {
            // Get context from AST analysis
            const astAnalysis = await this.runPythonAnalyzer(code, filePath);
            const context = this.buildContextString(astAnalysis);
            
            // Get GPT suggestions with context
            return await this.gptService.getSuggestions(code, context);
        } catch (error) {
            console.error('Failed to get suggestions:', error);
            throw error;
        }
    }

    private async runPythonAnalyzer(code: string, filePath: string): Promise<AnalysisResult> {
        return new Promise((resolve, reject) => {
            const pythonProcess = spawn('python', ['models/analyzer.py'], {
                stdio: ['pipe', 'pipe', 'pipe']
            });

            let output = '';
            let errorOutput = '';

            pythonProcess.stdout.on('data', (data) => {
                output += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                errorOutput += data.toString();
            });

            pythonProcess.on('close', (code) => {
                if (code === 0) {
                    try {
                        const result = JSON.parse(output);
                        resolve(result);
                    } catch (error) {
                        reject(new Error(`Failed to parse analyzer output: ${error}`));
                    }
                } else {
                    reject(new Error(`Python analyzer failed: ${errorOutput}`));
                }
            });

            // Send code to Python process
            pythonProcess.stdin.write(code);
            pythonProcess.stdin.end();
        });
    }

    private buildContextString(analysis: AnalysisResult): string {
        const context = [];
        
        if (analysis.functions.length > 0) {
            context.push(`File contains ${analysis.functions.length} functions`);
        }
        
        if (analysis.issues.length > 0) {
            context.push(`Found ${analysis.issues.length} code quality issues`);
        }
        
        if (analysis.complexityScore > 50) {
            context.push(`High complexity score: ${analysis.complexityScore}`);
        }
        
        return context.join('. ');
    }

    async refreshConfiguration(): Promise<void> {
        await this.gptService.refreshConfiguration();
    }
} 