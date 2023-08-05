import { CheckboxGroup, CheckboxGroupView } from "@bokehjs/models/widgets/checkbox_group";
import * as p from "@bokehjs/core/properties";
export declare class FastSwitchGroupView extends CheckboxGroupView {
    model: FastSwitchGroup;
    render(): void;
}
export declare namespace FastSwitchGroup {
    type Attrs = p.AttrsOf<Props>;
    type Props = CheckboxGroup.Props & {
        readonly: p.Property<boolean>;
        checked_message: p.Property<string>;
        unchecked_message: p.Property<string>;
    };
}
export interface FastSwitchGroup extends FastSwitchGroup.Attrs {
}
export declare class FastSwitchGroup extends CheckboxGroup {
    properties: FastSwitchGroup.Props;
    constructor(attrs?: Partial<FastSwitchGroup.Attrs>);
    static __module__: string;
    static init_FastSwitchGroup(): void;
}
