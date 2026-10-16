# syntax=docker/dockerfile:1
# Branded Vaultwarden for Coolify. Build context = this folder.
# Pin VW_VERSION to a release tag you have tested; "latest" can change under you.
ARG VW_VERSION=latest
ARG BRAND_NAME="Anands Vault"

FROM docker.io/vaultwarden/server:${VW_VERSION} AS upstream

# ---- Stage 1: patch the bundled web vault (files only, no Angular rebuild) ----
FROM docker.io/library/node:24-alpine AS brand
ARG BRAND_NAME
COPY --from=upstream /web-vault /web-vault
COPY web-vault/ /web-vault/
COPY scripts/ /scripts/
RUN node /scripts/brand-strings.mjs /web-vault "${BRAND_NAME}" \
 && node /scripts/patch-logos.mjs /web-vault "${BRAND_NAME}" \
 && sed -i "s/alt=\"Bitwarden\"/alt=\"${BRAND_NAME}\"/g; s/Bitwarden Web vault/${BRAND_NAME}/g; s/Bitwarden \(Duo Redirect\|WebAuthn\) Connector/${BRAND_NAME} \1 Connector/g; s/<title>Bitwarden<\/title>/<title>${BRAND_NAME}<\/title>/g" /web-vault/*.html \
 && sed -i "s/Vaultwarden Web/${BRAND_NAME}/g; s/\"Bitwarden\"/\"${BRAND_NAME}\"/g" /web-vault/*.json \
 && sed -i "s/Vaultwarden Web/${BRAND_NAME}/g; s/alt=\"Vaultwarden\"/alt=\"${BRAND_NAME}\"/g" \
        /web-vault/index.html /web-vault/manifest.json \
 && sed -i 's/#175DDC/#F68712/g' /web-vault/index.html

# ---- Stage 2: final image = upstream server + branded web vault + templates ----
FROM docker.io/vaultwarden/server:${VW_VERSION}
ARG BRAND_NAME
# Public https URL of your vault, e.g. https://vault.anands.xyz (used for the email logo link)
ARG PUBLIC_URL
RUN rm -rf /web-vault
COPY --from=brand /web-vault /web-vault
# Outside /data on purpose: /data is a mounted volume and would hide these files.
COPY templates /branding/templates
RUN test -n "${PUBLIC_URL}" \
 && sed -i "s|__PUBLIC_URL__|${PUBLIC_URL%/}|g" /branding/templates/email/email_header.hbs
# Login email pre-fill (ANANDS_VAULT_EMAIL, set at runtime) via a wrapper around upstream's /start.sh.
# The build fails loudly if upstream's start script or index.html ever change shape.
COPY prefill /branding/prefill
RUN test -f /start.sh \
 && mv /start.sh /start-upstream.sh \
 && cp /branding/prefill/start.sh /start.sh && chmod +x /start.sh \
 && touch /web-vault/anands-prefill.js && chmod a+rw /web-vault/anands-prefill.js \
 && sed -i 's#</head>#<script defer src="/anands-prefill.js"></script></head>#' /web-vault/index.html \
 && grep -q 'anands-prefill.js' /web-vault/index.html
ENV TEMPLATES_FOLDER=/branding/templates \
    SMTP_FROM_NAME="${BRAND_NAME}" \
    INVITATION_ORG_NAME="${BRAND_NAME}"
