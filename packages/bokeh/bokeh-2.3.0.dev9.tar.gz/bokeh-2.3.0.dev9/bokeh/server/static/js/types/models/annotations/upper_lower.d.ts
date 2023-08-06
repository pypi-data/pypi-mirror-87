import { Annotation, AnnotationView } from "./annotation";
import { ColumnarDataSource } from "../sources/columnar_data_source";
import { Arrayable } from "../../core/types";
import { Dimension, SpatialUnits } from "../../core/enums";
import * as p from "../../core/properties";
export declare abstract class UpperLowerView extends AnnotationView {
    model: UpperLower;
    visuals: UpperLower.Visuals;
    protected _lower: Arrayable<number>;
    protected _upper: Arrayable<number>;
    protected _base: Arrayable<number>;
    protected _lower_sx: Arrayable<number>;
    protected _lower_sy: Arrayable<number>;
    protected _upper_sx: Arrayable<number>;
    protected _upper_sy: Arrayable<number>;
    initialize(): void;
    set_data(source: ColumnarDataSource): void;
    protected _map_data(): void;
}
export declare class XOrYCoordinateSpec extends p.CoordinateSpec {
    readonly obj: UpperLower;
    spec: p.Spec & {
        units: SpatialUnits;
    };
    get dimension(): "x" | "y";
    get units(): SpatialUnits;
}
export declare namespace UpperLower {
    type Attrs = p.AttrsOf<Props>;
    type Props = Annotation.Props & {
        dimension: p.Property<Dimension>;
        lower: XOrYCoordinateSpec;
        upper: XOrYCoordinateSpec;
        base: XOrYCoordinateSpec;
        source: p.Property<ColumnarDataSource>;
    };
    type Visuals = Annotation.Visuals;
}
export interface UpperLower extends UpperLower.Attrs {
}
export declare class UpperLower extends Annotation {
    properties: UpperLower.Props;
    constructor(attrs?: Partial<UpperLower.Attrs>);
    static init_UpperLower(): void;
}
//# sourceMappingURL=upper_lower.d.ts.map