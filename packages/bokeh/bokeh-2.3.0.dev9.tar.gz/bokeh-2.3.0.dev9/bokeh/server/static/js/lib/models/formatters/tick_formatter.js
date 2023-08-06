import { Model } from "../../model";
export class TickFormatter extends Model {
    constructor(attrs) {
        super(attrs);
    }
    compute(tick, opts) {
        return this.doFormat([tick], opts ?? { loc: 0 })[0];
    }
    v_compute(tick, opts) {
        return this.doFormat(tick, opts ?? { loc: 0 });
    }
}
TickFormatter.__name__ = "TickFormatter";
//# sourceMappingURL=tick_formatter.js.map