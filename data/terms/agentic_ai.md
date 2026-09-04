---
id: "agentic-ai"
uri: "https://w3id.org/aigov-thesaurus/concept/agentic-ai"
prefLabel:
  en: "Agentic AI"
  it: "IA agentica"
altLabel:
  en: ["Autonomous AI Agents", "Agentic Systems", "Goal-directed AI"]
  it: ["Sistemi di IA agentica", "Agenti autonomi intelligenti", "IA orientata agli obiettivi"]
perspective:
  - "tecnico-operativa"
  - "concettuale-filosofica"
definition:
  en: "An advanced class of artificial intelligence systems endowed with autonomous decision-making capabilities that allow them to pursue complex, multi-step goals with minimal human intervention, exhibiting planning, tool use, reflexivity, and environmental interaction."
  it: "Una classe avanzata di sistemi di intelligenza artificiale dotata di capacità decisionali autonome che le consentono di perseguire obiettivi complessi e multi-fase con intervento umano minimo, manifestando pianificazione, uso di strumenti, riflessività e interazione attiva con l'ambiente."
scopeNote:
  en: "Emerging concept bridging autonomous agent theory (ISO/IEC 22989) with philosophical notions of agency, intentionality, and moral accountability. Poses novel challenges for human oversight and governance."
  it: "Concetto emergente che unisce la teoria ingegneristica degli agenti autonomi (ISO/IEC 22989) con le nozioni filosofiche di agenzia, intenzionalità e responsabilità morale. Pone sfide inedite per la supervisione umana e il monitoraggio dei rischi."
broader:
  - "ai-system"
narrower: []
related:
  - "gpai-model"
  - "human-oversight"
  - "ai-risk-management"
sources:
  - type: "standard"
    name: "ISO/IEC 22989:2022"
    reference: "Clausola 3.1.1 (Agent) e 5.4 (Autonomy levels)"
    url: "https://www.iso.org/standard/74296.html"
  - type: "standard"
    name: "NIST AI Governance Guidelines for Autonomous Systems (2025)"
    reference: "Section 4 (Agentic Behavior and Safeguards)"
    url: "https://www.nist.gov"
  - type: "scientifico"
    name: "Floridi, L. (2024)"
    reference: "On the Ethics and Governance of Autonomous AI Agents. Minds and Machines, 34(2)"
    url: "https://doi.org/10.1007/s11023-024-09670-w"
status: "approved"
version: "1.0.0"
lastUpdated: "2026-09-01"
---

# Agentic AI / IA agentica

### Inquadramento Concettuale
Il concetto di **IA agentica** (*Agentic AI*) descrive il passaggio dai modelli passivi di elaborazione del linguaggio o riconoscimento di pattern a entità software capaci di formulare piani autonomi, orchestrare strumenti esterni (API, calcolatori, database) e prendere decisioni esecutive in retroazione con l'ambiente.

### Sfide Etiche, Giuridiche e Tecniche
1. **Rottura del paradigma deterministico**: La capacità di adattamento continuo e di delega decisionale complica l'attribuzione di responsabilità giuridica secondo i canoni della colpa e del danno contrattuale/extracontrattuale.
2. **Supervisione Umana (*Human Oversight*)**: Con l'IA agentica il classico paradigma *Human-in-the-loop* (HITL) rischia di diventare impraticabile a causa della rapidità di esecuzione degli agenti, rendendo necessario transitare verso modelli *Human-on-the-loop* (HOTL) o *Human-in-command* con arresti d'emergenza (*kill switch*) verificabili.
3. **Allineamento e Controllo dei Rischi**: Gli standard NIST e ISO/IEC sottolineano la necessità di vincolare le funzioni di pianificazione (*planning modules*) a vincoli di sicurezza invalicabili (*guardrails*).
