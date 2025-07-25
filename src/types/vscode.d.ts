declare module 'vscode' {
    export interface Thenable<T> extends Promise<T> {}
    export interface ExtensionContext {
        subscriptions: Disposable[];
        extensionUri: Uri;
    }

    export interface Disposable {
        dispose(): void;
    }

    export interface Uri {
        fsPath: string;
    }

    export namespace Uri {
        export function joinPath(base: Uri, ...pathSegments: string[]): Uri;
    }

    export interface TextDocument {
        fileName: string;
        languageId: string;
        getText(range?: Range): string;
    }

    export interface Range {
        start: Position;
        end: Position;
    }

    export interface Position {
        line: number;
        character: number;
    }

    export interface TextEditor {
        document: TextDocument;
        selection: Range;
        viewColumn?: ViewColumn;
    }

    export interface TextDocumentChangeEvent {
        document: TextDocument;
    }

    export interface WebviewPanel {
        webview: Webview;
        onDidDispose(callback: () => void, thisArg?: any, disposables?: Disposable[]): Disposable;
        onDidChangeViewState(callback: (e: WebviewPanelOnDidChangeViewStateEvent) => void, thisArg?: any, disposables?: Disposable[]): Disposable;
        reveal(column?: ViewColumn): void;
        dispose(): void;
        visible: boolean;
    }

    export interface WebviewPanelOnDidChangeViewStateEvent {
        webviewPanel: WebviewPanel;
    }

    export interface Webview {
        html: string;
    }

    export enum ViewColumn {
        One = 1,
        Two = 2
    }

    export namespace window {
        export function createWebviewPanel(viewType: string, title: string, column: ViewColumn, options: any): WebviewPanel;
        export const activeTextEditor: TextEditor | undefined;
        export function showWarningMessage(message: string): Thenable<string | undefined>;
        export function showErrorMessage(message: string): Thenable<string | undefined>;
    }

    export namespace workspace {
        export function onDidChangeTextDocument(listener: (e: TextDocumentChangeEvent) => any): Disposable;
    }

    export namespace commands {
        export function registerCommand(command: string, callback: (...args: any[]) => any): Disposable;
    }
} 