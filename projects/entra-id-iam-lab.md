# Microsoft Entra ID IAM Lab: Least Privilege, MFA, and Access Reviews

## Summary

This lab demonstrates a beginner-friendly Microsoft Entra ID identity and access management workflow. The goal is to show how a small organization can create users and groups, assign access based on job role, require MFA for sensitive access, review group membership, and document least-privilege decisions.

This project is designed for entry-level IAM Analyst, User Access Management Analyst, SOC Analyst, and Junior Cloud Security Analyst roles.

## Scenario

A small company has four users who need different levels of access:

| User | Role | Business Need |
| --- | --- | --- |
| Alex Reed | IT Support Technician | Reset passwords and help users with account access |
| Jordan Miles | Finance Associate | Access finance files and reports |
| Taylor Brooks | HR Coordinator | Access employee records |
| Morgan Lee | Contractor | Temporary read-only project access |

The company wants to reduce unnecessary access, require stronger sign-in protection, and create an access review process for sensitive groups.

## Lab Objectives

- Create test users in Microsoft Entra ID.
- Create security groups based on job function.
- Assign users to groups instead of assigning access directly to individuals.
- Apply least privilege by matching access to job need.
- Require MFA for sensitive groups using Conditional Access.
- Create an access review plan for group membership.
- Document findings in a way an IAM or security team could understand.

## Tools and Requirements

- Microsoft Entra admin center
- Microsoft Entra ID test tenant or Microsoft developer tenant
- Test user accounts only
- Security groups for simulated departments
- Optional: Microsoft Entra ID P2 trial for access reviews and identity governance features

Do not use real personal data, real employee accounts, production tenants, or real business files in this lab.

## Key Microsoft Entra Concepts Used

| Concept | How It Is Used In This Lab |
| --- | --- |
| Users | Test identities for IT, Finance, HR, and Contractor roles |
| Groups | Access is assigned through department-based groups |
| Least privilege | Users receive only the access needed for their role |
| MFA | Sensitive groups require stronger authentication |
| Conditional Access | Policy logic decides when MFA is required |
| Access reviews | Group membership is reviewed to confirm access is still needed |
| Privileged roles | Admin permissions are limited and reviewed carefully |

Microsoft describes Conditional Access as the Zero Trust policy engine that uses identity-driven signals to enforce access decisions. Microsoft also recommends using the minimum permissions needed for a task and managing access according to least privilege.

Sources:

- https://learn.microsoft.com/en-us/entra/identity/conditional-access/overview
- https://learn.microsoft.com/en-us/entra/id-governance/scenarios/least-privileged
- https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/delegate-by-task

## Lab Design

### Groups

| Group Name | Purpose | Sensitivity |
| --- | --- | --- |
| IAM-IT-Support | Help desk and basic user support tasks | Medium |
| IAM-Finance-Users | Finance report access | High |
| IAM-HR-Users | Employee record access | High |
| IAM-Contractors | Temporary project access | Medium |
| IAM-Security-Reviewers | Read-only access review and audit visibility | High |

### User-to-Group Mapping

| User | Group Assignment | Reason |
| --- | --- | --- |
| Alex Reed | IAM-IT-Support | Needs help desk access |
| Jordan Miles | IAM-Finance-Users | Needs finance report access |
| Taylor Brooks | IAM-HR-Users | Needs employee record access |
| Morgan Lee | IAM-Contractors | Needs temporary limited access |

## Step 1: Create Test Users

In the Microsoft Entra admin center:

1. Go to Entra ID.
2. Open Users.
3. Select New user.
4. Create test users for Alex, Jordan, Taylor, and Morgan.
5. Use clearly fake names and lab-only usernames.

Evidence to capture:

- Screenshot of the test user list with private tenant datails hidden.
- A short note explaining why fake users were used.

Microsoft reference:

- https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users

## Step 2: Create Security Groups

Create these groups in Microsoft Entra ID:

- IAM-IT-Support
- IAM-Finance-Users
- IAM-HR-Users
- IAM-Contractors
- IAM-Security-Reviewers

Use security groups because they make access easier to manage and review. Instead of assigning permissions one user at a time, access can be managed by group membership.

Evidence to capture:

- Screenshot of the group list.
- Notes showing what each group is for.

Microsoft reference:

- https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups
- https://learn.microsoft.com/en-us/entra/fundamentals/concept-learn-about-groups

## Step 3: Assign Users to Groups

Assign each test user to the correct group:

| User | Correct Group | Incorrect Access To Avoid |
| --- | --- | --- |
| Alex Reed | IAM-IT-Support | Finance or HR file access |
| Jordan Miles | IAM-Finance-Users | Admin roles or HR access |
| Taylor Brooks | IAM-HR-Users | Finance access or admin roles |
| Morgan Lee | IAM-Contractors | HR, Finance, or admin access |

Security note:

> Group-based access supports least privilege because access can be matched to job function and reviewed more easily than individual one-off permissions.

## Step 4: Document Least-Privilege Decisions

Create a short access review table:

| User | Current Access | Needed Access | Decision |
| --- | --- | --- | --- |
| Alex Reed | IAM-IT-Support | IAM-IT-Support | Approve |
| Jordan Miles | IAM-Finance-Users | IAM-Finance-Users | Approve |
| Taylor Brooks | IAM-HR-Users | IAM-HR-Users | Approve |
| Morgan Lee | IAM-Contractors, IAM-Finance-Users | IAM-Contractors only | Remove Finance access |

Example finding:

- Finding: Morgan is a contractor but was added to IAM-Finance-Users.
- Risk: Contractor access to finance data is not required for the project role.
- Recommendation: Remove Morgan from IAM-Finance-Users and keep Morgan in IAM-Contractors only.
- Security principle: Least privilege.

## Step 5: Require MFA for Sensitive Groups

Create a Conditional Access policy that requires MFA for sensitive groups:

- IAM-Finance-Users
- IAM-HR-Users
- IAM-IT-Support
- IAM-Security-Reviewers

Suggested policy name:

`CA-Require-MFA-Sensitive-IAM-Groups`

Policy design:

| Setting | Lab Choice |
| --- | --- |
| Users or groups | Finance, HR, IT Support, Security Reviewers |
| Cloud apps | All cloud apps for lab simplicity |
| Conditions | Any location for the lab |
| Grant control | Require multifactor authentication |
| Policy state | Report-only first, then On after testing |

Security note:

> MFA reduces the risk that a stolen password alone can give an attacker access to sensitive systems.

Microsoft reference:

- https://learn.microsoft.com/en-us/entra/identity/authentication/tutorial-enable-azure-mfa
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/policy-all-users-mfa-strength

## Step 6: Create an Access Review Plan

If Microsoft Entra ID Governance / P2 features are available, create an access review for sensitive groups. If the license is not available, document a manual review process using the table below.

Access review schedule:

| Review Item | Lab Choice |
| --- | --- |
| Review frequency | Monthly |
| Reviewer | Security reviewer or group owner |
| Scope | HR, Finance, Contractor, and Security Reviewer groups |
| Decision options | Approve, remove, or investigate |
| Evidence | Export or screenshot review result |

Review questions:

- Does the user still need this access?
- Is the user in the correct department or role?
- Is the access too broad?
- Is the account temporary or contractor-based?
- Should the access expire?

Microsoft reference:

- https://learn.microsoft.com/en-us/entra/id-governance/access-reviews-overview
- https://learn.microsoft.com/en-us/entra/id-governance/create-access-review
- https://learn.microsoft.com/en-us/entra/id-governance/perform-access-review

## Step 7: Privileged Role Safety

Avoid assigning Global Administrator unless it is truly required. Use task-specific roles where possible, such as:

- Groups Administrator for group management.
- User Administrator for user account management.
- Reports Reader or Security Reader for read-only review work.
- Privileged Role Administrator only for privileged role assignment tasks.

Security note:

> Powerful administrator roles can create major risk if they are assigned too broadly. Least privilege means using the smallest role that can complete the task.

Microsoft reference:

- https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference
- https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/privileged-roles-permissions

## Evidence Checklist

Add screenshots after completing the live lab:

- Test users created.
- Security groups created.
- User membership inside each group.
- Conditional Access MFA policy in report-only mode.
- Access review result or manual access review table.
- Before-and-after note showing Morgan removed from Finance access.

Before adding screenshots to GitHub:

- Hide tenant IDs.
- Hide real email addresses.
- Hide personal phone numbers.
- Hide recovery methods.
- Do not show real passwords, tokens, keys, or production data.

## What I Learned

- IAM controls work best when access is based on job role.
- Groups make access easier to assign, audit, and remove.
- Least privilege reduces risk by removing unnecessary access.
- MFA protects sensitive groups from password-only compromise.
- Access reviews help confirm users still need access over time.
- Privileged administrator roles should be limited because they can affect many users and security settings.

## How This Maps To Job Roles

| Job Role | Lab Evidence |
| --- | --- |
| IAM Analyst | Users, groups, access reviews, least privilege |
| User Access Management Analyst | Provisioning, deprovisioning, group membership review |
| SOC Analyst | MFA, suspicious access risk, account misuse awareness |
| Junior Cloud Security Analyst | Cloud identity controls and Conditional Access |
| Help Desk / IT Support | User account basics and access troubleshooting |

## Resume Bullets From This Lab

- Built a Microsoft Entra ID IAM Lab using test users, security groups, MFA policy design, and access review documentation.
- Applied least privilege by mapping users to job-based groups and removing unnecessary contractor access.
- Documented Conditional Access MFA requirements for sensitive HR, Finance, IT Support, and Security Reviewer groups.
- Created an access review checklist to support identity governance and audit readiness.

## Next Improvements

- Complete the lab in a real Microsoft Entra developer tenant and add sanitized screenshots.
- Add a diagram showing users, groups, policies, and review flow.
- Connect this project to SC-300 study notes.
- Add a second version of this lab using AWS IAM users, groups, roles, and policies.
