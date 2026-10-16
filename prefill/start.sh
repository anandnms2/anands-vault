#!/bin/sh
# Anands Vault wrapper around upstream's start script (kept as /start-upstream.sh).
# Writes the login pre-fill script from ANANDS_VAULT_EMAIL, then hands over to Vaultwarden unchanged.
# Unset ANANDS_VAULT_EMAIL = no pre-fill. Only email-safe characters are allowed through.
EMAIL=$(printf '%s' "${ANANDS_VAULT_EMAIL:-}" | tr -cd 'A-Za-z0-9._%+@-')
if ! sed "s|__ANANDS_EMAIL__|${EMAIL}|g" /branding/prefill/anands-prefill.js > /web-vault/anands-prefill.js 2>/dev/null; then
  echo "[anands] could not write /web-vault/anands-prefill.js; login pre-fill disabled" >&2
fi
exec /start-upstream.sh "$@"
