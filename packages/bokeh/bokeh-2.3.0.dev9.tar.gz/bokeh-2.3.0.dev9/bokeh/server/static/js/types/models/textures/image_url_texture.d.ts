import { Texture } from "./texture";
import * as p from "../../core/properties";
import { Color } from "../../core/types";
import { Context2d } from "../../core/util/canvas";
export declare namespace ImageURLTexture {
    type Attrs = p.AttrsOf<Props>;
    type Props = Texture.Props & {
        url: p.Property<string>;
    };
}
export interface ImageURLTexture extends ImageURLTexture.Attrs {
}
export declare abstract class ImageURLTexture extends Texture {
    properties: ImageURLTexture.Props;
    constructor(attrs?: Partial<ImageURLTexture.Attrs>);
    static init_ImageURLTexture(): void;
    initialize(): void;
    get_pattern(_color: Color, _scale: number, _weight: number): (ctx: Context2d) => CanvasPattern | null;
    onload(defer_func: () => void): void;
    private _loader;
}
//# sourceMappingURL=image_url_texture.d.ts.map