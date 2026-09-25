# Hiring-Manager Portfolio Review

**Repository:** `iahmad90/cybersecurity-portfolio-starter`
**Baseline:** `main` at `d5e7a1b` (`Add GitHub Pages portfolio site`)
**Review date:** September 25, 2026
**Audience:** junior IAM, identity, provisioning, ICAM, and cloud-identity hiring teams

## Scorecard

| Dimension | Baseline score | Hiring-manager read |
| --- | ---: | --- |
| 30-second IAM role fit | 4/10 | The live site had a polished layout, but the lead described a broad cybersecurity learner rather than a junior IAM candidate. |
| Implementation evidence | 7/10 | The PAM simulator and AI-security gateway are runnable Python projects with tests and CI. Both are local learning prototypes with explicit production limits. |
| Match to repeated IAM requirements | 5/10 | The repo discusses MFA, least privilege, groups, access reviews, and PAM, but has no completed lifecycle/provisioning workflow or SailPoint/ServiceNow evidence. |
| Accuracy of project status | 4/10 | Entra ID and LDAP/GPO design documents were marked “Completed,” and one Entra resume bullet claimed the lab was built. The files describe plans/design, not live tenant/domain builds. |
| Navigation and freshness | 4/10 | The README repeated project summaries, retained generic role positioning, linked LinkedIn without a URL scheme, and had a dated learning-log placeholder and stale study items. |

**Overall baseline:** 5/10. **Estimated after this PR:** about 7/10 for a first-pass junior IAM portfolio. The estimate improves role fit and trust; it does not add production experience or close the hands-on provisioning gap.

## What a Hiring Manager Can Verify

- **PAM Vault Simulator:** working local FastAPI workflow with account-specific authorization, time-limited exclusive leases, owner-controlled check-in, mock rotation, and audit events. Tests cover success and denial cases.
- **AI Security Gateway:** working local demo with role checks, pattern-based input controls, output redaction, and privacy-safe audit events. The Entra proxy and Azure managed-identity path are integration designs; no Azure deployment is claimed.
- **Entra ID and LDAP/GPO:** detailed design and troubleshooting writeups, but no tenant/domain screenshots or implementation evidence.
- **IAM Fundamentals and CyberArk PAM:** concept explanations, useful as study evidence but not hands-on platform administration.
- **Other project files:** Linux plan and blank home-network, phishing, and policy-review templates; these are not evidence of completed work.

Both Pages routes were available at review time; the published homepage returned HTTP 200. Internal Markdown-relative links inspected in the repo resolve. The LinkedIn profile URL in the old README lacked `https://`; the replacement uses a complete URL.

## Market Comparison

The companion [posting sample](postings-used.md) covers 10 recent roles dated September 4–24: one employer-portal posting and nine LinkedIn copies, per Ibrahim's approval. Lifecycle/provisioning and directory skills appeared in 9/10; MFA and access reviews in 5/10; SSO/federation and SailPoint in 4/10; PAM in 2/10. Treat those counts as directional, not representative statistics.

## Changes in This PR

- Replaced the generic, repetitive README with a role-specific opening, earned-vs-study credential table, concise evidence map for every project file, runnable-project links, and explicit gaps.
- Updated GitHub Pages home and project copy so the title, first-screen story, credentials, and status badges match the README.
- Relabeled Entra ID and LDAP/GPO work as design writeups; replaced the inaccurate Entra “built” resume bullets with an accurate description of the document.
- Updated the projects index and certification learning log; removed the placeholder row and outdated Sophia, AWS, SC-900, and generic cloud-study claims from the current-status view.
- Added the 10-posting source list and this scorecard.
- Corrected the LinkedIn profile URL and clarified which integration paths are not deployed.

## Taste Calls and Non-Changes

- Put the two runnable projects first because they are the strongest implementation evidence; retained AI security as an adjacent differentiator, not the main IAM story.
- Kept design and concept writeups because they show relevant learning, but distinguished them from implemented work rather than deleting or inflating them.
- Kept the blank templates and future project plans in the repository, marked as such; they are not represented as proof of skill.
- Did not invent SailPoint, ServiceNow, provisioning, or live directory experience to mirror postings. The README names these as evidence gaps.
- Did not alter application/outreach issues or claim that applications or LinkedIn messages were sent.
- Did not change project code or CI workflows; validation is limited to the existing project tests and portfolio content/link checks.

## GitHub Issues and Projects Check

The connected GitHub account and repository query returned no visible Projects V2 board. The repository has five open issues; none is complete as a result of this portfolio-copy review, so none was closed or edited:

- [#1 Create a LinkedIn content calendar](https://github.com/iahmad90/cybersecurity-portfolio-starter/issues/1)
- [#4 Create an SC-300 study writeup](https://github.com/iahmad90/cybersecurity-portfolio-starter/issues/4)
- [#5 Track employer applications](https://github.com/iahmad90/cybersecurity-portfolio-starter/issues/5)
- [#6 Send the drafted LinkedIn recruiter notes](https://github.com/iahmad90/cybersecurity-portfolio-starter/issues/6)
- [#7 Continue SC-300 practice](https://github.com/iahmad90/cybersecurity-portfolio-starter/issues/7)

## Validation

- AI Security Gateway: 11 tests passed. PAM Vault Simulator: 7 tests passed.
- Each test run emitted an existing Starlette deprecation warning about the `httpx`-based test client; no project code was changed to address it.
- All local Markdown and HTML links resolve (27 Markdown files and both Pages HTML files checked).
- The currently published home and projects Pages routes return HTTP 200. They still serve `main`; these proposed copy changes will appear publicly only after the pull request is merged.

## Remaining Highest-Value Proof Gap

Build a small, safe identity lifecycle demo (create, change, disable test users; group-based access; approval/verification steps; audit output) or capture sanitized evidence from a real Entra ID/Active Directory learning tenant. Only claim what is actually run and verified.
