/**
 * Runs markdown-link-check on all course markdown files to validate external URLs.
 * Internal links (starting with /) are ignored via .markdown-link-check.json.
 */
const fs = require('fs');
const path = require('path');
const fg = require('fast-glob');
const markdownLinkCheck = require('markdown-link-check');

const COURSE_ROOT = path.join(__dirname, '..');
const configPath = path.join(COURSE_ROOT, '.markdown-link-check.json');
const config = fs.existsSync(configPath)
  ? JSON.parse(fs.readFileSync(configPath, 'utf-8'))
  : {};

// Convert ignorePatterns from JSON strings to RegExp for the API
if (config.ignorePatterns && Array.isArray(config.ignorePatterns)) {
  config.ignorePatterns = config.ignorePatterns.map(({pattern}) =>
    typeof pattern === 'string' ? {pattern: new RegExp(pattern)} : {pattern}
  );
}

async function checkFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  return new Promise((resolve) => {
    markdownLinkCheck(content, config, (err, results) => {
      if (err) return resolve([{file: filePath, err}]);
      const dead = results.filter((r) => r.status === 'dead');
      resolve(dead.map((r) => ({file: filePath, link: r.link, statusCode: r.statusCode, err: r.err})));
    });
  });
}

async function main() {
  const mdFiles = await fg('pages/**/*.md', {cwd: COURSE_ROOT, absolute: true});
  const allFailures = [];
  for (const file of mdFiles) {
    const failures = await checkFile(file);
    allFailures.push(...failures);
  }
  if (allFailures.length > 0) {
    console.error('Broken or unreachable external links:\n');
    for (const f of allFailures) {
      const rel = path.relative(process.cwd(), f.file);
      if (f.link) {
        console.error(`  ${rel} → ${f.link}`);
        if (f.statusCode) console.error(`    status: ${f.statusCode}`);
        if (f.err) console.error(`    ${f.err.message || f.err}`);
      } else {
        console.error(`  ${rel}: ${f.err?.message || f.err}`);
      }
      console.error('');
    }
    process.exit(1);
  }
  console.log('✅ All external links are reachable.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
