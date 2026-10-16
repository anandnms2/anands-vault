# Anands Vault: Vaultwarden branding overlay

Drop this folder into a Git repo and deploy it in Coolify with the Dockerfile build pack.

1. Build variable `PUBLIC_URL` = your vault's https URL (for example https://vault.anands.xyz). The build fails without it.
2. Optional build variables: `BRAND_NAME` (default "Anands Vault"), `VW_VERSION` (pin a tested release tag).
3. Runtime env: `DOMAIN`, `ADMIN_TOKEN` (Argon2 hash), SMTP settings, SSO settings. Mount a volume at `/data`.
4. While tuning colors or emails, set `RELOAD_TEMPLATES=true`; remove it afterwards.
5. After the first build, run `grep -rl Vaultwarden /web-vault | head` inside the container to find leftovers.

Not yet tested: the Docker build itself and the theme in a browser. See the guide for details.

## Upgrade an existing Coolify Vaultwarden service (keeps your data)
1. Push this folder to a GitHub repo `anandnms2/anands-vault`; the included workflow builds `ghcr.io/anandnms2/anands-vault:latest` (make the package public, or add GHCR credentials in Coolify).
2. Coolify > service "Anands Password" > Edit Compose: change only the `image:` line of the vaultwarden container to `ghcr.io/anandnms2/anands-vault:latest`. Leave the `vaultwarden-data` volume, DOMAIN, ADMIN_TOKEN and DB settings untouched.
3. Save and Deploy. The volume at /data (database, attachments, RSA keys) is reused as is.
4. Rollback: set `image:` back to `vaultwarden/server:latest`.
Before step 3, back up: stop nothing, just copy /data (or the sqlite/Postgres dump) first.

## Login email pre-fill
Set runtime env `ANANDS_VAULT_EMAIL` on the vaultwarden container (Coolify env, not in this public repo).
The login screen then opens with that email already filled in; you type the master password (or let the browser fill it)
and the OTP. Unset = no pre-fill. The master password is never stored or pre-filled by design.
Implementation: `prefill/start.sh` wraps upstream's `/start.sh`, writes `/web-vault/anands-prefill.js` from the env var,
and `index.html` loads it. Only the `#/login` route is touched, and nothing already typed is overwritten.

## Fewer prompts (settings in the vault itself, per device)
- Two-step login screen: tick **Remember me** on a trusted device, so the OTP is skipped for about 30 days.
- Settings > Options > **Vault timeout**: longer, or "On browser restart"; timeout action: **Lock**.
- Web extension / mobile app: Settings > Unlock with **PIN** or biometrics, so you rarely retype the master password.
