import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare class WebComponentView extends HTMLBoxView {
    model: WebComponent;
    webComponentElement: any;
    eventsCount: any;
    propertyValues: any;
    protected label_el: HTMLLabelElement;
    protected group_el: HTMLElement;
    connect_signals(): void;
    private handleNameChange;
    render(): void;
    after_layout(): void;
    private createOrUpdateWebComponentElement;
    addAttributesMutationObserver(): void;
    private addEventListeners;
    transform_cds_to_records(cds: ColumnDataSource): any;
    isFunction(functionToCheck: any): boolean;
    /**
     * Handles changes to `this.model.columnDataSource`
     * by
     * updating the data source of `this.webComponentElement`
     * using the function or property specifed in `this.model.columnDataSourceLoadFunction`
     */
    handleColumnDataSourceChange(): void;
    private activate_scripts;
    /**
     * Example:
     *
     * `get_nested_property(element, "textInput.value")` returns `element.textInput.value`
     *
     * @param element
     * @param property_
     */
    get_nested_property(element: any, property_: string): string;
    set_nested_property(element: any, property_: string, value: any): void;
    /**
     * Handles events from `eventsToWatch` by
     *
     * - Incrementing the count of the event
     * - Checking if any properties have changed
     *
     * @param ev The Event Fired
     */
    eventHandler(ev: Event): void;
    /** Checks if any properties have changed. In case this is communicated to the server.
     *
     * For example the Wired `DropDown` does not run the `onchange` event handler when the selection changes.
     * Insted the `select` event is fired. Thus we can subscribe to this event and manually check for property changes.
     */
    checkIfPropertiesChanged(): void;
    /** Handles the `WebComponentElement` `(on)change` event
     *
     * Communicates any changed properties in `propertiesToWatch` to the server
     * by updating `this.model.propertiesLastChange`.
     * @param ev
     */
    handlePropertiesChange(ev: any): void;
    initPropertyValues(): void;
    /**
     * Handles changes to `this.model.attributesLastChange`
     * by
     * updating the attributes of `this.webComponentElement` accordingly
     */
    handleAttributesLastChangeChange(): void;
    /**
    * Handles changes to `this.model.propertiesLastChange`
    * by
    * updating the properties of `this.webComponentElement` accordingly
    */
    handlePropertiesLastChangeChange(): void;
}
export declare namespace WebComponent {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        componentType: p.Property<string>;
        innerHTML: p.Property<string>;
        attributesToWatch: p.Property<any>;
        attributesLastChange: p.Property<any>;
        propertiesToWatch: p.Property<any>;
        propertiesLastChange: p.Property<any>;
        eventsToWatch: p.Property<any>;
        eventsCountLastChange: p.Property<any>;
        columnDataSource: p.Property<ColumnDataSource>;
        columnDataSourceOrient: p.Property<string>;
        columnDataSourceLoadFunction: p.Property<string>;
    };
}
export interface WebComponent extends WebComponent.Attrs {
}
export declare class WebComponent extends HTMLBox {
    properties: WebComponent.Props;
    constructor(attrs?: Partial<WebComponent.Attrs>);
    static __module__: string;
    static init_WebComponent(): void;
}
