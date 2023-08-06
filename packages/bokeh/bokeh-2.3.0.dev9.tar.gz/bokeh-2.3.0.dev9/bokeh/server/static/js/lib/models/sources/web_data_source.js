import { ColumnDataSource } from "./column_data_source";
import { UpdateMode } from "../../core/enums";
export class WebDataSource extends ColumnDataSource {
    constructor(attrs) {
        super(attrs);
    }
    get_column(colname) {
        const column = this.data[colname];
        return column != null ? column : [];
    }
    initialize() {
        super.initialize();
        this.setup();
    }
    load_data(raw_data, mode, max_size) {
        const { adapter } = this;
        let data;
        if (adapter != null)
            data = adapter.execute(this, { response: raw_data });
        else
            data = raw_data;
        switch (mode) {
            case "replace": {
                this.data = data;
                break;
            }
            case "append": {
                const original_data = this.data;
                for (const column of this.columns()) {
                    // XXX: support typed arrays
                    const old_col = Array.from(original_data[column]);
                    const new_col = Array.from(data[column]);
                    data[column] = old_col.concat(new_col).slice(-max_size);
                }
                this.data = data;
                break;
            }
        }
    }
    static init_WebDataSource() {
        this.define(({ Any, Int, String, Nullable }) => ({
            max_size: [Int],
            mode: [UpdateMode, "replace"],
            adapter: [Nullable(Any /*TODO*/), null],
            data_url: [String],
        }));
    }
}
WebDataSource.__name__ = "WebDataSource";
WebDataSource.init_WebDataSource();
//# sourceMappingURL=web_data_source.js.map