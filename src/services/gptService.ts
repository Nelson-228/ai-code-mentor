import * as vscode from 'vscode';
import OpenAI from 'openai';

export interface GPTSuggestion {
    improvedCode: string;
    timeComplexity: string;
    spaceComplexity: string;
    explanation: string;
    suggestions: string[];
}

export class GPTService {
    private openai: OpenAI | null = null;
    private apiKey: string | undefined;

    constructor() {
        this.initializeOpenAI();
    }

    private initializeOpenAI(): void {
        this.apiKey = vscode.workspace.getConfiguration('aiCodeMentor').get('openaiApiKey');
        
        if (this.apiKey) {
            this.openai = new OpenAI({
                apiKey: this.apiKey,
            });
        }
    }

    async getSuggestions(code: string, context?: string): Promise<GPTSuggestion> {
        if (!this.openai) {
            throw new Error('OpenAI API key not configured. Please set aiCodeMentor.openaiApiKey in settings.');
        }

        const prompt = this.buildPrompt(code, context);

        try {
            const completion = await this.openai.chat.completions.create({
                model: 'gpt-4',
                messages: [
                    {
                        role: 'system',
                        content: 'You are an expert Python code reviewer and mentor. Provide clear, actionable feedback with code examples.'
                    },
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                temperature: 0.3,
                max_tokens: 2000
            });

            const response = completion.choices[0]?.message?.content;
            if (!response) {
                throw new Error('No response from GPT-4');
            }

            return this.parseGPTResponse(response);
        } catch (error) {
            console.error('GPT API call failed:', error);
            throw new Error(`Failed to get GPT suggestions: ${error}`);
        }
    }

    private buildPrompt(code: string, context?: string): string {
        return `
Please analyze this Python code and provide:

1. **Improved Code**: A cleaner, more efficient version of the code
2. **Time Complexity**: O() notation and explanation
3. **Space Complexity**: O() notation and explanation  
4. **What the code is doing**: Clear explanation of the code's purpose and logic
5. **Suggestions**: 2-3 specific improvements for code quality, readability, or performance

Code to analyze:
\`\`\`python
${code}
\`\`\`

${context ? `Context: ${context}` : ''}

Please format your response as JSON with the following structure:
{
    "improvedCode": "your improved code here",
    "timeComplexity": "O(n) - explanation",
    "spaceComplexity": "O(1) - explanation", 
    "explanation": "what the code does",
    "suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}
`;
    }

    private parseGPTResponse(response: string): GPTSuggestion {
        try {
            // Try to extract JSON from the response
            const jsonMatch = response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                const parsed = JSON.parse(jsonMatch[0]);
                return {
                    improvedCode: parsed.improvedCode || 'No improved code provided',
                    timeComplexity: parsed.timeComplexity || 'Not analyzed',
                    spaceComplexity: parsed.spaceComplexity || 'Not analyzed',
                    explanation: parsed.explanation || 'No explanation provided',
                    suggestions: parsed.suggestions || []
                };
            }
        } catch (error) {
            console.warn('Failed to parse GPT response as JSON:', error);
        }

        // Fallback: return structured response even if JSON parsing failed
        return {
            improvedCode: 'Unable to parse improved code from response',
            timeComplexity: 'Not analyzed',
            spaceComplexity: 'Not analyzed',
            explanation: response,
            suggestions: ['Review the response manually for suggestions']
        };
    }

    async refreshConfiguration(): Promise<void> {
        this.initializeOpenAI();
    }
} 