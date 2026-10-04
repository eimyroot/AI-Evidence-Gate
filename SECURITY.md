# Security Policy

## Reporting

Do not disclose vulnerabilities through public issues. Report them privately to the repository owner with the affected component, reproduction steps, expected impact, and a minimal proof where appropriate. Do not include provider secrets or sensitive production data.

## Security expectations

- secrets and model-provider credentials must not be committed;
- untrusted evaluation inputs, model outputs, URLs, and artifacts must be validated at trust boundaries;
- release gates must fail closed when required evidence is missing or invalid;
- evidence must not be silently promoted to authority beyond its defined scope;
- dependencies should be updated deliberately and reviewed for impact;
- security-sensitive and release-sensitive changes should include tests where practical.

The latest default-branch state is the maintained development version unless a release says otherwise.
