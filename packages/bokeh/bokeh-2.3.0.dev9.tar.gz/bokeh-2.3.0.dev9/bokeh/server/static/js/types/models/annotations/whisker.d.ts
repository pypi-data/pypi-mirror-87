import { UpperLower, UpperLowerView } from "./upper_lower";
import { ArrowHead, ArrowHeadView } from "./arrow_head";
import { LineVector } from "../../core/property_mixins";
import * as visuals from "../../core/visuals";
import * as p from "../../core/properties";
export declare class WhiskerView extends UpperLowerView {
    model: Whisker;
    visuals: Whisker.Visuals;
    protected lower_head: ArrowHeadView | null;
    protected upper_head: ArrowHeadView | null;
    lazy_initialize(): Promise<void>;
    connect_signals(): void;
    protected _render(): void;
}
export declare namespace Whisker {
    type Attrs = p.AttrsOf<Props>;
    type Props = UpperLower.Props & {
        lower_head: p.Property<ArrowHead | null>;
        upper_head: p.Property<ArrowHead | null>;
    } & Mixins;
    type Mixins = LineVector;
    type Visuals = UpperLower.Visuals & {
        line: visuals.LineVector;
    };
}
export interface Whisker extends Whisker.Attrs {
}
export declare class Whisker extends UpperLower {
    properties: Whisker.Props;
    __view_type__: WhiskerView;
    constructor(attrs?: Partial<Whisker.Attrs>);
    static init_Whisker(): void;
}
//# sourceMappingURL=whisker.d.ts.map