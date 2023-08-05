import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class FastAnchorView extends HTMLBoxView {
    model: FastAnchor;
    anchor_el: HTMLElement;
    setAttr(attribute: string, value: string | null): void;
    connect_signals(): void;
    render(): void;
}
export declare namespace FastAnchor {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        appearance: p.Property<string>;
        download: p.Property<string>;
        href: p.Property<string>;
        hreflang: p.Property<string>;
        ping: p.Property<string>;
        referrerpolicy: p.Property<string>;
        referrer: p.Property<string>;
        rel: p.Property<string>;
        target: p.Property<string>;
        mimetype: p.Property<string>;
    };
}
export interface FastAnchor extends FastAnchor.Attrs {
}
export declare class FastAnchor extends HTMLBox {
    properties: FastAnchor.Props;
    constructor(attrs?: Partial<FastAnchor.Attrs>);
    static __module__: string;
    static init_FastAnchor(): void;
}
