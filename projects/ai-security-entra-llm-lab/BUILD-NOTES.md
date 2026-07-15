# How I Built the AI Security Lab

## Purpose

I built this lab to connect my identity and access management background with practical AI security work. The project shows how an organization could place a security gateway in front of a generative AI service and enforce identity, least privilege, prompt inspection, data protection, and audit logging before and after each model request.

The lab has two operating modes:

- **Local demo mode:** runs without an Azure subscription or paid AI model.
- **Azure mode:** is designed to use Microsoft Entra ID, App Service Authentication, managed identity, and Azure OpenAI.

## What the Lab Does

The application exposes a small FastAPI service with two endpoints:

- `GET /health` confirms the service is running.
- `POST /chat` accepts a security-learning prompt after applying access and content controls.

Every chat request follows this sequence:

```text
1. Confirm an identity is present
2. Confirm the identity has the AI-Lab-Users role
3. Inspect the prompt for injection or secret-exfiltration language
4. Inspect the prompt for sensitive data
5. Block unsafe requests before the model is called
6. Send allowed requests to the selected model provider
7. Redact sensitive data from the model response
8. Write a privacy-safe JSON security event
9. Return the sanitized response
```

## How I Built It

### 1. Started With a Threat Model

I first identified the risks the lab needed to address:

| Risk | Security Decision |
| --- | --- |
| Unauthorized users call the AI service | Require an identity and application role |
| Application stores an Azure API key | Use Microsoft Entra managed identity |
| Application identity has excessive permissions | Assign an inference-only role at resource scope |
| User tries to override system instructions | Inspect and block common prompt-injection patterns |
| User asks the model to reveal credentials | Detect secret-exfiltration requests |
| User submits sensitive data | Detect and block selected data patterns |
| Model returns sensitive data | Redact selected patterns before returning output |
| Logs expose prompts or personal data | Store hashes and metadata instead of raw content |

This threat model determined the project structure and test cases.

### 2. Created the FastAPI Gateway

I used FastAPI because it provides:

- Request validation
- Dependency-based authentication checks
- Clear HTTP status codes
- Automatic interactive API documentation
- A small amount of code for a working API

The main API is in `src/secure_ai_lab/main.py`. The `ChatRequest` model limits prompts to 2,000 characters. The `/chat` route runs identity checks, input inspection, provider selection, output redaction, and security logging.

### 3. Added Identity and Role Checks

Identity handling is in `src/secure_ai_lab/auth.py`.

In local demo mode, the app requires:

```text
X-Demo-User
X-Demo-Roles
```

The user must have the `AI-Lab-Users` role. A missing user returns HTTP 401, and a missing role returns HTTP 403.

These headers are intentionally labeled as demo controls. They are not presented as production authentication.

In Azure mode, the lab is designed to sit behind Azure App Service Authentication. The application reads the platform-created `X-MS-CLIENT-PRINCIPAL` value, extracts the user identifier and application roles, and applies the same `AI-Lab-Users` role check.

The application refuses to start in `entra_proxy` mode unless `WEBSITE_AUTH_ENABLED=True`. This reduces the chance of accidentally enabling proxy-header trust without the expected platform authentication.

### 4. Designed Passwordless Azure OpenAI Access

The Azure provider is in `src/secure_ai_lab/providers.py`.

Instead of reading an Azure OpenAI API key, it uses:

- `DefaultAzureCredential`
- `get_bearer_token_provider`
- The Azure AI token scope
- The OpenAI Python client

The intended Azure identity is the system-assigned managed identity of the App Service.

The identity should receive only:

```text
Cognitive Services OpenAI User
```

The role should be scoped to the specific Azure OpenAI resource. The application identity should not receive Owner, Contributor, or deployment-management permissions.

This design connects IAM principles to AI security:

- Passwordless authentication
- Workload identity
- Resource-scoped RBAC
- Least privilege
- No committed API secrets

### 5. Added a Provider Abstraction

The `LLMProvider` protocol allows the security gateway to use different model backends without changing the request-security workflow.

The lab includes:

- `LocalDemoProvider`, which returns a deterministic message and costs nothing.
- `AzureOpenAIProvider`, which is ready for managed-identity access after Azure resources are configured.

This separation also makes testing safer because the automated tests never call a live model.

### 6. Built Input Guardrails

Input controls are in `src/secure_ai_lab/security.py`.

The lab detects selected examples of:

- Requests to ignore or override previous instructions
- Requests to reveal system or developer prompts
- Jailbreak language
- Requests to expose API keys, passwords, tokens, or private keys
- Social Security numbers
- Credit-card-like number patterns
- Bearer tokens
- Private keys
- API-key-style values

If a category is detected, the request is blocked before reaching the model provider.

The code returns detection categories such as:

```text
prompt_injection
secret_exfiltration
sensitive_input:ssn
```

Pattern matching is only one defensive layer. The documentation clearly states that it cannot stop every prompt-injection technique.

### 7. Built Output Redaction

The same security module inspects model output before it is returned.

Selected values are replaced with labels such as:

```text
[REDACTED_EMAIL]
[REDACTED_SSN]
[REDACTED_TOKEN]
[REDACTED_SECRET]
[REDACTED_PRIVATE_KEY]
```

This demonstrates a basic data-loss-prevention control. A production system would need organization-specific data classifiers, monitoring, and human review.

### 8. Created Privacy-Safe Audit Logging

Logging is implemented in `src/secure_ai_lab/audit.py`.

The lab records:

- UTC timestamp
- Request ID
- Event type
- Allow or block decision
- Detection categories
- Hashed actor identifier
- SHA-256 prompt fingerprint
- Prompt length

The logger does not store:

- Raw prompts
- Raw model responses
- Tokens
- Passwords
- Personal identifiers

The prompt fingerprint can help correlate repeated content without placing the original prompt in the log.

### 9. Added Configuration Validation

Environment settings are loaded and validated in `src/secure_ai_lab/config.py`.

The app checks:

- Authentication mode is `demo` or `entra_proxy`.
- Provider is `local` or `azure`.
- Entra proxy mode is not used unless App Service Authentication is enabled.
- Azure mode has a base URL and deployment name.
- The Azure base URL uses the expected `/openai/v1/` path.

The `.env.example` file documents settings without containing credentials.

### 10. Added Automated Security Tests

I created tests for both the API and the guardrail functions.

The test suite verifies:

- Health endpoint availability
- Authentication is required
- The approved role is required
- A normal prompt is allowed
- A prompt-injection attempt is blocked
- A secret-exfiltration request is blocked
- Sensitive input is blocked
- Sensitive output is redacted
- Raw prompt text is absent from audit logs

The completed suite contains 11 passing tests.

### 11. Added Container and CI Controls

The Dockerfile:

- Uses a small Python base image
- Prevents Python bytecode files
- Runs the application as a non-root user
- Installs only runtime dependencies
- Exposes only the application port

The GitHub Actions workflow:

- Runs only when the lab or workflow changes
- Uses read-only repository permissions
- Installs the development dependencies
- Runs the complete test suite on Python 3.12

The final GitHub Actions run passed successfully.

## Local Validation Performed

I validated the project in four ways:

1. Compiled the Python source.
2. Ran all 11 automated tests.
3. Started the FastAPI application locally.
4. Sent both an allowed request and a prompt-injection request.

The allowed request reached the local provider. The injection attempt was blocked and labeled `prompt_injection`.

## File Responsibilities

| File | Responsibility |
| --- | --- |
| `main.py` | API routes and request workflow |
| `auth.py` | Demo identity, Entra principal parsing, and role enforcement |
| `security.py` | Input detection and output redaction |
| `audit.py` | Privacy-safe JSON security events |
| `providers.py` | Local and Azure OpenAI model providers |
| `config.py` | Environment settings and startup validation |
| `test_api.py` | API authentication and behavior tests |
| `test_security.py` | Guardrail, redaction, and logging tests |
| `Dockerfile` | Non-root container runtime |
| `ai-security-lab.yml` | GitHub Actions test automation |

## What This Project Demonstrates

This lab demonstrates that I can connect traditional security controls to an AI application:

- IAM and application roles
- Managed identity
- Azure RBAC
- Least privilege
- Secretless cloud authentication
- Prompt-injection defense
- Sensitive-data controls
- Secure audit logging
- Python API development
- Automated security testing
- CI/CD security basics

## Short Interview Explanation

> I built a Python security gateway for a generative AI application. It requires an approved user role, blocks selected prompt-injection and secret-exfiltration attempts, detects sensitive input, redacts sensitive model output, and writes audit logs without storing raw prompts. I also designed an Azure mode that uses Entra managed identity and a resource-scoped inference role instead of an API key. I validated the project with 11 automated tests and a successful GitHub Actions run.

## Next Improvements

- Deploy the application to an Azure test environment.
- Add sanitized screenshots of Entra authentication and the managed-identity role assignment.
- Add rate limiting and centralized monitoring.
- Add indirect prompt-injection test cases for retrieved documents.
- Add a stronger data-classification service.
- Send security events to Microsoft Sentinel.
- Add dependency and container vulnerability scanning.
