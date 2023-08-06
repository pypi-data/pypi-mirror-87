import { MarkerType } from "../../core/enums";
import { LineVector, FillVector } from "../../core/visuals";
import { Context2d } from "../../core/util/canvas";
export declare type RenderOne = (ctx: Context2d, i: number, r: number, line: LineVector, fill: FillVector) => void;
export declare const marker_funcs: {
    [key in MarkerType]: RenderOne;
};
//# sourceMappingURL=defs.d.ts.map