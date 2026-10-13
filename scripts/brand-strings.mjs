// Usage: node brand-strings.mjs <web-vault-dir> "<New Name>"
// Renames "Bitwarden" in English UI strings, but leaves alone any string that
// points at something you did NOT rebrand (browser extension, mobile/desktop apps,
// Authenticator, Send, cloud billing, official support links).
import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";

const [dir, name] = process.argv.slice(2);
if (!dir || !name) { console.error("usage: brand-strings.mjs <web-vault-dir> <name>"); process.exit(1); }

for (const loc of ["en", "en_GB", "en_IN"]) {
const file = `${dir}/locales/${loc}/messages.json`;
if (!existsSync(file)) continue;
const data = JSON.parse(readFileSync(file, "utf8"));
const keep = /Authenticator|Secrets Manager|Families|Key Connector|Duo|Directory Connector|bitwarden\.com|bitwarden\.net|customer|churn/i;

let changed = 0, kept = 0;
for (const entry of Object.values(data)) {
  const m = entry.message;
  if (typeof m !== "string" || !m.includes("Bitwarden")) continue;
  if (keep.test(m)) { kept++; continue; }
  entry.message = m.replaceAll("Bitwarden", name);
  changed++;
}
writeFileSync(file, JSON.stringify(data, null, 2) + "\n");
console.log(`${loc}: renamed ${changed} strings, left ${kept} that reference the official services`);
}

// "Vaultwarden" appears in a few translated strings too, in every language
for (const l of readdirSync(`${dir}/locales`)) {
  const f = `${dir}/locales/${l}/messages.json`;
  if (!existsSync(f)) continue;
  const t = readFileSync(f, "utf8");
  if (t.includes("Vaultwarden")) writeFileSync(f, t.replaceAll("Vaultwarden", name));
}
