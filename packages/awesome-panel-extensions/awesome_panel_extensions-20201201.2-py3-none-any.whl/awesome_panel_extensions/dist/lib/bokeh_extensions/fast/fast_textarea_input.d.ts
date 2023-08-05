import { TextAreaInput } from "@bokehjs/models/widgets/textarea_input";
import { InputWidgetView } from "@bokehjs/models/widgets/input_widget";
import * as p from "@bokehjs/core/properties";
export declare class FastTextAreaInputView extends InputWidgetView {
    model: FastTextAreaInput;
    protected input_el: HTMLTextAreaElement;
    get input_el_any(): any;
    connect_signals(): void;
    render(): void;
    change_input(): void;
}
export declare namespace FastTextAreaInput {
    type Attrs = p.AttrsOf<Props>;
    type Props = TextAreaInput.Props & {
        appearance: p.Property<string>;
        autofocus: p.Property<boolean>;
        resize: p.Property<string>;
        spellcheck: p.Property<boolean>;
        min_length: p.Property<number>;
        required: p.Property<boolean>;
        readonly: p.Property<boolean>;
    };
}
export interface FastTextAreaInput extends FastTextAreaInput.Attrs {
}
export declare class FastTextAreaInput extends TextAreaInput {
    properties: FastTextAreaInput.Props;
    constructor(attrs?: Partial<FastTextAreaInput.Attrs>);
    static __module__: string;
    static init_FastTextAreaInput(): void;
}
