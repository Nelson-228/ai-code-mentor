declare module 'path' {
    export function join(...paths: string[]): string;
    export function resolve(...paths: string[]): string;
    export function dirname(path: string): string;
    export function basename(path: string, ext?: string): string;
    export function extname(path: string): string;
}

declare module 'fs' {
    export function readFileSync(path: string, encoding: string): string;
    export function writeFileSync(path: string, data: string, encoding?: string): void;
    export function existsSync(path: string): boolean;
    export function mkdirSync(path: string, options?: any): void;
} 