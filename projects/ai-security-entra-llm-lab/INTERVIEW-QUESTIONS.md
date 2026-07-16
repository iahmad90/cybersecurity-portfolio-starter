# AI Security Lab Interview Questions and Answers

## 30-Second Project Introduction

> I built a Python security gateway for a generative AI application. It requires an approved user role, blocks selected prompt-injection and secret-exfiltration attempts, detects sensitive input, redacts sensitive output, and creates audit events without storing raw prompts. I also designed an Azure mode that uses Microsoft Entra managed identity and resource-scoped RBAC instead of an API key. The project has 11 automated tests and a passing GitHub Actions workflow.

## Core Project Questions

### 1. Tell me about your AI security lab.

**Sample answer:**
I built a FastAPI gateway that applies security controls before and after an AI model request. It checks identity and role membership, inspects prompts for injection or sensitive data, blocks unsafe requests, redacts selected sensitive values from output, and writes privacy-safe audit events. It runs locally with a demo provider and includes an Azure OpenAI design using Entra managed identity.

### 2. What problem were you trying to solve?

**Sample answer:**
I wanted to show how traditional controls such as IAM, least privilege, data-loss prevention, and logging apply to generative AI. A model should not be called directly without controls around who can use it, what data can be submitted, what output can be returned, and what activity is recorded.

### 3. Walk me through one request from start to finish.

**Sample answer:**
The API confirms a user identity, checks for the `AI-Lab-Users` role, validates the request, scans the prompt, and blocks it if a risk is detected. Allowed prompts go to the selected provider. The response is scanned for sensitive values, redacted if needed, logged without raw content, and returned with a request ID and security categories.

### 4. Why did you use FastAPI?

**Sample answer:**
FastAPI provides strong request validation, dependency-based access checks, automatic API documentation, and clear HTTP behavior with relatively little code. It was a good fit for a small security gateway that needed to be easy to test and demonstrate.

### 5. Why did you separate the provider from the security gateway?

**Sample answer:**
The provider abstraction keeps model access separate from security decisions. The same identity, inspection, redaction, and logging workflow can protect a local provider or Azure OpenAI. It also lets the tests run without calling a paid or external model.

## Identity and Azure Questions

### 6. How does authentication work in local mode?

**Sample answer:**
Local mode requires explicit demo headers for the user and roles. The names make it clear that this is not production authentication. A missing user returns 401, and a user without the required role receives 403.

### 7. What is the difference between HTTP 401 and 403?

**Sample answer:**
401 means the request does not have a valid authenticated identity. 403 means the identity is known but does not have permission to perform the action.

### 8. How would authentication work in Azure?

**Sample answer:**
I would enable Microsoft Entra authentication on Azure App Service and require sign-in. App Service would validate the identity and provide the principal claims to the application. The gateway would then enforce the `AI-Lab-Users` application role.

### 9. Why use managed identity instead of an API key?

**Sample answer:**
Managed identity avoids storing or rotating a long-lived application secret. Azure issues short-lived tokens to the workload, and access is controlled through RBAC. This reduces the risk of keys being committed, copied, or exposed in configuration.

### 10. Which Azure role would you assign to the application?

**Sample answer:**
I would assign `Cognitive Services OpenAI User` to the App Service managed identity at the specific Azure OpenAI resource scope. I would not give the application Owner, Contributor, or deployment-management permissions.

### 11. How does this project demonstrate least privilege?

**Sample answer:**
Users need a specific application role, and the workload identity receives only inference access to one AI resource. The design separates user authorization from workload authorization and avoids broad Azure roles.

## AI Security Questions

### 12. What is prompt injection?

**Sample answer:**
Prompt injection is an attempt to manipulate a model into ignoring its intended rules or performing an unauthorized action. An example is asking it to disregard previous instructions and reveal hidden system content.

### 13. How does your lab detect prompt injection?

**Sample answer:**
The input guard checks for selected phrases involving instruction override, hidden-prompt disclosure, jailbreak language, and secret exfiltration. If detected, the request is blocked before the provider is called and the event is logged with a category.

### 14. Can regular expressions stop every prompt injection?

**Sample answer:**
No. Pattern matching is a useful demonstration and one defensive layer, but attackers can use indirect, encoded, multilingual, or novel instructions. A production system needs layered controls, restricted tools, data boundaries, monitoring, testing, and human review.

### 15. What is indirect prompt injection?

**Sample answer:**
Indirect prompt injection comes from content the model retrieves or processes, such as a webpage, email, document, or database record. The malicious instruction is inside the external content rather than typed directly by the user.

### 16. How would you improve the prompt-injection defense?

**Sample answer:**
I would add structured input separation, an allowlist of permitted actions, tool-level authorization, retrieval-content labeling, rate limits, stronger classifiers, indirect-injection tests, output validation, and monitoring for repeated attack patterns.

## Data Protection and Logging Questions

### 17. How does the lab protect sensitive data?

**Sample answer:**
It blocks selected sensitive patterns in input, including SSNs, bearer tokens, private keys, and API-key-style values. It also scans output and replaces selected values with redaction labels before returning the response.

### 18. Why inspect both input and output?

**Sample answer:**
Input inspection reduces the chance of sending sensitive data to the model. Output inspection reduces the chance of returning data that the model or a connected source exposed. Both directions are important for data-loss prevention.

### 19. What information is written to the audit log?

**Sample answer:**
The log contains a timestamp, request ID, event type, decision, detection categories, hashed actor identifier, prompt fingerprint, and prompt length. It does not contain the raw prompt or raw response.

### 20. Why hash the actor and prompt?

**Sample answer:**
Hashing allows repeated actors or prompt content to be correlated without placing the original values in the log. It reduces exposure, although hashes still require protection because predictable values may sometimes be guessed.

### 21. What would you send to Microsoft Sentinel?

**Sample answer:**
I would send allow and block decisions, user and workload identifiers in an approved format, request IDs, detection categories, source information, latency, model deployment, and error events. I would create alerts for repeated injection attempts, unusual volume, or sensitive-data detections.

## Testing and Engineering Questions

### 22. What did you test?

**Sample answer:**
I tested the health endpoint, missing identity, missing role, normal prompts, direct prompt injection, secret exfiltration, sensitive input, output redaction, and the requirement that raw prompt text never appears in audit logs.

### 23. Why are automated tests important for security controls?

**Sample answer:**
Security controls can break during ordinary code changes. Automated tests verify that known attacks remain blocked, approved requests still work, and sensitive information is not accidentally added to logs.

### 24. What does the GitHub Actions workflow do?

**Sample answer:**
It checks out the repository, sets up Python, installs the lab dependencies, and runs the complete test suite when the lab changes. The workflow has read-only repository permissions.

### 25. What security choices are in the Dockerfile?

**Sample answer:**
The container uses a small Python image, avoids bytecode and unnecessary cache files, installs only runtime dependencies, and runs the API as a non-root user.

## Limitations and Scenario Questions

### 26. What is the biggest limitation of the current lab?

**Sample answer:**
The local version demonstrates controls but does not use real Entra authentication or a live model. Its pattern-based detection is also limited. The next major step is an Azure test deployment with real managed identity, sanitized evidence, and stronger monitoring.

### 27. What could happen if someone bypassed App Service Authentication?

**Sample answer:**
If the application trusted identity headers on a direct unprotected network path, an attacker might spoof those headers. I would restrict direct access, use the supported Azure authentication architecture, validate the deployment, and test that unauthenticated paths are closed.

### 28. A legitimate request is blocked. What would you do?

**Sample answer:**
I would use the request ID and detection category to investigate without exposing raw data. I would reproduce the request with safe test content, identify the rule that caused the false positive, adjust it carefully, and add a regression test.

### 29. A user repeatedly triggers prompt-injection alerts. What would you do?

**Sample answer:**
I would correlate the actor hash, request IDs, timing, categories, source, and volume. I would determine whether it is testing, misuse, or compromise, apply rate or access controls if needed, preserve approved evidence, and escalate according to the incident process.

### 30. What would you build next?

**Sample answer:**
I would deploy it to an Azure test environment, add Entra app-role evidence, send events to Sentinel, add rate limiting, test indirect prompt injection, add dependency and container scanning, and create an incident-response playbook.

## Live Demo Script

1. Open the FastAPI documentation at `/docs`.
2. Show the `/health` endpoint.
3. Send a normal request with the approved demo role.
4. Point out the allowed response and request ID.
5. Send an instruction-override prompt.
6. Show that the request is blocked as `prompt_injection`.
7. Show the audit event contains a fingerprint, not the raw prompt.
8. Open the automated tests and explain the main scenarios.
9. Explain how local demo headers would be replaced by Entra authentication.
10. End with the managed-identity and least-privilege design.

## Rapid-Fire Practice Questions

- What is the difference between authentication and authorization?
- What is a workload identity?
- Why should an AI model response be treated as untrusted input?
- What is the purpose of a request ID?
- Why is raw prompt logging risky?
- How would rate limiting improve this project?
- What is the difference between direct and indirect prompt injection?
- Why use resource-level role scope?
- How would you investigate a false positive?
- Which evidence would you capture without exposing secrets?

## Practice Guidance

- Keep the project introduction under 30 seconds.
- Use one clear example for each control.
- Be honest that the local headers are a demonstration.
- Do not claim pattern matching solves prompt injection.
- Connect every technical choice to risk reduction.
- Emphasize Entra ID, managed identity, RBAC, testing, and logging because these connect directly to IAM and cloud-security roles.
