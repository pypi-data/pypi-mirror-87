import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class IntegerEventView extends HTMLBoxView {
    model: any;
    element: any;
    render(): void;
}
export declare namespace IntegerEvent {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        element: p.Property<string>;
        event: p.Property<string>;
        value: p.Property<number>;
    };
}
export interface IntegerEvent extends IntegerEvent.Attrs {
}
export declare class IntegerEvent extends HTMLBox {
    properties: IntegerEvent.Props;
    constructor(attrs?: Partial<IntegerEvent.Attrs>);
    static __module__: string;
    static init_IntegerEvent(): void;
}
