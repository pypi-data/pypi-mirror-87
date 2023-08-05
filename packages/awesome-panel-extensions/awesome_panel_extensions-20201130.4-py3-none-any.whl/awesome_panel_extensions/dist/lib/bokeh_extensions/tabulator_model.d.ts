import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare function set_size(el: HTMLElement, model: HTMLBox): void;
export declare class TabulatorModelView extends HTMLBoxView {
    model: TabulatorModel;
    tabulator: any;
    _tabulator_cell_updating: boolean;
    connect_signals(): void;
    render(): void;
    getConfiguration(): any;
    after_layout(): void;
    setData(): void;
    addData(): void;
    updateOrAddData(): void;
    updateSelection(): void;
}
export declare namespace TabulatorModel {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        configuration: p.Property<any>;
        source: p.Property<ColumnDataSource>;
        _cell_change: p.Property<any>;
    };
}
export interface TabulatorModel extends TabulatorModel.Attrs {
}
export declare class TabulatorModel extends HTMLBox {
    properties: TabulatorModel.Props;
    constructor(attrs?: Partial<TabulatorModel.Attrs>);
    static __module__: string;
    static init_TabulatorModel(): void;
}
