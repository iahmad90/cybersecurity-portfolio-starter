# Linux Homelab: Security Monitoring and Network Segmentation

## Overview

This project is a planned Linux security homelab designed to practice real skills used in entry-level cybersecurity, SOC, IAM, and cloud support roles. The goal is to build a small virtual lab that includes a firewall, segmented networks, a hardened Linux server, and basic security monitoring.

For a hiring manager, this project shows that I can plan a realistic lab environment, think about secure network design, document technical steps, and connect Linux administration to security operations work.

## Architecture

The lab will be built with virtualization so it can run on a personal computer without needing expensive hardware. The main options are Proxmox for a dedicated lab machine or VirtualBox for a simpler beginner setup on a laptop.

Planned lab components:

- Hypervisor: Proxmox or VirtualBox
- Firewall: pfSense virtual firewall
- Linux server: Ubuntu Server or Debian
- Security monitoring: Wazuh or Security Onion
- Network segmentation: separate LAN, server, and monitoring networks
- Test workstation: Kali Linux, Ubuntu Desktop, or another Linux client

Planned network layout:

```text
Internet / Home Router
        |
        |
pfSense Firewall
        |
        |-- LAN Network: test workstation
        |
        |-- Server Network: hardened Linux server
        |
        |-- Monitoring Network: Wazuh or Security Onion
```

The firewall will control traffic between each network segment. The Linux server will send logs to the monitoring system, and the monitoring system will help identify authentication events, configuration changes, and possible suspicious activity.

## Skills Demonstrated

- Linux administration and command-line practice
- Virtual machine setup and basic hypervisor management
- pfSense firewall configuration
- Network segmentation and traffic control
- Linux user, group, SSH, and service hardening
- CIS benchmark research and basic hardening documentation
- Log collection and security monitoring
- Wazuh or Security Onion setup
- Writing clear security documentation for a portfolio

## Step by Step Build Plan

1. Choose the virtualization platform.
   - Use VirtualBox for the easiest beginner setup.
   - Use Proxmox if a spare computer or dedicated lab machine is available.
   - Create a folder for screenshots, diagrams, configuration notes, and lessons learned.

2. Create the virtual networks.
   - Build at least two internal networks: one for the test workstation and one for the Linux server.
   - Add a separate monitoring network if system resources allow it.
   - Document each network name, IP range, gateway, and purpose.

3. Install and configure pfSense.
   - Create a pfSense VM with one WAN interface and multiple LAN interfaces.
   - Assign interfaces for the LAN, server, and monitoring networks.
   - Configure DHCP where needed.
   - Create basic firewall rules that allow only required traffic between segments.

4. Build the Linux server.
   - Install Ubuntu Server or Debian.
   - Create a non-root admin user.
   - Update all packages.
   - Enable SSH with safer settings.
   - Disable password login if key-based login is configured.
   - Install only required services.

5. Harden the Linux server.
   - Review basic CIS benchmark recommendations for the chosen Linux distribution.
   - Check file permissions on sensitive files.
   - Confirm unnecessary services are disabled.
   - Configure automatic security updates if appropriate.
   - Enable a host firewall such as UFW.
   - Document each hardening step and explain the security reason behind it.

6. Install security monitoring.
   - Deploy Wazuh or Security Onion in a separate monitoring VM.
   - Install an agent on the Linux server if using Wazuh.
   - Forward authentication logs, system logs, and important security events.
   - Confirm that login attempts, privilege changes, and service events appear in the dashboard.

7. Test the lab.
   - Attempt SSH login from the test workstation.
   - Confirm allowed traffic works as expected.
   - Confirm blocked traffic is denied by pfSense.
   - Generate a failed login event and verify it appears in the monitoring system.
   - Take screenshots of the firewall rules, network diagram, Linux hardening checks, and monitoring alerts.

8. Document the results.
   - Create a final writeup with screenshots and clear explanations.
   - Include what worked, what failed, and what was fixed.
   - Explain how the lab connects to SOC analyst, Linux administration, cloud security, and IAM work.

## Security Impact

This homelab is useful because it connects several security topics into one hands-on environment. A firewall helps control what systems can communicate. Network segmentation limits how far an attacker or misconfigured device can move inside a network. Linux hardening reduces the attack surface of the server. Log monitoring helps detect suspicious activity instead of relying only on prevention.

These skills are practical for entry-level security work. A SOC analyst may need to review failed logins, suspicious SSH activity, or firewall events. A cloud support or IAM analyst may need to understand access control, secure administration, least privilege, and logging. A help desk or junior systems administrator may need to harden Linux servers and explain why certain services or ports should be restricted.

## Recommendation

The best way to complete this project is to start small and build in phases. The first version should include only a firewall, one Linux server, one test workstation, and basic logging. After that works, the lab can be improved with stronger firewall rules, more segmentation, vulnerability scanning, alerts, and screenshots for the portfolio.

A strong final project should include:

- A simple network diagram
- A table of virtual machines and IP addresses
- pfSense firewall rules with explanations
- Linux hardening checklist
- Screenshots of log events in Wazuh or Security Onion
- A short reflection explaining what was learned

## Next Steps

- Build the first version in VirtualBox or Proxmox.
- Create the pfSense firewall and define the lab network ranges.
- Install the Linux server and apply basic hardening.
- Deploy Wazuh or Security Onion for monitoring.
- Capture screenshots and turn the build notes into a completed portfolio writeup.
- Add a future improvement section for vulnerability scanning, IDS rules, and cloud logging practice.

## Reflection

This project plan helped me understand how different cybersecurity skills connect together. Linux administration, firewall rules, logging, and segmentation are not separate topics in a real environment. They work together to protect systems, limit access, and give analysts the information they need to investigate problems.

The biggest lesson from planning this lab is that security should be built in layers. A hardened Linux server is stronger when it is also behind a firewall, placed in the correct network segment, and monitored for suspicious activity. As a next step, I would like to build the lab, collect screenshots, and update this writeup with real results from the environment.
