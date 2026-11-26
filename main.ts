// Entry for make.fun's news-image-20261126 bounty (Node 22, stdlib only):
// the program copies the front page image beside it to /output/entry.png.
// The image itself is drawn by build_image.py (PIL) from the day's news.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
