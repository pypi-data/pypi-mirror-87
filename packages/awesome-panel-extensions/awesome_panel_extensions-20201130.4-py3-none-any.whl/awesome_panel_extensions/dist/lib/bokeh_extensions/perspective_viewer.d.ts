import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare class PerspectiveViewerView extends HTMLBoxView {
    model: PerspectiveViewer;
    perspective_element: any;
    connect_signals(): void;
    render(): void;
    private getInnerHTML;
    setData(): void;
    addData(): void;
    updateOrAddData(): void;
    updateAttribute(attribute: string, value: any, stringify: boolean): void;
    updateColumns(): void;
    updateParsedComputedColumns(): void;
    updateComputedColumns(): void;
    updateColumnPivots(): void;
    updateRowPivots(): void;
    updateAggregates(): void;
    updateSort(): void;
    updateFilters(): void;
    updatePlugin(): void;
    updateTheme(): void;
    /** Helper function to generate the new class attribute string
     *
     * If old_class = 'perspective-viewer-material dragging' and theme = 'material-dark'
     * then 'perspective-viewer-material-dark dragging' is returned
     *
     * @param old_class For example 'perspective-viewer-material' or 'perspective-viewer-material dragging'
     * @param theme The name of the new theme. For example 'material-dark'
     */
    private toNewClassAttribute;
}
export declare namespace PerspectiveViewer {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        source: p.Property<ColumnDataSource>;
        source_stream: p.Property<ColumnDataSource>;
        source_patch: p.Property<ColumnDataSource>;
        columns: p.Property<any[]>;
        parsed_computed_columns: p.Property<any[]>;
        computed_columns: p.Property<any[]>;
        column_pivots: p.Property<any[]>;
        row_pivots: p.Property<any[]>;
        aggregates: p.Property<any>;
        sort: p.Property<any[]>;
        filters: p.Property<any[]>;
        plugin: p.Property<any>;
        theme: p.Property<any>;
    };
}
export interface PerspectiveViewer extends PerspectiveViewer.Attrs {
}
export declare class PerspectiveViewer extends HTMLBox {
    properties: PerspectiveViewer.Props;
    constructor(attrs?: Partial<PerspectiveViewer.Attrs>);
    static __module__: string;
    static init_PerspectiveViewer(): void;
}
