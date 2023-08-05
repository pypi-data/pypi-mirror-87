import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
import * as p from "@bokehjs/core/properties";
export class IntegerEventView extends HTMLBoxView {
    render() {
        super.render();
        this.element = document.getElementById(this.model.element);
        if (this.element === null) {
            this.element = document.querySelector(this.model.element);
        }
        if (this.element === null) {
            return;
        }
        if (this.model.event != null && this.model.event !== "") {
            const view = this;
            this.element.addEventListener(this.model.event, function () {
                view.model.value += 1;
            });
        }
    }
}
IntegerEventView.__name__ = "IntegerEventView";
export class IntegerEvent extends HTMLBox {
    constructor(attrs) {
        super(attrs);
    }
    static init_IntegerEvent() {
        this.prototype.default_view = IntegerEventView;
        this.define({
            element: [p.String,],
            event: [p.String,],
            value: [p.Int,],
        });
    }
}
IntegerEvent.__name__ = "IntegerEvent";
IntegerEvent.__module__ = "awesome_panel_extensions.bokeh_extensions.data_models.events";
IntegerEvent.init_IntegerEvent();
//# sourceMappingURL=events.js.map