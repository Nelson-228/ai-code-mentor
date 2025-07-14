import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('ai-code-mentor'));
    });

    test('Should activate', async () => {
        const ext = vscode.extensions.getExtension('ai-code-mentor');
        if (ext) {
            await ext.activate();
            assert.ok(true);
        }
    });

    test('Should register commands', async () => {
        const commands = await vscode.commands.getCommands();
        assert.ok(commands.includes('ai-code-mentor.analyzeCode'));
        assert.ok(commands.includes('ai-code-mentor.getSuggestions'));
    });
}); 