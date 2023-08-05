import { AbstractIcon, AbstractIconView } from "@bokehjs/models/widgets/abstract_icon";
import * as p from "@bokehjs/core/properties";
export declare class SVGIconView extends AbstractIconView {
    model: SVGIcon;
    connect_signals(): void;
    render(): void;
}
export declare namespace SVGIcon {
    type Attrs = p.AttrsOf<Props>;
    type Props = AbstractIcon.Props & {
        icon_name: p.Property<string>;
        svg: p.Property<string>;
        size: p.Property<number>;
        fill_color: p.Property<string>;
        spin_duration: p.Property<number>;
    };
}
export interface SVGIcon extends SVGIcon.Attrs {
}
export declare class SVGIcon extends AbstractIcon {
    properties: SVGIcon.Props;
    constructor(attrs?: Partial<SVGIcon.Attrs>);
    static __module__: string;
    static init_SVGIcon(): void;
}
