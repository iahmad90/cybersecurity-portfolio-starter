# IAM and Cloud Fundamentals Study Guide

Beginner-friendly notes for IT and cybersecurity study.

## 1. IAM Fundamentals

## What IAM Means

- IAM stands for Identity and Access Management.
- IAM answers two big questions:
  - Who are you?
  - What are you allowed to access?
- IAM helps companies control access to systems, apps, cloud accounts, data, and devices.
- In cybersecurity, IAM matters because many attacks start with stolen passwords, overpowered accounts, or weak access controls.

## Core IAM Terms

## Users

- A user is an identity for one person or service.
- Example: an employee account like `jordan@company.com`.
- Users should only get the access they need for their job.
- Avoid sharing user accounts.

## Groups

- A group is a collection of users.
- Permissions can be assigned to the group instead of each person.
- Example:
  - `HelpDesk` group can reset passwords.
  - `Developers` group can access test servers.
  - `Finance` group can access billing systems.
- Groups make access easier to manage when people join, leave, or change roles.

## Roles

- A role is a set of permissions that can be assumed temporarily.
- Roles are often used by apps, cloud services, and admins who need short-term access.
- Example:
  - A cloud server assumes a role that lets it read files from storage.
  - A security analyst assumes an admin role only during an investigation.
- Roles are safer than long-term access keys when used correctly.

## Policies

- A policy is a rule document that says what actions are allowed or denied.
- Policies usually define:
  - Who the rule applies to.
  - What actions are allowed.
  - Which resources can be accessed.
  - Conditions for access.
- Example idea:
  - Allow read-only access to logs.
  - Deny deleting production databases.
  - Require MFA before allowing admin actions.

## Principle of Least Privilege

- Least privilege means giving only the access required to do the job.
- Do not give admin access "just in case."
- Start with small permissions and add more only when needed.
- Review access regularly and remove unused permissions.
- Good least-privilege questions:
  - Does this user need this access every day?
  - Can this be read-only instead of full access?
  - Can this access expire after the task is done?
  - Is this permission still being used?

## Authentication vs Authorization

## Authentication

- Authentication proves who someone is.
- Simple meaning: "Are you really this person?"
- Common authentication methods:
  - Password
  - MFA code
  - Security key
  - Biometric login
  - Certificate

## Authorization

- Authorization decides what an authenticated identity can do.
- Simple meaning: "Now that we know who you are, what are you allowed to access?"
- Example:
  - You log in successfully.
  - You can view your own files.
  - You cannot view payroll records because you are not authorized.

## MFA

- MFA stands for Multi-Factor Authentication.
- MFA requires more than one proof of identity.
- Common factors:
  - Something you know: password or PIN.
  - Something you have: phone app, hardware key, smart card.
  - Something you are: fingerprint or face scan.
- MFA helps protect accounts even if a password is stolen.
- Stronger MFA options:
  - Authenticator app
  - Hardware security key
  - Passkeys
- Weaker MFA options:
  - SMS codes, because phone numbers can be hijacked or intercepted.

## Common IAM Services

## AWS IAM

- AWS IAM stands for AWS Identity and Access Management.
- Used to manage access to AWS resources.
- Common AWS IAM parts:
  - IAM users
  - IAM groups
  - IAM roles
  - IAM policies
  - Permission boundaries
  - MFA
  - Access keys
- Beginner AWS IAM habits:
  - Do not use the root account for daily work.
  - Turn on MFA for important accounts.
  - Prefer roles over long-term access keys.
  - Give least-privilege permissions.
  - Remove unused users, roles, and keys.

## Azure IAM

- Microsoft Entra ID is Microsoft's cloud identity and access management service.
- It was previously known as Azure Active Directory.
- Common Entra ID / Azure IAM parts:
  - Users
  - Groups
  - Roles
  - Conditional Access
  - MFA
  - Single sign-on
  - Identity governance
  - Privileged Identity Management
- Beginner Azure IAM habits:
  - Enable MFA for users.
  - Use groups to organize access.
  - Use role-based access control for Azure resources.
  - Use Conditional Access to require stronger login rules.
  - Limit Global Administrator access.

## 2. Cloud Fundamentals

## What Cloud Computing Is

- Cloud computing means renting computing resources over the internet instead of owning all the hardware yourself.
- You can rent servers, storage, databases, networking, security tools, and software.
- Big cloud providers include:
  - Amazon Web Services
  - Microsoft Azure
  - Google Cloud
- Cloud is popular because it is flexible, scalable, and usually faster than buying physical hardware.

## Why Companies Use Cloud

- Faster setup for servers and apps.
- Pay for what is used.
- Scale up during busy periods.
- Scale down when demand drops.
- Access services from many regions.
- Use built-in security, logging, backup, and monitoring tools.

## IaaS, PaaS, and SaaS

## IaaS: Infrastructure as a Service

- The cloud provider gives you basic infrastructure.
- You manage more of the system yourself.
- Examples:
  - Virtual machines
  - Virtual networks
  - Cloud storage
  - Firewalls
- Cybersecurity focus:
  - Patch operating systems.
  - Secure network rules.
  - Control admin access.
  - Monitor logs.

## PaaS: Platform as a Service

- The cloud provider gives you a platform to build and run apps.
- You manage the app and data.
- The provider manages more of the servers and runtime.
- Examples:
  - Managed databases
  - App hosting platforms
  - Serverless functions
- Cybersecurity focus:
  - Secure app permissions.
  - Protect secrets.
  - Configure database access.
  - Review logs and alerts.

## SaaS: Software as a Service

- The cloud provider delivers a complete app.
- Users access it through a browser or client app.
- Examples:
  - Microsoft 365
  - Google Workspace
  - Salesforce
  - GitHub
- Cybersecurity focus:
  - Manage users and groups.
  - Enable MFA.
  - Review sharing settings.
  - Monitor suspicious logins.
  - Remove access when users leave.

## Public, Private, and Hybrid Cloud

## Public Cloud

- Cloud services shared across many customers.
- Each customer has isolated accounts and resources.
- Examples:
  - AWS
  - Azure
  - Google Cloud
- Common use:
  - Websites
  - Apps
  - Data storage
  - Security monitoring

## Private Cloud

- Cloud-style infrastructure used by one organization.
- Can be hosted in the company's own data center or by a provider.
- Common use:
  - Highly regulated systems
  - Internal business apps
  - Sensitive workloads

## Hybrid Cloud

- A mix of public cloud and private or on-premises systems.
- Common use:
  - Company keeps some systems in its data center.
  - Company also uses AWS, Azure, or another public cloud.
- Cybersecurity focus:
  - Secure connections between environments.
  - Consistent identity controls.
  - Centralized logging.
  - Clear data protection rules.

## Core Cloud Services

## Compute

- Compute means processing power.
- Examples:
  - Virtual machines
  - Containers
  - Serverless functions
- Security tasks:
  - Patch systems.
  - Limit admin access.
  - Use secure images.
  - Monitor CPU, memory, and unusual behavior.

## Storage

- Storage means saving files, objects, backups, and data.
- Examples:
  - Object storage
  - File storage
  - Disk storage
  - Database storage
- Security tasks:
  - Block public access unless required.
  - Encrypt sensitive data.
  - Control who can read, write, and delete.
  - Enable backups and versioning.

## Networking

- Networking connects cloud resources to each other and to users.
- Examples:
  - Virtual networks
  - Subnets
  - Firewalls
  - Security groups
  - Load balancers
  - DNS
- Security tasks:
  - Restrict inbound traffic.
  - Separate public and private systems.
  - Use network logs.
  - Watch for exposed ports.

## Why Cloud Skills Matter for Cybersecurity

- Many companies run important systems in AWS, Azure, or Google Cloud.
- Security jobs often require understanding cloud identity, logging, networks, and storage.
- Common cloud security work includes:
  - Locking down user access.
  - Investigating suspicious logins.
  - Reviewing IAM permissions.
  - Finding public storage buckets.
  - Checking firewall rules.
  - Monitoring cloud logs.
  - Responding to alerts.
  - Helping teams follow security best practices.
- Cloud knowledge helps with roles like:
  - Help desk analyst
  - SOC analyst
  - IAM analyst
  - Cloud support associate
  - Security analyst
  - Junior cloud security analyst

## 3. Free Next Steps and Beginner Certifications

## Free Learning Steps

- Build a basic GitHub portfolio.
  - Add notes, labs, screenshots, and short writeups.
  - Keep each project simple and clear.

- Learn basic networking.
  - IP addresses
  - DNS
  - HTTP and HTTPS
  - Firewalls
  - VPNs
  - Ports

- Practice IAM in a free cloud account.
  - Create a test user.
  - Create a group.
  - Attach read-only permissions.
  - Turn on MFA.
  - Write down what each step does.

- Practice cloud storage security.
  - Create a storage bucket or container.
  - Keep it private.
  - Test what happens when permissions are changed.
  - Document the secure setup.

- Learn basic Linux commands.
  - `pwd`
  - `ls`
  - `cd`
  - `cat`
  - `grep`
  - `chmod`
  - `ssh`

- Learn basic SQL.
  - This connects well with database coursework.
  - Security analysts often search logs and event data with query languages.

## Certifications to Consider

## AWS Certified Cloud Practitioner

- Good for learning AWS basics.
- Beginner-friendly cloud certification.
- Covers cloud concepts, AWS services, security basics, pricing, and support.
- Useful for:
  - Cloud support
  - IT support
  - SOC analyst foundations
  - Entry-level cloud security study
- Suggested path:
  - Use free AWS Skill Builder lessons.
  - Take free AWS practice question sets.
  - Build 1 or 2 small AWS labs for the portfolio.

## Microsoft AZ-900: Azure Fundamentals

- Good for learning Azure basics.
- Beginner-level Microsoft certification.
- Covers cloud concepts, core Azure services, management, governance, and security basics.
- Useful for:
  - Microsoft-heavy IT environments
  - Help desk
  - Azure support
  - Identity and access learning
- Suggested path:
  - Use Microsoft Learn's free AZ-900 modules.
  - Take Microsoft practice assessments.
  - Build simple Azure notes and screenshots for the portfolio.

## Microsoft SC-900: Security, Compliance, and Identity Fundamentals

- Good after or alongside AZ-900.
- Focuses more directly on security, compliance, and identity concepts.
- Useful for:
  - IAM interest
  - SOC analyst foundations
  - Microsoft security tools
  - Compliance awareness
- Suggested path:
  - Learn Entra ID basics first.
  - Study MFA, Conditional Access, Zero Trust, and compliance terms.

## CompTIA Security+

- Strong general cybersecurity certification.
- More security-focused than AWS Cloud Practitioner or AZ-900.
- Covers threats, vulnerabilities, architecture, operations, incident response, governance, and risk.
- Useful for:
  - SOC analyst
  - Help desk to security transition
  - Junior cybersecurity roles
  - Government or contractor environments
- Suggested path:
  - Learn networking basics first.
  - Learn IAM and cloud fundamentals.
  - Use free videos, practice questions, and notes before paying for the exam.

## Practical Portfolio Projects

## Project 1: IAM Mini Lab

- Goal: show that you understand users, groups, roles, MFA, and least privilege.
- Include:
  - What you created.
  - What permissions you assigned.
  - Why least privilege matters.
  - Screenshots with sensitive details hidden.

## Project 2: Cloud Storage Security Lab

- Goal: show that you understand private vs public storage.
- Include:
  - A private storage bucket or container.
  - Encryption setting notes.
  - Access control notes.
  - A short explanation of why public storage can be risky.

## Project 3: Login Security Notes

- Goal: explain how authentication, authorization, and MFA work.
- Include:
  - Simple definitions.
  - A diagram or bullet list.
  - Examples of weak vs strong login security.

## Project 4: Cloud Security Checklist

- Goal: create a beginner checklist for reviewing a cloud account.
- Include:
  - MFA enabled.
  - No daily root/admin account use.
  - Least-privilege permissions.
  - No public storage unless required.
  - Logging enabled.
  - Old users and keys removed.

## Quick Review

- IAM controls identity and access.
- Authentication proves who you are.
- Authorization controls what you can do.
- MFA makes account takeover harder.
- Least privilege reduces damage from mistakes or attacks.
- Cloud computing rents technology resources over the internet.
- IaaS gives more control and more responsibility.
- PaaS manages more infrastructure for you.
- SaaS gives you a ready-to-use app.
- Cloud security skills are important because companies store data, apps, logs, and identities in cloud platforms.

## Source Notes Checked

- AWS IAM best practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- AWS Certified Cloud Practitioner: https://aws.amazon.com/certification/certified-cloud-practitioner/
- AWS certification prep: https://aws.amazon.com/certification/certification-prep/
- Microsoft Entra identity fundamentals: https://learn.microsoft.com/en-us/entra/fundamentals/identity-fundamental-concepts
- Microsoft Entra ID overview: https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id
- Microsoft Azure Fundamentals AZ-900: https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/
- Microsoft AZ-900 study guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900
- CompTIA Security+ certification information: https://www.comptia.org/certifications/security
