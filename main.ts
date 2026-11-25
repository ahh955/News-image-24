// News-image-20261124 v2 — deterministic entrypoint.
//
// The front page is fully rendered at build time by compose.py and stored
// as entry.png next to this file. This script only validates the PNG
// signature and copies the exact bytes to /output/entry.png, so every
// run produces byte-identical output.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const out = join("/output", "entry.png");

const bytes = readFileSync(src);
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (
  bytes.length < PNG_SIGNATURE.length ||
  !PNG_SIGNATURE.every((b, i) => bytes[i] === b)
) {
  throw new Error(`entry.png is not a valid PNG file: ${src}`);
}

mkdirSync("/output", { recursive: true });
writeFileSync(out, bytes);
console.log(`wrote ${out} (${bytes.length} bytes)`);
