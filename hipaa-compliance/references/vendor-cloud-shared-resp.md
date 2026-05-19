# Vendor / Cloud Shared Responsibility

## The model

When a CE or BA uses a cloud provider, SaaS vendor, or AI service to handle ePHI, **both** parties have HIPAA obligations. The cloud provider is generally a BA (or subcontractor BA) and must sign a BAA. The CE/BA retains responsibility for configuration and use of the service.

This is the **shared responsibility model**:

| Provider responsibility | Customer responsibility |
|---|---|
| Physical security of data centers | Application architecture |
| Hypervisor and host security | OS hardening (IaaS) |
| Network infrastructure | Network configuration (VPC, subnets, security groups) |
| Hardware integrity | IAM design, key management policies |
| Service-level controls per the BAA | Workload configuration, encryption choice, logging |
| Eligible service list maintenance | **Using only eligible services for ePHI** |

> The single most common failure: assuming "we're on AWS / Azure / GCP, so we're HIPAA-compliant." The provider's BAA covers an **eligible-services** list - if a workload uses a service **not** on that list, the BAA does not cover it.

## Cloud provider BAAs - eligible services

Each major cloud provider publishes an eligible-services list and a BAA. The lists change. **Always verify against the current published list** before architecting an ePHI workload. The lists below are illustrative of what to look for, not authoritative.

### AWS

- Signs a BAA covering AWS HIPAA-eligible services (commonly includes EC2, S3, EBS, RDS, DynamoDB, Lambda, KMS, CloudTrail, Bedrock for certain models, and many others; the full list is published and updated)
- Customer responsibilities include: encryption configuration (KMS), IAM design, VPC isolation, logging via CloudTrail + CloudWatch + log-store encryption, S3 bucket policies, public-access blocks
- Common failure: using a service not on the list (some analytics services, some AI services, some preview-stage services)

### Azure

- Signs a BAA via the Microsoft Online Services Data Protection Addendum (DPA) which incorporates HIPAA terms
- Covers most production-grade services; Azure publishes the in-scope list
- Azure OpenAI is BAA-covered subject to the standard service-specific conditions; verify retention, abuse-monitoring, and human-review settings before sending ePHI
- Customer responsibilities mirror AWS structure

### GCP

- Signs a BAA covering Google Cloud HIPAA-included services
- Vertex AI and certain Cloud AI services included subject to configuration
- Workspace (Gmail, Drive, etc.) BAA available but separate; verify the contract you signed covers the surface in use

### Cross-provider notes

- **AI / ML services** are the highest-risk category for "BAA-covered or not" because they evolve fast and have model-specific carve-outs (training, fine-tuning, abuse monitoring, human review)
- **Preview / beta** services are typically **not** BAA-covered
- **Cross-region** deployments may pull in services from regions with different coverage
- **Marketplace** third-party offerings are not covered by the platform BAA - separate BAA required with the marketplace seller

## SaaS vendors

For any SaaS that touches ePHI (CRM with patient names, ticketing system with PHI in attachments, support chat, email service, analytics, monitoring, error tracking, log aggregator):

- BAA required before sending ePHI
- BAA must cover all subcontractors used by the SaaS (subcontractor flow-down per [`baa-review.md`](baa-review.md))
- Encryption at rest + in transit configured
- Audit logging available for export
- Access controls support SSO + RBAC + MFA + termination automation
- Data residency aligned with internal requirements
- Termination clause includes return / destruction of ePHI

### High-risk SaaS categories to inventory

- Email and calendaring (especially if attachments contain PHI)
- Helpdesk / ticketing (free-text fields collect PHI from users)
- CRM (patient outreach often carries PHI)
- Marketing automation (segmentation may pull from clinical attributes)
- Web analytics and tag managers (see web tracking pixels - active OCR enforcement)
- Session replay and customer-experience tools
- Error tracking and APM (request/response bodies often capture PHI)
- Logging and SIEM (logs are ePHI)
- Backup and DR
- Communication (chat, video, voice, fax over IP, secure messaging)
- File sharing and collaboration
- AI / ML platforms

## AI services - specific guidance

Active and unsettled area. As of writing:

| Provider / service | BAA available? | Key conditions to verify |
|---|---|---|
| AWS Bedrock | Generally yes for HIPAA-eligible models | Per-model coverage; logging settings; abuse-monitoring opt-out where applicable |
| Azure OpenAI | Yes via Microsoft DPA | Abuse monitoring + human review settings; managed-key vs platform-managed-key; data residency |
| Google Vertex AI | Yes for in-scope services | Per-service coverage; logging; training opt-out |
| OpenAI (direct API) | BAA available with eligible plan | Verify which models / endpoints are covered; data retention; zero-retention option |
| Anthropic (direct API) | BAA available on request | Verify retention + abuse monitoring posture |
| Open-source models self-hosted | No external BAA needed (you're the operator) | Your own Security Rule program covers the deployment |
| Consumer chatbots (ChatGPT consumer, Claude.ai consumer, Gemini consumer) | **No BAA, do not use with ePHI** | Always |

**Always verify the BAA against the current product offering.** Vendor pages, pricing tiers, and model lists change. Get it in writing for the specific endpoints and models you'll use.

### AI service configuration checklist for ePHI

- BAA in place and covers the specific endpoint / model / region in use
- Logging / retention disabled or contractually constrained (vendors commonly default to 30-day retention for safety/abuse monitoring - opt out where the BAA allows)
- Human-review / abuse-monitoring carve-out where the BAA allows
- Training on customer data disabled (most BAA-covered services already do this by default)
- Inference traffic encrypted in transit (TLS 1.2+)
- Inputs and outputs encrypted at rest in your environment
- Prompts minimized to the necessary fields (minimum necessary)
- Output review for PHI leakage (model may return unintended record)
- Per-user attribution in your application logs (not the model's)
- Rate limiting + anomaly detection on the integration

## On-prem and hybrid

- The cloud BAA does not cover on-prem components - your own Security Rule program does
- Hybrid pipelines must trace ePHI flow end-to-end and identify which leg is covered by which BAA
- Direct-connect / private-link between on-prem and cloud is still in scope for transmission security

## Vendor risk assessment

Before onboarding any vendor that will touch ePHI:

1. **BAA**: signed, covers all subcontractors, breach notification ≤ 5 business days (or faster per CE policy)
2. **Independent attestation**: SOC 2 Type II + (HITRUST or ISO 27001 + HIPAA mapping); review the most recent report and exceptions
3. **Encryption**: at rest + in transit, FIPS-validated; documented key custody
4. **Access**: SSO / SAML / OIDC, MFA, audit log export
5. **Incident response**: documented, tested, includes breach notification protocol
6. **Data residency**: US-only or per CE policy; no transfer outside permitted regions
7. **Subcontractors**: list available; flow-down BAA in place
8. **Data return / destruction**: contractual on termination; certificate of destruction
9. **Use of ePHI for vendor purposes**: explicitly prohibited or contractually constrained (training, analytics, product improvement)
10. **Insurance**: cyber liability + tech E&O at appropriate limits

## Common engineering pitfalls

- "AWS / Azure / GCP signed a BAA so we're compliant" - the BAA covers eligible services + customer-correct configuration
- Using a non-eligible service for an ePHI workload
- AI service onboarded without BAA, or with default retention left on
- Marketplace / third-party plugin treated as covered by the platform BAA
- Tracking pixel / analytics tag on a patient-facing page without BAA with the analytics vendor
- Cross-region deployment that pulls in a region with different coverage
- Vendor risk review done at procurement but never re-run when the vendor adds AI features or changes ownership
- BAA with the vendor but no BAA with the vendor's sub-processors (flow-down failure)

## Defer to security officer + privacy officer + counsel when

- Onboarding any new vendor with ePHI access
- Adopting any new AI service for an ePHI workload
- Changing region, sub-processor, or storage location for an existing ePHI workload
- Vendor refuses standard BAA terms
- Vendor reports a security incident affecting ePHI
- Vendor is acquired or changes ownership
