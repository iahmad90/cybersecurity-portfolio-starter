# How I Built the PAM Vault Simulator

## Purpose

I built this lab to turn the Privileged Access Management concepts in my CyberArk Defender PAM studies into a working local project. The simulator demonstrates the lifecycle of a privileged credential: vault storage, authorized checkout, a limited access window, check-in, rotation, and auditing.

## Design Decisions

### 1. Used an In-Memory Vault

The lab stores two fake privileged accounts in memory. Each account contains:

- An account identifier
- A target username
- A mock credential
- A credential version
- A set of actors authorized for the account

This keeps the lab safe and easy to run. No real passwords, cloud resources, or database are required.

### 2. Applied Two Authorization Layers

The API first requires the `PAM-Users` role. The vault then checks whether the actor is allowed to access the specific privileged account.

This models:

- PAM platform access
- Safe or account-level permissions
- Least privilege

The `GET /audit` endpoint requires `PAM-Auditors`, which models separation of duties between credential users and reviewers.

### 3. Created Time-Limited Exclusive Leases

Checkout creates a lease with:

- A unique lease ID
- The privileged account
- The requesting actor
- Checkout time
- Expiration time
- Current status

Only one unexpired lease can exist for an account. A lease can last from 1 second to 1 hour. Check-in is denied when the lease is expired, inactive, or presented by a different actor.

### 4. Rotated the Credential After Check-In

A successful check-in:

1. Generates a new mock secret.
2. Replaces the old mock secret.
3. Increments the credential version.
4. Marks the lease as checked in.
5. Writes a successful audit event.

This models the purpose of CyberArk Central Policy Manager rotation without connecting to a real target system.

### 5. Logged Security Decisions

The audit trail records:

- UTC timestamp
- Event type
- Success or denial
- Actor
- Account
- Lease ID
- Decision detail

Both successful and denied checkout and check-in attempts are recorded. The audit endpoint does not expose the credential.

### 6. Made Time and Rotation Testable

The vault accepts an injected clock and secret generator. Tests can move time forward without waiting and can prove that the credential changed to the expected value.

This allows deterministic tests for:

- Valid checkout
- Successful check-in
- Credential rotation
- Expired lease denial
- Audit event order and details

## Local Validation

The project is validated with pytest and a GitHub Actions workflow. The workflow installs the development dependencies and runs the test suite whenever the simulator files change.

## Production Improvements

A production design would add:

- Encrypted persistent storage or a hardware-backed vault
- Microsoft Entra ID, SAML, or OIDC authentication
- MFA and conditional access
- Policy-based approvals
- Just-in-time elevation
- Session proxying, isolation, and recording
- Strong credential generation
- Target-system password reconciliation
- Centralized tamper-resistant logging
- Monitoring and alerting
- High availability and disaster recovery
