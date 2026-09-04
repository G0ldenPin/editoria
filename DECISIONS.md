# Registro delle Decisioni Editoriali (Editorial Decision Records - EDR)

Il presente documento costituisce l'archivio pubblico e immutabile delle delibere assunte dal Comitato Editoriale Interdisciplinare del **Tesauro sulla Governance dell'Intelligenza Artificiale**. 
In ottemperanza ai principi di trasparenza, verificabilità scientifica e tracciabilità del workflow documentale, ogni decisione di approvazione, modifica o rigetto viene verbalizzata pubblicamente.

---

## Struttura di un Record Decisionale (EDR)
Ogni delibera segue il seguente schema formale:
- **ID Record**: `EDR-YYYY-NNN`
- **Data Delibera**: ISO 8601 (`YYYY-MM-DD`)
- **Termine Oggetto**: `[ID Termine]` - `[prefLabel EN / IT]`
- **Tipologia**: `Nuovo Termine` | `Revisione Definizione` | `Aggiunta Relazione` | `Rigetto Proposta`
- **Issue/PR di Riferimento**: Link all'issue pubblica di tracciamento
- **Revisori Coinvolti**:
  - *Revisore Giuridico-Normativo*
  - *Revisore Tecnico-Operativo*
  - *Revisore Concettuale-Filosofico*
- **Esito**: `APPROVATO` | `APPROVATO CON MODIFICHE` | `RESPINTO`
- **Motivazione Pubblica**: Giustificazione argomentata con citazione puntuale delle fonti e degli standard.

---

## Registro Storico delle Decisioni

### EDR-2026-001: Inclusione del termine "Agentic AI / IA agentica"
- **Data**: 2026-08-25
- **Termine**: `agentic-ai` (Agentic AI / IA agentica)
- **Tipologia**: Nuovo Termine
- **Issue di Riferimento**: #12
- **Revisori**:
  - *Dr. E. Rossi* (Esperto Normativo)
  - *Ing. M. Bianchi* (Esperto Tecnico)
  - *Prof.ssa S. Conti* (Esperta Filosofico-Etica)
- **Esito**: `APPROVATO CON MODIFICHE`
- **Giustificazione Pubblica**:
  > La proposta iniziale (#12) qualificava l'IA agentica esclusivamente come "sistema software capace di agire indipendentemente da qualsiasi intenzione umana". 
  > Il comitato, dopo esame congiunto, ha deliberato di respingere tale formulazione per evitare allucinazioni ontologiche incompatibili con il quadro normativo europeo (Art. 14 AI Act sulla necessaria supervisione umana) e con la clausola 3.1.1 di ISO/IEC 22989:2022.
  > È stata approvata all'unanimità una definizione armonizzata che caratterizza l'IA agentica sulla base di "obiettivi complessi perseguiti con livelli elevati di autonomia, pianificazione ed interazione con l'ambiente", collegandola tassonomicamente come *Narrower Term* di `ai-system` e istituendo una relazione associativa (*Related Term*) obbligatoria con `human-oversight`.

---

### EDR-2026-002: Armonizzazione della definizione di "AI System"
- **Data**: 2026-08-28
- **Termine**: `ai-system` (Artificial Intelligence System / Sistema di Intelligenza Artificiale)
- **Tipologia**: Revisione Definizione
- **Issue di Riferimento**: #15
- **Revisori**:
  - *Dr. E. Rossi* (Esperto Normativo)
  - *Ing. M. Bianchi* (Esperto Tecnico)
- **Esito**: `APPROVATO`
- **Giustificazione Pubblica**:
  > Con l'entrata in vigore definitiva del Regolamento UE 2024/1689 (AI Act) e la pubblicazione del recepimento nel DDL italiano del 2025, si è resa necessaria la piena convergenza testuale con l'Articolo 3(1). 
  > La precedente bozza conteneva riferimenti generici all'approccio logico/statistico della prima proposta Commissione 2021. La nuova formulazione è perfettamente speculare alla definizione concordata OCSE 2023 e ISO/IEC 22989:2022.

---

### EDR-2026-003: Rigetto della proposta di inclusione del termine "Soggettività Giuridica dell'IA"
- **Data**: 2026-09-02
- **Termine Proposto**: `ai-legal-personhood`
- **Tipologia**: Nuovo Termine
- **Issue di Riferimento**: #23
- **Revisori**:
  - *Dr. E. Rossi* (Esperto Normativo)
  - *Prof.ssa S. Conti* (Esperta Filosofico-Etica)
- **Esito**: `RESPINTO`
- **Giustificazione Pubblica**:
  > La proposta non soddisfa i criteri di ammissibilità fissati dalle linee guida editoriali.
  > Dal punto di vista del diritto positivo europeo e comparato (AI Act e Convenzione quadro del Consiglio d'Europa CETS 225), la soggettività giuridica per i sistemi algoritmici non trova alcun riscontro normativo, confermando l'attribuzione della responsabilità esclusivamente a fornitori, deployer e persone fisiche. 
  > Sebbene il tema sia oggetto di dibattito dottrinale speculativo, non rappresenta allo stato attuale un termine controllato funzionale alla governance operativa e normativa dell'IA. Il termine potrà essere riconsiderato unicamente qualora dovessero emergere orientamenti giurisprudenziali o legislativi vincolanti.
