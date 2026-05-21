# CapabilityStatement skeleton

> Starter skeleton for a server `CapabilityStatement`. Replace `{{...}}`. Publish at `[base]/metadata`. Pin every IG version. Declare every search param + combination per the relevant IG.
>
> All example payloads, identifiers, and URLs are `[synthetic]` placeholders.

---

```json
{
  "resourceType": "CapabilityStatement",
  "id": "{{server-id}}",
  "url": "{{`http://example.org/CapabilityStatement/server`}}",
  "version": "{{semver}}",
  "name": "{{ServerName}}",
  "title": "{{Human-friendly title}}",
  "status": "active",
  "experimental": false,
  "date": "{{YYYY-MM-DD}}",
  "publisher": "{{org}}",
  "kind": "instance",
  "instantiates": [
    "{{e.g., http://hl7.org/fhir/us/core/CapabilityStatement/us-core-server|6.1.0}}"
  ],
  "implementation": {
    "description": "{{description}}",
    "url": "{{base FHIR URL}}"
  },
  "fhirVersion": "{{4.0.1 | 4.3.0 | 5.0.0}}",
  "format": ["application/fhir+json", "application/fhir+xml"],
  "implementationGuide": [
    "{{e.g., http://hl7.org/fhir/us/core/ImplementationGuide/hl7.fhir.us.core|6.1.0}}",
    "{{e.g., http://hl7.org/fhir/us/carin-bb/ImplementationGuide/hl7.fhir.us.carin-bb|2.1.0}}"
  ],
  "rest": [
    {
      "mode": "server",
      "security": {
        "service": [
          {
            "coding": [
              { "system": "http://terminology.hl7.org/CodeSystem/restful-security-service", "code": "SMART-on-FHIR" }
            ]
          }
        ],
        "extension": [
          {
            "url": "http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris",
            "extension": [
              { "url": "authorize", "valueUri": "{{authorize endpoint}}" },
              { "url": "token", "valueUri": "{{token endpoint}}" },
              { "url": "register", "valueUri": "{{register endpoint, if dynamic}}" },
              { "url": "introspect", "valueUri": "{{introspection endpoint, if exposed}}" }
            ]
          }
        ]
      },
      "resource": [
        {
          "type": "Patient",
          "supportedProfile": [
            "{{http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient|6.1.0}}"
          ],
          "interaction": [
            { "code": "read" },
            { "code": "vread" },
            { "code": "search-type" },
            { "code": "create" },
            { "code": "update" }
          ],
          "versioning": "versioned",
          "readHistory": true,
          "updateCreate": false,
          "conditionalCreate": true,
          "conditionalUpdate": false,
          "conditionalDelete": "not-supported",
          "referencePolicy": ["literal"],
          "searchInclude": ["Patient:general-practitioner", "Patient:organization"],
          "searchRevInclude": ["Provenance:target"],
          "searchParam": [
            { "name": "_id", "type": "token" },
            { "name": "_lastUpdated", "type": "date" },
            { "name": "identifier", "type": "token" },
            { "name": "name", "type": "string" },
            { "name": "family", "type": "string" },
            { "name": "given", "type": "string" },
            { "name": "birthdate", "type": "date" },
            { "name": "gender", "type": "token" }
          ],
          "operation": [
            { "name": "validate", "definition": "http://hl7.org/fhir/OperationDefinition/Resource-validate" },
            { "name": "everything", "definition": "http://hl7.org/fhir/OperationDefinition/Patient-everything" }
          ]
        },
        {
          "type": "{{Resource}}",
          "supportedProfile": [
            "{{profile canonical URL with version pin}}"
          ],
          "interaction": [ { "code": "read" }, { "code": "search-type" } ],
          "searchParam": [
            { "name": "{{param}}", "type": "{{type}}" }
          ],
          "operation": []
        }
      ],
      "interaction": [
        { "code": "transaction" },
        { "code": "batch" },
        { "code": "search-system" }
      ],
      "operation": [
        { "name": "export", "definition": "http://hl7.org/fhir/uv/bulkdata/OperationDefinition/export|2.0.0" }
      ]
    }
  ]
}
```

## Required customizations per IG

### US Core (per version)

- Declare `supportedProfile` for every US Core profile the server exposes.
- Declare every required search param + combination per resource (see [`us-core-ig.md`](../references/us-core-ig.md) §6 and per-profile US Core pages).

### CARIN BB

- Declare all five `ExplanationOfBenefit` profile flavors used.
- Declare `patient`, `_lastUpdated`, `type`, `service-date`, `identifier` on `ExplanationOfBenefit`.

### SMART App Launch

- Declare `SMART-on-FHIR` in `security.service`.
- Populate the `oauth-uris` extension with `authorize`, `token`, and optionally `register` / `introspect`.
- Expose `.well-known/smart-configuration` separately per SMART IG.

### Bulk Data

- Declare `$export` operation at system, Patient-type, and Group-instance levels as supported.

## Validation

- Run HAPI Validator CLI against the CapabilityStatement: `java -jar validator_cli.jar capabilitystatement.json -version {{x.y.z}}`.
- Run Inferno discovery against `[base]/metadata` - verifies declared profiles + search params + operations.

## Sign-off

| Role | Name | Date |
|---|---|---|
| Author | {{}} | {{}} |
| FHIR reviewer | {{}} | {{}} |
| Security reviewer | {{}} | {{}} |
