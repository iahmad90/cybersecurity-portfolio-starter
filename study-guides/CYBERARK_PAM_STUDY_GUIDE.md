# CyberArk Defender PAM Study Guide

Plain-language prep notes for the CyberArk Defender - PAM certification.

Last updated: July 12, 2026

## Quick Exam Snapshot

CyberArk Defender - PAM is an entry-to-intermediate certification focused on the day-to-day administration and core concepts of CyberArk Privileged Access Management. Public exam-prep sources commonly describe the exam as multiple choice, about 65 questions, 90 minutes, and around a 70% passing target. Always confirm the current details in CyberArk University or Pearson VUE before scheduling, because exam policies can change.

Public CyberArk training page referenced: CyberArk University, "Defender - PAM Sample Items & Study Guide"
CyberArk product docs referenced:

- PVWA: https://docs.cyberark.com/pam-self-hosted/latest/en/content/pasimp/password-vault-web-access.htm
- CPM: https://docs.cyberark.com/pam-self-hosted/latest/en/content/landing%20pages/lpcentralpolicymanager.htm
- PSM: https://docs.cyberark.com/pam-self-hosted/latest/en/content/pasimp/privileged-session%20manager-introduction.htm
- PSM system description: https://docs.cyberark.com/pam-self-hosted/latest/en/content/pas%20sysreq/system%20requirements%20-%20psm.htm

## 1. What PAM Is and Why It Matters

PAM stands for Privileged Access Management.

In normal IAM, users get access based on who they are and what they need. PAM focuses on the most powerful accounts: administrator accounts, root accounts, service accounts, database admin accounts, cloud admin accounts, and other identities that can change systems, view sensitive data, or disable security controls.

The big idea:

> PAM protects high-risk accounts by storing credentials securely, controlling who can use them, rotating passwords, recording privileged sessions, and auditing what happened.

Why it matters:

- Privileged accounts are major targets for attackers.
- Admin passwords are often reused, shared, or forgotten.
- A stolen admin credential can lead to full environment compromise.
- PAM helps enforce least privilege, accountability, password rotation, session monitoring, and audit trails.

In CyberArk, think of PAM like a secure system for checking out and using powerful accounts without casually exposing the password.

## 2. Core CyberArk Defender Exam Topics

### PAM Fundamentals

Know what privileged access is and why it needs stronger controls than normal user access.

You should understand:

- Privileged accounts versus standard user accounts
- Least privilege
- Credential vaulting
- Password rotation
- Session monitoring
- Audit logs
- Approval workflows
- Break-glass or emergency access concepts

### Vaulting and Safes

The CyberArk Vault stores privileged account credentials and related data. A Safe is a logical container inside the Vault.

Common Safe ideas:

- A Safe groups accounts and files.
- Users and groups receive permissions on Safes.
- Safe permissions control actions like list accounts, retrieve passwords, use accounts, manage Safe members, and view audit activity.
- Safes help separate access by team, system type, environment, or business owner.

Example:

- `Windows-Admins-Prod` Safe stores production Windows admin accounts.
- `DBA-Oracle-Prod` Safe stores production Oracle database admin accounts.

### Policies and Platforms

CyberArk uses policies/platforms to define how accounts are managed.

Know that policies can control:

- Password change frequency
- Password verification
- Password reconciliation
- Password complexity
- Allowed connection methods
- Session recording behavior
- Whether users can view passwords or only connect through PSM

Simple way to remember:

> The account is the credential. The Safe controls who can access it. The platform/policy controls how CyberArk manages it.

### CPM: Central Policy Manager

CPM is the component that manages passwords automatically.

It can:

- Change passwords
- Verify passwords
- Reconcile passwords when they get out of sync
- Enforce password policy rules
- Communicate with target systems to update credentials

Exam-style idea:

> If the question is about automatic password rotation, verification, or reconciliation, think CPM.

### PVWA: Password Vault Web Access

PVWA is the web interface used by administrators and end users to access and manage privileged accounts.

Users commonly use PVWA to:

- Search for accounts
- Request access
- Retrieve or use credentials
- Launch connections through PSM
- Manage accounts and Safes, depending on permissions
- Review account details and activity

Exam-style idea:

> If the question is about the web portal where users interact with accounts and Safes, think PVWA.

### PSM: Privileged Session Manager

PSM secures, controls, monitors, and records privileged sessions.

Instead of giving a user the admin password directly, CyberArk can broker the connection through PSM. This lets the organization monitor the session and create audit evidence.

PSM can help with:

- RDP, SSH, and other privileged connections
- Session isolation
- Session recording
- Command/activity monitoring, depending on configuration
- Reducing direct password exposure

Exam-style idea:

> If the question is about launching, monitoring, isolating, or recording a privileged session, think PSM.

### Account Lifecycle Management

Account lifecycle management means handling privileged accounts from discovery through retirement.

Know these stages:

1. Discover or identify privileged accounts.
2. Onboard accounts into CyberArk.
3. Assign accounts to the right Safe.
4. Apply the correct platform/policy.
5. Set permissions for users or groups.
6. Rotate, verify, and reconcile passwords.
7. Monitor usage and review audit logs.
8. Disable or remove accounts when no longer needed.

### Security and Audit Functions

CyberArk Defender candidates should understand how CyberArk supports accountability.

Important ideas:

- Who accessed which privileged account?
- Was the password viewed or was a session launched through PSM?
- Was approval required?
- Was the session recorded?
- Did CPM successfully rotate the password?
- Are failed login, failed change, or failed reconcile events visible?

## 3. Key Terminology

### Vault

The secure CyberArk storage location for privileged credentials and sensitive account information. Think of it as the protected core of the PAM system.

### Safe

A logical container inside the Vault. Safes hold accounts and define who can access or manage those accounts.

### CPM

Central Policy Manager. The CyberArk component responsible for password management tasks such as automatic password changes, verification, and reconciliation.

### PVWA

Password Vault Web Access. The CyberArk web portal where users and admins interact with privileged accounts, Safes, policies, and workflows.

### PSM

Privileged Session Manager. The CyberArk component that brokers, monitors, and records privileged sessions so users can connect without directly handling passwords.

### PTA

Privileged Threat Analytics. A CyberArk analytics component historically used to detect risky privileged behavior, suspicious activity, and possible credential misuse. Know the purpose at a high level: behavior analytics and threat detection around privileged access.

### Platform

A configuration template that tells CyberArk how to manage a type of account, such as Windows local admin, Unix root, database admin, or network device credentials.

### Reconcile

A password recovery process used when the stored password and the real target-system password are out of sync. CPM can use a reconcile account to regain control.

### Verify

The process of checking whether the password stored in CyberArk still works on the target system.

### Rotation / Change

The process of changing a privileged account password according to policy.

### Account Onboarding

Adding a privileged account into CyberArk so it can be vaulted, managed, rotated, and audited.

## 4. Sample Practice Questions

These are original practice questions written in a similar multiple-choice style. They are not copied from CyberArk's exam.

### Question 1

What is the main purpose of Privileged Access Management?

A. To replace all firewalls
B. To protect and control high-risk administrator accounts
C. To make every user a local administrator
D. To remove the need for passwords

Answer: B

Explanation: PAM focuses on powerful accounts like admin, root, service, cloud admin, and database admin accounts. These accounts need stronger controls because misuse can cause major damage.

### Question 2

Which CyberArk component is mainly responsible for automatic password changes and verification?

A. PVWA
B. CPM
C. PSM
D. PTA

Answer: B

Explanation: CPM handles password management tasks such as changing, verifying, and reconciling privileged account passwords.

### Question 3

A user needs to connect to a server without seeing the actual privileged password. Which component is most likely used?

A. PSM
B. PTA
C. Safe
D. Vault license file

Answer: A

Explanation: PSM can broker a privileged session so the user connects through CyberArk without directly viewing or copying the password.

### Question 4

What is a CyberArk Safe?

A. A firewall rule
B. A logical container that stores accounts and controls access permissions
C. A backup copy of the operating system
D. A type of endpoint antivirus policy

Answer: B

Explanation: Safes organize vaulted accounts and control which users or groups can access, use, or manage them.

### Question 5

Which component is the CyberArk web interface used by administrators and end users?

A. CPM
B. PSM
C. PVWA
D. PTA

Answer: C

Explanation: PVWA stands for Password Vault Web Access. It is the browser-based interface for working with accounts, Safes, and access workflows.

### Question 6

An account password in the Vault no longer matches the password on the target server. What process helps restore control?

A. Reconciliation
B. Session recording
C. Browser refresh
D. Account deletion

Answer: A

Explanation: Reconciliation is used when CyberArk needs to regain control of an account whose password is out of sync.

### Question 7

Which statement best describes the relationship between a Safe and a platform?

A. A Safe controls password complexity, and a platform stores audit logs.
B. A Safe controls who can access accounts, while a platform controls how account passwords are managed.
C. A Safe is only used for session recording, while a platform is only used for web login.
D. They mean the same thing.

Answer: B

Explanation: Safes are about storage and access permissions. Platforms define management rules such as password rotation, verification, and connection behavior.

### Question 8

Which CyberArk feature is most directly related to auditing what an administrator did during a privileged session?

A. PSM recording
B. Password complexity
C. Safe naming convention
D. Browser bookmark

Answer: A

Explanation: PSM can monitor and record privileged sessions, creating evidence for audits and investigations.

### Question 9

What is the best reason to rotate privileged passwords regularly?

A. To make usernames shorter
B. To reduce the risk from stolen or shared credentials
C. To increase browser speed
D. To avoid creating Safes

Answer: B

Explanation: If a privileged password is exposed, regular rotation limits how long that password remains useful to an attacker.

### Question 10

Which scenario is the best example of least privilege?

A. Every help desk user has Domain Admin access.
B. Users receive only the privileged access required for their role and task.
C. All passwords are stored in a shared spreadsheet.
D. Admin accounts are never audited.

Answer: B

Explanation: Least privilege means giving users only the access they need, when they need it, and no more.

## 5. Fast Memorization Table

| Term | Plain Meaning | Remember This |
| --- | --- | --- |
| Vault | Secure credential storage | Where secrets live |
| Safe | Container and permission boundary | Who can access what |
| CPM | Password management engine | Change, verify, reconcile |
| PVWA | Web portal | Search, request, manage, launch |
| PSM | Session broker/recorder | Connect, monitor, record |
| PTA | Threat analytics | Detect risky privileged behavior |
| Platform | Account management template | Rules for account handling |
| Reconcile | Fix password mismatch | Regain control |
| Verify | Check password works | Test the stored password |
| Rotate | Change password | Reduce credential risk |

## 6. High-Yield Study Checklist

Before taking the exam, be able to explain:

- What PAM is and why privileged accounts are dangerous.
- The difference between Vault, Safe, account, platform, and policy.
- What CPM does.
- What PVWA does.
- What PSM does.
- Why session recording matters.
- How password rotation, verification, and reconciliation differ.
- How Safe permissions control user access.
- How account onboarding fits into the privileged account lifecycle.
- How CyberArk supports auditability and accountability.

## 7. Simple Mental Model

Use this flow:

1. The account is stored in the Vault.
2. The account lives inside a Safe.
3. Safe permissions decide who can use it.
4. The platform decides how the password is managed.
5. CPM rotates, verifies, and reconciles the password.
6. PVWA is where users and admins interact with it.
7. PSM lets users connect while monitoring and recording the session.

If you can explain that flow clearly, you are covering a large part of the Defender PAM foundation.
