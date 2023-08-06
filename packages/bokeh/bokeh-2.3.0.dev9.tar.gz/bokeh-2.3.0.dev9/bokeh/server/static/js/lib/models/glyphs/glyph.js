import * as p from "../../core/properties";
import * as bbox from "../../core/util/bbox";
import * as visuals from "../../core/visuals";
import { View } from "../../core/view";
import { Model } from "../../model";
import { logger } from "../../core/logging";
import { Indices } from "../../core/types";
import { RaggedArray } from "../../core/util/ragged_array";
import { map, max } from "../../core/util/arrayable";
import { values } from "../../core/util/object";
import { is_equal } from "../../core/util/eq";
import { SpatialIndex } from "../../core/util/spatial";
import { FactorRange } from "../ranges/factor_range";
import { Selection } from "../selections/selection";
export class GlyphView extends View {
    constructor() {
        super(...arguments);
        this._index = null;
        this._data_size = null;
        this._nohit_warned = new Set();
    }
    get renderer() {
        return this.parent;
    }
    get has_webgl() {
        return this.glglyph != null;
    }
    get index() {
        const { _index } = this;
        if (_index != null)
            return _index;
        else
            throw new Error(`${this}.index_data() wasn't called`);
    }
    get data_size() {
        const { _data_size } = this;
        if (_data_size != null)
            return _data_size;
        else
            throw new Error(`${this}.set_data() wasn't called`);
    }
    initialize() {
        super.initialize();
        this.visuals = new visuals.Visuals(this);
    }
    render(ctx, indices, data) {
        ctx.beginPath();
        if (this.glglyph != null) {
            this.renderer.needs_webgl_blit = this.glglyph.render(ctx, indices, data);
            if (this.renderer.needs_webgl_blit)
                return;
        }
        this._render(ctx, indices, data);
    }
    has_finished() {
        return true;
    }
    notify_finished() {
        this.renderer.notify_finished();
    }
    _bounds(bounds) {
        return bounds;
    }
    bounds() {
        return this._bounds(this.index.bbox);
    }
    log_bounds() {
        const { x0, x1 } = this.index.bounds(bbox.positive_x());
        const { y0, y1 } = this.index.bounds(bbox.positive_y());
        return this._bounds({ x0, y0, x1, y1 });
    }
    get_anchor_point(anchor, i, [sx, sy]) {
        switch (anchor) {
            case "center": {
                const [x, y] = this.scenterxy(i, sx, sy);
                return { x, y };
            }
            default:
                return null;
        }
    }
    /** @deprecated */
    scenterx(i, sx, sy) {
        return this.scenterxy(i, sx, sy)[0];
    }
    /** @deprecated */
    scentery(i, sx, sy) {
        return this.scenterxy(i, sx, sy)[1];
    }
    sdist(scale, pts, spans, pts_location = "edge", dilate = false) {
        let pt0;
        let pt1;
        const n = pts.length;
        if (pts_location == 'center') {
            const halfspan = map(spans, (d) => d / 2);
            pt0 = new Float64Array(n);
            for (let i = 0; i < n; i++) {
                pt0[i] = pts[i] - halfspan[i];
            }
            pt1 = new Float64Array(n);
            for (let i = 0; i < n; i++) {
                pt1[i] = pts[i] + halfspan[i];
            }
        }
        else {
            pt0 = pts;
            pt1 = new Float64Array(n);
            for (let i = 0; i < n; i++) {
                pt1[i] = pt0[i] + spans[i];
            }
        }
        const spt0 = scale.v_compute(pt0);
        const spt1 = scale.v_compute(pt1);
        if (dilate)
            return map(spt0, (_, i) => Math.ceil(Math.abs(spt1[i] - spt0[i])));
        else
            return map(spt0, (_, i) => Math.abs(spt1[i] - spt0[i]));
    }
    draw_legend_for_index(_ctx, _bbox, _index) { }
    hit_test(geometry) {
        switch (geometry.type) {
            case "point":
                if (this._hit_point != null)
                    return this._hit_point(geometry);
                break;
            case "span":
                if (this._hit_span != null)
                    return this._hit_span(geometry);
                break;
            case "rect":
                if (this._hit_rect != null)
                    return this._hit_rect(geometry);
                break;
            case "poly":
                if (this._hit_poly != null)
                    return this._hit_poly(geometry);
                break;
        }
        if (!this._nohit_warned.has(geometry.type)) {
            logger.debug(`'${geometry.type}' selection not available for ${this.model.type}`);
            this._nohit_warned.add(geometry.type);
        }
        return null;
    }
    _hit_rect_against_index(geometry) {
        const { sx0, sx1, sy0, sy1 } = geometry;
        const [x0, x1] = this.renderer.coordinates.x_scale.r_invert(sx0, sx1);
        const [y0, y1] = this.renderer.coordinates.y_scale.r_invert(sy0, sy1);
        const indices = [...this.index.indices({ x0, x1, y0, y1 })];
        return new Selection({ indices });
    }
    _project_data() { }
    *_iter_visuals() {
        for (const visual of values(this.visuals)) {
            for (const prop of visual) {
                if (prop instanceof p.VectorSpec)
                    yield prop;
            }
        }
    }
    set_base(base) {
        if (base != this && base instanceof this.constructor)
            this.base = base;
    }
    set_visuals(source, indices) {
        const self = this;
        for (const prop of this._iter_visuals()) {
            const { base } = this;
            if (base != null) {
                const base_prop = base.model.properties[prop.attr];
                if (base_prop != null && is_equal(prop.get_value(), base_prop.get_value())) {
                    self[`_${prop.attr}`] = base[`_${prop.attr}`];
                    self[`_${prop.attr}_view`] = base[`_${prop.attr}_view`];
                    continue;
                }
            }
            const base_array = prop.array(source);
            const array = indices.select(base_array);
            self[`_${prop.attr}`] = array;
            if (array instanceof Uint32Array)
                self[`_${prop.attr}_view`] = new DataView(array.buffer);
        }
        this.glglyph?.set_visuals_changed();
    }
    set_data(source, indices, indices_to_update) {
        const { x_range, y_range } = this.renderer.coordinates;
        this._data_size = indices.count;
        const visual_props = new Set(this._iter_visuals());
        for (const prop of this.model) {
            if (!(prop instanceof p.VectorSpec))
                continue;
            if (visual_props.has(prop)) // let set_visuals() do the work, at least for now
                continue;
            // this skips optional properties like radius for circles
            if (prop.optional && prop.spec.value == null && !prop.dirty)
                continue;
            const name = prop.attr;
            const base_array = prop.array(source);
            let array = indices.select(base_array);
            if (prop instanceof p.BaseCoordinateSpec) {
                const range = prop.dimension == "x" ? x_range : y_range;
                if (range instanceof FactorRange) {
                    if (prop instanceof p.CoordinateSpec) {
                        array = range.v_synthetic(array);
                    }
                    else if (prop instanceof p.CoordinateSeqSpec) {
                        for (let i = 0; i < array.length; i++) {
                            array[i] = range.v_synthetic(array[i]);
                        }
                    }
                }
                if (prop instanceof p.CoordinateSeqSpec) {
                    array = RaggedArray.from(array);
                }
            }
            else if (prop instanceof p.DistanceSpec) {
                this[`max_${name}`] = max(array);
            }
            this[`_${name}`] = array;
        }
        if (this.renderer.plot_view.model.use_map) {
            this._project_data();
        }
        this._set_data(indices_to_update); // TODO doesn't take subset indices into account
        this.glglyph?.set_data_changed();
        this.index_data();
    }
    _set_data(_indices) { }
    get _index_size() {
        return this.data_size;
    }
    index_data() {
        const index = new SpatialIndex(this._index_size);
        this._index_data(index);
        index.finish();
        this._index = index;
    }
    mask_data() {
        /** Returns subset indices in the viewport. */
        if (this._mask_data == null)
            return Indices.all_set(this.data_size);
        else
            return this._mask_data();
    }
    map_data() {
        const self = this;
        const { x_scale, y_scale } = this.renderer.coordinates;
        for (const prop of this.model) {
            if (prop instanceof p.BaseCoordinateSpec) {
                const scale = prop.dimension == "x" ? x_scale : y_scale;
                let array = self[`_${prop.attr}`];
                if (array instanceof RaggedArray) {
                    const screen = scale.v_compute(array.array);
                    array = new RaggedArray(array.offsets, screen);
                }
                else {
                    array = scale.v_compute(array);
                }
                this[`s${prop.attr}`] = array;
            }
        }
        this._map_data();
        this.glglyph?.set_data_changed();
    }
    // This is where specs not included in coords are computed, e.g. radius.
    _map_data() { }
}
GlyphView.__name__ = "GlyphView";
export class Glyph extends Model {
    constructor(attrs) {
        super(attrs);
    }
}
Glyph.__name__ = "Glyph";
//# sourceMappingURL=glyph.js.map