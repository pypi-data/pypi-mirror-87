// Bokeh model for perspective-viewer
// See https://github.com/finos/perspective/tree/master/packages/perspective-viewer
// See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { div } from "@bokehjs/core/dom";
// See https://docs.bokeh.org/en/latest/docs/reference/core/properties.html
import * as p from "@bokehjs/core/properties";
import { set_size, toAttribute, transform_cds_to_records } from "./shared";
const PERSPECTIVE_VIEWER_CLASSES = [
    "perspective-viewer-material",
    "perspective-viewer-material-dark",
    "perspective-viewer-material-dense",
    "perspective-viewer-material-dense-dark",
    "perspective-viewer-vaporwave",
];
function is_not_perspective_class(item) {
    return !PERSPECTIVE_VIEWER_CLASSES.includes(item);
}
function theme_to_class(theme) {
    return "perspective-viewer-" + theme;
}
// The view of the Bokeh extension/ HTML element
// Here you can define how to render the model as well as react to model changes or View events.
export class PerspectiveViewerView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.source.properties.data.change, this.setData);
        this.connect(this.model.source_stream.properties.data.change, this.addData);
        this.connect(this.model.source_patch.properties.data.change, this.updateOrAddData);
        this.connect(this.model.properties.columns.change, this.updateColumns);
        this.connect(this.model.properties.parsed_computed_columns.change, this.updateParsedComputedColumns);
        this.connect(this.model.properties.computed_columns.change, this.updateComputedColumns);
        this.connect(this.model.properties.column_pivots.change, this.updateColumnPivots);
        this.connect(this.model.properties.row_pivots.change, this.updateRowPivots);
        this.connect(this.model.properties.aggregates.change, this.updateAggregates);
        this.connect(this.model.properties.filters.change, this.updateFilters);
        this.connect(this.model.properties.plugin.change, this.updatePlugin);
        this.connect(this.model.properties.theme.change, this.updateTheme);
    }
    render() {
        super.render();
        const container = div({ class: "pnx-perspective-viewer" });
        container.innerHTML = this.getInnerHTML();
        this.perspective_element = container.children[0];
        set_size(container, this.model);
        this.el.appendChild(container);
        this.setData();
        let viewer = this;
        function handleConfigurationChange() {
            // this refers to the perspective-viewer element
            // viewer refers to the PerspectiveViewerView element
            viewer.model.columns = this.columns; // Note columns is available as a property
            viewer.model.column_pivots = JSON.parse(this.getAttribute("column-pivots"));
            viewer.model.parsed_computed_columns = JSON.parse(this.getAttribute("parsed-computed-columns"));
            viewer.model.computed_columns = JSON.parse(this.getAttribute("computed-columns"));
            viewer.model.row_pivots = JSON.parse(this.getAttribute("row-pivots"));
            viewer.model.aggregates = JSON.parse(this.getAttribute("aggregates"));
            viewer.model.sort = JSON.parse(this.getAttribute("sort"));
            viewer.model.filters = JSON.parse(this.getAttribute("filters"));
            // Perspective uses a plugin called 'debug' once in a while.
            // We don't send this back to the python side
            // Because then we would have to include it in the list of plugins
            // the user can select from.
            const plugin = this.getAttribute("plugin");
            if (plugin !== "debug") {
                viewer.model.plugin = this.getAttribute("plugin");
            }
        }
        this.perspective_element.addEventListener("perspective-config-update", handleConfigurationChange);
    }
    getInnerHTML() {
        let innerHTML = "<perspective-viewer style='height:100%;width:100%;'";
        innerHTML += toAttribute("class", theme_to_class(this.model.theme));
        innerHTML += toAttribute("columns", this.model.columns);
        innerHTML += toAttribute("column-pivots", this.model.column_pivots);
        innerHTML += toAttribute("computed-columns", this.model.computed_columns);
        innerHTML += toAttribute("row-pivots", this.model.row_pivots);
        innerHTML += toAttribute("aggregates", this.model.aggregates);
        innerHTML += toAttribute("sort", this.model.sort);
        innerHTML += toAttribute("filters", this.model.filters);
        innerHTML += toAttribute("plugin", this.model.plugin);
        innerHTML += "></perspective-viewer>";
        // We don't set the parsed-computed-columns
        // It's not documented. Don't know if it is an internal thing?
        // I think it gets generated from the computed-columns currently
        // innerHTML += toAttribute("parsed-computed-columns", this.model.parsed_computed_columns)
        return innerHTML;
    }
    setData() {
        console.log("setData");
        console.log(this.model.source.data);
        let data = transform_cds_to_records(this.model.source);
        this.perspective_element.load(data);
    }
    addData() {
        // I need to find out how to only load the streamed data
        // using this.perspective_element.update
        console.log("addData");
        this.setData();
    }
    updateOrAddData() {
        // I need to find out how to only load the patched data
        // using this.perspective_element.update
        console.log("updateOrAddData");
        this.setData();
    }
    updateAttribute(attribute, value, stringify) {
        // Might need som more testing/ a better understanding
        // I'm not sure we should return here.
        if (value === undefined || value === null || value === []) {
            return;
        }
        const old_value = this.perspective_element.getAttribute(attribute);
        if (stringify) {
            value = JSON.stringify(value);
        }
        // We should only set the attribute if the new value is different to old_value
        // Otherwise we would get a recoursion/ stack overflow error
        if (old_value !== value) {
            this.perspective_element.setAttribute(attribute, value);
        }
    }
    updateColumns() { this.updateAttribute("columns", this.model.columns, true); }
    updateParsedComputedColumns() { this.updateAttribute("parsed-computed-columns", this.model.parsed_computed_columns, true); }
    updateComputedColumns() { this.updateAttribute("computed-columns", this.model.computed_columns, true); }
    updateColumnPivots() { this.updateAttribute("column-pivots", this.model.column_pivots, true); }
    updateRowPivots() { this.updateAttribute("row-pivots", this.model.row_pivots, true); }
    updateAggregates() { this.updateAttribute("aggregates", this.model.row_pivots, true); }
    updateSort() { this.updateAttribute("sort", this.model.sort, true); }
    updateFilters() { this.updateAttribute("sort", this.model.filters, true); }
    updatePlugin() { this.updateAttribute("plugin", this.model.plugin, false); }
    updateTheme() {
        // When you update the class attribute you have to be carefull
        // For example when the user is dragging an element then 'dragging' is a part of the class attribute
        let old_class = this.perspective_element.getAttribute("class");
        let new_class = this.toNewClassAttribute(old_class, this.model.theme);
        this.perspective_element.setAttribute("class", new_class);
    }
    /** Helper function to generate the new class attribute string
     *
     * If old_class = 'perspective-viewer-material dragging' and theme = 'material-dark'
     * then 'perspective-viewer-material-dark dragging' is returned
     *
     * @param old_class For example 'perspective-viewer-material' or 'perspective-viewer-material dragging'
     * @param theme The name of the new theme. For example 'material-dark'
     */
    toNewClassAttribute(old_class, theme) {
        let new_classes = [];
        if (old_class != null) {
            new_classes = old_class.split(" ").filter(is_not_perspective_class);
        }
        new_classes.push(theme_to_class(theme));
        let new_class = new_classes.join(" ");
        return new_class;
    }
}
PerspectiveViewerView.__name__ = "PerspectiveViewerView";
// The Bokeh .ts model corresponding to the Bokeh .py model
export class PerspectiveViewer extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_PerspectiveViewer() {
        this.prototype.default_view = PerspectiveViewerView;
        this.define({
            source: [p.Any,],
            source_stream: [p.Any,],
            source_patch: [p.Any,],
            columns: [p.Array,],
            parsed_computed_columns: [p.Array, []],
            computed_columns: [p.Array,],
            column_pivots: [p.Array,],
            row_pivots: [p.Array,],
            aggregates: [p.Any,],
            sort: [p.Array,],
            filters: [p.Array,],
            plugin: [p.String,],
            theme: [p.String,],
        });
    }
}
PerspectiveViewer.__name__ = "PerspectiveViewer";
PerspectiveViewer.__module__ = "awesome_panel_extensions.bokeh_extensions.perspective_viewer";
PerspectiveViewer.init_PerspectiveViewer();
//# sourceMappingURL=perspective_viewer.js.map