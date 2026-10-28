# Cybersecurity Portfolio

**SECROSES** · Cybersecurity & IT Student · Mexico City

![Linux](https://img.shields.io/badge/Linux-CLI_%26_Hardening-FCC624?style=flat-square&logo=linux&logoColor=black)
![GCP](https://img.shields.io/badge/Google_Cloud-Security-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Log_Analysis-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-Beginner-3776AB?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Open_to-Help_Desk_%2F_SOC_Jr-brightgreen?style=flat-square)

Hands-on security research and lab work built while pursuing a B.S. in Information Technologies (Universidad Nacional Rosario Castellanos) and independent cybersecurity training. Current focus: SOC analysis, threat detection, and AI security.

---

Case studies and lab work built while pursuing a B.S. in Information Technologies (Universidad Nacional Rosario Castellanos, 3rd semester) and independent cybersecurity training. Focus: **SOC analysis, threat detection, incident response and AI security**. Currently looking for SOC Analyst Jr / Help Desk IT roles.

[LinkedIn](https://www.linkedin.com/in/yair-rosas) · [Email](mailto:Edgaryair0032@gmail.com) · [GitHub profile](https://github.com/secroses)

---

## Featured projects (own repositories)

Larger projects with code live in their own repos. This repository holds the written case studies.

| Project | What it is | Status |
|---|---|---|
| [SOC Detection Lab](https://github.com/secroses/soc-detection-lab) | Home SOC on limited resources: Wazuh SIEM, Sysmon Modular, custom correlation rules mapped to MITRE ATT&CK, SOAR with Active Response. | Active |
| [BloomID-v6](https://github.com/secroses/BloomID-v6) | Identity-fraud detection through behavioral biometrics (Isolation Forest), with an API shield protecting the inference pipeline. | Working MVP |
| Phishing Analyzer | Local email triage tool: parses `.eml` files, scores risk with YAML rules mapped to ATT&CK, extracts IoCs. Tested against emails from my own Gophish lab. | In progress |
| Gophish Lab: MegaCorp | Write-up of a phishing-awareness campaign run in an isolated lab, from pretext design to results and detection ideas. | In progress |
| MagicSniffer | File-spoofing detector (extension vs. real file signature). Reused as the attachment module of the Phishing Analyzer. | v0.1 |

---

## Case studies in this repository

| Case study | Summary | Skills shown |
|---|---|---|
| [Cymbal Retail: GCP incident response](incident-response/cymbal-retail-gcp/) | Full incident lifecycle for a simulated breach at a retail company on Google Cloud: VM isolation and restore from snapshot, public bucket ACL revocation, IAP-only SSH, firewall hardening, PCI DSS 3.2.1 re-audit. | Incident response, GCP, PCI DSS |
| [PASTA threat model: sneaker e-commerce app](threat-modeling/pasta-sneaker-app/) | Threat model with attack surface enumeration, threat actor profiling and risk-prioritized mitigations. | Threat modeling, risk analysis |
| [E-commerce database exposure](vulnerability-assessment/ecommerce-db-exposure/) | Vulnerability assessment of a database exposure risk, with classification, impact analysis and remediation. | Vulnerability assessment, reporting |
| [LLM guardrail evaluation](ai-security/llm-guardrail-evaluation/) | Red-team exercise from the MenCISO AI Security session (April 2026), mapped to OWASP LLM Top 10. Output redacted. | AI security, responsible disclosure |

### Fundamentals

| Lab | Summary |
|---|---|
| [Linux file permissions](fundamentals/linux-file-permissions/) | `chmod`, `chown`, permission bits and least privilege, with baseline analysis and verification. |
| [SQL security investigation](fundamentals/sql-log-investigation/) | Log analysis with SQL to investigate a simulated incident: filtering, aggregation and pattern detection. |

---

## Where each skill is demonstrated

| Skill | Evidence |
|---|---|
| SIEM and detection engineering | SOC Detection Lab |
| Incident response | Cymbal Retail case, SOC Detection Lab (SOAR) |
| Threat modeling | PASTA sneaker app |
| Phishing analysis | Phishing Analyzer, Gophish Lab |
| Cloud security (GCP) | Cymbal Retail case |
| Log analysis | SQL investigation, SOC Detection Lab |
| Python, C++ | MagicSniffer, BloomID-v6, Phishing Analyzer |

---

## Certifications

- Google Cybersecurity Professional Certificate (Google, 2026)
- Splunk Search Expert (Splunk)
- Google Cloud Cybersecurity Certificate (Google Cloud, Apr 2026)
- Google IT Support Professional Certificate (Google, Dec 2025)
- Google Cloud Computing Foundations (Google Cloud, Oct 2025)
- Introduction to Cybersecurity (Cisco, Jul 2025)

Full list and verification links on [LinkedIn](https://www.linkedin.com/in/yair-rosas).

---

## Ethical commitment

All work here was done in isolated, controlled educational environments, using fictional accounts and domains or systems I own. Findings follow responsible disclosure practices: methodology is documented, while sensitive or regulated data is redacted before publication. Nothing in this repository is intended for use against systems without authorization.

---

License: [MIT](LICENSE)
