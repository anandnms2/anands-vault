// Usage: node patch-logos.mjs <web-vault-dir> "<Brand Name>"
// Vaultwarden's web vault draws several logos as inline SVG inside app/main.*.js.
// Replace each with an SVG that points at our own image files (images/logo*.svg, icon-*.png).
import { readFileSync, writeFileSync, readdirSync, renameSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";

const [dir, name] = process.argv.slice(2);
const f = readdirSync(`${dir}/app`).find((n) => /^main\..*\.js$/.test(n));
const path = `${dir}/app/${f}`;
let js = readFileSync(path, "utf8");

const NS = 'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"';
const pair = (vb, w, h, light, dark) =>
  `<svg version="1.1" viewBox="${vb}" ${NS}><title>${name}</title>` +
  `<image class="av-on-light" href="${light}" x="0" y="0" width="${w}" height="${h}" preserveAspectRatio="xMinYMid meet"/>` +
  `<image class="av-on-dark" href="${dark}" x="0" y="0" width="${w}" height="${h}" preserveAspectRatio="xMinYMid meet"/></svg>`;

const targets = [
  // [viewBox marker, replacement]
  ['viewBox="0 0 290 60"', pair("0 0 300 60", 300, 60, "images/logo.svg", "images/logo-white.svg")],
  ['viewBox="0 0 800 200"', pair("0 0 300 60", 300, 60, "images/logo-white.svg", "images/logo-white.svg")],
  ['viewBox="0 0 580 104"', pair("0 0 300 60", 300, 60, "images/logo.svg", "images/logo-white.svg")],
  ['viewBox="0 0 60 60"', pair("0 0 60 60", 60, 60, "images/icon-dark.png", "images/icon-white.png")],
];

let n = 0;
for (const [marker, repl] of targets) {
  let from = 0;
  for (;;) {
    const m = js.indexOf(marker, from);
    if (m < 0) break;
    const st = js.lastIndexOf("<svg", m);
    const en = js.indexOf("</svg>", m);
    // sanity: marker must sit in the opening tag of this svg
    if (st < 0 || en < 0 || m - st > 80) { from = m + marker.length; continue; }
    js = js.slice(0, st) + repl + js.slice(en + 6);
    from = st + repl.length;
    n++;
  }
}
// Visible text hard-coded in the app bundle
const swaps = [
  ['"Vaultwarden Web"', JSON.stringify(name)],
  [' A modified version of the Bitwarden\u00ae Web Vault for Vaultwarden (an unofficial rewrite of the Bitwarden\u00ae server).', ` ${name}, your private password manager.`],
  [' Vaultwarden is not associated with the Bitwarden\u00ae project nor Bitwarden Inc. ', ' '],
  ['otpauth://totp/Vaultwarden:', `otpauth://totp/${name.replace(/ /g, "%20")}:`],
];
let t = 0;
for (const [a, b] of swaps) { const c = js.split(a).length - 1; if (c) { js = js.split(a).join(b); t += c; } else console.warn("not found:", a.slice(0, 50)); }
console.log(`replaced ${t} hard-coded text strings`);
writeFileSync(path, js);

// Cache-bust: the bundle file name is unchanged by our edits, so browsers keep serving the old copy.
// Give it a new content-based name and update every reference.
const oldHash = f.match(/^main\.(.*)\.js$/)[1];
const newHash = createHash("sha1").update(js).digest("hex").slice(0, oldHash.length);
if (newHash !== oldHash) {
  renameSync(path, `${dir}/app/main.${newHash}.js`);
  if (existsSync(path + ".map")) renameSync(path + ".map", `${dir}/app/main.${newHash}.js.map`);
  const walk = (d) => readdirSync(d, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? (e.name === "locales" || e.name === "images" || e.name === "fonts" ? [] : walk(`${d}/${e.name}`)) : [`${d}/${e.name}`]);
  let refs = 0;
  for (const file of walk(dir)) {
    if (!/\.(html|js|json|css)$/.test(file)) continue;
    const t = readFileSync(file, "utf8");
    if (t.includes(oldHash)) { writeFileSync(file, t.split(oldHash).join(newHash)); refs++; }
  }
  console.log(`renamed bundle ${oldHash} -> ${newHash}, updated ${refs} files`);
}
console.log(`patched ${n} inline logo SVGs in ${f}`);
if (n < 4) { console.error("expected at least 4 replacements"); process.exit(1); }
