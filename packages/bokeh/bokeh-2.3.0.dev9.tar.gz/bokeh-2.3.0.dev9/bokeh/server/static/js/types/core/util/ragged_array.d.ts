import { NumberArray } from "../types";
import { equals, Equatable, Comparator } from "./eq";
export declare class RaggedArray implements Equatable {
    readonly offsets: Uint32Array;
    readonly array: NumberArray;
    static [Symbol.toStringTag]: string;
    constructor(offsets: Uint32Array, array: NumberArray);
    [equals](that: this, cmp: Comparator): boolean;
    get length(): number;
    clone(): RaggedArray;
    static from(items: number[][]): RaggedArray;
    [Symbol.iterator](): IterableIterator<NumberArray>;
    private _check_bounds;
    get(i: number): NumberArray;
    set(i: number, array: ArrayLike<number>): void;
}
//# sourceMappingURL=ragged_array.d.ts.map