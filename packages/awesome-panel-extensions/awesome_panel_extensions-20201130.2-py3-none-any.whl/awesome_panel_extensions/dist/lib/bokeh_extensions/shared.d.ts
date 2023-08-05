import { HTMLBox } from "@bokehjs/models/layouts/html_box";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
/** Function copied from the panel\models\layout.ts file of Panel
 * It is used for some models like deckgl, progress and vtlklayout
 * I have not yet understood why
 * @param el
 * @param model
 */
export declare function set_size(el: HTMLElement, model: HTMLBox): void;
/** Transform the data of the cds to 'records' format, i.e. a list of objects
 *
 *  For example transforms to [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
 *
 *  Some js libraries like perspective-viewer uses this format to load data.
 *
 * @param cds
 */
export declare function transform_cds_to_records(cds: ColumnDataSource): any;
/** Helper function used to incrementally build a html element string
 *
 *  For example toAttribute("columns", ['x','y']) returns ' columns="['x','y']"
 *  For example toAttribute("columns", null) returns ""
 *
 * @param attribute
 * @param value
 */
export declare function toAttribute(attribute: string, value: any): string;
