import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class StringAttributeView extends HTMLBoxView {
    model: StringAttribute;
    element: any;
    connect_signals(): void;
    private updateElement;
    render(): void;
    addAttributesMutationObserver(): void;
}
export declare namespace StringAttribute {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        element: p.Property<string>;
        event: p.Property<string>;
        attribute: p.Property<string>;
        value: p.Property<string>;
    };
}
export interface StringAttribute extends StringAttribute.Attrs {
}
export declare class StringAttribute extends HTMLBox {
    properties: StringAttribute.Props;
    constructor(attrs?: Partial<StringAttribute.Attrs>);
    static __module__: string;
    static init_StringAttribute(): void;
}
