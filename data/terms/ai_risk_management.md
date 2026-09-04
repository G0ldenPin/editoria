---
id: "ai-risk-management"
uri: "https://w3id.org/aigov-thesaurus/concept/ai-risk-management"
prefLabel:
  en: "AI Risk Management"
  it: "Gestione del rischio dell'IA"
altLabel:
  en: ["AI Risk Assessment", "Risk Management System"]
  it: ["Sistema di gestione dei rischi", "Valutazione dei rischi dell'IA"]
perspective:
  - "tecnico-operativa"
  - "normativa-giuridica"
definition:
  en: "A continuous, iterative process implemented throughout the entire lifecycle of an AI system to identify, estimate, evaluate, mitigate, and monitor risks, ensuring safety, security, trustworthiness, and adherence to legal and ethical standards."
  it: "Un processo continuo e iterativo implementato durante l'intero ciclo di vita di un sistema di IA per identificare, stimare, valutare, mitigare e monitorare i rischi, garantendo sicurezza, affidabilità e rispetto degli standard legali ed etici."
scopeNote:
  en: "Harmonized framework combining ISO/IEC 23894:2023 guidelines with the NIST AI RMF core functions (Govern, Map, Measure, Manage) and Article 9 compliance under the EU AI Act."
  it: "Quadro metodologico armonizzato che combina le linee guida dello standard ISO/IEC 23894:2023 con le funzioni cardine del NIST AI RMF (Govern, Map, Measure, Manage) e con i requisiti dell'Art. 9 dell'AI Act europeo."
broader: []
narrower: []
related:
  - "high-risk-ai"
  - "ai-system"
  - "human-oversight"
sources:
  - type: "standard"
    name: "ISO/IEC 23894:2023"
    reference: "Clausola 5 (AI Risk Management Process) e Clausola 6"
    url: "https://www.iso.org/standard/77304.html"
  - type: "standard"
    name: "NIST AI Risk Management Framework (NIST AI RMF 1.0)"
    reference: "Part 1 (Foundational Information) e Part 2 (Core Functions)"
    url: "https://www.nist.gov/itl/ai-risk-management-framework"
  - type: "normativa"
    name: "EU AI Act (Reg. UE 2024/1689)"
    reference: "Articolo 9 (Sistema di gestione dei rischi)"
    url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"
status: "approved"
version: "1.0.0"
lastUpdated: "2026-09-01"
---

# AI Risk Management / Gestione del rischio dell'IA

### Inquadramento Concettuale
La **Gestione del rischio dell'IA** rappresenta il punto di convergenza fondamentale tra la conformità normativa e le pratiche ingegneristiche di sviluppo software. Supera l'approccio statico della certificazione *una tantum* introducendo un controllo iterativo lungo tutto il ciclo di vita del sistema (*life-cycle approach*).

### Le Funzioni Cardine
1. **Govern (Governance)**: Definizione di politiche, ruoli, responsabilità e cultura della trasparenza.
2. **Map (Mappatura)**: Comprensione del contesto, degli stakeholder, delle interazioni socio-tecniche e dei potenziali impatti.
3. **Measure (Misurazione)**: Quantificazione e analisi qualitativa dei rischi, testing, metriche di robustezza e bias.
4. **Manage (Gestione)**: Applicazione di controlli tecnici e organizzativi di mitigazione del rischio residuo.
