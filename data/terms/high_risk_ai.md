---
id: "high-risk-ai"
uri: "https://w3id.org/aigov-thesaurus/concept/high-risk-ai"
prefLabel:
  en: "High-Risk AI System"
  it: "Sistema di IA ad alto rischio"
altLabel:
  en: ["High-Risk AI"]
  it: ["IA ad alto rischio", "Sistemi a rischio elevato"]
perspective:
  - "normativa-giuridica"
  - "tecnico-operativa"
definition:
  en: "An artificial intelligence system that poses significant risks to the health, safety, or fundamental rights of natural persons, subjecting it to stringent ex-ante compliance, conformity assessment, and risk management requirements under applicable regulations."
  it: "Un sistema di intelligenza artificiale che presenta rischi significativi per la salute, la sicurezza o i diritti fondamentali delle persone fisiche, e che è pertanto soggetto a stringenti requisiti di conformità ex-ante, valutazione di conformità e gestione del rischio previsti dalla normativa applicabile."
scopeNote:
  en: "Under the EU AI Act, high-risk systems are categorized through a dual mechanism: systems used as safety components of products subject to third-party conformity assessment (Annex I) and stand-alone systems in critical areas listed in Annex III."
  it: "Nel contesto del Regolamento UE 2024/1689, i sistemi ad alto rischio sono individuati tramite una doppia classificazione: componenti di sicurezza di prodotti soggetti a certificazione di terzi (Allegato I) e sistemi autonomi impiegati in settori critici elencati nell'Allegato III."
broader:
  - "ai-system"
narrower: []
related:
  - "ai-risk-management"
  - "human-oversight"
sources:
  - type: "normativa"
    name: "EU AI Act (Reg. UE 2024/1689)"
    reference: "Articolo 6, Allegati I e III"
    url: "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"
  - type: "normativa"
    name: "Convenzione Quadro Consiglio d'Europa sull'IA (CETS 225)"
    reference: "Articolo 16 (Valutazione e mitigazione dei rischi)"
    url: "https://www.coe.int"
  - type: "standard"
    name: "ISO/IEC 23894:2023"
    reference: "Clausola 6.2 (Risk Identification for High Impact Systems)"
    url: "https://www.iso.org/standard/77304.html"
status: "approved"
version: "1.0.0"
lastUpdated: "2026-09-01"
---

# High-Risk AI System / Sistema di IA ad alto rischio

### Inquadramento Concettuale
Il concetto di **Sistema ad alto rischio** è l'architrave dell'approccio basato sul rischio (*risk-based approach*) che caratterizza la governance europea ed internazionale dell'IA.

### Implicazioni Operative
I fornitori e gli utenti di sistemi ad alto rischio devono soddisfare requisiti vincolanti:
- Adozione di un sistema continuativo di gestione dei rischi (ISO/IEC 23894 e Art. 9 AI Act).
- Governance dei dati e mitigazione dei bias (Art. 10).
- Trasparenza e fornitura di istruzioni per l'uso (Art. 13).
- Progettazione orientata alla supervisione umana effettiva (*Human Oversight*, Art. 14).
