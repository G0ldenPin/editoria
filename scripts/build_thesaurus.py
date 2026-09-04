#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROGETTO D'ESAME DI EDITORIA DIGITALE - UNIVERSITÀ DEGLI STUDI DI MILANO
Script: build_thesaurus.py
Descrizione: Generatore automatico degli artefatti finali di pubblicazione.
================================================================================
SCOPO NELL'ARCHITETTURA EDITORIALE:
Questo script implementa il paradigma del "Single Source of Truth" (SSOT):
a partire da un unico insieme di file sorgente leggibili (Markdown + YAML),
compila simultaneamente due canali di distribuzione multicanale:
  1. dist/thesaurus.json : Dataset strutturato per l'interoperabilità software
                           e il riuso secondo i principi degli Open Data;
  2. dist/index.html     : Portale web statico, interattivo, bilingue, accessibile
                           e responsive, pronto per il deploy su GitHub Pages.

VANTAGGI PER L'ESAME:
  - Nessuna dipendenza complessa (richiede solo Python standard e PyYAML);
  - Generazione di un sito statico puro (HTML/CSS/JS) a zero costi di hosting;
  - Prestazioni elevatissime e tempo di caricamento istantaneo nel browser.
================================================================================
"""

import json
import os
import re
import sys
import yaml

# -----------------------------------------------------------------------------
# DEFINIZIONE DEI PERCORSI DEL PROGETTO
# -----------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS_DIR = os.path.join(ROOT_DIR, "data", "terms")     # Cartella sorgenti
DIST_DIR = os.path.join(ROOT_DIR, "dist")              # Cartella di distribuzione (artefatti)


def extract_frontmatter(content):
    """
    Separa i metadati YAML dal testo Markdown del termine tramite RegEx.
    Ritorna una tupla: (stringa_yaml, testo_markdown).
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)


def load_terms():
    """
    Carica tutti i termini Markdown dalla cartella data/terms/:
      1. Legge ciascun file .md;
      2. Isola e deserializza il frontmatter YAML con yaml.safe_load;
      3. Allega il corpo descrittivo Markdown nel campo 'content_md';
      4. Ordina i termini alfabeticamente in base all'etichetta inglese.
    
    Ritorna:
      - lista di dizionari con i dati completi di ogni termine.
    """
    terms = []
    for filename in os.listdir(TERMS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(TERMS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            fm_str, body = extract_frontmatter(content)
            if fm_str:
                data = yaml.safe_load(fm_str)
                data["content_md"] = body.strip()
                terms.append(data)
                
    # Ordinamento alfabetico per etichetta inglese per facilitare la consultazione
    terms.sort(key=lambda x: x["prefLabel"]["en"])
    return terms


def build_web_portal(terms, output_path):
    """
    Genera un'applicazione web statica autonoma (Single-Page Application in HTML5/CSS3/JS)
    incorporando l'intero dataset dei termini all'interno della pagina.
    
    Caratteristiche progettuali:
      - Palette cromatica formale conforme a linee guida di accessibilità WCAG 2.1 AA;
      - Ricerca istantanea full-text bilingue lato client (zero chiamate a server esterni);
      - Filtri combinati per prospettiva disciplinare e fonte/standard normativo;
      - Navigazione ipertestuale delle relazioni (Broader, Narrower, Related) con smooth scrolling;
      - Toggle immediato per la visualizzazione con priorità linguistica IT o EN.
    """
    terms_json = json.dumps(terms, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesauro sulla Governance dell'Intelligenza Artificiale | AI Governance Thesaurus</title>
    <style>
        :root {{
            --primary: #1a365d;
            --primary-light: #2b6cb0;
            --accent: #319795;
            --bg: #f7fafc;
            --card-bg: #ffffff;
            --text: #2d3748;
            --text-muted: #718096;
            --border: #e2e8f0;
            --tag-legal: #e2e8f0;
            --tag-tech: #bee3f8;
            --tag-phil: #feebc8;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        header {{
            background: linear-gradient(135deg, var(--primary) 0%, #2c5282 100%);
            color: white;
            padding: 2.5rem 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        header h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 700; }}
        header p {{ font-size: 1.1rem; opacity: 0.9; max-width: 800px; margin: 0 auto 1.5rem; }}
        .badge-bar {{ display: flex; justify-content: center; gap: 0.75rem; flex-wrap: wrap; }}
        .badge {{ background: rgba(255,255,255,0.15); padding: 0.3rem 0.8rem; border-radius: 9999px; font-size: 0.85rem; }}
        
        .main-container {{
            max-width: 1200px;
            margin: -1.5rem auto 3rem;
            padding: 0 1rem;
        }}
        .controls-card {{
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.07);
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        .search-bar {{
            width: 100%;
            padding: 0.85rem 1.2rem;
            font-size: 1.05rem;
            border: 2px solid var(--border);
            border-radius: 8px;
            transition: border-color 0.2s;
        }}
        .search-bar:focus {{ outline: none; border-color: var(--primary-light); }}
        
        .filter-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            align-items: center;
            justify-content: space-between;
        }}
        .filter-group {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.95rem; }}
        .filter-group label {{ font-weight: 600; color: var(--primary); }}
        select, .btn-toggle {{
            padding: 0.45rem 0.8rem;
            border-radius: 6px;
            border: 1px solid var(--border);
            background: white;
            font-size: 0.9rem;
            cursor: pointer;
        }}
        .btn-toggle.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }}
        .concept-card {{
            background: var(--card-bg);
            border-radius: 10px;
            border: 1px solid var(--border);
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .concept-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        }}
        .card-header {{ margin-bottom: 1rem; }}
        .card-title {{ font-size: 1.35rem; color: var(--primary); margin-bottom: 0.25rem; }}
        .card-subtitle {{ font-size: 1rem; color: var(--text-muted); font-style: italic; }}
        .perspectives-bar {{ display: flex; gap: 0.4rem; margin-top: 0.6rem; flex-wrap: wrap; }}
        .tag {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 700;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
        }}
        .tag-normativa-giuridica {{ background: #c6f6d5; color: #22543d; }}
        .tag-tecnico-operativa {{ background: #bee3f8; color: #2a4365; }}
        .tag-concettuale-filosofica {{ background: #feebc8; color: #744210; }}
        
        .card-body {{ margin-bottom: 1.2rem; }}
        .def-text {{ font-size: 0.95rem; margin-bottom: 0.75rem; }}
        .scope-note {{
            font-size: 0.85rem;
            background: #edf2f7;
            padding: 0.6rem;
            border-radius: 6px;
            border-left: 3px solid var(--primary-light);
            margin-bottom: 0.75rem;
        }}
        
        .relations-section {{
            font-size: 0.85rem;
            border-top: 1px dashed var(--border);
            padding-top: 0.75rem;
            margin-top: 0.75rem;
        }}
        .rel-item {{ margin-bottom: 0.35rem; }}
        .rel-label {{ font-weight: 600; color: var(--text-muted); display: inline-block; width: 90px; }}
        .rel-badge {{
            display: inline-block;
            background: #e2e8f0;
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            margin-right: 0.3rem;
            cursor: pointer;
            color: var(--primary);
            text-decoration: none;
        }}
        .rel-badge:hover {{ background: #cbd5e0; }}
        
        .sources-section {{
            font-size: 0.82rem;
            background: #f8fafc;
            padding: 0.6rem;
            border-radius: 6px;
            margin-top: 0.75rem;
        }}
        .source-entry {{ margin-bottom: 0.25rem; }}
        .source-entry a {{ color: var(--primary-light); text-decoration: none; }}
        .source-entry a:hover {{ text-decoration: underline; }}
        
        .card-footer {{
            border-top: 1px solid var(--border);
            padding-top: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}
        .btn-feedback {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            background: white;
            color: var(--primary);
            border: 1px solid var(--primary-light);
            padding: 0.3rem 0.6rem;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.8rem;
            transition: all 0.2s;
        }}
        .btn-feedback:hover {{ background: var(--primary); color: white; }}
        
        footer {{
            text-align: center;
            padding: 2.5rem 1rem;
            background: #edf2f7;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 4rem;
        }}
        footer a {{ color: var(--primary-light); }}
    </style>
</head>
<body>
    <header>
        <h1>AI Governance Bilingual Thesaurus</h1>
        <p>Tesauro bilingue e controllato per la Governance dell'Intelligenza Artificiale. Armonizzazione delle prospettive normativa-giuridica, tecnico-operativa ed etico-filosofica.</p>
        <div class="badge-bar">
            <span class="badge">W3C SKOS Compliant</span>
            <span class="badge">EU AI Act (2024/1689)</span>
            <span class="badge">ISO/IEC 22989 &amp; 23894</span>
            <span class="badge">NIST AI RMF 1.0</span>
            <span class="badge">Consiglio d'Europa (CETS 225)</span>
        </div>
    </header>

    <main class="main-container">
        <div class="controls-card">
            <input type="text" id="searchInput" class="search-bar" placeholder="Cerca termine, definizione o acronimo (es. High-Risk, Agentic, Autonomia, ISO)...">
            <div class="filter-row">
                <div class="filter-group">
                    <label>Lingua Principale:</label>
                    <button id="btnLangIT" class="btn-toggle active" onclick="setLang('it')">Italiano (IT)</button>
                    <button id="btnLangEN" class="btn-toggle" onclick="setLang('en')">English (EN)</button>
                </div>
                <div class="filter-group">
                    <label for="perspectiveSelect">Prospettiva:</label>
                    <select id="perspectiveSelect" onchange="renderCards()">
                        <option value="all">Tutte le prospettive</option>
                        <option value="normativa-giuridica">Normativa-giuridica</option>
                        <option value="tecnico-operativa">Tecnico-operativa</option>
                        <option value="concettuale-filosofica">Concettuale-filosofica</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label for="sourceSelect">Fonte / Standard:</label>
                    <select id="sourceSelect" onchange="renderCards()">
                        <option value="all">Tutte le fonti</option>
                        <option value="AI Act">EU AI Act</option>
                        <option value="ISO/IEC">ISO/IEC</option>
                        <option value="NIST">NIST AI RMF</option>
                        <option value="Consiglio d'Europa">Consiglio d'Europa</option>
                        <option value="DDL AI">DDL AI Italia</option>
                    </select>
                </div>
                <div class="filter-group">
                    <a href="thesaurus.json" download class="btn-toggle" style="text-decoration:none; display:inline-block;">Scarica Dataset JSON</a>
                </div>
            </div>
        </div>

        <div id="cardsGrid" class="grid">
            <!-- Verrà popolato dinamicamente via JavaScript -->
        </div>
    </main>

    <footer>
        <p><strong>Tesauro Editoriale Aperto sulla Governance dell'Intelligenza Artificiale</strong></p>
        <p>Progetto d'Esame di Editoria Digitale - Università degli Studi di Milano | Workflow documentale aperto con Git, CI/CD e W3C SKOS.</p>
        <p style="margin-top:0.5rem;"><a href="https://github.com" target="_blank">Repository Documentale</a> &bull; <a href="../DECISIONS.md">Registro Decisioni Editoriali (EDR)</a></p>
    </footer>

    <script>
        const termsData = {terms_json};
        let currentLang = 'it';

        function setLang(lang) {{
            currentLang = lang;
            document.getElementById('btnLangIT').classList.toggle('active', lang === 'it');
            document.getElementById('btnLangEN').classList.toggle('active', lang === 'en');
            renderCards();
        }}

        function getTermLabel(id, lang) {{
            const t = termsData.find(x => x.id === id);
            return t ? t.prefLabel[lang] : id;
        }}

        function renderCards() {{
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            const selectedPersp = document.getElementById('perspectiveSelect').value;
            const selectedSource = document.getElementById('sourceSelect').value;
            const container = document.getElementById('cardsGrid');
            container.innerHTML = '';

            const filtered = termsData.filter(t => {{
                // Search query filter
                const matchQuery = !query || 
                    t.prefLabel.it.toLowerCase().includes(query) ||
                    t.prefLabel.en.toLowerCase().includes(query) ||
                    t.definition.it.toLowerCase().includes(query) ||
                    t.definition.en.toLowerCase().includes(query) ||
                    (t.altLabel && (
                        (t.altLabel.it && t.altLabel.it.some(a => a.toLowerCase().includes(query))) ||
                        (t.altLabel.en && t.altLabel.en.some(a => a.toLowerCase().includes(query)))
                    ));

                // Perspective filter
                const matchPersp = (selectedPersp === 'all') || t.perspective.includes(selectedPersp);

                // Source filter
                const matchSource = (selectedSource === 'all') || 
                    t.sources.some(s => s.name.toLowerCase().includes(selectedSource.toLowerCase()));

                return matchQuery && matchPersp && matchSource;
            }});

            if (filtered.length === 0) {{
                container.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:3rem; color:var(--text-muted);">Nessun termine corrisponde ai filtri selezionati.</div>';
                return;
            }}

            filtered.forEach(t => {{
                const mainLabel = currentLang === 'it' ? t.prefLabel.it : t.prefLabel.en;
                const secLabel = currentLang === 'it' ? t.prefLabel.en : t.prefLabel.it;
                const defText = currentLang === 'it' ? t.definition.it : t.definition.en;
                const scopeNote = t.scopeNote ? (currentLang === 'it' ? t.scopeNote.it : t.scopeNote.en) : null;
                const alts = t.altLabel ? (currentLang === 'it' ? t.altLabel.it : t.altLabel.en) : [];

                const card = document.createElement('div');
                card.className = 'concept-card';
                card.id = `card-${{t.id}}`;

                let perspBadges = t.perspective.map(p => 
                    `<span class="tag tag-${{p}}">${{p}}</span>`
                ).join(' ');

                let relsHtml = '';
                if (t.broader && t.broader.length > 0) {{
                    const badges = t.broader.map(b => `<a href="#card-${{b}}" class="rel-badge" onclick="highlightTerm('${{b}}')">↑ ${{getTermLabel(b, currentLang)}}</a>`).join('');
                    relsHtml += `<div class="rel-item"><span class="rel-label">Broader (BT):</span> ${{badges}}</div>`;
                }}
                if (t.narrower && t.narrower.length > 0) {{
                    const badges = t.narrower.map(n => `<a href="#card-${{n}}" class="rel-badge" onclick="highlightTerm('${{n}}')">↓ ${{getTermLabel(n, currentLang)}}</a>`).join('');
                    relsHtml += `<div class="rel-item"><span class="rel-label">Narrower (NT):</span> ${{badges}}</div>`;
                }}
                if (t.related && t.related.length > 0) {{
                    const badges = t.related.map(r => `<a href="#card-${{r}}" class="rel-badge" onclick="highlightTerm('${{r}}')">↔ ${{getTermLabel(r, currentLang)}}</a>`).join('');
                    relsHtml += `<div class="rel-item"><span class="rel-label">Related (RT):</span> ${{badges}}</div>`;
                }}

                let sourcesHtml = t.sources.map(s => 
                    `<div class="source-entry"><strong>[${{s.type.toUpperCase()}}]</strong> ${{s.name}} — <em>${{s.reference}}</em></div>`
                ).join('');

                card.innerHTML = `
                    <div>
                        <div class="card-header">
                            <h2 class="card-title">${{mainLabel}}</h2>
                            <div class="card-subtitle">${{secLabel}} ${{alts && alts.length ? '(' + alts.join(', ') + ')' : ''}}</div>
                            <div class="perspectives-bar">${{perspBadges}}</div>
                        </div>
                        <div class="card-body">
                            <p class="def-text">${{defText}}</p>
                            ${{scopeNote ? `<div class="scope-note">${{scopeNote}}</div>` : ''}}
                            ${{relsHtml ? `<div class="relations-section">${{relsHtml}}</div>` : ''}}
                            <div class="sources-section">${{sourcesHtml}}</div>
                        </div>
                    </div>
                    <div class="card-footer">
                        <span>v${{t.version}} &bull; ${{t.lastUpdated}}</span>
                        <a href="https://github.com/issues/new?title=[Proposta]%20Modifica%20a%20${{encodeURIComponent(t.id)}}" target="_blank" class="btn-feedback">
                            ✍ Proponi modifica
                        </a>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function highlightTerm(id) {{
            setTimeout(() => {{
                const target = document.getElementById(`card-${{id}}`);
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    target.style.outline = '3px solid var(--primary-light)';
                    setTimeout(() => {{ target.style.outline = ''; }}, 2000);
                }}
            }}, 100);
        }}

        document.getElementById('searchInput').addEventListener('input', renderCards);
        renderCards();
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[BUILD] Generato Portale Web Statico: {output_path}")

def main():
    """
    Orchestra la pipeline di compilazione degli artefatti finali:
      PASSO 1: Crea la cartella di output 'dist/' se non esiste già;
      PASSO 2: Carica e unifica tutti i termini Markdown da 'data/terms/';
      PASSO 3: Esporta l'indice strutturato 'dist/thesaurus.json';
      PASSO 4: Compila l'applicazione web interattiva 'dist/index.html' (pronta per GitHub Pages);
      PASSO 5: Crea una copia sincronizzata in 'web_mockup/index.html' per consultazione locale.
    """
    print("=" * 70)
    print("COMPILAZIONE ARTEFATTI DEL TESAURO SULLA GOVERNANCE DELL'IA")
    print("=" * 70)
    
    # PASSO 1: Assicura la presenza della cartella di distribuzione
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # PASSO 2: Ingestione e parsing dei dati sorgente
    terms = load_terms()
    print(f"Caricati {len(terms)} termini sorgente.")
    
    # PASSO 3: Serializzazione in formato JSON (Interoperabilità / Dati Aperti)
    json_path = os.path.join(DIST_DIR, "thesaurus.json")
    with open(json_path, "w", encoding="utf-8") as f:
        # ensure_ascii=False preserva correttamente caratteri accentati ed emoticon UTF-8
        json.dump(terms, f, ensure_ascii=False, indent=2)
    print(f"[BUILD] Esportato Dataset JSON: {json_path}")
    
    # PASSO 4: Compilazione del portale statico per GitHub Pages
    html_path = os.path.join(DIST_DIR, "index.html")
    build_web_portal(terms, html_path)
    
    # Crea .nojekyll per disabilitare il processore Jekyll di GitHub Pages
    nojekyll_path = os.path.join(DIST_DIR, ".nojekyll")
    open(nojekyll_path, "w", encoding="utf-8").close()
    
    # PASSO 5: Copia locale di backup nella cartella web_mockup/
    web_mockup_dir = os.path.join(ROOT_DIR, "web_mockup")
    os.makedirs(web_mockup_dir, exist_ok=True)
    mockup_html_path = os.path.join(web_mockup_dir, "index.html")
    build_web_portal(terms, mockup_html_path)
    
    print("=" * 70)
    print("BUILD COMPLETATA CON SUCCESSO!")


if __name__ == "__main__":
    main()

