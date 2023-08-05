import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export declare class PropertyModelView extends HTMLBoxView {
    model: any;
    element: any;
    connect_signals(): void;
    private updateElement;
    render(): void;
}
export declare namespace PropertyModel {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        element: p.Property<string>;
        event: p.Property<string>;
        property_: p.Property<string>;
    };
}
export interface PropertyModel extends PropertyModel.Attrs {
}
export declare class PropertyModel extends HTMLBox {
    properties: PropertyModel.Props;
    constructor(attrs?: Partial<PropertyModel.Attrs>);
    static __module__: string;
    static init_PropertyModel(): void;
}
export declare class StringPropertyView extends PropertyModelView {
    model: StringProperty;
}
export declare namespace StringProperty {
    type Attrs = p.AttrsOf<Props>;
    type Props = PropertyModel.Props & {
        value: p.Property<string>;
    };
}
export interface StringProperty extends StringProperty.Attrs {
}
export declare class StringProperty extends PropertyModel {
    properties: StringProperty.Props;
    constructor(attrs?: Partial<StringProperty.Attrs>);
    static init_StringProperty(): void;
}
export declare class BooleanPropertyView extends PropertyModelView {
    model: BooleanProperty;
}
export declare namespace BooleanProperty {
    type Attrs = p.AttrsOf<Props>;
    type Props = PropertyModel.Props & {
        value: p.Property<boolean>;
    };
}
export interface BooleanProperty extends BooleanProperty.Attrs {
}
export declare class BooleanProperty extends PropertyModel {
    properties: BooleanProperty.Props;
    constructor(attrs?: Partial<BooleanProperty.Attrs>);
    static init_BooleanProperty(): void;
}
