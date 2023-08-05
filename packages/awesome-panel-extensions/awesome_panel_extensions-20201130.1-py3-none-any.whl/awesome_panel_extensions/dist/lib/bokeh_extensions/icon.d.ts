import { AbstractIcon, AbstractIconView } from "@bokehjs/models/widgets/abstract_icon";
import * as p from "@bokehjs/core/properties";
export declare class IconView extends AbstractIconView {
    model: Icon;
    connect_signals(): void;
    render(): void;
}
export declare namespace Icon {
    type Attrs = p.AttrsOf<Props>;
    type Props = AbstractIcon.Props & {
        label: p.Property<string>;
        text: p.Property<string>;
        size: p.Property<number>;
        fill_color: p.Property<string>;
        spin_duration: p.Property<number>;
    };
}
export interface Icon extends Icon.Attrs {
}
export declare class Icon extends AbstractIcon {
    properties: Icon.Props;
    constructor(attrs?: Partial<Icon.Attrs>);
    static __module__: string;
    static init_Icon(): void;
}
