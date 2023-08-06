import * as mixins from "./property_mixins";
import * as p from "./properties";
import { Context2d } from "./util/canvas";
import { Arrayable, uint32 } from "./types";
import { LineJoin, LineCap, FontStyle, TextAlign, TextBaseline } from "./enums";
import { View } from "./view";
export declare const hatch_aliases: {
    [key: string]: mixins.HatchPattern;
};
export declare abstract class ContextProperties {
    readonly obj: View;
    readonly prefix: string;
    /** @prototype */
    attrs: string[];
    protected readonly cache: {
        [key: string]: any;
    };
    private readonly _props;
    [Symbol.iterator](): Generator<p.Property<unknown>, void, undefined>;
    constructor(obj: View, prefix?: string);
    protected _v_get_color(prop: p.Property<unknown>, i: number): uint32;
    cache_select(prop: p.Property<unknown>, i: number): any;
    get_array(prop: p.Property<unknown>): Arrayable;
    abstract get doit(): boolean;
    protected abstract _set_vectorize(ctx: Context2d, i: number): void;
    protected abstract _set_value(ctx: Context2d): void;
}
declare class _Line extends ContextProperties {
    name: string;
    readonly line_color: p.ColorSpec;
    readonly line_width: p.NumberSpec;
    readonly line_alpha: p.NumberSpec;
    readonly line_join: p.Property<LineJoin>;
    readonly line_cap: p.Property<LineCap>;
    readonly line_dash: p.Array;
    readonly line_dash_offset: p.Number;
    get doit(): boolean;
    protected _set_value(ctx: Context2d): void;
    protected _set_vectorize(ctx: Context2d, i: number): void;
    color_value(): string;
}
declare class _Fill extends ContextProperties {
    name: string;
    readonly fill_color: p.ColorSpec;
    readonly fill_alpha: p.NumberSpec;
    get doit(): boolean;
    protected _set_value(ctx: Context2d): void;
    protected _set_vectorize(ctx: Context2d, i: number): void;
    color_value(): string;
}
declare class _Hatch extends ContextProperties {
    name: string;
    readonly hatch_color: p.ColorSpec;
    readonly hatch_alpha: p.NumberSpec;
    readonly hatch_scale: p.NumberSpec;
    readonly hatch_pattern: p.StringSpec;
    readonly hatch_weight: p.NumberSpec;
    protected _try_defer(defer_func: () => void): void;
    get doit(): boolean;
    protected _set_vectorize(ctx: Context2d, i: number): void;
    protected _set_value(ctx: Context2d): void;
    v_pattern(i: number): (ctx: Context2d) => CanvasPattern | null;
    pattern(): (ctx: Context2d) => CanvasPattern | null;
    color_value(): string;
}
declare class _Text extends ContextProperties {
    name: string;
    readonly text_font: p.Font;
    readonly text_font_size: p.StringSpec;
    readonly text_font_style: p.Property<FontStyle>;
    readonly text_color: p.ColorSpec;
    readonly text_alpha: p.NumberSpec;
    readonly text_align: p.Property<TextAlign>;
    readonly text_baseline: p.Property<TextBaseline>;
    readonly text_line_height: p.Number;
    color_value(): string;
    font_value(): string;
    v_font_value(i: number): string;
    get doit(): boolean;
    protected _set_value(ctx: Context2d): void;
    protected _set_vectorize(ctx: Context2d, i: number): void;
}
export declare class Visuals {
    constructor(view: View);
}
export declare class Line extends _Line {
    set_value(ctx: Context2d): void;
}
export declare class LineScalar extends Line {
}
export declare class LineVector extends _Line {
    set_vectorize(ctx: Context2d, i: number): void;
}
export declare class Fill extends _Fill {
    set_value(ctx: Context2d): void;
}
export declare class FillScalar extends Fill {
}
export declare class FillVector extends _Fill {
    set_vectorize(ctx: Context2d, i: number): void;
}
export declare class Text extends _Text {
    set_value(ctx: Context2d): void;
}
export declare class TextScalar extends Text {
}
export declare class TextVector extends _Text {
    set_vectorize(ctx: Context2d, i: number): void;
}
export declare class Hatch extends _Hatch {
    set_value(ctx: Context2d): void;
    doit2(ctx: Context2d, ready_func: () => void, defer_func: () => void): void;
}
export declare class HatchScalar extends Hatch {
}
export declare class HatchVector extends _Hatch {
    set_vectorize(ctx: Context2d, i: number): void;
    doit2(ctx: Context2d, i: number, ready_func: () => void, defer_func: () => void): void;
}
export {};
//# sourceMappingURL=visuals.d.ts.map