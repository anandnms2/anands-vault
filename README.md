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
