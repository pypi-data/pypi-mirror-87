import { Annotation, AnnotationView } from "./annotation";
import { ArrowHead, ArrowHeadView } from "./arrow_head";
import { ColumnarDataSource } from "../sources/columnar_data_source";
import { LineVector } from "../../core/property_mixins";
import * as visuals from "../../core/visuals";
import { SpatialUnits } from "../../core/enums";
import { Arrayable, NumberArray } from "../../core/types";
import * as p from "../../core/properties";
export declare type Coords = [Arrayable<number>, Arrayable<number>];
export declare class ArrowView extends AnnotationView {
    model: Arrow;
    visuals: Arrow.Visuals;
    protected start: ArrowHeadView | null;
    protected end: ArrowHeadView | null;
    protected _x_start: Arrayable<number>;
    protected _y_start: Arrayable<number>;
    protected _x_end: Arrayable<number>;
    protected _y_end: Arrayable<number>;
    protected _sx_start: NumberArray;
    protected _sy_start: NumberArray;
    protected _sx_end: NumberArray;
    protected _sy_end: NumberArray;
    protected _angles: NumberArray;
    initialize(): void;
    lazy_initialize(): Promise<void>;
    remove(): void;
    connect_signals(): void;
    set_data(source: ColumnarDataSource): void;
    protected _map_data(): void;
    protected _render(): void;
}
export declare namespace Arrow {
    type Attrs = p.AttrsOf<Props>;
    type Props = Annotation.Props & {
        x_start: p.XCoordinateSpec;
        y_start: p.YCoordinateSpec;
        start_units: p.Property<SpatialUnits>;
        start: p.Property<ArrowHead | null>;
        x_end: p.XCoordinateSpec;
        y_end: p.YCoordinateSpec;
        end_units: p.Property<SpatialUnits>;
        end: p.Property<ArrowHead | null>;
        source: p.Property<ColumnarDataSource>;
    } & Mixins;
    type Mixins = LineVector;
    type Visuals = Annotation.Visuals & {
        line: visuals.LineVector;
    };
}
export interface Arrow extends Arrow.Attrs {
}
export declare class Arrow extends Annotation {
    properties: Arrow.Props;
    __view_type__: ArrowView;
    constructor(attrs?: Partial<Arrow.Attrs>);
    static init_Arrow(): void;
}
//# sourceMappingURL=arrow.d.ts.map