# Natalyx

**A clearer way to navigate fertility journeys.**

Natalyx is building a unified platform for assisted reproductive technology (ART) journeys; helping intended parents, gestational carriers, donors, clinics, and partners move through complex fertility pathways with more structure, transparency, and support.

Fertility care is often fragmented across agencies, clinics, donor banks, legal teams, coordinators, and spreadsheets. Natalyx brings more of that journey into one coordinated digital experience: education, intake, routing, profile workflows, partner coordination, and structured support from early exploration through later-stage journey management.

We are currently building in private.

---

## What we’re building

Natalyx combines marketplace infrastructure, journey management, and decision-support tools for modern fertility care.

Our platform is designed to support:

- **Intended parents** exploring IVF, donor conception, surrogacy, or combined pathways.
- **Gestational carrier applicants** moving through education, intake, screening, and matching readiness.
- **Egg and sperm donor pathways** where users need clearer discovery, comparison, and coordination.
- **Clinics and partner networks** that need cleaner intake, better routing, and more structured handoffs.
- **Internal teams and coordinators** managing complex, multi-party journeys with less operational drag.

**Natalyx is not a replacement for clinicians, lawyers, agencies, or licensed care teams.** It is the coordination and orchestration layer that helps people understand where they are, what may come next, and which support pathway is most appropriate.

---

## Natalyx Intelligence

Natalyx Intelligence is the guidance and decision-support layer behind the product. It is designed to make fertility journeys feel less opaque, less fragmented, and less procedural.

In the target AWS architecture, Natalyx Intelligence runs as a private backend service. The public app calls it across an internal service boundary; it is not directly exposed to the internet.

Current intelligence work includes:

### Pathfinder

A softer onboarding and triage experience that helps users explain what they are trying to do, understand which pathway may fit, and move toward the right next step without starting from a rigid form.

### Signals

Lightweight, contextual guidance embedded inside forms, profiles, and workflows. Signals help surface possible issues, missing information, timing conflicts, or jurisdictional considerations without interrupting the user’s flow.

### Ask Natalyx

A conversational support layer for questions, clarification, and sensemaking. Ask Natalyx is designed to provide guidance grounded in the user’s context while keeping clear boundaries around uncertainty, consent, and escalation.

### Match Insights

A structured compatibility and explanation layer for matching workflows. Rather than treating matching as a black box, Match Insights helps surface areas of alignment, possible friction, unknowns, and useful follow-ups.

Match Insights is decision support only. It does not approve, reject, rank, clear, or finalize a match.

---

## Platform architecture

Natalyx is organized around three core repositories:

### `natalyx-app`

The public product surface. This repo owns authenticated user and developer workflows, core product UI, application routing, app persistence calls, app-to-intelligence service calls, and public-facing product behavior.

It should not own AWS account-level infrastructure, model provider implementation details, or prompt orchestration logic.

### `natalyx-intelligence`

The private intelligence service. This repo owns Pathfinder service logic, Ask Natalyx service logic, Match Insights orchestration, model orchestration and provider adapters, Bedrock runtime integration, prompt and routing logic, deterministic fallbacks, and safe metadata-only diagnostics.

It should not be publicly reachable.

### `natalyx-infra`

The AWS infrastructure layer. This repo owns AWS accounts and environment configuration, DNS and TLS, Cognito, ECS, ECR, ALB, service networking, RDS PostgreSQL, S3, IAM, KMS, SSM Parameter Store, CloudWatch, CloudTrail, and deployment roles.

Product behavior, prompt logic, and model output policy should remain outside this repo.

---

## AWS dev/demo platform

Natalyx is migrating from a local and Render-oriented development posture toward a secure AWS dev/demo platform.

The current target architecture is:

```text
Dev/demo user
    |
    v
Cognito app login
    |
    v
HTTPS ALB: dev.app.natalyx.health
    |
    v
natalyx-app ECS service
    |\
    | v
    | RDS PostgreSQL
    v
private natalyx-intelligence ECS service
    |
    v
Amazon Bedrock
```

Core platform rules:

- Only `natalyx-app` is public.
- `natalyx-intelligence` is private and callable only from the app service boundary.
- Cognito gates the dev/demo site.
- RDS PostgreSQL is the cloud persistence layer for core flows.
- Amazon Bedrock is the AWS runtime LLM boundary.
- Deterministic fallback remains mandatory.
- Render relay and direct OpenAI paths may remain for local, legacy, or explicit debug use, but they are not part of the AWS PHI-adjacent runtime path.

---

## Data and safety posture

Natalyx is currently synthetic-data only in dev/demo environments.

Real PHI must remain disabled until the PHI readiness gate is complete and explicitly accepted. PHI activation should be fail-closed and should depend on verified infrastructure, logging, service eligibility, access-control, retention, vendor, and audit requirements.

AI outputs are advisory. Natalyx Intelligence may suggest, summarize, explain, retrieve approved guidance, ask follow-up questions, or flag issues, but it must not:

- Provide medical or legal advice.
- Approve or reject users.
- Gate eligibility.
- Finalize participant facts.
- Finalize matches.
- Override worker-confirmed data.
- Invent unsupported product pathways.
- Write sensitive free text, prompts, generated outputs, uploads, or PHI-bearing payloads to logs.

Human boundaries, escalation paths, consent, and reviewed records remain central to the product.

---

## Product principles

We build around a few core beliefs:

- **Clarity over complexity.** Fertility journeys are already hard; the product should make them feel more legible.
- **Support over self-service chaos.** Users should feel guided, not abandoned inside a marketplace.
- **Structure over guesswork.** Important decisions should be supported by clean data, transparent reasoning, and consistent workflows.
- **Human boundaries matter.** Sensitive journeys require consent, escalation paths, and careful language.
- **Marketplace design should protect people.** Matching and routing systems need to account for readiness, safety, fit, and trust.
- **AI should support judgment, not replace it.** Intelligence features should explain, guide, and surface context without becoming the final authority.

---

## Repositories

This organization contains the core platform, intelligence, infrastructure, and supporting tools used to build Natalyx.

Some repositories are private while the product is in development.

Key areas of work include:

- Application experience and user-facing workflows.
- Intelligence, routing, and decision-support systems.
- Data structures, journey taxonomies, and curated guidance content.
- Infrastructure, deployment, and operational tooling.
- Internal reviewer and coordination workspaces.

---

## Status

Natalyx is pre-launch and in active product development.

We are currently focused on:

- Building the ART and fertility journey routing experience.
- Expanding the non-surrogacy IVF pathway.
- Developing donor and clinic-network workflows.
- Improving the gestational carrier and intended parent journey experience.
- Making Natalyx Intelligence useful, explainable, and safe from the first interaction.
- Moving the platform toward a Cognito-gated AWS dev/demo environment.
- Establishing the private app-to-intelligence service boundary.
- Running synthetic-data-only dev/demo workflows.
- Using Amazon Bedrock as the AWS runtime LLM boundary.
- Maintaining deterministic fallback behavior when configuration, models, or services fail.

---

## Learn more

Public product materials will be added as Natalyx moves closer to launch.

For now, this organization is home to the systems, tools, and infrastructure behind the Natalyx platform.
