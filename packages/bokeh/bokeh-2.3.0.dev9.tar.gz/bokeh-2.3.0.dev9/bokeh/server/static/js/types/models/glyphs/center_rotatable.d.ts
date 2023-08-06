import { XYGlyph, XYGlyphView, XYGlyphData } from "./xy_glyph";
import { LineVector, FillVector } from "../../core/property_mixins";
import * as visuals from "../../core/visuals";
import { NumberArray, Rect } from "../../core/types";
import * as p from "../../core/properties";
export interface CenterRotatableData extends XYGlyphData {
    _angle: NumberArray;
    _width: NumberArray;
    _height: NumberArray;
    sw: NumberArray;
    sh: NumberArray;
    max_width: number;
    max_height: number;
}
export interface CenterRotatableView extends CenterRotatableData {
}
export declare abstract class CenterRotatableView extends XYGlyphView {
    model: CenterRotatable;
    visuals: CenterRotatable.Visuals;
    get max_w2(): number;
    get max_h2(): number;
    protected _bounds({ x0, x1, y0, y1 }: Rect): Rect;
}
export declare namespace CenterRotatable {
    type Attrs = p.AttrsOf<Props>;
    type Props = XYGlyph.Props & {
        angle: p.AngleSpec;
        width: p.DistanceSpec;
        height: p.DistanceSpec;
    } & Mixins;
    type Mixins = LineVector & FillVector;
    type Visuals = XYGlyph.Visuals & {
        line: visuals.LineVector;
        fill: visuals.FillVector;
    };
}
export interface CenterRotatable extends CenterRotatable.Attrs {
}
export declare abstract class CenterRotatable extends XYGlyph {
    properties: CenterRotatable.Props;
    __view_type__: CenterRotatableView;
    constructor(attrs?: Partial<CenterRotatable.Attrs>);
    static init_CenterRotatable(): void;
}
//# sourceMappingURL=center_rotatable.d.ts.map