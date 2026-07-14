# IAM LDAP and Group Policy Lab: Directory Access Controls

## Overview

This lab explains how LDAP, Active Directory objects, security groups, and Group Policy Objects (GPOs) work together to manage identity and access in a Windows domain.

The scenario uses a small organization with Finance, Human Resources, IT Support, and Contractor users. The goal is to create a manageable directory, assign access through groups, enforce security requirements with GPOs, and document troubleshooting steps.

## Objective

- Explain LDAP directory structure and object organization.
- Assign access through job-based security groups.
- Map GPOs to IAM and endpoint security requirements.
- Troubleshoot authentication, membership, and GPO issues.

## Lab Design

The proposed directory structure is:

```text
DC=example,DC=local
|
|-- OU=Users
|   |-- OU=Finance
|   |-- OU=Human Resources
|   |-- OU=IT Support
|   `-- OU=Contractors
|
|-- OU=Groups
|   |-- CN=GG-Finance-Users
|   |-- CN=GG-HR-Users
|   |-- CN=GG-IT-Support
|   `-- CN=GG-Contractors
|
|-- OU=Computers
|   |-- OU=Workstations
|   `-- OU=Servers
|
`-- OU=Service Accounts
```

This separates identities and devices by purpose and provides clear locations for delegated management and policy links.

## Steps Taken

### 1. Reviewed LDAP Directory Structure

I mapped the main directory objects and naming components:

| Object | Purpose | Example |
| --- | --- | --- |
| Domain component | Represents part of the domain name | `DC=example,DC=local` |
| Organizational unit | Organizes objects and supports delegation or GPO links | `OU=Finance,OU=Users,DC=example,DC=local` |
| Common name | Identifies an object such as a user or group | `CN=Alex Reed,OU=Finance,OU=Users,DC=example,DC=local` |
| User | Represents a person or service identity | Finance employee |
| Group | Collects identities for access assignment | `GG-Finance-Users` |
| Computer | Represents a domain-joined endpoint | Finance workstation |

A distinguished name identifies an object's full directory location. Attributes such as `sAMAccountName`, `userPrincipalName`, and `memberOf` help teams query and manage identities.

### 2. Designed Organizational Units

I separated users, groups, computers, and service accounts into purpose-based OUs.

- OUs organize objects, support delegated administration, and provide GPO link targets.
- OUs do not grant resource permissions by themselves.
- Security groups are used to assign access.
- Service and contractor accounts are separated for tighter review.
- Workstations and servers are separated because they require different security policies.

### 3. Created a Group-Based Access Model

| Identity | Security Group | Intended Access |
| --- | --- | --- |
| Finance employees | `GG-Finance-Users` | Finance applications and shared folders |
| HR employees | `GG-HR-Users` | Employee-record systems and HR folders |
| IT support staff | `GG-IT-Support` | Approved support and password-reset tasks |
| Contractors | `GG-Contractors` | Temporary project resources only |

This supports least privilege because access can be reviewed and removed through group membership instead of many direct permissions.

### 4. Planned Group Policy Objects

| GPO | Link Target | IAM or Security Purpose |
| --- | --- | --- |
| Domain Password and Lockout Policy | Domain | Enforces password and account lockout requirements |
| Workstation Security Baseline | Workstations OU | Applies screen lock, firewall, audit, and endpoint settings |
| Finance User Restrictions | Finance Users OU | Applies department-specific user settings |
| Contractor Restrictions | Contractors OU | Applies stricter controls to temporary users |
| Local Administrators Control | Workstations OU | Restricts privileged local group membership |
| Audit Policy | Domain controllers, servers, and workstations | Records logon, account, and policy-change events |

### 5. Documented GPO Enforcement

Group Policy uses Active Directory and SYSVOL to distribute settings to domain-joined users and computers. A GPO contains settings, a link to a site, domain, or OU, and filtering that determines which targets receive it.

Processing generally follows Local, Site, Domain, and OU order. Policies applied later usually take precedence unless inheritance, enforcement, or another rule changes the result.

GPOs support access control by:

- Enforcing password and lockout requirements.
- Restricting local administrator membership.
- Assigning or denying user rights such as local or remote logon.
- Applying firewall, security option, and audit settings.
- Controlling workstation features.
- Using security filtering to target approved identities or devices.

GPOs do not replace resource permissions. They work with security groups, access control lists, authentication, and authorization as layered controls.

### 6. Defined a Validation Process

1. Join a Windows client to the test domain.
2. Place the user and computer in the correct OUs and groups.
3. Link the GPO and confirm its security filtering.
4. Run `gpupdate /force`, then sign out or restart if required.
5. Run `gpresult /r` or create an HTML report.
6. Confirm the policy is applied and test the expected control.

## Key Concepts

### LDAP and Active Directory

- LDAP is a protocol for querying and modifying directory information.
- Active Directory stores users, groups, computers, and organizational units.
- LDAP commonly uses TCP 389; LDAP protected with TLS commonly uses TCP 636.
- Distinguished names and attributes identify and describe directory objects.

## Troubleshooting Steps

### LDAP or Authentication Problems

1. Confirm network connectivity to the domain controller.
2. Verify the client uses the domain DNS service.
3. Use `nslookup` to confirm domain controller records resolve.
4. Check time synchronization because Kerberos is time-sensitive.
5. Confirm the account is enabled, not expired, and not locked out.
6. Verify the username or distinguished name used by the application.
7. Review Event Viewer for LDAP, Kerberos, or Netlogon errors.
8. Confirm valid certificates when LDAP over TLS is used.

### Group Membership or Permission Problems

1. Run `whoami /user` and `whoami /groups`.
2. Check direct and nested group memberships.
3. Confirm the group type and scope fit the resource.
4. Review both share and NTFS permissions.
5. Check for explicit deny entries.
6. Sign out and back in after membership changes.
7. Compare the access with the user's approved job need.

### GPO Application Problems

1. Confirm user and computer objects are in the expected OUs.
2. Confirm the GPO link is enabled and points to the correct location.
3. Check inheritance, enforcement, security filtering, and WMI filters.
4. Run `gpupdate /force`.
5. Use `gpresult` or Resultant Set of Policy.
6. Confirm the client can reach the domain controller and SYSVOL.
7. Review the GroupPolicy Operational log.
8. Check for a higher-precedence GPO configuring the same setting.

## Security Impact

A well-designed directory and GPO structure makes access consistent, reviewable, and scalable. Weak OU design, excessive memberships, broad administrator access, insecure LDAP, or poorly scoped GPOs can create unauthorized access. Regular reviews, testing, logging, and least privilege reduce these risks.

## Lessons Learned

- LDAP directory structure is a foundation for centralized identity administration.
- OUs and security groups serve different purposes.
- Job-based group permissions are easier to audit and remove.
- GPO scope and processing order must be understood for reliable enforcement.
- DNS, time synchronization, access tokens, OU placement, and filtering are common causes of failures.
- `gpresult`, `gpupdate`, `whoami`, Event Viewer, and DNS tests provide useful troubleshooting evidence.
- Directory design, least privilege, policy enforcement, logging, and access reviews work best together.
