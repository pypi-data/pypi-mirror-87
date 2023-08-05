import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare class PivotTableView extends HTMLBoxView {
    model: PivotTable;
    container: any;
    pivot_table_element: any;
    connect_signals(): void;
    render(): void;
    setData(): void;
}
export declare namespace PivotTable {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        source: p.Property<ColumnDataSource>;
        source_stream: p.Property<ColumnDataSource>;
        source_patch: p.Property<ColumnDataSource>;
    };
}
export interface PivotTable extends PivotTable.Attrs {
}
export declare class PivotTable extends HTMLBox {
    properties: PivotTable.Props;
    constructor(attrs?: Partial<PivotTable.Attrs>);
    static __module__: string;
    static init_PivotTable(): void;
}
