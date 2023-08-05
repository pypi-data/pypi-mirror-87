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
export declare class IntegerPropertyView extends PropertyModelView {
    model: IntegerProperty;
}
export declare namespace IntegerProperty {
    type Attrs = p.AttrsOf<Props>;
    type Props = PropertyModel.Props & {
        value: p.Property<number>;
    };
}
export interface IntegerProperty extends IntegerProperty.Attrs {
}
export declare class IntegerProperty extends PropertyModel {
    properties: IntegerProperty.Props;
    constructor(attrs?: Partial<IntegerProperty.Attrs>);
    static init_IntegerProperty(): void;
}
export declare class FloatPropertyView extends PropertyModelView {
    model: FloatProperty;
}
export declare namespace FloatProperty {
    type Attrs = p.AttrsOf<Props>;
    type Props = PropertyModel.Props & {
        value: p.Property<number>;
    };
}
export interface FloatProperty extends FloatProperty.Attrs {
}
export declare class FloatProperty extends PropertyModel {
    properties: FloatProperty.Props;
    constructor(attrs?: Partial<FloatProperty.Attrs>);
    static init_FloatProperty(): void;
}
export declare class ListPropertyView extends PropertyModelView {
    model: ListProperty;
}
export declare namespace ListProperty {
    type Attrs = p.AttrsOf<Props>;
    type Props = PropertyModel.Props & {
        value: p.Property<any>;
    };
}
export interface ListProperty extends ListProperty.Attrs {
}
export declare class ListProperty extends PropertyModel {
    properties: ListProperty.Props;
    constructor(attrs?: Partial<ListProperty.Attrs>);
    static init_ListProperty(): void;
}
export declare class DictPropertyView extends PropertyModelView {
    model: DictProperty;
}
export declare namespace DictProperty {
    type Attrs = p.AttrsOf<Props>;
    type Props = PropertyModel.Props & {
        value: p.Property<any>;
    };
}
export interface DictProperty extends DictProperty.Attrs {
}
export declare class DictProperty extends PropertyModel {
    properties: DictProperty.Props;
    constructor(attrs?: Partial<DictProperty.Attrs>);
    static init_DictProperty(): void;
}
