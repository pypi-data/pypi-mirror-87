import { Annotation, AnnotationView } from "./annotation";
import { ArrowHead, OpenHead } from "./arrow_head";
import { ColumnarDataSource } from "../sources/columnar_data_source";
import { ColumnDataSource } from "../sources/column_data_source";
import { LineVector } from "../../core/property_mixins";
import { SpatialUnits } from "../../core/enums";
import { NumberArray } from "../../core/types";
import { build_view } from "../../core/build_views";
import * as p from "../../core/properties";
import { atan2 } from "../../core/util/math";
export class ArrowView extends AnnotationView {
    initialize() {
        super.initialize();
        this.set_data(this.model.source);
    }
    async lazy_initialize() {
        await super.lazy_initialize();
        const { start, end } = this.model;
        const { parent } = this;
        if (start != null)
            this.start = await build_view(start, { parent });
        if (end != null)
            this.end = await build_view(end, { parent });
    }
    remove() {
        this.start?.remove();
        this.end?.remove();
        super.remove();
    }
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.change, () => this.set_data(this.model.source));
        this.connect(this.model.source.streaming, () => this.set_data(this.model.source));
        this.connect(this.model.source.patching, () => this.set_data(this.model.source));
        this.connect(this.model.source.change, () => this.set_data(this.model.source));
    }
    set_data(source) {
        super.set_data(source);
        this.plot_view.request_render();
    }
    _map_data() {
        const { frame } = this.plot_view;
        if (this.model.start_units == "data") {
            this._sx_start = this.coordinates.x_scale.v_compute(this._x_start);
            this._sy_start = this.coordinates.y_scale.v_compute(this._y_start);
        }
        else {
            this._sx_start = frame.xview.v_compute(this._x_start);
            this._sy_start = frame.yview.v_compute(this._y_start);
        }
        if (this.model.end_units == "data") {
            this._sx_end = this.coordinates.x_scale.v_compute(this._x_end);
            this._sy_end = this.coordinates.y_scale.v_compute(this._y_end);
        }
        else {
            this._sx_end = frame.xview.v_compute(this._x_end);
            this._sy_end = frame.yview.v_compute(this._y_end);
        }
        const { _sx_start, _sy_start, _sx_end, _sy_end } = this;
        const n = _sx_start.length;
        const angles = this._angles = new NumberArray(n);
        for (let i = 0; i < n; i++) {
            // arrow head runs orthogonal to arrow body (???)
            angles[i] = Math.PI / 2 + atan2([_sx_start[i], _sy_start[i]], [_sx_end[i], _sy_end[i]]);
        }
    }
    _render() {
        this._map_data();
        const { ctx } = this.layer;
        const { start, end } = this;
        const { _sx_start, _sy_start, _sx_end, _sy_end, _angles } = this;
        const { x, y, width, height } = this.plot_view.frame.bbox;
        for (let i = 0, n = _sx_start.length; i < n; i++) {
            if (end != null) {
                ctx.save();
                ctx.translate(_sx_end[i], _sy_end[i]);
                ctx.rotate(_angles[i]);
                end.render(ctx, i);
                ctx.restore();
            }
            if (start != null) {
                ctx.save();
                ctx.translate(_sx_start[i], _sy_start[i]);
                ctx.rotate(_angles[i] + Math.PI);
                start.render(ctx, i);
                ctx.restore();
            }
            if (this.visuals.line.doit) {
                ctx.save();
                if (start != null || end != null) {
                    ctx.beginPath();
                    ctx.rect(x, y, width, height);
                    if (end != null) {
                        ctx.save();
                        ctx.translate(_sx_end[i], _sy_end[i]);
                        ctx.rotate(_angles[i]);
                        end.clip(ctx, i);
                        ctx.restore();
                    }
                    if (start != null) {
                        ctx.save();
                        ctx.translate(_sx_start[i], _sy_start[i]);
                        ctx.rotate(_angles[i] + Math.PI);
                        start.clip(ctx, i);
                        ctx.restore();
                    }
                    ctx.closePath();
                    ctx.clip();
                }
                this.visuals.line.set_vectorize(ctx, i);
                ctx.beginPath();
                ctx.moveTo(_sx_start[i], _sy_start[i]);
                ctx.lineTo(_sx_end[i], _sy_end[i]);
                ctx.stroke();
                ctx.restore();
            }
        }
    }
}
ArrowView.__name__ = "ArrowView";
export class Arrow extends Annotation {
    constructor(attrs) {
        super(attrs);
    }
    static init_Arrow() {
        this.prototype.default_view = ArrowView;
        this.mixins(LineVector);
        this.define(({ Ref, Nullable }) => ({
            x_start: [p.XCoordinateSpec],
            y_start: [p.YCoordinateSpec],
            start_units: [SpatialUnits, "data"],
            start: [Nullable(Ref(ArrowHead)), null],
            x_end: [p.XCoordinateSpec],
            y_end: [p.YCoordinateSpec],
            end_units: [SpatialUnits, "data"],
            end: [Nullable(Ref(ArrowHead)), () => new OpenHead()],
            source: [Ref(ColumnarDataSource), () => new ColumnDataSource()],
        }));
    }
}
Arrow.__name__ = "Arrow";
Arrow.init_Arrow();
//# sourceMappingURL=arrow.js.map