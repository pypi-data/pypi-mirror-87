// Bokeh model for perspective-viewer
// See https://github.com/finos/perspective/tree/master/packages/perspective-viewer
// See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { div } from "@bokehjs/core/dom";
// See https://docs.bokeh.org/en/latest/docs/reference/core/properties.html
import * as p from "@bokehjs/core/properties";
import { set_size, transform_cds_to_records } from "./shared";
// The view of the Bokeh extension/ HTML element
// Here you can define how to render the model as well as react to model changes or View events.
export class PivotTableView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.source.properties.data.change, this.setData);
    }
    render() {
        super.render();
        this.container = div({ class: "pnx-pivot-table" });
        set_size(this.container, this.model);
        this.el.appendChild(this.container);
        this.setData();
    }
    setData() {
        console.log("setData");
        console.log(this.model.source.data);
        let data = transform_cds_to_records(this.model.source);
        this.pivot_table_element = $(this.container);
        console.log(data);
        this.pivot_table_element.pivotUI(data, {});
    }
}
PivotTableView.__name__ = "PivotTableView";
// The Bokeh .ts model corresponding to the Bokeh .py model
export class PivotTable extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_PivotTable() {
        this.prototype.default_view = PivotTableView;
        this.define({
            source: [p.Any,],
            source_stream: [p.Any,],
            source_patch: [p.Any,],
        });
    }
}
PivotTable.__name__ = "PivotTable";
PivotTable.__module__ = "awesome_panel_extensions.bokeh_extensions.pivot_table";
PivotTable.init_PivotTable();
//# sourceMappingURL=pivot_table.js.map