import { BBox } from "./bbox";
import { OutputBackend } from "../enums";
export declare type Context2d = {
    setImageSmoothingEnabled(value: boolean): void;
    getImageSmoothingEnabled(): boolean;
    measureText(text: string): TextMetrics & {
        ascent: number;
    };
    lineDash: number[];
} & CanvasRenderingContext2D;
export declare class CanvasLayer {
    readonly backend: OutputBackend;
    readonly hidpi: boolean;
    private readonly _canvas;
    get canvas(): HTMLCanvasElement;
    private readonly _ctx;
    get ctx(): Context2d;
    private readonly _el;
    get el(): HTMLElement;
    readonly pixel_ratio: number;
    bbox: BBox;
    constructor(backend: OutputBackend, hidpi: boolean);
    resize(width: number, height: number): void;
    prepare(): void;
    clear(): void;
    finish(): void;
    to_blob(): Promise<Blob>;
}
//# sourceMappingURL=canvas.d.ts.map