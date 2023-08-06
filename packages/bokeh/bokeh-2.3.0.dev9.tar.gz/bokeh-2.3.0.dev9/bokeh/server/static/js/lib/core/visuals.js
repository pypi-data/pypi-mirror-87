import * as mixins from "./property_mixins";
import { color2css } from "./util/color";
import { SVGRenderingContext2D } from "./util/svg";
import { CanvasLayer } from "./util/canvas";
const { hasOwnProperty } = Object.prototype;
function _horz(ctx, h, h2) {
    ctx.moveTo(0, h2 + 0.5);
    ctx.lineTo(h, h2 + 0.5);
    ctx.stroke();
}
function _vert(ctx, h, h2) {
    ctx.moveTo(h2 + 0.5, 0);
    ctx.lineTo(h2 + 0.5, h);
    ctx.stroke();
}
function _x(ctx, h) {
    ctx.moveTo(0, h);
    ctx.lineTo(h, 0);
    ctx.stroke();
    ctx.moveTo(0, 0);
    ctx.lineTo(h, h);
    ctx.stroke();
}
export const hatch_aliases = {
    " ": "blank",
    ".": "dot",
    o: "ring",
    "-": "horizontal_line",
    "|": "vertical_line",
    "+": "cross",
    "\"": "horizontal_dash",
    ":": "vertical_dash",
    "@": "spiral",
    "/": "right_diagonal_line",
    "\\": "left_diagonal_line",
    x: "diagonal_cross",
    ",": "right_diagonal_dash",
    "`": "left_diagonal_dash",
    v: "horizontal_wave",
    ">": "vertical_wave",
    "*": "criss_cross",
};
function get_pattern(pattern, color, alpha, scale, weight) {
    return (ctx) => {
        // TODO: this needs a canvas provider instead of trying to guess what to use
        const output_backend = ctx instanceof SVGRenderingContext2D ? "svg" : "canvas";
        const region = new CanvasLayer(output_backend, true);
        region.resize(scale, scale);
        region.prepare();
        create_hatch_canvas(region.ctx, pattern, color, alpha, scale, weight);
        return ctx.createPattern(region.canvas, "repeat");
    };
}
function create_hatch_canvas(ctx, hatch_pattern, hatch_color, hatch_alpha, hatch_scale, hatch_weight) {
    const h = hatch_scale;
    const h2 = h / 2;
    const h4 = h2 / 2;
    const color = color2css(hatch_color, hatch_alpha);
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineCap = "square";
    ctx.lineWidth = hatch_weight;
    switch (hatch_aliases[hatch_pattern] ?? hatch_pattern) {
        // we should not need these if code conditions on hatch.doit, but
        // include them here just for completeness
        case "blank":
            break;
        case "dot":
            ctx.arc(h2, h2, h2 / 2, 0, 2 * Math.PI, true);
            ctx.fill();
            break;
        case "ring":
            ctx.arc(h2, h2, h2 / 2, 0, 2 * Math.PI, true);
            ctx.stroke();
            break;
        case "horizontal_line":
            _horz(ctx, h, h2);
            break;
        case "vertical_line":
            _vert(ctx, h, h2);
            break;
        case "cross":
            _horz(ctx, h, h2);
            _vert(ctx, h, h2);
            break;
        case "horizontal_dash":
            _horz(ctx, h2, h2);
            break;
        case "vertical_dash":
            _vert(ctx, h2, h2);
            break;
        case "spiral": {
            const h30 = h / 30;
            ctx.moveTo(h2, h2);
            for (let i = 0; i < 360; i++) {
                const angle = 0.1 * i;
                const x = h2 + (h30 * angle) * Math.cos(angle);
                const y = h2 + (h30 * angle) * Math.sin(angle);
                ctx.lineTo(x, y);
            }
            ctx.stroke();
            break;
        }
        case "right_diagonal_line":
            ctx.moveTo(-h4 + 0.5, h);
            ctx.lineTo(h4 + 0.5, 0);
            ctx.stroke();
            ctx.moveTo(h4 + 0.5, h);
            ctx.lineTo(3 * h4 + 0.5, 0);
            ctx.stroke();
            ctx.moveTo(3 * h4 + 0.5, h);
            ctx.lineTo(5 * h4 + 0.5, 0);
            ctx.stroke();
            ctx.stroke();
            break;
        case "left_diagonal_line":
            ctx.moveTo(h4 + 0.5, h);
            ctx.lineTo(-h4 + 0.5, 0);
            ctx.stroke();
            ctx.moveTo(3 * h4 + 0.5, h);
            ctx.lineTo(h4 + 0.5, 0);
            ctx.stroke();
            ctx.moveTo(5 * h4 + 0.5, h);
            ctx.lineTo(3 * h4 + 0.5, 0);
            ctx.stroke();
            ctx.stroke();
            break;
        case "diagonal_cross":
            _x(ctx, h);
            break;
        case "right_diagonal_dash":
            ctx.moveTo(h4 + 0.5, 3 * h4 + 0.5);
            ctx.lineTo(3 * h4 + 0.5, h4 + 0.5);
            ctx.stroke();
            break;
        case "left_diagonal_dash":
            ctx.moveTo(h4 + 0.5, h4 + 0.5);
            ctx.lineTo(3 * h4 + 0.5, 3 * h4 + 0.5);
            ctx.stroke();
            break;
        case "horizontal_wave":
            ctx.moveTo(0, h4);
            ctx.lineTo(h2, 3 * h4);
            ctx.lineTo(h, h4);
            ctx.stroke();
            break;
        case "vertical_wave":
            ctx.moveTo(h4, 0);
            ctx.lineTo(3 * h4, h2);
            ctx.lineTo(h4, h);
            ctx.stroke();
            break;
        case "criss_cross":
            _x(ctx, h);
            _horz(ctx, h, h2);
            _vert(ctx, h, h2);
            break;
    }
}
export class ContextProperties {
    constructor(obj, prefix = "") {
        this.obj = obj;
        this.prefix = prefix;
        this.cache = {};
        const self = this;
        this._props = [];
        for (const attr of this.attrs) {
            const prop = obj.model.properties[prefix + attr];
            self[attr] = prop;
            this._props.push(prop);
        }
    }
    *[Symbol.iterator]() {
        yield* this._props;
    }
    _v_get_color(prop, i) {
        if (prop.is_value)
            return prop.spec.value;
        else {
            const view = this.obj[`_${prop.attr}_view`];
            return view.getUint32(4 * i);
        }
    }
    cache_select(prop, i) {
        if (prop.is_value)
            return prop.spec.value;
        else
            return this.obj[`_${prop.attr}`][i];
    }
    get_array(prop) {
        return this.obj[`_${prop.attr}`];
    }
}
ContextProperties.__name__ = "ContextProperties";
class _Line extends ContextProperties {
    constructor() {
        super(...arguments);
        this.name = "line";
    }
    get doit() {
        return !(this.line_color.spec.value === null ||
            this.line_alpha.spec.value == 0 ||
            this.line_width.spec.value == 0);
    }
    _set_value(ctx) {
        const color = this.line_color.value();
        const alpha = this.line_alpha.value();
        ctx.strokeStyle = color2css(color, alpha);
        ctx.lineWidth = this.line_width.value();
        ctx.lineJoin = this.line_join.value();
        ctx.lineCap = this.line_cap.value();
        ctx.lineDash = this.line_dash.value();
        ctx.lineDashOffset = this.line_dash_offset.value();
    }
    _set_vectorize(ctx, i) {
        const color = this._v_get_color(this.line_color, i);
        const alpha = this.cache_select(this.line_alpha, i);
        const width = this.cache_select(this.line_width, i);
        const join = this.cache_select(this.line_join, i);
        const cap = this.cache_select(this.line_cap, i);
        const dash = this.cache_select(this.line_dash, i);
        const offset = this.cache_select(this.line_dash_offset, i);
        ctx.strokeStyle = color2css(color, alpha);
        ctx.lineWidth = width;
        ctx.lineJoin = join;
        ctx.lineCap = cap;
        ctx.lineDash = dash;
        ctx.lineDashOffset = offset;
    }
    color_value() {
        return color2css(this.line_color.value(), this.line_alpha.value());
    }
}
_Line.__name__ = "_Line";
_Line.prototype.attrs = Object.keys(mixins.LineVector);
class _Fill extends ContextProperties {
    constructor() {
        super(...arguments);
        this.name = "fill";
    }
    get doit() {
        return !(this.fill_color.spec.value === null ||
            this.fill_alpha.spec.value == 0);
    }
    _set_value(ctx) {
        const color = this.fill_color.value();
        const alpha = this.fill_alpha.value();
        ctx.fillStyle = color2css(color, alpha);
    }
    _set_vectorize(ctx, i) {
        const color = this._v_get_color(this.fill_color, i);
        const alpha = this.cache_select(this.fill_alpha, i);
        ctx.fillStyle = color2css(color, alpha);
    }
    color_value() {
        return color2css(this.fill_color.value(), this.fill_alpha.value());
    }
}
_Fill.__name__ = "_Fill";
_Fill.prototype.attrs = Object.keys(mixins.FillVector);
class _Hatch extends ContextProperties {
    constructor() {
        super(...arguments);
        this.name = "hatch";
    }
    _try_defer(defer_func) {
        const { hatch_pattern, hatch_extra } = this.cache;
        if (hatch_extra != null && hasOwnProperty.call(hatch_extra, hatch_pattern)) {
            const custom = hatch_extra[hatch_pattern];
            custom.onload(defer_func);
        }
    }
    get doit() {
        return !(this.hatch_color.spec.value === null ||
            this.hatch_alpha.spec.value == 0 ||
            this.hatch_pattern.spec.value == " " ||
            this.hatch_pattern.spec.value == "blank" ||
            this.hatch_pattern.spec.value === null);
    }
    _set_vectorize(ctx, i) {
        const pattern = this.v_pattern(i)(ctx);
        ctx.fillStyle = pattern != null ? pattern : ""; // XXX: deal with null
    }
    _set_value(ctx) {
        const pattern = this.pattern()(ctx);
        ctx.fillStyle = pattern != null ? pattern : ""; // XXX: deal with null
    }
    v_pattern(i) {
        const color = this._v_get_color(this.hatch_color, i);
        const alpha = this.cache_select(this.hatch_alpha, i);
        const scale = this.cache_select(this.hatch_scale, i);
        const pattern = this.cache_select(this.hatch_pattern, i);
        const weight = this.cache_select(this.hatch_weight, i);
        const { hatch_extra } = this.cache;
        if (hatch_extra != null && hasOwnProperty.call(hatch_extra, pattern))
            this.cache.pattern = hatch_extra[pattern].get_pattern(color, alpha, scale, weight);
        else
            this.cache.pattern = get_pattern(pattern, color, alpha, scale, weight);
        return this.cache.pattern;
    }
    pattern() {
        const color = this.hatch_color.value();
        const alpha = this.hatch_alpha.value();
        const scale = this.hatch_scale.value();
        const pattern = this.hatch_pattern.value();
        const weight = this.hatch_weight.value();
        const { hatch_extra } = this.cache;
        if (hatch_extra != null && hasOwnProperty.call(hatch_extra, pattern))
            return hatch_extra[pattern].get_pattern(color, alpha, scale, weight);
        else
            return get_pattern(pattern, color, alpha, scale, weight);
    }
    color_value() {
        return color2css(this.hatch_color.value(), this.hatch_alpha.value());
    }
}
_Hatch.__name__ = "_Hatch";
_Hatch.prototype.attrs = Object.keys(mixins.HatchVector);
class _Text extends ContextProperties {
    constructor() {
        super(...arguments);
        this.name = "text";
    }
    color_value() {
        return color2css(this.text_color.value(), this.text_alpha.value());
    }
    font_value() {
        const style = this.text_font_style.value();
        const size = this.text_font_size.value();
        const face = this.text_font.value();
        return `${style} ${size} ${face}`;
    }
    v_font_value(i) {
        const style = super.cache_select(this.text_font_style, i);
        const size = super.cache_select(this.text_font_size, i);
        const face = super.cache_select(this.text_font, i);
        return `${style} ${size} ${face}`;
    }
    get doit() {
        return !(this.text_color.spec.value === null ||
            this.text_alpha.spec.value == 0);
    }
    _set_value(ctx) {
        const color = this.text_color.value();
        const alpha = this.text_alpha.value();
        ctx.fillStyle = color2css(color, alpha);
        ctx.font = this.font_value();
        ctx.textAlign = this.text_align.value();
        ctx.textBaseline = this.text_baseline.value();
    }
    _set_vectorize(ctx, i) {
        const color = this._v_get_color(this.text_color, i);
        const alpha = this.cache_select(this.text_alpha, i);
        const font = this.v_font_value(i);
        const align = this.cache_select(this.text_align, i);
        const baseline = this.cache_select(this.text_baseline, i);
        ctx.fillStyle = color2css(color, alpha);
        ctx.font = font;
        ctx.textAlign = align;
        ctx.textBaseline = baseline;
    }
}
_Text.__name__ = "_Text";
_Text.prototype.attrs = Object.keys(mixins.TextVector);
export class Visuals {
    constructor(view) {
        const self = this;
        for (const [prefix, mixin] of view.model._mixins) {
            const visual = (() => {
                switch (mixin) {
                    case mixins.Line: return new Line(view, prefix);
                    case mixins.LineScalar: return new LineScalar(view, prefix);
                    case mixins.LineVector: return new LineVector(view, prefix);
                    case mixins.Fill: return new Fill(view, prefix);
                    case mixins.FillScalar: return new FillScalar(view, prefix);
                    case mixins.FillVector: return new FillVector(view, prefix);
                    case mixins.Text: return new Text(view, prefix);
                    case mixins.TextScalar: return new TextScalar(view, prefix);
                    case mixins.TextVector: return new TextVector(view, prefix);
                    case mixins.Hatch: return new Hatch(view, prefix);
                    case mixins.HatchScalar: return new HatchScalar(view, prefix);
                    case mixins.HatchVector: return new HatchVector(view, prefix);
                    default:
                        throw new Error("unknown visual");
                }
            })();
            self[prefix + visual.name] = visual;
        }
    }
}
Visuals.__name__ = "Visuals";
export class Line extends _Line {
    set_value(ctx) {
        this._set_value(ctx);
    }
}
Line.__name__ = "Line";
export class LineScalar extends Line {
}
LineScalar.__name__ = "LineScalar";
export class LineVector extends _Line {
    set_vectorize(ctx, i) {
        this._set_vectorize(ctx, i);
    }
}
LineVector.__name__ = "LineVector";
export class Fill extends _Fill {
    set_value(ctx) {
        this._set_value(ctx);
    }
}
Fill.__name__ = "Fill";
export class FillScalar extends Fill {
}
FillScalar.__name__ = "FillScalar";
export class FillVector extends _Fill {
    set_vectorize(ctx, i) {
        this._set_vectorize(ctx, i);
    }
}
FillVector.__name__ = "FillVector";
export class Text extends _Text {
    set_value(ctx) {
        this._set_value(ctx);
    }
}
Text.__name__ = "Text";
export class TextScalar extends Text {
}
TextScalar.__name__ = "TextScalar";
export class TextVector extends _Text {
    set_vectorize(ctx, i) {
        this._set_vectorize(ctx, i);
    }
}
TextVector.__name__ = "TextVector";
export class Hatch extends _Hatch {
    set_value(ctx) {
        this._set_value(ctx);
    }
    doit2(ctx, ready_func, defer_func) {
        if (!this.doit)
            return;
        const pattern = this.pattern()(ctx);
        if (pattern == null) {
            this._try_defer(defer_func);
        }
        else {
            this._set_value(ctx);
            ready_func();
        }
    }
}
Hatch.__name__ = "Hatch";
export class HatchScalar extends Hatch {
}
HatchScalar.__name__ = "HatchScalar";
export class HatchVector extends _Hatch {
    set_vectorize(ctx, i) {
        this._set_vectorize(ctx, i);
    }
    doit2(ctx, i, ready_func, defer_func) {
        if (!this.doit)
            return;
        const pattern = this.v_pattern(i)(ctx);
        if (pattern == null) {
            this._try_defer(defer_func);
        }
        else {
            this._set_vectorize(ctx, i);
            ready_func();
        }
    }
}
HatchVector.__name__ = "HatchVector";
//# sourceMappingURL=visuals.js.map