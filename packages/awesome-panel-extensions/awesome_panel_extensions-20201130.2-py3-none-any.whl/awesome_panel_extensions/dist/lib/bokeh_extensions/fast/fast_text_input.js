import { TextInput } from "@bokehjs/models/widgets/text_input";
import { InputWidgetView } from "@bokehjs/models/widgets/input_widget";
import * as p from "@bokehjs/core/properties";
// I tried to inherit from TextInputView but I could not
// get it working. It created two textinputs.
export class FastTextInputView extends InputWidgetView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.name.change, () => { var _a; return this.input_el.name = (_a = this.model.name) !== null && _a !== void 0 ? _a : ""; });
        this.connect(this.model.properties.value.change, () => { this.input_el.value = this.model.value; console.log("value"); });
        this.connect(this.model.properties.value_input.change, () => this.input_el.value = this.model.value_input);
        this.connect(this.model.properties.disabled.change, () => this.input_el.disabled = this.model.disabled);
        this.connect(this.model.properties.placeholder.change, () => this.input_el.placeholder = this.model.placeholder);
        this.connect(this.model.properties.appearance.change, () => this.input_el_any.appearance = this.model.appearance);
        this.connect(this.model.properties.autofocus.change, () => this.input_el_any.autofocus = this.model.autofocus);
        this.connect(this.model.properties.type_of_text.change, () => this.input_el_any.type = this.model.type_of_text);
        this.connect(this.model.properties.max_length.change, () => this.input_el_any.setAttribute("maxlength", this.model.max_length));
        this.connect(this.model.properties.min_length.change, () => this.input_el_any.setAttribute("minlength", this.model.min_length));
        this.connect(this.model.properties.pattern.change, () => this.input_el_any.pattern = this.model.pattern);
        // Could not get size working. It raises an error
        // this.connect(this.model.properties.size.change, () => this.input_el_any.size = this.model.size)
        this.connect(this.model.properties.spellcheck.change, () => this.input_el_any.spellcheck = this.model.spellcheck);
        this.connect(this.model.properties.required.change, () => this.input_el_any.required = this.model.required);
        // Could not get readonly working as a property.
        // https://github.com/microsoft/fast/issues/3852
        this.connect(this.model.properties.readonly.change, () => this.input_el_any.setAttribute("readonly", this.model.readonly));
    }
    get input_el_any() {
        return this.input_el;
    }
    render() {
        super.render();
        const fastTextField = document.createElement("fast-text-field");
        this.input_el = fastTextField;
        this.input_el.className = "bk-fast-input";
        this.input_el.addEventListener("change", () => this.change_input());
        this.input_el.addEventListener("input", () => this.change_input_oninput());
        this.group_el.appendChild(this.input_el);
        // For some unknown reason we need to set these properties after the above
        // Otherwise for example the value is reset to ""
        fastTextField.name = this.model.name;
        fastTextField.value = this.model.value;
        fastTextField.appearance = this.model.appearance;
        fastTextField.autofocus = this.model.autofocus;
        fastTextField.placeholder = this.model.placeholder;
        fastTextField.disabled = this.model.disabled;
        fastTextField.type = this.model.type_of_text;
        fastTextField.setAttribute("maxlength", this.model.max_length);
        fastTextField.setAttribute("minlength", this.model.min_length);
        fastTextField.pattern = this.model.pattern;
        // Could not get size working. It raises an error.
        // fastTextField.size = this.model.size;
        fastTextField.spellcheck = this.model.spellcheck;
        fastTextField.required = this.model.required;
        fastTextField.disabled = this.model.disabled;
        fastTextField.setAttribute("readonly", this.model.readonly);
    }
    change_input() {
        this.model.value = this.input_el.value;
        super.change_input();
    }
    change_input_oninput() {
        this.model.value_input = this.input_el.value;
        super.change_input();
    }
}
FastTextInputView.__name__ = "FastTextInputView";
export class FastTextInput extends TextInput {
    constructor(attrs) {
        super(attrs);
    }
    static init_FastTextInput() {
        this.prototype.default_view = FastTextInputView;
        this.define({
            // name inherited
            // value inherited
            appearance: [p.String,],
            autofocus: [p.Boolean,],
            // placeholder inherited
            type_of_text: [p.String,],
            max_length: [p.Number,],
            min_length: [p.Number,],
            pattern: [p.String,],
            size: [p.Any,],
            spellcheck: [p.Boolean,],
            required: [p.Boolean,],
            // disabled inherited
            readonly: [p.Boolean, false],
        });
    }
}
FastTextInput.__name__ = "FastTextInput";
FastTextInput.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_text_input";
FastTextInput.init_FastTextInput();
//# sourceMappingURL=fast_text_input.js.map