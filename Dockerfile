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
 && sed -i "s/Vaultwarden Web/${BRAND_NAME}/g; s/alt=\"Vaultwarden\"/alt=\"${BRAND_NAME}\"/g" \
        /web-vault/index.html /web-vault/manifest.json \
 && sed -i 's/#175DDC/#F68712/g' /web-vault/index.html

# ---- Stage 2: final image = upstream server + branded web vault + templates ----
FROM docker.io/vaultwarden/server:${VW_VERSION}
ARG BRAND_NAME
# Public https URL of your vault, e.g. https://vault.anands.xyz (used for the email logo link)
ARG PUBLIC_URL
COPY --from=brand /web-vault /web-vault
# Outside /data on purpose: /data is a mounted volume and would hide these files.
COPY templates /branding/templates
RUN test -n "${PUBLIC_URL}" \
 && sed -i "s|__PUBLIC_URL__|${PUBLIC_URL%/}|g" /branding/templates/email/email_header.hbs
ENV TEMPLATES_FOLDER=/branding/templates \
    SMTP_FROM_NAME="${BRAND_NAME}" \
    INVITATION_ORG_NAME="${BRAND_NAME}"
