import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// news-image-20261124 v3: the entry is a single pre-rendered image.
// This entrypoint only copies it to the grader's output directory.
// The copy is byte-for-byte, so two runs produce identical output.
// Output path is fixed by the competition sandbox: /output/entry.png.
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
