import { CheckboxGroup, CheckboxGroupView } from "@bokehjs/models/widgets/checkbox_group";
import * as p from "@bokehjs/core/properties";
export declare class FastCheckboxGroupView extends CheckboxGroupView {
    model: FastCheckboxGroup;
    render(): void;
}
export declare namespace FastCheckboxGroup {
    type Attrs = p.AttrsOf<Props>;
    type Props = CheckboxGroup.Props & {
        readonly: p.Property<boolean>;
    };
}
export interface FastCheckboxGroup extends FastCheckboxGroup.Attrs {
}
export declare class FastCheckboxGroup extends CheckboxGroup {
    properties: FastCheckboxGroup.Props;
    constructor(attrs?: Partial<FastCheckboxGroup.Attrs>);
    static __module__: string;
    static init_FastCheckboxGroup(): void;
}
