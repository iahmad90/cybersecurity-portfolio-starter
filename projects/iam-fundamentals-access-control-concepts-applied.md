# IAM Fundamentals: Access Control Concepts Applied

## Objective

This project explains the core ideas behind Identity and Access Management (IAM) and why they matter in cybersecurity work. The goal was to take beginner IAM and cloud security notes and turn them into a practical project writeup that shows understanding of users, groups, roles, permissions, authentication, authorization, MFA, and least privilege.

For a hiring manager, this project shows that I can learn security concepts, organize them clearly, and explain how they apply to real workplace access control decisions.

## Tools Used

- IAM and cloud fundamentals study notes
- Beginner cloud security concepts
- Access control terminology
- GitHub markdown documentation
- Cybersecurity portfolio writeup structure

## Steps Taken

1. Reviewed IAM basics, including users, groups, roles, and policies.
2. Compared authentication and authorization to understand the difference between proving identity and controlling access.
3. Studied multi-factor authentication and why stronger login protection helps reduce account takeover risk.
4. Reviewed the principle of least privilege and how it limits unnecessary access.
5. Connected IAM concepts to real cloud security tasks such as reviewing permissions, removing unused access, monitoring suspicious logins, and protecting storage or admin accounts.

## Findings

IAM is important because many security problems start with weak identity controls. A user may have too much access, an old account may still be active, a password may be stolen, or an admin account may not have MFA enabled. If those issues are not managed, an attacker or careless user can reach systems and data they should not be able to access.

The main IAM concepts I learned were:

- Users represent individual people or services and should not be shared.
- Groups make permissions easier to manage when employees join, leave, or change roles.
- Roles allow temporary access and are useful for admins, applications, and cloud services.
- Policies define what actions are allowed or denied, which resources can be accessed, and under what conditions.
- Authentication verifies who someone is.
- Authorization controls what that verified identity is allowed to do.
- MFA adds another layer of protection if a password is stolen.
- Least privilege means giving only the access needed for a task or job role.

I also learned that IAM is closely connected to cloud security. In AWS, Azure, Google Cloud, and SaaS platforms, security teams need to manage accounts, groups, roles, permissions, MFA, access keys, public exposure, and logging. These controls help protect company data and reduce the damage from mistakes or compromised accounts.

## Security Impact

Good IAM reduces risk by making access intentional, limited, and easier to review. If an employee only needs read-only access to logs, giving full administrator access creates unnecessary risk. If an account is no longer used, leaving it active gives attackers another possible entry point. If MFA is not enabled on important accounts, a stolen password can become a full security incident.

These IAM basics apply directly to entry-level security work. A SOC analyst, IAM analyst, help desk analyst, or cloud support associate may be asked to investigate suspicious logins, confirm whether access is appropriate, help remove unused accounts, check MFA status, or document risky permissions. Understanding access control makes it easier to explain what happened, why it matters, and what should be fixed.

## Recommendation

Organizations should treat IAM as a regular security practice, not a one-time setup task. A strong beginner IAM checklist would include:

- Use unique accounts for each person instead of shared logins.
- Place users into groups based on job responsibilities.
- Use roles for temporary or service-based access when possible.
- Enable MFA for important accounts, especially admin accounts.
- Avoid using root or global admin accounts for daily work.
- Apply least privilege instead of giving broad access by default.
- Review access regularly and remove permissions that are no longer needed.
- Remove old users, unused roles, and inactive access keys.
- Use read-only permissions when full access is not required.
- Monitor login activity and permission changes.

## Reflection

This project helped me understand that IAM is one of the foundations of cybersecurity. It is not only about creating accounts. It is about making sure the right people have the right access at the right time, and that unnecessary access is removed before it becomes a risk.

The biggest lesson I learned is that small access control decisions can have a large security impact. MFA, least privilege, role-based access, and regular access reviews all help reduce the chance that a stolen password, old account, or overpowered permission turns into a larger incident.

As a next step, I would like to build a simple IAM mini lab in a cloud environment. I would create a test user, assign the user to a group, apply read-only permissions, enable MFA, and document why each control matters from a security perspective.
