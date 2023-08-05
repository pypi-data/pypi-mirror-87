import { AbstractIcon, AbstractIconView } from "@bokehjs/models/widgets/abstract_icon";
import * as p from "@bokehjs/core/properties";
// See https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}
export class SVGIconView extends AbstractIconView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.change, () => this.render());
    }
    render() {
        super.render();
        console.log(this.model);
        if (this.model.svg === null && this.model.svg === "") {
            return;
        }
        const el = htmlToElement(this.model.svg);
        this.el.innerHTML = "";
        this.el.appendChild(el);
        this.el.style.display = "inline";
        this.el.style.verticalAlign = "middle";
        el.style.height = `${this.model.size}em`;
        el.style.width = `${this.model.size}em`;
        el.style.fill = this.model.fill_color;
        if (this.model.spin_duration > 0) {
            // See https://codepen.io/eveness/pen/BjLaoa
            const animationDuration = `${this.model.spin_duration}ms`;
            el.style.setProperty("-webkit-animation-name", "spin");
            el.style.setProperty("-webkit-animation-duration", animationDuration);
            el.style.setProperty("-webkit-animation-iteration-count", "infinite");
            el.style.setProperty("-webkit-animation-timing-function", "linear");
            el.style.setProperty("-moz-animation-name", "spin");
            el.style.setProperty("-moz-animation-duration", animationDuration);
            el.style.setProperty("-moz-animation-iteration-count", "infinite");
            el.style.setProperty("-moz-animation-timing-function", "linear");
            el.style.setProperty("-ms-animation-name", "spin");
            el.style.setProperty("-ms-animation-duration", animationDuration);
            el.style.setProperty("-ms-animation-iteration-count", "infinite");
            el.style.setProperty("-ms-animation-timing-function", "linear");
            el.style.setProperty("animation-name", "spin");
            el.style.setProperty("animation-duration", animationDuration);
            el.style.setProperty("animation-iteration-count", "infinite");
            el.style.setProperty("animation-timing-function", "linear");
        }
        el.classList.add("icon");
        if (this.model.icon_name != null && this.model.icon_name !== "") {
            el.classList.add(`icon-${this.model.icon_name}`);
        }
    }
}
SVGIconView.__name__ = "SVGIconView";
export class SVGIcon extends AbstractIcon {
    constructor(attrs) {
        super(attrs);
    }
    static init_SVGIcon() {
        this.prototype.default_view = SVGIconView;
        this.define({
            icon_name: [p.String,],
            svg: [p.String,],
            size: [p.Number, 1.0],
            fill_color: [p.String, "currentColor"],
            spin_duration: [p.Int, 0],
        });
    }
}
SVGIcon.__name__ = "SVGIcon";
SVGIcon.__module__ = "awesome_panel_extensions.bokeh_extensions.svg_icon";
SVGIcon.init_SVGIcon();
//# sourceMappingURL=svg_icon.js.map