---
id: "human-oversight"
uri: "https://w3id.org/aigov-thesaurus/concept/human-oversight"
prefLabel:
  en: "Human Oversight"
  it: "Supervisione umana"
altLabel:
  en: ["Human-in-the-loop", "Human Control", "Human-on-the-loop"]
  it: ["Controllo umano", "Supervisione umana attiva", "Uomo nel circuito"]
perspective:
  - "normativa-giuridica"
  - "tecnico-operativa"
  - "concettuale-filosofica"
definition:
  en: "Measures and design choices enabling natural persons to effectively oversee, monitor, intervene in, or override the operation of an AI system, preventing or minimizing risks to health, safety, fundamental rights, and human autonomy."
  it: "Insieme delle misure e scelte progettuali che consentono a persone fisiche di sorvegliare, monitorare, intervenire o sovrascrivere efficacemente il funzionamento di un sistema di IA, prevenendo o minimizzando i rischi per la salute, la sicurezza, i diritti fondamentali e l'autonomia umana."
scopeNote:
  en: "Article 14 of the EU AI Act mandates human oversight for high-risk AI systems. Articulated in three operational modes: human-in-the-loop (HITL), human-on-the-loop (HOTL), and human-in-command (HIC)."
  it: "L'Articolo 14 dell'AI Act impone la supervisione umana per i sistemi ad alto rischio. Essa si declina tecnicamente in tre modalità: uomo nel circuito (HITL), uomo sul circuito (HOTL) e uomo al comando (HIC)."
broader: []
narrower: []
related:
  - "ai-system"
  - "high-risk-ai"
  - "agentic-ai"
  - "ai-risk-management"
sources:
  - type: "normativa"
    name: "EU AI Act (Reg. UE 2024/1689)"
    reference: "Articolo 14 (Supervisione umana)"
    url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"
  - type: "normativa"
    name: "Convenzione Quadro Consiglio d'Europa sull'IA (CETS 225)"
    reference: "Articolo 13 (Autonomia umana e supervisione)"
    url: "https://www.coe.int"
  - type: "standard"
    name: "NIST AI RMF 1.0"
    reference: "Govern 1.2 e Govern 1.3"
    url: "https://www.nist.gov/itl/ai-risk-management-framework"
  - type: "standard"
    name: "ISO/IEC 22989:2022"
    reference: "Clausola 3.4.11 (Human-machine teaming and oversight)"
    url: "https://www.iso.org/standard/74296.html"
status: "approved"
version: "1.0.0"
lastUpdated: "2026-09-01"
---

# Human Oversight / Supervisione umana

### Inquadramento Concettuale
La **Supervisione umana** rappresenta il principio cardine dell'approccio antropocentrico (*human-centric*) promosso dalle istituzioni europee ed internazionali. Si contrappone a qualsiasi forma di automazione de-responsabilizzante e garantisce la primazia dell'essere umano sulle decisioni algoritmiche.

### Declinazione Interdisciplinare
1. **Diritto**: Requisito cogente di liceità per i sistemi ad alto rischio (Art. 14 AI Act); presupposto per l'imputabilità della responsabilità giuridica.
2. **Tecnologia**: Implementazione di interfacce persona-macchina (HCI), pulsanti di arresto d'emergenza (*stop button*), e meccanismi che prevengano il fenomeno dell'*automation bias* (la tendenza degli operatori a fidarsi ciecamente dell'output del sistema).
3. **Filosofia ed Etica**: Salvaguardia dell'autonomia e dell'agenzia morale umana di fronte a sistemi predittivi e decisionali.
