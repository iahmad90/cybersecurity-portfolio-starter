# CyberArk PAM Fundamentals: Privileged Access Concepts Applied

## Overview

This project explains the core ideas behind Privileged Access Management (PAM) and how CyberArk helps protect high-risk accounts. The goal was to take CyberArk Defender PAM study notes and turn them into a practical portfolio writeup that shows understanding of privileged accounts, credential vaulting, Safes, session isolation, password rotation, least privilege, and auditability.

For a hiring manager, this project shows that I can learn identity security concepts, organize vendor-specific PAM terminology, and explain how privileged access controls reduce risk in real workplace environments.

## Tools Used

- CyberArk Defender PAM study guide notes
- Privileged Access Management terminology
- CyberArk architecture concepts
- GitHub markdown documentation
- Cybersecurity portfolio writeup structure

## Steps Taken

1. Reviewed PAM basics and compared privileged accounts with standard user accounts.
2. Studied CyberArk Vaults and Safes to understand how privileged credentials are stored and access-controlled.
3. Reviewed CyberArk components such as CPM, PVWA, PSM, platforms, and policies.
4. Connected password rotation, verification, and reconciliation to credential lifecycle management.
5. Studied session isolation and recording to understand how CyberArk supports monitoring, auditing, and accountability.
6. Organized CyberArk Defender PAM sample question patterns into practical concepts that can be explained in a portfolio project.

## Key Concepts Learned

PAM is important because privileged accounts can change systems, access sensitive data, disable security controls, and create major risk if they are misused. These accounts include domain administrator accounts, root accounts, database administrator accounts, service accounts, cloud administrator accounts, and other high-impact identities.

The main PAM and CyberArk concepts I learned were:

- Privileged Access Management focuses on protecting the most powerful accounts in an organization.
- Credential vaulting stores privileged credentials in a protected system instead of leaving them in shared documents, scripts, or memory.
- A CyberArk Vault is the secure storage location for privileged credentials and related sensitive account data.
- A Safe is a logical container inside the Vault that controls which users or groups can access specific accounts.
- Safe permissions help separate access by team, system type, environment, or business owner.
- Platforms and policies define how CyberArk manages accounts, including password complexity, rotation, verification, reconciliation, and connection behavior.
- CPM, or Central Policy Manager, handles password changes, verification, and reconciliation.
- PVWA, or Password Vault Web Access, is the web portal where users and administrators search for accounts, request access, manage Safes, and launch connections.
- PSM, or Privileged Session Manager, brokers, isolates, monitors, and records privileged sessions so users can connect without directly handling passwords.
- Least privilege means users should receive only the privileged access required for their role or task.
- Audit logs and session recordings help show who accessed an account, when they used it, and what happened during the session.

I also learned a simple CyberArk mental model: the account is stored in the Vault, the account lives inside a Safe, Safe permissions decide who can use it, the platform decides how the password is managed, CPM rotates and verifies the password, PVWA is where users interact with it, and PSM lets users connect while monitoring the session.

## Why It Matters for IAM/PAM Roles

PAM is a deeper part of identity security because it focuses on the accounts that can cause the most damage. A normal user account may access email or a business application, but a privileged account may create users, change system settings, access databases, disable logging, or move across systems. If one of those accounts is stolen or shared too widely, the impact can be much larger.

These concepts apply directly to IAM analyst, PAM analyst, SOC analyst, help desk, cloud support, and junior security roles. A security team may need to review who has privileged access, investigate a suspicious admin login, confirm whether a password was rotated, check whether a session was recorded, or document why a user should not receive broad administrator rights.

Understanding CyberArk also helps with security communication. If a question mentions password rotation, verification, or reconciliation, CPM is likely involved. If the question mentions the web portal for users and administrators, PVWA is likely involved. If the question mentions launching, isolating, monitoring, or recording a privileged session, PSM is likely involved. Knowing these patterns makes it easier to understand PAM workflows and explain them clearly.

## Security Impact

Strong PAM reduces risk by making privileged access controlled, temporary, monitored, and easier to audit. Instead of sharing administrator passwords directly, an organization can store them in a Vault, limit access through Safes, rotate them by policy, and broker privileged sessions through PSM.

This reduces the risk from stolen passwords, shared admin accounts, stale service account credentials, excessive access, and unmonitored privileged activity. It also supports compliance and incident response because the organization can review who accessed a privileged account and what happened during the session.

## Recommendation

Organizations should treat privileged access as a high-risk area that needs stronger controls than normal user access. A strong beginner PAM checklist would include:

- Identify privileged accounts across servers, databases, network devices, cloud platforms, and applications.
- Store privileged credentials in a secure vault instead of shared files or spreadsheets.
- Use Safes or similar access boundaries to control who can use each account.
- Apply least privilege so users only receive the access needed for their job or task.
- Rotate privileged passwords regularly and after high-risk use.
- Verify that stored credentials still work on target systems.
- Reconcile accounts when passwords become out of sync.
- Use session brokering and recording for high-risk administrative access.
- Review audit logs for privileged account use, failed changes, failed reconciliations, and unusual activity.
- Remove or disable privileged accounts that are no longer needed.

## Resources

- CyberArk Defender PAM study notes in this portfolio
- CyberArk University Defender PAM sample item and study guide references
- CyberArk documentation for PVWA, CPM, and PSM
- General IAM and least privilege study notes

## Reflection

This project helped me understand that PAM is one of the most important areas inside identity security. IAM controls who can access systems, but PAM focuses on the accounts that can make the biggest changes and create the largest risk.

The biggest lesson I learned is that protecting privileged access is not only about hiding passwords. It is about controlling who can use powerful accounts, rotating credentials, isolating sessions, recording activity, and creating evidence that can be reviewed later.

As a next step, I would like to build a simple PAM lab outline that maps a few example privileged accounts to Safes, policies, password rotation rules, and session monitoring requirements.
