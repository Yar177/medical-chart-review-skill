# SMART on FHIR

> **Why this file exists:** SMART on FHIR is the authorization layer that every EHR-app and member-facing payer-API uses. Two flavors matter: **SMART App Launch** (user-facing apps with OAuth 2.0 + PKCE + launch context) and **SMART Backend Services** (system-to-system, asymmetric client auth with JWKS). Getting the scopes wrong is the most common Inferno failure mode. Getting the `aud` parameter wrong is the most common security bug. This file covers both flavors at the level needed to design an integration and pass Inferno's SMART App Launch + Backend Services tests.

Spec: SMART App Launch 2.2.0 - <https://hl7.org/fhir/smart-app-launch/>. SMART Backend Services is part of the same IG.

## 1. SMART App Launch - two launch flows

| Flow | Trigger | Use |
|---|---|---|
| **EHR launch** | Initiated by the EHR (with launch context: patient, encounter, user). | App embedded in EHR chrome. |
| **Standalone launch** | Initiated by the user (e.g., from a member portal). | Member-facing app; no EHR context. |

Both flows produce an OAuth 2.0 access token scoped to FHIR resources.

## 2. Launch flow - step-by-step

### 2.1 EHR launch

1. EHR opens the app's launch URL with `iss` (FHIR base URL) and `launch` (launch token) parameters:

   ```
   https://app.example.org/launch?iss=https://ehr.example.org/fhir&launch=abc123
   ```

2. App fetches the SMART configuration at `{iss}/.well-known/smart-configuration`:

   ```json
   {
     "authorization_endpoint": "https://ehr.example.org/oauth/authorize",
     "token_endpoint": "https://ehr.example.org/oauth/token",
     "scopes_supported": ["launch", "patient/*.rs", "user/*.rs", ...],
     "response_types_supported": ["code"],
     "capabilities": ["launch-ehr", "client-public", "context-passthrough-banner", "permission-patient"]
   }
   ```

3. App redirects to `authorization_endpoint` with PKCE challenge:

   ```
   GET /oauth/authorize
     ?response_type=code
     &client_id=app-client-id
     &redirect_uri=https://app.example.org/callback
     &scope=launch openid fhirUser patient/Patient.read patient/Observation.read
     &state=...
     &aud=https://ehr.example.org/fhir
     &launch=abc123
     &code_challenge=...
     &code_challenge_method=S256
   ```

4. EHR authenticates user, returns to redirect URI with `code`:

   ```
   https://app.example.org/callback?code=xyz789&state=...
   ```

5. App exchanges `code` for tokens at `token_endpoint` with PKCE `code_verifier`:

   ```
   POST /oauth/token
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code
   &code=xyz789
   &redirect_uri=https://app.example.org/callback
   &client_id=app-client-id
   &code_verifier=...
   ```

6. Server returns:

   ```json
   {
     "access_token": "...",
     "token_type": "Bearer",
     "expires_in": 3600,
     "refresh_token": "...",
     "scope": "launch openid fhirUser patient/Patient.read patient/Observation.read",
     "id_token": "...",
     "patient": "p-001",
     "encounter": "e-001",
     "fhirContext": [{ "reference": "Coverage/c-001" }]
   }
   ```

7. App uses `access_token` for FHIR calls: `Authorization: Bearer ...`. Launch context (`patient`, `encounter`, `fhirContext`) provided in the token response, not in the access token claims.

### 2.2 Standalone launch

Same as EHR launch except:

- No `launch` parameter.
- App requests launch context via scopes: `launch/patient` (request patient context at consent time).
- The EHR / user picks a patient during the authorization step.

## 3. Scopes - v2 syntax

SMART App Launch 2.x introduces a more expressive scope grammar:

```
[patient|user|system]/[ResourceType|*].[c|r|u|d|s]?param=value&...
```

Where:

- `patient/` - scoped to the launch-context patient.
- `user/` - scoped to whatever the user can see.
- `system/` - system-level (Backend Services only).
- `[ResourceType|*]` - specific resource type or wildcard.
- `[c|r|u|d|s]` - granular permissions: **c**reate, **r**ead, **u**pdate, **d**elete, **s**earch.
- Optional query string: scope-narrowed query criteria.

### 3.1 Examples

| Scope | Meaning |
|---|---|
| `patient/Patient.r` | Read patient resource for launch-context patient. |
| `patient/Observation.rs` | Read and search Observations for launch-context patient. |
| `patient/*.cruds` | All operations on all resources for launch-context patient. |
| `user/Practitioner.r` | Read any Practitioner the user can see. |
| `system/Patient.r` | System-level read of any Patient (Backend Services). |
| `patient/Observation.rs?category=laboratory` | Read / search laboratory Observations only. |
| `launch` | Permission to use the launch protocol. |
| `launch/patient` | Standalone-launch patient selection. |
| `launch/encounter` | Standalone-launch encounter selection. |
| `openid`, `fhirUser`, `profile` | OpenID Connect claims (e.g., `fhirUser` returns a Practitioner / Patient reference identifying the launching user). |
| `offline_access` | Refresh-token issuance. |
| `online_access` | Session-scoped (no refresh token). |

### 3.2 Backwards-compatible v1 scopes

Older syntax: `patient/Observation.read`, `patient/*.write`. SMART 2.x servers typically support both but Inferno v2 tests target the v2 grammar.

## 4. PKCE - required

SMART App Launch 2.x **requires** PKCE for public clients (and recommends it for confidential clients). The flow:

1. App generates a high-entropy `code_verifier`.
2. App computes `code_challenge = BASE64URL(SHA256(code_verifier))`.
3. App sends `code_challenge` + `code_challenge_method=S256` to `/authorize`.
4. App sends `code_verifier` to `/token`.
5. Server verifies hash matches.

This blocks the authorization-code-interception attack on public clients (mobile apps, SPAs).

## 5. `aud` parameter - required

Every authorization request **must** include `aud` set to the FHIR base URL (`iss`). Servers reject requests where `aud` doesn't match. This prevents an authorization-server compromise from issuing tokens for the wrong resource server.

```
&aud=https://ehr.example.org/fhir
```

## 6. Refresh tokens

- App requests `offline_access` scope.
- Server issues `refresh_token` alongside `access_token`.
- App exchanges refresh token for a new access token at `/token`:

  ```
  POST /oauth/token
  Content-Type: application/x-www-form-urlencoded

  grant_type=refresh_token
  &refresh_token=...
  &client_id=app-client-id
  ```

- Refresh tokens may rotate (server returns a new one). Apps must always store the latest.

## 7. SMART Backend Services - system-to-system

For non-interactive, system-level access: payer-to-payer Bulk Data export, analytics pipelines, scheduled extracts.

### 7.1 Flow

1. Client generates an asymmetric key pair (RSA or ECDSA). Public key goes into a **JWKS** (JSON Web Key Set) hosted at a URL the server can fetch.
2. Server is configured with the client's JWKS URL and `client_id`.
3. Client requests access token by signing a JWT (`client_assertion`) with its private key:

   ```
   POST /token
   Content-Type: application/x-www-form-urlencoded

   grant_type=client_credentials
   &scope=system/Patient.r system/Observation.rs
   &client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer
   &client_assertion=eyJhbGciOiJSUzI1NiIs...
   ```

4. JWT claims:

   ```json
   {
     "iss": "client-id",
     "sub": "client-id",
     "aud": "https://server.example.org/token",
     "jti": "random-unique-id",
     "exp": 1234567890
   }
   ```

5. Server fetches client's JWKS, validates JWT signature, issues short-lived access token.

### 7.2 Key rotation

- JWKS includes a `kid` (key id) on each key.
- Rotate by publishing the new key alongside the old one (overlapping window), then remove the old key after the window.
- Client signs new JWTs with the new key (matching `kid` in JWT header).

### 7.3 Scope grammar - `system/*`

`system/Patient.r`, `system/*.r`, `system/Observation.rs?category=laboratory`. No `patient/` or `user/` scoping (no user / launch context).

### 7.4 Backend Services + Bulk Data

The canonical use case. Bulk Data Export `$export` requires Backend Services for cross-organization use. See [`bulk-data-export.md`](bulk-data-export.md).

## 8. Pre-Inferno checklist (high-level)

| Item | Requirement |
|---|---|
| `.well-known/smart-configuration` | Published at `[iss]/.well-known/smart-configuration` with `authorization_endpoint`, `token_endpoint`, `capabilities`, `scopes_supported`. |
| PKCE | `code_challenge` on every authorize, `code_verifier` on token exchange. |
| `aud` | Sent on every authorize, matched to `iss`. |
| Scopes | v2 grammar supported; documented scope set. |
| Launch context | `patient` (and where applicable `encounter`, `fhirContext`) returned in token response. |
| Refresh | `offline_access` issues refresh tokens; rotation handled. |
| `openid` + `fhirUser` | `id_token` carries `fhirUser` claim for user identity. |
| Backend Services | JWKS published; `client_credentials` + JWT assertion accepted. |
| `CapabilityStatement.rest.security.service` | Declares `SMART-on-FHIR` plus OAuth URIs extension. |

See [`templates/smart-app-launch-checklist.md`](../templates/smart-app-launch-checklist.md) for the full pre-Inferno checklist with common Inferno test IDs.

## 9. Worked example - standalone launch with PKCE

> **[synthetic]** A member-facing patient-access app (Medicare Advantage member portal companion) using SMART App Launch standalone:

1. App generates `code_verifier`, computes `code_challenge`.
2. Redirect to:

   ```
   https://payer.example.org/oauth/authorize
     ?response_type=code
     &client_id=member-app
     &redirect_uri=https://member-app.example.org/callback
     &scope=launch/patient openid fhirUser offline_access patient/Patient.r patient/ExplanationOfBenefit.rs patient/Coverage.r patient/Observation.rs
     &state=opaque-csrf-token
     &aud=https://payer.example.org/fhir
     &code_challenge=...
     &code_challenge_method=S256
   ```

3. Payer authenticates the member; member consents to scopes; payer redirects with `code`.
4. App exchanges `code` + `code_verifier` for token; receives `patient = m-001` in the token response.
5. App calls `GET https://payer.example.org/fhir/ExplanationOfBenefit?patient=m-001` with `Authorization: Bearer ...`.

## 10. Pitfalls (cross-reference)

See [`common-pitfalls.md`](common-pitfalls.md) for:

- Missing `aud` (server rejects, hard to debug)
- Public client without PKCE (Inferno fails, also a real security gap)
- Hardcoding `authorization_endpoint` / `token_endpoint` instead of reading `.well-known/smart-configuration` (breaks across deployments)
- Storing refresh tokens insecurely on mobile devices (use OS keystore)
- Backend Services JWT with `exp` too far in the future (server rejects)
- JWKS without `kid` (rotation impossible)
- Mixing `patient/` scopes with `system/` scopes (different flows)
- Assuming launch context is in the access token JWT (it's in the token *response* body)

## 11. Related references

- Bulk Data `$export` (requires Backend Services) → [`bulk-data-export.md`](bulk-data-export.md)
- `CapabilityStatement.rest.security` shape → [`profiles-and-conformance.md`](profiles-and-conformance.md) §6
- Inferno SMART App Launch + Backend Services kits → [`conformance-testing.md`](conformance-testing.md)
- SMART App Launch IG → <https://hl7.org/fhir/smart-app-launch/>
