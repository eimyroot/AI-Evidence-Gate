# Coalbrain fit assessment

Independent assessment based on Coalbrain's public product pages as of 2026-09-11. This repository is not affiliated with Coalbrain or coalfamily.

## Why the fit is strong
Coalbrain publicly describes a portfolio spanning AI opportunity analysis, document/order automation, meeting intelligence, shift planning and long-term operation/support. Those products share one recurring problem: model/provider/prompt changes must be evaluated against the actual business process before production promotion.

AI Evidence Gate provides that shared layer:

## Lifecycle placement

The strongest fit is not as a replacement for Coalbrain's consulting or delivery work, but as a control layer at the transition from implementation into long-term operation:

```text
AI analysis → team training / adoption → process automation → [ AI EVIDENCE GATE ] → operation & development
                                                        ↑                          │
                                                        └── each model/prompt/agent change ──┘
```

That means two concrete moments of value:

- **Before first production release:** prove that the implemented workflow satisfies process-specific quality and safety gates.
- **During operation and development:** replay the same evidence whenever a model, prompt, provider or agent step changes, so a cheaper/faster candidate cannot silently introduce a regression.

This lifecycle mapping is based on the public four-step delivery framing shown by Coalbrain: opportunity analysis, team enablement, process automation, and ongoing operation/development. It is an independent interpretation, not a statement about Coalbrain's internal architecture.

AI Evidence Gate provides that shared layer:

- use-case-specific golden and regression datasets
- quality, safety, latency and cost metrics
- human escalation and unsafe-action measurement
- hard security gates
- release receipts and audit history
- cloud/on-prem/hybrid deployment metadata

Public references used: https://coalbrain.cz/, https://coalbrain.cz/ai-analyza-prilezitosti/, https://coalbrain.cz/ai-zpracovani-dokladu/, https://coalbrain.cz/ai-zamestnanci/, https://coalbrain.cz/coalshift/
## Product-by-product mapping
- Document processing / AI Fakturant: critical-field extraction, schema compliance, prompt-injection tests, double-check disagreements and human review.
- Logistics order automation: agent tool ordering, approval-before-ERP hard gates, recovery/escalation and regression promotion.
- AI Zapisovatel: decisions, tasks, owners, deadlines, fabricated-task rate and abstention quality.
- Coalshift: legal-rest, qualification and availability hard constraints plus fairness/overtime soft metrics.
- AI opportunity analysis: measured pilot evidence can be attached to a prioritised roadmap and ROI assumptions.

## Important gaps before client production
This MVP is strong enough as a portfolio and internal pilot scaffold. It is not yet a drop-in certified client platform. Production work still needs client-specific data contracts, ERP/HR adapters, SSO/RBAC, tenant isolation, secrets management, retention policies, observability and deployment hardening.

## Recommended Coalbrain positioning
Pitch the product as an internal quality/release layer that can serve multiple Coalbrain products, not as a claim that Coalbrain currently lacks evaluation. The right discovery question is: “How do you validate model, prompt and agent changes against real client workflows today?”
