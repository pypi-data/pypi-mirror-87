const SQ3 = Math.sqrt(3);
function _one_line(ctx, r) {
    ctx.moveTo(-r, 0);
    ctx.lineTo(r, 0);
}
function _one_x(ctx, r) {
    ctx.rotate(Math.PI / 4);
    _one_cross(ctx, r);
    ctx.rotate(-Math.PI / 4);
}
function _one_y(ctx, r) {
    const h = r * SQ3;
    const a = h / 3;
    ctx.moveTo(-h / 2, -a);
    ctx.lineTo(0, 0);
    ctx.lineTo(h / 2, -a);
    ctx.lineTo(0, 0);
    ctx.lineTo(0, r);
}
function _one_cross(ctx, r) {
    ctx.moveTo(0, r);
    ctx.lineTo(0, -r);
    ctx.moveTo(-r, 0);
    ctx.lineTo(r, 0);
}
function _one_dot(ctx, r) {
    ctx.beginPath();
    ctx.arc(0, 0, r / 4, 0, 2 * Math.PI, false);
    ctx.closePath();
}
function _one_diamond(ctx, r) {
    ctx.moveTo(0, r);
    ctx.lineTo(r / 1.5, 0);
    ctx.lineTo(0, -r);
    ctx.lineTo(-r / 1.5, 0);
    ctx.closePath();
}
function _one_hex(ctx, r) {
    const r2 = r / 2;
    const h = SQ3 * r2;
    ctx.moveTo(r, 0);
    ctx.lineTo(r2, -h);
    ctx.lineTo(-r2, -h);
    ctx.lineTo(-r, 0);
    ctx.lineTo(-r2, h);
    ctx.lineTo(r2, h);
    ctx.closePath();
}
function _one_tri(ctx, r) {
    const h = r * SQ3;
    const a = h / 3;
    ctx.moveTo(-r, a);
    ctx.lineTo(r, a);
    ctx.lineTo(0, a - h);
    ctx.closePath();
}
function asterisk(ctx, i, r, line, _fill) {
    _one_cross(ctx, r);
    _one_x(ctx, r);
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function circle(ctx, i, r, line, fill) {
    ctx.arc(0, 0, r, 0, 2 * Math.PI, false);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function circle_cross(ctx, i, r, line, fill) {
    ctx.arc(0, 0, r, 0, 2 * Math.PI, false);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        _one_cross(ctx, r);
        ctx.stroke();
    }
}
function circle_dot(ctx, i, r, line, fill) {
    circle(ctx, i, r, line, fill);
    dot(ctx, i, r, line, fill);
}
function circle_y(ctx, i, r, line, fill) {
    ctx.arc(0, 0, r, 0, 2 * Math.PI, false);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        _one_y(ctx, r);
        ctx.stroke();
    }
}
function circle_x(ctx, i, r, line, fill) {
    ctx.arc(0, 0, r, 0, 2 * Math.PI, false);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        _one_x(ctx, r);
        ctx.stroke();
    }
}
function cross(ctx, i, r, line, _fill) {
    _one_cross(ctx, r);
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function diamond(ctx, i, r, line, fill) {
    _one_diamond(ctx, r);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function diamond_cross(ctx, i, r, line, fill) {
    _one_diamond(ctx, r);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.moveTo(0, r);
        ctx.lineTo(0, -r);
        ctx.moveTo(-r / 1.5, 0);
        ctx.lineTo(r / 1.5, 0);
        ctx.stroke();
    }
}
function diamond_dot(ctx, i, r, line, fill) {
    diamond(ctx, i, r, line, fill);
    dot(ctx, i, r, line, fill);
}
function dot(ctx, i, r, line, _fill) {
    _one_dot(ctx, r);
    line.set_vectorize(ctx, i);
    ctx.fillStyle = ctx.strokeStyle; // NOTE: dots use line color for fill to match
    ctx.fill();
}
function hex(ctx, i, r, line, fill) {
    _one_hex(ctx, r);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function hex_dot(ctx, i, r, line, fill) {
    hex(ctx, i, r, line, fill);
    dot(ctx, i, r, line, fill);
}
function inverted_triangle(ctx, i, r, line, fill) {
    ctx.rotate(Math.PI);
    _one_tri(ctx, r);
    ctx.rotate(-Math.PI);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function plus(ctx, i, r, line, fill) {
    const a = 3 * r / 8;
    const b = r;
    const xs = [a, a, b, b, a, a, -a, -a, -b, -b, -a, -a];
    const ys = [b, a, a, -a, -a, -b, -b, -a, -a, a, a, b];
    ctx.beginPath();
    for (let j = 0; j < 12; j++) {
        ctx.lineTo(xs[j], ys[j]);
    }
    ctx.closePath();
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function square(ctx, i, r, line, fill) {
    const size = 2 * r;
    ctx.rect(-r, -r, size, size);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function square_pin(ctx, i, r, line, fill) {
    const a = 3 * r / 8;
    ctx.moveTo(-r, -r);
    /* eslint-disable space-in-parens */
    ctx.quadraticCurveTo(0, -a, r, -r);
    ctx.quadraticCurveTo(a, 0, r, r);
    ctx.quadraticCurveTo(0, a, -r, r);
    ctx.quadraticCurveTo(-a, 0, -r, -r);
    /* eslint-ensable space-in-parens */
    ctx.closePath();
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function square_cross(ctx, i, r, line, fill) {
    const size = 2 * r;
    ctx.rect(-r, -r, size, size);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        _one_cross(ctx, r);
        ctx.stroke();
    }
}
function square_dot(ctx, i, r, line, fill) {
    square(ctx, i, r, line, fill);
    dot(ctx, i, r, line, fill);
}
function square_x(ctx, i, r, line, fill) {
    const size = 2 * r;
    ctx.rect(-r, -r, size, size);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.moveTo(-r, r);
        ctx.lineTo(r, -r);
        ctx.moveTo(-r, -r);
        ctx.lineTo(r, r);
        ctx.stroke();
    }
}
function triangle(ctx, i, r, line, fill) {
    _one_tri(ctx, r);
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function triangle_dot(ctx, i, r, line, fill) {
    triangle(ctx, i, r, line, fill);
    dot(ctx, i, r, line, fill);
}
function triangle_pin(ctx, i, r, line, fill) {
    const h = r * SQ3;
    const a = h / 3;
    const b = 3 * a / 8;
    ctx.moveTo(-r, a);
    ctx.quadraticCurveTo(0, b, r, a);
    ctx.quadraticCurveTo(SQ3 * b / 2, b / 2, 0, a - h);
    ctx.quadraticCurveTo(-SQ3 * b / 2, b / 2, -r, a);
    ctx.closePath();
    if (fill.doit) {
        fill.set_vectorize(ctx, i);
        ctx.fill();
    }
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function dash(ctx, i, r, line, _fill) {
    _one_line(ctx, r);
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function x(ctx, i, r, line, _fill) {
    _one_x(ctx, r);
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
function y(ctx, i, r, line, _fill) {
    _one_y(ctx, r);
    if (line.doit) {
        line.set_vectorize(ctx, i);
        ctx.stroke();
    }
}
export const marker_funcs = {
    asterisk,
    circle,
    circle_cross,
    circle_dot,
    circle_y,
    circle_x,
    cross,
    diamond,
    diamond_dot,
    diamond_cross,
    dot,
    hex,
    hex_dot,
    inverted_triangle,
    plus,
    square,
    square_cross,
    square_dot,
    square_pin,
    square_x,
    triangle,
    triangle_dot,
    triangle_pin,
    dash,
    x,
    y,
};
//# sourceMappingURL=defs.js.map