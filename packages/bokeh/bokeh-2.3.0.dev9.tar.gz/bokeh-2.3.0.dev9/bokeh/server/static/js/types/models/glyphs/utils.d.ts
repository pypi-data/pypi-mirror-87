import { Line, LineVector, Fill, FillVector, Hatch, HatchVector } from "../../core/visuals";
import { Context2d } from "../../core/util/canvas";
import { Rect } from "../../core/types";
import { PointGeometry, SpanGeometry } from "../../core/geometry";
import { GlyphRendererView } from "../renderers/glyph_renderer";
export declare function generic_line_scalar_legend(visuals: {
    line: Line;
}, ctx: Context2d, { x0, x1, y0, y1 }: Rect): void;
export declare function generic_line_vector_legend(visuals: {
    line: LineVector;
}, ctx: Context2d, { x0, x1, y0, y1 }: Rect, index: number): void;
export declare function generic_area_scalar_legend(visuals: {
    line?: Line;
    fill: Fill;
    hatch?: Hatch;
}, ctx: Context2d, { x0, x1, y0, y1 }: Rect): void;
export declare function generic_area_vector_legend(visuals: {
    line?: LineVector;
    fill: FillVector;
    hatch?: HatchVector;
}, ctx: Context2d, { x0, x1, y0, y1 }: Rect, index: number): void;
export { generic_line_vector_legend as generic_line_legend };
export { generic_area_vector_legend as generic_area_legend };
export declare function line_interpolation(renderer: GlyphRendererView, geometry: PointGeometry | SpanGeometry, x2: number, y2: number, x3: number, y3: number): [number, number];
//# sourceMappingURL=utils.d.ts.map