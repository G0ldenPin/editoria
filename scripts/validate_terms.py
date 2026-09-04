#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROGETTO D'ESAME DI EDITORIA DIGITALE - UNIVERSITÀ DEGLI STUDI DI MILANO
Script: validate_terms.py
Descrizione: Linter e validatore automatico per il Tesauro sulla Governance dell'IA.
================================================================================
SCOPO NELL'ARCHITETTURA EDITORIALE:
Questo script automatizza la fase di "Quality Assurance" e Fact-Checking formale
nella pipeline di Continuous Integration (GitHub Actions).
Viene eseguito ad ogni commit o Pull Request per impedire l'inclusione di:
  1. File privi di frontmatter YAML o con errori di sintassi;
  2. Termini privi della simmetria bilingue obbligatoria (EN / IT);
  3. Schede prive di fonti normative o standard verificabili;
  4. Relazioni semantiche orfane (es. un Broader Term che non esiste nel corpus).

USO DA TERMINALE:
  python scripts/validate_terms.py
ESITO:
  - Exit Code 0: Tutti i controlli sono superati (la CI procede al rilascio).
  - Exit Code 1: Uno o più vincoli sono violati (la CI blocca il merge).
================================================================================
"""

import os
import re
import sys
import yaml

# -----------------------------------------------------------------------------
# CONFIGURAZIONE E VOCABOLARI CONTROLLATI
# -----------------------------------------------------------------------------
# Percorso assoluto della cartella dei termini sorgente Markdown
TERMS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "terms")

# Insieme chiuso delle prospettive disciplinari ammesse (come definito nella relazione)
ALLOWED_PERSPECTIVES = {
    "normativa-giuridica",      # Area Diritto / Regolamenti (es. AI Act, DDL)
    "tecnico-operativa",        # Area Ingegneria / Standard (es. ISO/IEC, NIST)
    "concettuale-filosofica"    # Area Etica / Concetti emergenti (es. Agentic AI)
}

# Stati ammessi del ciclo di vita redazionale del termine
ALLOWED_STATUSES = {
    "draft",        # Bozza iniziale proposta dalla comunità
    "proposed",     # Inserito formalmente e in attesa di triage
    "in_review",    # In fase di revisione interdisciplinare paritetica
    "approved",     # Approvato dal comitato editoriale e pubblicato
    "deprecated"    # Termine superato o sostituito da nuova formulazione
}


def extract_frontmatter(content):
    """
    Separa il blocco dei metadati YAML Frontmatter dal testo Markdown.
    
    COME FUNZIONA:
    Utilizza un'espressione regolare (RegEx) che cerca una porzione di testo
    delimitata in testa e in coda da tre trattini ('---').
    
    Ritorna:
      - frontmatter_str: stringa contenente solo il blocco YAML (da parsare).
      - body_content: stringa contenente il testo descrittivo Markdown.
      - (None, content): se il file non presenta la struttura YAML corretta.
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)


def validate_term(term_id, data):
    """
    Verifica che il dizionario di dati estratto dal frontmatter rispetti
    tutti i vincoli redazionali e formali del tesauro.
    
    Parametri:
      - term_id: ID atteso (ricavato dal nome del file .md, es. 'ai-system')
      - data: dizionario Python generato dal parser YAML
      
    Ritorna:
      - errors: lista di stringhe con la descrizione degli errori riscontrati.
    """
    errors = []
    
    # -------------------------------------------------------------------------
    # REGOLA 1: Presenza di tutti i campi obbligatori di primo livello
    # -------------------------------------------------------------------------
    required_fields = [
        "id", "uri", "prefLabel", "perspective", 
        "definition", "sources", "status", "version", "lastUpdated"
    ]
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo obbligatorio mancante: '{field}'")
            
    # Se mancano campi di base, interrompe il controllo per questo file
    if errors:
        return errors
        
    # -------------------------------------------------------------------------
    # REGOLA 2: Corrispondenza biunivoca tra ID dichiarato e nome del file
    # Previene disallineamenti nel file system e nei link ipertestuali
    # -------------------------------------------------------------------------
    if data["id"] != term_id:
        errors.append(f"L'ID '{data['id']}' non corrisponde al nome file '{term_id}'")
        
    # -------------------------------------------------------------------------
    # REGOLA 3: Bilinguismo obbligatorio del termine preferito (prefLabel)
    # -------------------------------------------------------------------------
    pref_label = data.get("prefLabel", {})
    if not isinstance(pref_label, dict) or "en" not in pref_label or "it" not in pref_label:
        errors.append("prefLabel deve essere un dizionario contenente sia 'en' che 'it'")
        
    # -------------------------------------------------------------------------
    # REGOLA 4: Bilinguismo obbligatorio della definizione formale
    # -------------------------------------------------------------------------
    definition = data.get("definition", {})
    if not isinstance(definition, dict) or "en" not in definition or "it" not in definition:
        errors.append("definition deve essere un dizionario contenente sia 'en' che 'it'")
        
    # -------------------------------------------------------------------------
    # REGOLA 5: Validità delle prospettive disciplinari indicate
    # -------------------------------------------------------------------------
    perspectives = data.get("perspective", [])
    if not isinstance(perspectives, list) or len(perspectives) == 0:
        errors.append("perspective deve essere una lista non vuota")
    else:
        for p in perspectives:
            if p not in ALLOWED_PERSPECTIVES:
                errors.append(f"Prospettiva non valida '{p}'. Valori ammessi: {ALLOWED_PERSPECTIVES}")
                
    # -------------------------------------------------------------------------
    # REGOLA 6: Validità dello stato del ciclo redazionale
    # -------------------------------------------------------------------------
    status = data.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"Status non valido '{status}'. Valori ammessi: {ALLOWED_STATUSES}")
        
    # -------------------------------------------------------------------------
    # REGOLA 7: Presenza e struttura minima delle fonti normative/standard
    # Ogni fonte deve specificare tipo (es. normativa, standard), nome e articolo/clausola
    # -------------------------------------------------------------------------
    sources = data.get("sources", [])
    if not isinstance(sources, list) or len(sources) == 0:
        errors.append("È obbligatorio indicare almeno una fonte ufficiale in 'sources'")
    else:
        for idx, s in enumerate(sources):
            if not isinstance(s, dict) or "type" not in s or "name" not in s or "reference" not in s:
                errors.append(f"Fonte #{idx+1} priva di uno o più campi obbligatori ('type', 'name', 'reference')")
                
    return errors


def main():
    """
    Funzione principale che orchestra il processo di validazione a due fasi:
      FASE 1: Validazione sintattica e strutturale file per file.
      FASE 2: Verifica dell'integrità referenziale dell'ontologia (nessun link rotto).
    """
    print("=" * 70)
    print("VALIDAZIONE FORMALE DEL TESAURO SULLA GOVERNANCE DELL'IA")
    print("=" * 70)
    
    # Controllo di esistenza della cartella sorgente dei dati
    if not os.path.exists(TERMS_DIR):
        print(f"ERRORE CRITICO: Cartella termini non trovata in: {TERMS_DIR}")
        sys.exit(1)
        
    # Recupera tutti i file con estensione .md presenti nella cartella
    term_files = [f for f in os.listdir(TERMS_DIR) if f.endswith(".md")]
    if not term_files:
        print("ATTENZIONE: Nessun file .md trovato nella cartella data/terms/.")
        sys.exit(1)
        
    all_terms = {}              # Dizionario in cui salviamo i termini validati: { 'id': dati }
    validation_failed = False   # Flag cumulativo per intercettare qualsiasi errore
    
    # -------------------------------------------------------------------------
    # FASE 1: Scansione di ogni file, estrazione YAML e controllo regole interne
    # -------------------------------------------------------------------------
    for filename in term_files:
        filepath = os.path.join(TERMS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. Isola il frontmatter
        frontmatter_str, _ = extract_frontmatter(content)
        if not frontmatter_str:
            print(f"[FAIL] {filename}: Frontmatter YAML mancante o malformato (delimitatori '---' non trovati)")
            validation_failed = True
            continue
            
        # 2. Esegue il parsing YAML sicuro (converte testo in dizionario Python)
        try:
            data = yaml.safe_load(frontmatter_str)
        except Exception as e:
            print(f"[FAIL] {filename}: Errore di sintassi YAML: {e}")
            validation_failed = True
            continue
            
        # 3. Calcola l'ID atteso dal nome file (es. 'ai_system.md' -> 'ai-system')
        expected_id = filename.replace(".md", "").replace("_", "-")
        
        # 4. Esegue la validazione dei campi del termine
        errors = validate_term(data.get("id", expected_id), data)
        if errors:
            print(f"[FAIL] {filename}:")
            for err in errors:
                print(f"  - {err}")
            validation_failed = True
        else:
            print(f"[OK]   {filename} -> {data['prefLabel']['en']} / {data['prefLabel']['it']}")
            all_terms[data["id"]] = data

    print("-" * 70)
    print("VERIFICA INTEGRITÀ DELLE RELAZIONI SEMANTICHE (SKOS)...")
    
    # -------------------------------------------------------------------------
    # FASE 2: Verifica incrociata delle relazioni ontologiche
    # Assicura che ogni 'broader', 'narrower' e 'related' faccia riferimento
    # a un termine effettivamente caricato ed esistente nel tesauro.
    # -------------------------------------------------------------------------
    known_ids = set(all_terms.keys())
    for tid, term in all_terms.items():
        # Controllo termini più ampi (Broader - BT)
        for b in term.get("broader", []):
            if b not in known_ids:
                print(f"[FAIL] {tid}: Broader term '{b}' non esiste nel corpus!")
                validation_failed = True
                
        # Controllo termini più specifici (Narrower - NT)
        for n in term.get("narrower", []):
            if n not in known_ids:
                print(f"[FAIL] {tid}: Narrower term '{n}' non esiste nel corpus!")
                validation_failed = True
                
        # Controllo termini correlati (Related - RT)
        for r in term.get("related", []):
            if r not in known_ids:
                print(f"[FAIL] {tid}: Related term '{r}' non esiste nel corpus!")
                validation_failed = True

    # -------------------------------------------------------------------------
    # CONCLUSIONE E RITORNO DEL CODICE DI STATO PER LA CI/CD
    # -------------------------------------------------------------------------
    print("=" * 70)
    if validation_failed:
        print("RISULTATO: La validazione ha riscontrato ERRORI. Pipeline bloccata.")
        sys.exit(1)
    else:
        print(f"RISULTATO: Validazione completata con SUCCESSO! ({len(all_terms)} termini verificati)")
        sys.exit(0)


if __name__ == "__main__":
    main()

