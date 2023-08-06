import { View } from "../../core/view";
import { RenderLevel } from "../../core/enums";
import * as p from "../../core/properties";
import { Model } from "../../model";
import { BBox } from "../../core/util/bbox";
import { CanvasLayer } from "../../core/util/canvas";
import type { Plot, PlotView } from "../plots/plot";
import { CoordinateTransform } from "../canvas/coordinates";
export declare abstract class RendererView extends View {
    model: Renderer;
    visuals: Renderer.Visuals;
    readonly parent: PlotView;
    needs_webgl_blit: boolean;
    private _coordinates;
    get coordinates(): CoordinateTransform;
    initialize(): void;
    connect_signals(): void;
    protected _initialize_coordinates(): void;
    get plot_view(): PlotView;
    get plot_model(): Plot;
    get layer(): CanvasLayer;
    request_render(): void;
    notify_finished(): void;
    interactive_bbox?(sx: number, sy: number): BBox;
    interactive_hit?(sx: number, sy: number): boolean;
    get needs_clip(): boolean;
    get has_webgl(): boolean;
    render(): void;
    protected abstract _render(): void;
    renderer_view<T extends Renderer>(_renderer: T): T["__view_type__"] | undefined;
}
export declare namespace Renderer {
    type Attrs = p.AttrsOf<Props>;
    type Props = Model.Props & {
        level: p.Property<RenderLevel>;
        visible: p.Property<boolean>;
        x_range_name: p.Property<string>;
        y_range_name: p.Property<string>;
    };
    type Visuals = {};
}
export interface Renderer extends Renderer.Attrs {
}
export declare abstract class Renderer extends Model {
    properties: Renderer.Props;
    __view_type__: RendererView;
    constructor(attrs?: Partial<Renderer.Attrs>);
    static init_Renderer(): void;
}
//# sourceMappingURL=renderer.d.ts.map