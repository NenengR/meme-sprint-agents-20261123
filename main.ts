// Meme Sprint entry (Node 22, standard library only): the meme is this
// directory's entry.png, a 1024x1024 picture drawn programmatically, and the
// program hands it in. It copies entry.png from beside this file to /output
// as /output/entry.png, the one file the gate checks. It resolves its own
// directory from import.meta.url, never from the working directory, so it
// runs the same from anywhere.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const DEFAULT_OUTPUT_DIR = '/output';

function resolveScriptDir() {
  return fileURLToPath(new URL('.', import.meta.url));
}

function resolveOutputDir() {
  return process.env.MAKEFUN_OUTPUT_DIR ?? DEFAULT_OUTPUT_DIR;
}

function handInEntry(scriptDir, outputDir) {
  mkdirSync(outputDir, { recursive: true });
  copyFileSync(join(scriptDir, 'entry.png'), join(outputDir, 'entry.png'));
}

handInEntry(resolveScriptDir(), resolveOutputDir());
