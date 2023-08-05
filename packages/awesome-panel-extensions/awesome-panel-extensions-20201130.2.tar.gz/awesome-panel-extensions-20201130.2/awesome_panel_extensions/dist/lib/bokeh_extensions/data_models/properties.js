import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export class PropertyModelView extends HTMLBoxView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.value.change, this.updateElement);
    }
    updateElement() {
        if (this.element) {
            const newValue = this.model.value;
            const oldValue = this.element[this.model.property_];
            if (newValue !== oldValue) {
                this.element[this.model.property_] = newValue;
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
        if (this.model.event != null && this.model.event !== "") {
            const view = this;
            this.element.addEventListener(this.model.event, function () {
                const newValue = view.element[view.model.property_];
                const oldValue = view.model.value;
                if (newValue !== oldValue) {
                    view.model.value = newValue;
                }
            });
        }
    }
}
PropertyModelView.__name__ = "PropertyModelView";
export class PropertyModel extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_PropertyModel() {
        this.prototype.default_view = PropertyModelView;
        this.define({
            element: [p.String,],
            event: [p.String,],
            property_: [p.String,],
        });
    }
}
PropertyModel.__name__ = "PropertyModel";
PropertyModel.__module__ = "awesome_panel_extensions.bokeh_extensions.data_models.properties";
PropertyModel.init_PropertyModel();
export class StringPropertyView extends PropertyModelView {
}
StringPropertyView.__name__ = "StringPropertyView";
export class StringProperty extends PropertyModel {
    constructor(attrs) {
        super(attrs);
    }
    static init_StringProperty() {
        this.prototype.default_view = StringPropertyView;
        this.define({
            value: [p.String,],
        });
    }
}
StringProperty.__name__ = "StringProperty";
StringProperty.init_StringProperty();
export class BooleanPropertyView extends PropertyModelView {
}
BooleanPropertyView.__name__ = "BooleanPropertyView";
export class BooleanProperty extends PropertyModel {
    constructor(attrs) {
        super(attrs);
    }
    static init_BooleanProperty() {
        this.prototype.default_view = BooleanPropertyView;
        this.define({
            value: [p.Boolean,],
        });
    }
}
BooleanProperty.__name__ = "BooleanProperty";
BooleanProperty.init_BooleanProperty();
export class IntegerPropertyView extends PropertyModelView {
}
IntegerPropertyView.__name__ = "IntegerPropertyView";
export class IntegerProperty extends PropertyModel {
    constructor(attrs) {
        super(attrs);
    }
    static init_IntegerProperty() {
        this.prototype.default_view = IntegerPropertyView;
        this.define({
            value: [p.Int,],
        });
    }
}
IntegerProperty.__name__ = "IntegerProperty";
IntegerProperty.init_IntegerProperty();
export class FloatPropertyView extends PropertyModelView {
}
FloatPropertyView.__name__ = "FloatPropertyView";
export class FloatProperty extends PropertyModel {
    constructor(attrs) {
        super(attrs);
    }
    static init_FloatProperty() {
        this.prototype.default_view = FloatPropertyView;
        this.define({
            value: [p.Number,],
        });
    }
}
FloatProperty.__name__ = "FloatProperty";
FloatProperty.init_FloatProperty();
export class ListPropertyView extends PropertyModelView {
}
ListPropertyView.__name__ = "ListPropertyView";
export class ListProperty extends PropertyModel {
    constructor(attrs) {
        super(attrs);
    }
    static init_ListProperty() {
        this.prototype.default_view = ListPropertyView;
        this.define({
            value: [p.Array,],
        });
    }
}
ListProperty.__name__ = "ListProperty";
ListProperty.init_ListProperty();
export class DictPropertyView extends PropertyModelView {
}
DictPropertyView.__name__ = "DictPropertyView";
export class DictProperty extends PropertyModel {
    constructor(attrs) {
        super(attrs);
    }
    static init_DictProperty() {
        this.prototype.default_view = DictPropertyView;
        this.define({
            value: [p.Any,],
        });
    }
}
DictProperty.__name__ = "DictProperty";
DictProperty.init_DictProperty();
//# sourceMappingURL=properties.js.map