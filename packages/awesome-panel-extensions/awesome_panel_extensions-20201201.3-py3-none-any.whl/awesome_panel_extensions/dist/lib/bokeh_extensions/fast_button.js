import { Button, ButtonView } from "@bokehjs/models/widgets/button";
import * as p from "@bokehjs/core/properties";
export class FastButtonView extends ButtonView {
    _render_button(..._) {
        const button = document.createElement("fast-button");
        button.innerText = this.model.label;
        button.disabled = this.model.disabled;
        button.appearance = this.model.appearance;
        button.autofocus = this.model.autofocus;
        button.style.width = "100%";
        button.style.height = "100%";
        return button;
    }
}
FastButtonView.__name__ = "FastButtonView";
export class FastButton extends Button {
    // __view_type__: FastButtonView
    constructor(attrs) {
        super(attrs);
    }
    static init_FastButton() {
        this.prototype.default_view = FastButtonView;
        this.define({
            appearance: [p.String,],
            autofocus: [p.Boolean,],
        });
    }
}
FastButton.__name__ = "FastButton";
FastButton.__module__ = "awesome_panel_extensions.bokeh_extensions.fast_button";
FastButton.init_FastButton();
//# sourceMappingURL=fast_button.js.map