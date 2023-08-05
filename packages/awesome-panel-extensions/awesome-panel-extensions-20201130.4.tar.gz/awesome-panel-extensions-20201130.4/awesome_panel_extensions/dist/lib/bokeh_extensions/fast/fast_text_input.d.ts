import { TextInput } from "@bokehjs/models/widgets/text_input";
import { InputWidgetView } from "@bokehjs/models/widgets/input_widget";
import * as p from "@bokehjs/core/properties";
export declare class FastTextInputView extends InputWidgetView {
    model: FastTextInput;
    protected input_el: HTMLInputElement;
    connect_signals(): void;
    get input_el_any(): any;
    render(): void;
    change_input(): void;
    change_input_oninput(): void;
}
export declare namespace FastTextInput {
    type Attrs = p.AttrsOf<Props>;
    type Props = TextInput.Props & {
        appearance: p.Property<string>;
        autofocus: p.Property<boolean>;
        type_of_text: p.Property<string>;
        max_length: p.Property<number>;
        min_length: p.Property<number>;
        pattern: p.Property<string>;
        size: p.Property<number>;
        spellcheck: p.Property<boolean>;
        required: p.Property<boolean>;
        readonly: p.Property<boolean>;
    };
}
export interface FastTextInput extends FastTextInput.Attrs {
}
export declare class FastTextInput extends TextInput {
    properties: FastTextInput.Props;
    constructor(attrs?: Partial<FastTextInput.Attrs>);
    static __module__: string;
    static init_FastTextInput(): void;
}
