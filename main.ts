// Entrypoint for the news-image-20261124 entry.
//
// The front page is pre-built by compose.py into entry.png, which sits
// next to this file. All this loader does is check the PNG is genuine
// and within the competition size limit, then copy it to /output, where
// the judge reads it. Nothing is generated at run time, so the output
// is byte-identical on every run.
//
// Run with: node main.ts
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png is missing next to main.ts");
}
const info = statSync(source);
if (info.size > MAX_BYTES) {
  throw new Error(`entry.png is ${info.size} bytes, over the 1 MiB limit`);
}
const head = readFileSync(source).subarray(0, 8);
if (!head.equals(PNG_MAGIC)) {
  throw new Error("entry.png does not start with the PNG signature");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`copied entry.png (${info.size} bytes) to ${target}`);
