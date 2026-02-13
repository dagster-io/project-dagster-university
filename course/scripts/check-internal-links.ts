/**
 * Checks that internal markdown links (href starting with /) resolve to existing
 * pages. Next.js routes like /dagster-testing/lesson-1/0-about-this-course
 * map to pages/dagster-testing/lesson-1/0-about-this-course.md
 */
import * as fs from 'fs';
import * as path from 'path';
import fg from 'fast-glob';

const PAGES_DIR = path.join(__dirname, '..', 'pages');
const INTERNAL_LINK_RE = /\]\s*\(\s*(\/[^)\s#]*)/g;

// Static assets are served from public/; we don't expect a .md for these
const STATIC_EXT = /\.(png|jpe?g|gif|svg|webp|ico|woff2?|ttf|eot)$/i;
const IMAGES_PREFIX = '/images/';

function isStaticAsset(href: string): boolean {
  return href.startsWith(IMAGES_PREFIX) || STATIC_EXT.test(href);
}

async function main(): Promise<void> {
  const mdFiles = await fg(['pages/**/*.md'], {cwd: path.join(__dirname, '..'), absolute: true});
  const broken: Array<{file: string; href: string; targetPath: string}> = [];

  for (const file of mdFiles) {
    const content = fs.readFileSync(file, 'utf-8');
    let m: RegExpExecArray | null;
    INTERNAL_LINK_RE.lastIndex = 0;
    while ((m = INTERNAL_LINK_RE.exec(content)) !== null) {
      const href = m[1];
      if (isStaticAsset(href)) continue;

      // Map /path/segment -> pages/path/segment.md, or /path/file.md -> pages/path/file.md
      const relativePath = href.replace(/^\//, '');
      const targetPath = path.join(
        PAGES_DIR,
        relativePath.endsWith('.md') ? relativePath : relativePath + '.md'
      );
      const normalized = path.normalize(targetPath);
      if (!path.relative(PAGES_DIR, normalized).startsWith('..') && !fs.existsSync(normalized)) {
        broken.push({
          file: path.relative(process.cwd(), file),
          href,
          targetPath: path.relative(process.cwd(), normalized),
        });
      }
    }
  }

  if (broken.length > 0) {
    console.error('Broken internal links:\n');
    for (const {file, href, targetPath} of broken) {
      console.error(`  ${file} → ${href}`);
      console.error(`    (expected file: ${targetPath})\n`);
    }
    process.exit(1);
  }

  console.log('✅ All internal links resolve to existing pages.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
