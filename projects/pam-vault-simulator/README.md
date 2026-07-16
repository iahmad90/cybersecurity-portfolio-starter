# PAM Vault Simulator: Credential Checkout, Rotation, and Audit

## Summary

This hands-on lab simulates core Privileged Access Management workflows with a local FastAPI service. It models a vault that stores mock privileged credentials, account-level authorization, exclusive time-limited checkout leases, secure check-in, credential rotation, and an audit trail.

The project runs entirely on a local computer and never uses real passwords. It connects CyberArk Defender PAM study topics to a working Python application that can be demonstrated in an interview.

## Security Objectives

- Store mock privileged credentials behind a vault service instead of distributing them directly.
- Limit checkout access by application role and by the specific account.
- Allow only one active lease for a privileged account at a time.
- Set a maximum checkout time and deny use of expired leases.
- Require the same actor who checked out a credential to check it in.
- Rotate the mock credential after a successful check-in.
- Record successful and denied checkout and check-in events.
- Restrict audit-log access to an auditor role.

## Architecture

```text
PAM user
   |
   v
FastAPI identity and role check
   |
   v
In-memory vault
  |-- privileged account metadata
  |-- account-level allowed actors
  |-- mock credential
  |-- credential version
   |
   v
Exclusive time-limited lease
   |
   +--> checkout returns mock credential
   |
   +--> check-in validates owner and expiry
              |
              v
       mock credential rotation

Every decision --> append-only in-memory audit trail
PAM auditor ----> role-restricted audit endpoint
```

## PAM Workflow

```text
1. A user presents a demo identity and the PAM-Users role.
2. The service verifies the user is allowed to access the requested account.
3. The vault confirms no unexpired lease already exists.
4. The vault creates a lease with a fixed expiration time.
5. The user receives the mock credential for the lease period.
6. Check-in verifies the lease owner, status, and expiration.
7. A successful check-in rotates the mock secret and increments its version.
8. The service records the checkout or check-in decision in the audit log.
```

## Security Controls Modeled

| Control | Lab Implementation | PAM Concept |
| --- | --- | --- |
| Credential vaulting | Mock secrets are held inside the vault object | Centralized protection of privileged credentials |
| Least privilege | `PAM-Users` role plus account-specific actor allowlist | Users receive access only to approved accounts |
| Exclusive checkout | A second active lease for the same account is denied | Reduces uncontrolled concurrent credential use |
| Session time limit | Leases expire after 1 to 3,600 seconds | Limits the window of privileged access |
| Lease ownership | Only the actor who checked out the account can check it in | Prevents another user from controlling the lease |
| Password rotation | The mock secret changes after successful check-in | Models CyberArk CPM credential rotation |
| Audit trail | Every checkout and check-in decision records actor, account, outcome, time, and lease | Supports accountability and investigations |
| Separation of duties | Audit access requires `PAM-Auditors` | Separates credential users from reviewers |

## API Endpoints

| Endpoint | Role | Purpose |
| --- | --- | --- |
| `GET /health` | None | Confirms the service is running |
| `POST /accounts/{account_id}/checkout` | `PAM-Users` | Creates a time-limited credential lease |
| `POST /leases/{lease_id}/checkin` | `PAM-Users` | Ends the lease and rotates the mock credential |
| `GET /audit` | `PAM-Auditors` | Returns the audit trail |

Demo identity headers are intentionally simple and are not production authentication:

```text
X-Demo-Actor: pam-analyst
X-Demo-Roles: PAM-Users
```

## Project Files

```text
pam-vault-simulator/
├── .gitignore
├── BUILD-NOTES.md
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── src/
│   └── pam_vault_simulator/
│       ├── __init__.py
│       ├── main.py
│       └── vault.py
└── tests/
    └── test_api.py
```

## Run Locally

Use Python 3.11 or newer.

```bash
cd projects/pam-vault-simulator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn pam_vault_simulator.main:app --app-dir src --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

### Check Out a Credential

```bash
curl -s http://127.0.0.1:8000/accounts/linux-root/checkout \
  -H 'Content-Type: application/json' \
  -H 'X-Demo-Actor: pam-analyst' \
  -H 'X-Demo-Roles: PAM-Users' \
  -d '{"duration_seconds":300}'
```

Copy the returned `lease_id` for check-in:

```bash
curl -s -X POST http://127.0.0.1:8000/leases/LEASE_ID/checkin \
  -H 'X-Demo-Actor: pam-analyst' \
  -H 'X-Demo-Roles: PAM-Users'
```

Review the audit trail:

```bash
curl -s http://127.0.0.1:8000/audit \
  -H 'X-Demo-Actor: security-auditor' \
  -H 'X-Demo-Roles: PAM-Auditors'
```

## Run Automated Tests

```bash
pytest -q
```

The tests verify:

- Authorized credential checkout
- Account-level least privilege
- Check-in and mock credential rotation
- Expired lease denial without rotation
- Checkout and check-in audit correctness
- Audit records for denied expired leases
- Auditor-role enforcement

## CyberArk Concept Mapping

| Simulator | CyberArk Concept |
| --- | --- |
| In-memory vault | Digital Vault |
| Account allowlist | Safe permissions and account authorization |
| Checkout endpoint | PVWA or API credential request |
| Time-limited lease | Temporary privileged access window |
| Mock secret rotation | Central Policy Manager rotation |
| Audit endpoint | Activity monitoring and audit reports |

This is a learning model, not an implementation of CyberArk components or protocols.

## Interview Talking Points

- I built a working PAM workflow instead of only writing about PAM concepts.
- I applied two authorization layers: a PAM application role and an account-specific allowlist.
- I used time-limited, exclusive leases so privileged access is controlled and cannot remain open indefinitely.
- I made credential rotation part of the successful check-in transaction and tracked credential versions.
- I recorded both successful and denied activity so the audit trail can support accountability and investigations.
- I separated PAM users from auditors to demonstrate separation of duties.
- I used dependency injection for the clock and secret generator so expiration and rotation behavior could be tested deterministically.
- I can explain how the simulator maps to CyberArk Vault, Safes, PVWA, CPM, and auditing concepts.

## Skills Demonstrated

- Privileged Access Management fundamentals
- CyberArk concept mapping
- Least-privilege authorization
- Time-limited access design
- Credential lifecycle and rotation
- Security audit logging
- Python and FastAPI
- Automated security testing with pytest
- GitHub Actions continuous integration

## Resume Bullets

- Built a FastAPI PAM vault simulator with account-level authorization, exclusive time-limited credential checkout, secure check-in, and automated mock-password rotation.
- Implemented role-separated audit access and event logging for successful and denied privileged credential activity.
- Created automated pytest coverage for checkout, check-in, credential rotation, expired lease denial, and audit-log correctness.

## Limitations

- The vault, leases, and audit trail are in memory and reset when the service restarts.
- Demo headers are not real authentication and must not be trusted in production.
- Credentials are intentionally fake and are returned directly for learning purposes.
- Production PAM requires encrypted durable storage, strong identity validation, high availability, policy management, session isolation and recording, alerting, and secure secret generation.
