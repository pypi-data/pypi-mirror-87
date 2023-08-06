import { View } from "../../core/view";
import * as visuals from "../../core/visuals";
import { RenderLevel } from "../../core/enums";
import { Model } from "../../model";
import { CoordinateTransform } from "../canvas/coordinates";
export class RendererView extends View {
    get coordinates() {
        return this._coordinates;
    }
    initialize() {
        super.initialize();
        this.visuals = new visuals.Visuals(this);
        this.needs_webgl_blit = false;
        this._initialize_coordinates();
    }
    connect_signals() {
        super.connect_signals();
        const { x_range_name, y_range_name } = this.model.properties;
        this.on_change([x_range_name, y_range_name], () => this._initialize_coordinates());
    }
    _initialize_coordinates() {
        const { x_range_name, y_range_name } = this.model;
        const { frame } = this.plot_view;
        const x_scale = frame.x_scales.get(x_range_name);
        const y_scale = frame.y_scales.get(y_range_name);
        this._coordinates = new CoordinateTransform(x_scale, y_scale);
    }
    get plot_view() {
        return this.parent;
    }
    get plot_model() {
        return this.parent.model;
    }
    get layer() {
        const { overlays, primary } = this.plot_view.canvas_view;
        return this.model.level == "overlay" ? overlays : primary;
    }
    request_render() {
        this.plot_view.request_render();
    }
    notify_finished() {
        this.plot_view.notify_finished();
    }
    get needs_clip() {
        return false;
    }
    get has_webgl() {
        return false;
    }
    render() {
        if (this.model.visible) {
            this._render();
        }
        this._has_finished = true;
    }
    renderer_view(_renderer) {
        return undefined;
    }
}
RendererView.__name__ = "RendererView";
export class Renderer extends Model {
    constructor(attrs) {
        super(attrs);
    }
    static init_Renderer() {
        this.define(({ Boolean, String }) => ({
            level: [RenderLevel, "image"],
            visible: [Boolean, true],
            x_range_name: [String, "default"],
            y_range_name: [String, "default"],
        }));
    }
}
Renderer.__name__ = "Renderer";
Renderer.init_Renderer();
//# sourceMappingURL=renderer.js.map