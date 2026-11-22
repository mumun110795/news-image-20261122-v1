// Entry point for the news-image-20261122 submission.
//
// The deliverable image (entry.png) is rendered ahead of time by render.py
// and committed next to this file. This program's only job is to place a
// byte-identical copy of that image into the output directory the harness
// designates, so repeated runs always produce exactly the same bytes.
//
// Output directory: $MAKEFUN_OUTPUT_DIR when set, otherwise /output.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (looked in ${here})`);
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
// Create the directory if needed, but never remove it: on the grading
// runner it may be a mounted volume, and deleting a mount point fails.
mkdirSync(outDir, { recursive: true });

const target = join(outDir, "entry.png");
copyFileSync(source, target);

const { size } = statSync(target);
console.log(`wrote ${target} (${size} bytes)`);
