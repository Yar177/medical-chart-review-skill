# SMART App Launch pre-Inferno checklist

> Run this checklist before submitting your SMART app or server to the Inferno SMART App Launch kit. Most Inferno failures map to one of these items. Replace `{{...}}`.
>
> All example payloads, identifiers, URLs, and tokens are `[synthetic]` placeholders.

---

## Identity

- **App / Server name**: {{}}
- **Launch type**: {{EHR launch | Standalone launch | both}}
- **SMART App Launch IG version**: {{e.g., 2.2.0}}
- **FHIR base version**: {{R4 4.0.1 | R4B 4.3.0 | R5 5.0.0}}
- **Owner**: {{team}}
- **Last reviewed**: {{YYYY-MM-DD}}

---

## A. Discovery

- [ ] `.well-known/smart-configuration` exposed at `[fhir-base]/.well-known/smart-configuration` (and at `/.well-known/smart-configuration` for the issuer).
- [ ] Response is `application/json`.
- [ ] `authorization_endpoint` present.
- [ ] `token_endpoint` present.
- [ ] `capabilities[]` includes the modes supported (`launch-ehr`, `launch-standalone`, `client-public`, `client-confidential-symmetric`, `client-confidential-asymmetric`, `permission-patient`, `permission-user`, `permission-v2`, `permission-offline`, ...).
- [ ] `scopes_supported[]` lists every scope the server will issue.
- [ ] `response_types_supported` includes `code`.
- [ ] `code_challenge_methods_supported` includes `S256` (PKCE).
- [ ] `grant_types_supported` includes `authorization_code` (and `client_credentials` if Backend Services).
- [ ] `token_endpoint_auth_methods_supported` includes the expected method (`none` for public client; `private_key_jwt` for Backend Services).
- [ ] `CapabilityStatement` (`[base]/metadata`) declares `SMART-on-FHIR` security service with `oauth-uris` extension (see [`templates/capability-statement-skeleton.md`](capability-statement-skeleton.md)).

## B. Scopes

- [ ] Using **v2 scopes** if server advertises `permission-v2`. v2 uses `c|r|u|d|s` letters and optional `?` query qualifier (e.g., `patient/Observation.rs`, `patient/Observation.rs?category=laboratory`).
- [ ] Using **v1 scopes** only if server advertises v1 (`permission-patient`, `permission-user` without `permission-v2`).
- [ ] Not mixing v1 and v2 syntax in one request.
- [ ] Requesting only scopes the user / context will actually need.
- [ ] `launch` scope present for EHR launch.
- [ ] `launch/patient` or `launch/encounter` scope present for standalone launch needing patient picker.
- [ ] `openid fhirUser` if needing user identity.
- [ ] `offline_access` only if app needs a refresh token (and server advertises it).

## C. EHR launch flow

- [ ] App registered with the EHR's launch URL.
- [ ] EHR redirects to launch URL with `iss` (FHIR base) and `launch` (opaque token) params.
- [ ] App fetches discovery from `iss/.well-known/smart-configuration`.
- [ ] App initiates authorization with `launch=<token>` parameter included.
- [ ] App validates `iss` against expected trusted issuers (not just any URL).

## D. Standalone launch flow

- [ ] App initiates discovery from a server URL the user (or config) supplied.
- [ ] App requests `launch/patient` (or `launch/encounter`) to invoke server-side picker.
- [ ] App handles patient context in the token response (`patient` field).

## E. Authorization request

- [ ] `response_type=code`.
- [ ] `client_id=<registered>`.
- [ ] `redirect_uri=<exact match to registration>` (HTTPS in prod; `http://localhost` allowed for native dev).
- [ ] `scope` set per Section B.
- [ ] `state` is unguessable random (CSRF defense). Validated on callback.
- [ ] `aud=<FHIR base URL>` matches exactly the server's FHIR base.
- [ ] PKCE: `code_challenge` (S256 hash of `code_verifier`) + `code_challenge_method=S256`.

## F. Token exchange

- [ ] `grant_type=authorization_code`.
- [ ] `code=<from callback>`.
- [ ] `redirect_uri=<same as authorization request>`.
- [ ] `client_id=<registered>` (public client) or `client_assertion` (confidential asymmetric).
- [ ] `code_verifier=<original>` (PKCE).
- [ ] App handles `error` response (`invalid_grant`, `invalid_scope`, etc.) gracefully.

## G. Token response handling

- [ ] `access_token` stored securely (memory only for SPA; OS keychain for native; encrypted storage for server-side).
- [ ] `id_token` (if `openid` scope) validated: signature, `iss`, `aud`, `exp`, `iat`, `nonce`.
- [ ] `patient` / `encounter` / `fhirUser` context fields applied to UI.
- [ ] `expires_in` honored - proactive refresh before expiry.
- [ ] `refresh_token` (if granted) stored securely and used to refresh.
- [ ] `scope` field in response reflects what was actually granted (may be subset of requested).

## H. FHIR API calls with the token

- [ ] `Authorization: Bearer <access_token>` on every FHIR request.
- [ ] Calls scoped to the granted permissions only (don't request resources outside scope).
- [ ] Handle `401 Unauthorized` (token expired) → refresh or re-auth.
- [ ] Handle `403 Forbidden` (scope insufficient) → request additional scopes or surface to user.

## I. Refresh

- [ ] `grant_type=refresh_token` + `refresh_token=<value>`.
- [ ] On rotation, replace stored refresh token with new one in response.
- [ ] Detect refresh-token revocation (`invalid_grant`) → require re-auth.

## J. Logout / session termination

- [ ] App invalidates local tokens on logout.
- [ ] If server supports revocation (`revocation_endpoint`), call it.

## K. Security hardening

- [ ] HTTPS only (no `http://` in production).
- [ ] No tokens in URL query strings (except short-lived `code` in authorize callback).
- [ ] No tokens in logs.
- [ ] Strict-Transport-Security on all SMART endpoints.
- [ ] Content-Security-Policy on app pages handling tokens.
- [ ] Service-worker / page-load XSS surface reviewed.

## L. Common Inferno SMART App Launch failure IDs

| Failure | Common cause | Fix |
|---|---|---|
| `smart_discovery_endpoint` | discovery missing or returns wrong content-type | expose `.well-known/smart-configuration` as `application/json` |
| `smart_launch_aud_validation` | server accepts arbitrary `aud` | validate `aud` matches FHIR base |
| `smart_v2_scopes` | v1 scopes requested when v2 advertised | switch to v2 syntax |
| `smart_pkce_required` | server accepted auth without PKCE | enforce `code_challenge` |
| `smart_refresh_token_with_scope` | refresh-token issued without `offline_access` | gate refresh on `offline_access` scope |
| `smart_context_launch_patient` | app didn't request `launch/patient` for standalone | request the scope |

## M. Sign-off

| Role | Name | Date |
|---|---|---|
| App author | {{}} | {{}} |
| Security reviewer | {{}} | {{}} |
| Pre-Inferno gate | {{}} | {{}} |
