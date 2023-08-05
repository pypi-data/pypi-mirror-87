import { Button, ButtonView } from "@bokehjs/models/widgets/button";
import * as p from "@bokehjs/core/properties";
export declare class FastButtonView extends ButtonView {
    model: FastButton;
    _render_button(..._: (string | HTMLElement)[]): HTMLButtonElement;
}
export declare namespace FastButton {
    type Attrs = p.AttrsOf<Props>;
    type Props = Button.Props & {
        appearance: p.Property<string>;
        autofocus: p.Property<boolean>;
    };
}
export interface FastButton extends FastButton.Attrs {
}
export declare class FastButton extends Button {
    properties: FastButton.Props;
    constructor(attrs?: Partial<FastButton.Attrs>);
    static __module__: string;
    static init_FastButton(): void;
}
