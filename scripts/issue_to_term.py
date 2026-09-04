#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROGETTO D'ESAME DI EDITORIA DIGITALE - UNIVERSITÀ DEGLI STUDI DI MILANO
Script: issue_to_term.py
Descrizione: Convertitore automatico da GitHub Issue Form a Termine Markdown/YAML.
================================================================================
SCOPO NELL'ARCHITETTURA EDITORIALE (CHATOPS / LABEL-DRIVEN CI/CD):
Questo script automatizza la transizione dalla proposta della comunità (Issue)
alla scheda formale del termine (data/terms/<id>.md).
Viene eseguito dalla GitHub Action 'publish_on_approval.yml' quando il Chief Editor
assegna l'etichetta 'approved' a una issue di proposta nuovo termine.

Può anche essere eseguito manualmente in locale per test o dimostrazione all'esame:
  python scripts/issue_to_term.py --demo
  python scripts/issue_to_term.py --file path/to/issue.md --issue-number 42
================================================================================
"""

import argparse
from datetime import datetime
import os
import re
import sys
import yaml

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS_DIR = os.path.join(ROOT_DIR, "data", "terms")
DECISIONS_FILE = os.path.join(ROOT_DIR, "DECISIONS.md")

DEMO_ISSUE_BODY = """### Termine in Inglese (Preferred Label EN)*

Algorithmic Bias

### Termine in Italiano (Preferred Label IT)*

Bias Algoritmico

### Varianti terminologiche o sinonimi (AltLabels)

Bias dell'IA, Distorsione algoritmica, AI Bias

### Prospettiva Primaria di Riferimento*

- tecnico-operativa
- normativa-giuridica

### Proposta di Definizione in Inglese*

Systematic and repeatable errors in a computer system that create unfair outcomes, such as privileging one arbitrary group of users over others.

### Proposta di Definizione in Italiano*

Errori sistematici e ripetibili in un sistema informatico che producono esiti iniqui, favorendo arbitrariamente determinati gruppi di utenti rispetto ad altri.

### Motivazione dell'Inclusione nel Tesauro*

Il concetto di bias algoritmico è centrale per la prevenzione delle discriminazioni nell'AI Act (Art. 10 sui requisiti di qualità dei dati) e costituisce la metrica fondamentale di verifica tecnica secondo lo standard ISO/IEC 24027.

### Fonti Normative, Standard o Documenti Ufficiali a Supporto*

- [STANDARD] ISO/IEC 24027:2021 — Clausola 3.1 (Bias in AI systems and AI aided decision making)
- [NORMATIVA] EU AI Act (Reg. UE 2024/1689) — Articolo 10, paragrafo 2, lettera f
"""

def slugify(text):
    """Converte un testo in uno slug valido per ID e nome file (es. 'Algorithmic Bias' -> 'algorithmic-bias')."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")

def parse_issue_sections(body):
    """
    Estrae le sezioni dell'Issue Form generate da GitHub Markdown.
    GitHub formatta ogni campo dell'Issue Form come '### Titolo del campo\n\nValore'.
    """
    sections = {}
    pattern = r"###\s+([^\n]+)\n+(.*?)(?=(?:\n###\s+[^\n]+)|\Z)"
    matches = re.findall(pattern, body, re.DOTALL)
    for title, content in matches:
        clean_title = title.replace("*", "").strip()
        sections[clean_title] = content.strip()
    return sections

def find_section(sections, keywords):
    """Cerca una sezione confrontando parole chiave nel titolo."""
    for title, content in sections.items():
        title_lower = title.lower()
        if any(k.lower() in title_lower for k in keywords):
            return content
    return ""

def parse_sources(sources_text):
    """
    Estrae le fonti da elenchi puntati formattati come:
    - [TIPO] NomeFonte — Riferimento
    oppure semplici linee di testo.
    """
    sources = []
    lines = [line.strip().lstrip("-*").strip() for line in sources_text.splitlines() if line.strip()]
    
    for line in lines:
        if not line or line.startswith("http"):
            continue
        # Estrae tipo se presente [STANDARD] o [NORMATIVA]
        stype = "standard" if any(w in line.lower() for w in ["iso", "ieee", "nist", "standard"]) else "normativa"
        
        # Prova a separare nome e riferimento da trattino lungo o doppio trattino
        parts = re.split(r"—|--|-", line, maxsplit=1)
        if len(parts) == 2:
            sname = re.sub(r"\[.*?\]", "", parts[0]).strip()
            sref = parts[1].strip()
        else:
            sname = line
            sref = "Consultazione documentale ufficiale"
            
        sources.append({
            "type": stype,
            "name": sname,
            "reference": sref,
            "url": "https://eur-lex.europa.eu" if stype == "normativa" else "https://www.iso.org"
        })
        
    if not sources:
        sources.append({
            "type": "normativa",
            "name": "Riferimento ufficiale indicato nell'Issue",
            "reference": "Clausola definitoria",
            "url": "https://eur-lex.europa.eu"
        })
    return sources

def convert_issue_to_term(issue_body, issue_number=None):
    """
    Esegue il parsing dei campi dell'issue e genera il file .md in data/terms/.
    """
    sections = parse_issue_sections(issue_body)
    
    term_en = find_section(sections, ["Inglese", "Preferred Label EN", "term_en"])
    term_it = find_section(sections, ["Italiano", "Preferred Label IT", "term_it"])
    synonyms_raw = find_section(sections, ["sinonimi", "altlabel", "varianti"])
    persp_raw = find_section(sections, ["prospettiva", "perspectives"])
    def_en = find_section(sections, ["Definizione in Inglese", "definition_en"])
    def_it = find_section(sections, ["Definizione in Italiano", "definition_it"])
    rationale = find_section(sections, ["motivazione", "rationale"])
    sources_raw = find_section(sections, ["fonti", "sources"])
    
    if not term_en or not term_it or not def_en or not def_it:
        raise ValueError("Impossibile convertire l'issue: mancano i campi obbligatori (termini bilingui o definizioni).")
        
    term_id = slugify(term_en)
    file_id = term_id.replace("-", "_")
    filepath = os.path.join(TERMS_DIR, f"{file_id}.md")
    
    # Parsing sinonimi
    alt_labels_en = []
    alt_labels_it = []
    if synonyms_raw:
        items = [s.strip() for s in re.split(r"[,;\n]", synonyms_raw) if s.strip()]
        alt_labels_en = items[:2]
        alt_labels_it = items[2:] if len(items) > 2 else items[:2]
        
    # Parsing prospettive
    allowed = {"normativa-giuridica", "tecnico-operativa", "concettuale-filosofica"}
    perspectives = []
    for p in allowed:
        if p in persp_raw.lower():
            perspectives.append(p)
    if not perspectives:
        perspectives = ["tecnico-operativa", "normativa-giuridica"]
        
    # Parsing fonti
    sources = parse_sources(sources_raw)
    
    # Data odierna
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Struttura Frontmatter YAML
    term_data = {
        "id": term_id,
        "uri": f"https://w3id.org/aigov-thesaurus/concept/{term_id}",
        "prefLabel": {
            "en": term_en,
            "it": term_it
        },
        "altLabel": {
            "en": alt_labels_en if alt_labels_en else [term_en],
            "it": alt_labels_it if alt_labels_it else [term_it]
        },
        "perspective": perspectives,
        "definition": {
            "en": def_en,
            "it": def_it
        },
        "scopeNote": {
            "en": f"Approved entry based on proposal #{issue_number if issue_number else 'N/A'}. Motivated for AI governance alignment.",
            "it": f"Voce approvata sulla base della proposta #{issue_number if issue_number else 'N/A'}. Allineamento per la governance dell'IA."
        },
        "broader": ["ai-system"],
        "narrower": [],
        "related": ["ai-risk-management"],
        "sources": sources,
        "status": "approved",
        "version": "1.0.0",
        "lastUpdated": today_str
    }
    
    yaml_frontmatter = yaml.dump(term_data, sort_keys=False, allow_unicode=True, default_flow_style=False)
    
    markdown_body = f"""---
{yaml_frontmatter}---

# {term_en} / {term_it}

### Inquadramento Concettuale
Il termine **{term_it}** ({term_en}) è stato introdotto nel vocabolario controllato su proposta approvata dal comitato interdisciplinare.

### Motivazione della Decisione Editoriale
{rationale if rationale else 'Definizione inserita a presidio della trasparenza e mitigazione del rischio nei sistemi algoritmici.'}
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_body)
        
    print(f"[SUCCESSO] Scheda termine creata: {filepath}")
    
    # Aggiornamento DECISIONS.md
    record_edr = append_edr(term_id, term_en, term_it, rationale, issue_number, today_str)
    print(f"[SUCCESSO] Registro DECISIONS.md aggiornato con {record_edr}")
    
    return filepath

def append_edr(term_id, term_en, term_it, rationale, issue_number, today_str):
    """Aggiunge una voce EDR a DECISIONS.md."""
    if not os.path.exists(DECISIONS_FILE):
        return ""
        
    with open(DECISIONS_FILE, "r", encoding="utf-8") as f:
        decisions_content = f.read()
        
    # Calcola il prossimo progressivo EDR
    edr_matches = re.findall(r"EDR-\d{4}-(\d{3})", decisions_content)
    next_idx = max([int(m) for m in edr_matches], default=3) + 1
    record_id = f"EDR-2026-{next_idx:03d}"
    
    entry = f"""
---

### {record_id}: Inclusione automatica del termine \"{term_en} / {term_it}\"
- **Data**: {today_str}
- **Termine**: `{term_id}` ({term_en} / {term_it})
- **Tipologia**: Nuovo Termine (Flusso da GitHub Issue)
- **Issue di Riferimento**: #{issue_number if issue_number else 'Automated'}
- **Revisori**:
  - *Chief Editor* (Amministrazione e Triage)
  - *Comitato Interdisciplinare* (Consenso accertato con label 'approved')
- **Esito**: `APPROVATO`
- **Giustificazione Pubblica**:
  > {rationale.strip() if rationale else 'Proposta validata formalmente e approvata dal comitato con delibera su GitHub.'}
"""
    
    with open(DECISIONS_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
        
    return record_id

def main():
    parser = argparse.ArgumentParser(description="Genera un termine Markdown da un'Issue di GitHub")
    parser.add_argument("--file", help="Percorso a un file contenente il corpo dell'Issue")
    parser.add_argument("--issue-body", help="Testo raw del corpo dell'Issue")
    parser.add_argument("--issue-number", default="1", help="Numero dell'Issue di GitHub")
    parser.add_argument("--demo", action="store_true", help="Esegue la conversione con una issue di prova")
    args = parser.parse_args()
    
    # 1. Recupero del corpo dell'issue
    if args.demo:
        print("[DEMO] Utilizzo della proposta di esempio: 'Algorithmic Bias'...")
        body = DEMO_ISSUE_BODY
        num = "25"
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            body = f.read()
        num = args.issue_number
    elif args.issue_body:
        body = args.issue_body
        num = args.issue_number
    elif "ISSUE_BODY" in os.environ:
        body = os.environ["ISSUE_BODY"]
        num = os.environ.get("ISSUE_NUMBER", "1")
    else:
        print("ERRORE: Nessun testo issue fornito. Usa --demo, --file o imposta la variabile d'ambiente ISSUE_BODY.")
        sys.exit(1)
        
    try:
        filepath = convert_issue_to_term(body, num)
        print(f"Elaborazione completata. File generato in: {filepath}")
    except Exception as e:
        print(f"[ERRORE]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
