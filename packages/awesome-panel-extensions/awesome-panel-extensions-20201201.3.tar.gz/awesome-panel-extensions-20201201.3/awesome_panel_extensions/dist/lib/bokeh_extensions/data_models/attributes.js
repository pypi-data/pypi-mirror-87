import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export class StringAttributeView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.value.change, this.updateElement);
    }
    updateElement() {
        if (this.element) {
            const newValue = this.model.value;
            const oldValue = this.element.getAttribute(this.model.attribute);
            if (newValue !== oldValue) {
                this.element.setAttribute(this.model.attribute, newValue);
            }
        }
    }
    render() {
        super.render();
        this.element = document.getElementById(this.model.element);
        if (this.element === null) {
            this.element = document.querySelector(this.model.element);
        }
        if (this.element === null) {
            return;
        }
        this.updateElement();
        this.addAttributesMutationObserver();
    }
    addAttributesMutationObserver() {
        let options = {
            childList: false,
            attributes: true,
            characterData: false,
            subtree: false,
            attributeFilter: [this.model.attribute],
            attributeOldValue: false,
            characterDataOldValue: false
        };
        const handleAttributeChange = (_) => {
            var newValue = this.element.getAttribute(this.model.attribute);
            if (newValue === true || newValue === false) {
                newValue = "";
            }
            const oldValue = this.model.value;
            if (newValue !== oldValue) {
                this.model.value = newValue;
            }
        };
        let observer = new MutationObserver(handleAttributeChange);
        observer.observe(this.element, options);
    }
}
StringAttributeView.__name__ = "StringAttributeView";
export class StringAttribute extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_StringAttribute() {
        this.prototype.default_view = StringAttributeView;
        this.define({
            element: [p.String,],
            event: [p.String,],
            attribute: [p.String,],
            value: [p.String,],
        });
    }
}
StringAttribute.__name__ = "StringAttribute";
StringAttribute.__module__ = "awesome_panel_extensions.bokeh_extensions.data_models.attributes";
StringAttribute.init_StringAttribute();
//# sourceMappingURL=attributes.js.map