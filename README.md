# Ibrahim Ahmad | Junior IAM Portfolio

**Junior IAM / Cloud Identity Candidate · CompTIA Security+ · Google Cybersecurity Certificate**

I focus on identity and access management, privileged access, and cloud identity controls. This portfolio leads with two runnable, tested Python projects—a PAM credential-checkout simulator and an AI-security gateway—followed by clearly labeled Entra ID, Active Directory, LDAP, and Group Policy design writeups. The design documents are not claims of live tenant or domain implementation.

[Live portfolio](https://iahmad90.github.io/cybersecurity-portfolio-starter/) · [Projects](docs/projects.html) · [GitHub](https://github.com/iahmad90) · [LinkedIn](https://www.linkedin.com/in/ibrahim-ahmad-b0b966267) · [Email](mailto:iahmad90@icloud.com)

## Credentials

| Status | Credential |
| --- | --- |
| Earned | CompTIA Security+ |
| Earned | Google Cybersecurity Certificate |
| In progress — study | Microsoft Identity and Access Administrator (SC-300) |
| In progress — study | CyberArk Defender - PAM |
| In progress — study | Red Hat Certified System Administrator (RHCSA / EX200) |

See the [certification and learning log](certs/learning-log.md) for the current study focus. No in-progress item is presented as an earned credential.

## Selected Work

| Project | Evidence status | Skills and signals shown |
| --- | --- | --- |
| [PAM Vault Simulator](projects/pam-vault-simulator/README.md) | Built and tested | Privileged access, account-level authorization, time-limited checkout, mock credential rotation, audit events, Python, FastAPI, pytest |
| [AI Security Gateway](projects/ai-security-entra-llm-lab/README.md) | Built and tested locally; Azure deployment not claimed | Application-role checks, an Entra-authentication integration path, least-privilege workload RBAC design, data handling, privacy-safe audit events, Python, pytest |
| [Entra ID IAM Lab Design](projects/entra-id-iam-lab.md) | Design writeup; no live tenant evidence | Test-user and group model, least-privilege decisions, Conditional Access MFA policy design, access-review workflow |
| [LDAP and Group Policy Lab Design](projects/iam-ldap-group-policy-lab.md) | Design writeup; no AD domain implementation claimed | Active Directory and LDAP concepts, group-based access, GPO scope, directory troubleshooting |
| [CyberArk PAM Fundamentals](projects/cyberark-pam-fundamentals.md) | Concept writeup | Vault and Safe concepts, CPM/PVWA/PSM roles, privileged-account lifecycle, rotation, auditing |
| [IAM Fundamentals](projects/iam-fundamentals-access-control-concepts-applied.md) | Concept writeup | Authentication vs. authorization, MFA, groups, roles, least privilege, access-review fundamentals |
| [Linux Homelab](projects/linux-homelab.md) | Planned; not built | Proposed Linux hardening, network segmentation, firewalling, and monitoring work |
| [Home Lab Network Security](projects/home-lab-network-security.md) | Blank template; no assessment evidence | No skills claimed until a real configuration is documented |
| [Phishing Email Analysis](projects/phishing-email-analysis.md) | Blank template; no sample analysis | No analysis result claimed |
| [Basic IAM Policy Review](projects/basic-iam-policy-review.md) | Blank template; no policy reviewed | No access-review result claimed |
| [Cloud Fundamentals Writeup](projects/cloud-fundamentals-writeup.md) | Planned | Study-guide material exists; a distinct project writeup is not complete |
| [SQL / Database Security Project](projects/sql-database-security-project.md) | Planned | A separate project and results are not complete |

The two runnable projects are the strongest implementation evidence. The Entra ID and LDAP/Group Policy documents show design and explanation, not completed provisioning in Microsoft Entra ID or Active Directory.

## Role-Skill Fit

The recent 10-posting comparison most often mentioned account lifecycle/provisioning and directory platforms (9 of 10 each). MFA and access reviews/recertification appeared in 5 of 10; SSO/federation and SailPoint appeared in 4 of 10; PAM appeared in 2 of 10. The sample is directional—not a market-wide statistic—and includes one employer-portal posting plus nine clearly identified LinkedIn job-board copies.

This repository shows identity concepts, access-control design, PAM workflow modeling, and audit logging. It does **not yet** demonstrate a completed joiner-mover-leaver workflow, a working SailPoint or ServiceNow environment, or live Entra ID/Active Directory administration. See [the posting sample and sources](output/postings-used.md) for scope and links.

## Run the Flagship Projects

Each project has setup instructions, limitations, and tests:

- [PAM Vault Simulator](projects/pam-vault-simulator/README.md)
- [AI Security Gateway](projects/ai-security-entra-llm-lab/README.md)

Both labs use local demo identities and test data; neither is a production IAM or PAM platform. Their GitHub Actions workflows run the project-specific pytest suites.

## Study and Reference Material

- [IAM and Cloud Fundamentals Study Guide](iam-and-cloud-fundamentals-study-guide.md)
- [CyberArk Defender PAM Study Guide](study-guides/CYBERARK_PAM_STUDY_GUIDE.md)
- [IAM and Cloud Security Mock Interview](interview-prep/MOCK_INTERVIEW.md)
- [Project writeup template](writeups/writeup-template.md)
- [Hiring-manager review and scorecard](output/portfolio-review.md)

## Contact

- GitHub: [github.com/iahmad90](https://github.com/iahmad90)
- LinkedIn: [linkedin.com/in/ibrahim-ahmad-b0b966267](https://www.linkedin.com/in/ibrahim-ahmad-b0b966267)
- Email: [iahmad90@icloud.com](mailto:iahmad90@icloud.com)
