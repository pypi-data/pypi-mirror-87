import { Marker, MarkerView } from "./marker";
import { marker_funcs } from "./defs";
import { MarkerGL } from "./webgl/markers";
import * as p from "../../core/properties";
export class ScatterView extends MarkerView {
    _init_webgl() {
        const { webgl } = this.renderer.plot_view.canvas_view;
        if (webgl != null) {
            const marker_types = new Set(this._marker);
            if (marker_types.size == 1) {
                const [marker_type] = [...marker_types];
                if (MarkerGL.is_supported(marker_type)) {
                    const { glglyph } = this;
                    if (glglyph == null || glglyph.marker_type != marker_type) {
                        this.glglyph = new MarkerGL(webgl.gl, this, marker_type);
                        return;
                    }
                }
            }
        }
        delete this.glglyph;
    }
    _set_data(indices) {
        super._set_data(indices);
        this._init_webgl();
    }
    _render(ctx, indices, { sx, sy, _size, _angle, _marker }) {
        for (const i of indices) {
            if (isNaN(sx[i] + sy[i] + _size[i] + _angle[i]) || _marker[i] == null)
                continue;
            const r = _size[i] / 2;
            ctx.beginPath();
            ctx.translate(sx[i], sy[i]);
            if (_angle[i])
                ctx.rotate(_angle[i]);
            marker_funcs[_marker[i]](ctx, i, r, this.visuals.line, this.visuals.fill);
            if (_angle[i])
                ctx.rotate(-_angle[i]);
            ctx.translate(-sx[i], -sy[i]);
        }
    }
    draw_legend_for_index(ctx, { x0, x1, y0, y1 }, index) {
        const args = this._get_legend_args({ x0, x1, y0, y1 }, index);
        const len = index + 1;
        const marker = new Array(len);
        marker[index] = this._marker[index];
        args._marker = marker;
        this._render(ctx, [index], args); // XXX
    }
}
ScatterView.__name__ = "ScatterView";
export class Scatter extends Marker {
    constructor(attrs) {
        super(attrs);
    }
    static init_Scatter() {
        this.prototype.default_view = ScatterView;
        this.define(() => ({
            marker: [p.MarkerSpec, { value: "circle" }],
        }));
    }
}
Scatter.__name__ = "Scatter";
Scatter.init_Scatter();
//# sourceMappingURL=scatter.js.map