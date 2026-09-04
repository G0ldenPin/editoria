#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compila simultaneamente due canali di distribuzione multicanale:
  1. dist/thesaurus.json : Dataset strutturato per l'interoperabilità software e il riuso secondo i principi degli Open Data;
  2. dist/index.html     : Portale web statico, interattivo, bilingue, accessibile e responsive, pronto per il deploy su GitHub Pages.
"""

import json
import os
import re
import sys
import yaml

# -----------------------------------------------------------------------------
# PERCORSI DEL PROGETTO
# -----------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS_DIR = os.path.join(ROOT_DIR, "data", "terms")     # Cartella sorgenti
DIST_DIR = os.path.join(ROOT_DIR, "dist")              # Cartella di distribuzione


def extract_frontmatter(content):
    """
    Separa i metadati YAML dal testo Markdown del termine tramite RegEx  -> RegEx è l'unico modo affidabile per isolare il frontmatter YAML in presenza di delimitatori '---' multipli nel corpo del testo.
    Ritorna: (stringa_yaml, testo_markdown).
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), match.group(2)


def load_terms():
    """
      1. Legge ciascun file .md;
      2. Isola il frontmatter YAML con yaml.safe_load;
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
    Genera il portale statico
    """
    terms_json = json.dumps(terms, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesauro sulla Governance dell'Intelligenza Artificiale | AI Governance Thesaurus</title>
    <!-- Google Fonts: Rubik con pesi multipli (300, 400, 500, 600, 700, 800) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* Palette Richiesta:
               - Protagonisti Verdi: #253122 (Verde bosco profondo) & #437742 (Verde foglia vibrante)
               - Accenti: #793327 (Rosso mattone / terracotta rustico) & #a6a159 (Oliva dorato caldo)
               - Bianco e nero non puri per il massimo comfort visivo */
            --c-primary: #253122;        /* Protagonista 1: Verde scuro bosco profondo */
            --c-primary-dark: #161e14;   /* Verde notte profondo per footer e contrasti */
            --c-secondary: #437742;      /* Protagonista 2: Verde foglia vibrante */
            --c-secondary-light: #edf3ec;/* Tinta chiarissima salvia/foglia per sfondi/evidenziazioni */
            --c-secondary-glow: rgba(67, 119, 66, 0.35);
            --c-accent-red: #793327;     /* Accento 1: Rosso mattone / terracotta (CTA/azioni chiave) */
            --c-accent-olive: #a6a159;   /* Accento 2: Oliva dorato caldo (dettagli/bordi decorativi) */
            
            /* Bianco e Nero non puri */
            --c-bg: #f5f6f3;             /* Sfondo pagina: bianco caldo naturale */
            --c-card-bg: #ffffff;        /* Sfondo tessere: bianco ottico pulito */
            --c-text: #181b17;           /* Testo principale: nero carbone boschivo profondo */
            --c-text-muted: #535b50;     /* Testo secondario: ardesia vegetale medio */
            --c-border: #d8ded6;         /* Bordo tenue */
            --c-border-light: #ecf0ea;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Rubik', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-weight: 400;
            background-color: var(--c-bg);
            color: var(--c-text);
            line-height: 1.6;
        }}
        header {{
            background: linear-gradient(135deg, var(--c-primary) 0%, var(--c-primary-dark) 100%);
            border-bottom: 4px solid var(--c-secondary);
            color: #ffffff;
            padding: 3rem 1.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(22, 30, 20, 0.2);
        }}
        header h1 {{
            font-size: 2.3rem;
            margin-bottom: 0.6rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        header p {{
            font-size: 1.15rem;
            color: #e4eae2;
            font-weight: 300;
            max-width: 820px;
            margin: 0 auto 1.6rem;
            line-height: 1.65;
        }}
        .badge-bar {{
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}
        .badge {{
            background: rgba(67, 119, 66, 0.25);
            border: 1px solid rgba(166, 161, 89, 0.45);
            color: #f3f6f2;
            font-weight: 500;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.82rem;
            letter-spacing: 0.3px;
        }}
        
        .main-container {{
            max-width: 1200px;
            margin: -1.8rem auto 3rem;
            padding: 0 1rem;
        }}
        .controls-card {{
            background: var(--c-card-bg);
            border-radius: 14px;
            padding: 1.6rem;
            box-shadow: 0 10px 25px -5px rgba(37, 49, 34, 0.08), 0 4px 6px -2px rgba(37, 49, 34, 0.03);
            border: 1px solid var(--c-border);
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }}
        .search-bar {{
            width: 100%;
            padding: 0.9rem 1.3rem;
            font-family: 'Rubik', sans-serif;
            font-size: 1.05rem;
            font-weight: 400;
            color: var(--c-text);
            border: 2px solid var(--c-border);
            border-radius: 10px;
            background: #ffffff;
            transition: all 0.2s ease;
        }}
        .search-bar:focus {{
            outline: none;
            border-color: var(--c-secondary);
            box-shadow: 0 0 0 4px var(--c-secondary-glow);
        }}
        
        .filter-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            align-items: center;
            justify-content: space-between;
        }}
        .filter-group {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.92rem;
        }}
        .filter-group label {{
            font-weight: 600;
            color: var(--c-primary);
        }}
        select, .btn-toggle {{
            font-family: 'Rubik', sans-serif;
            font-weight: 500;
            padding: 0.5rem 0.9rem;
            border-radius: 8px;
            border: 1px solid var(--c-border);
            background: #ffffff;
            color: var(--c-text);
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
        }}
        select:focus {{
            outline: none;
            border-color: var(--c-secondary);
        }}
        .btn-toggle:hover:not(.active) {{
            border-color: var(--c-secondary);
            color: var(--c-primary);
        }}
        .btn-toggle.active {{
            background: var(--c-primary);
            color: #ffffff;
            border-color: var(--c-primary);
            font-weight: 600;
            box-shadow: 0 2px 5px rgba(37, 49, 34, 0.25);
        }}
        .btn-download {{
            background: var(--c-secondary-light);
            color: var(--c-primary);
            border: 1px solid var(--c-secondary);
            font-weight: 600;
        }}
        .btn-download:hover {{
            background: var(--c-secondary);
            color: #ffffff;
            border-color: var(--c-secondary);
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.5rem;
        }}
        .concept-card {{
            background: var(--c-card-bg);
            border-radius: 12px;
            border: 1px solid var(--c-border);
            border-top: 4px solid var(--c-primary);
            padding: 1.6rem;
            box-shadow: 0 4px 6px -1px rgba(37, 49, 34, 0.05);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s, border-top-color 0.2s;
        }}
        .concept-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -4px rgba(37, 49, 34, 0.14);
            border-top-color: var(--c-secondary);
        }}
        .card-header {{ margin-bottom: 1rem; }}
        .card-title {{
            font-size: 1.35rem;
            color: var(--c-primary);
            margin-bottom: 0.25rem;
            font-weight: 700;
            letter-spacing: -0.3px;
        }}
        .card-subtitle {{
            font-size: 0.96rem;
            color: var(--c-text-muted);
            font-style: italic;
            font-weight: 400;
        }}
        .perspectives-bar {{
            display: flex;
            gap: 0.45rem;
            margin-top: 0.7rem;
            flex-wrap: wrap;
        }}
        .tag {{
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
        }}
        .tag-normativa-giuridica {{
            background: #eaf2e9;
            color: #1d3d1b;
            border: 1px solid var(--c-secondary);
        }}
        .tag-tecnico-operativa {{
            background: #ebedeb;
            color: var(--c-primary);
            border: 1px solid #aeb6ac;
        }}
        .tag-concettuale-filosofica {{
            background: #f6ecea;
            color: #5e2218;
            border: 1px solid var(--c-accent-red);
        }}
        
        .card-body {{ margin-bottom: 1.2rem; }}
        .def-text {{
            font-size: 0.96rem;
            font-weight: 400;
            margin-bottom: 0.85rem;
            line-height: 1.62;
            color: var(--c-text);
        }}
        .scope-note {{
            font-size: 0.87rem;
            font-weight: 400;
            background: var(--c-secondary-light);
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            border-left: 3px solid var(--c-secondary);
            margin-bottom: 0.85rem;
            color: var(--c-primary-dark);
        }}
        
        .relations-section {{
            font-size: 0.85rem;
            border-top: 1px dashed var(--c-border);
            padding-top: 0.8rem;
            margin-top: 0.8rem;
        }}
        .rel-item {{ margin-bottom: 0.4rem; }}
        .rel-label {{
            font-weight: 600;
            color: var(--c-text-muted);
            display: inline-block;
            width: 95px;
            font-size: 0.82rem;
        }}
        .rel-badge {{
            display: inline-block;
            background: #eff2ee;
            padding: 0.18rem 0.55rem;
            border-radius: 6px;
            margin-right: 0.35rem;
            margin-bottom: 0.25rem;
            cursor: pointer;
            color: var(--c-primary);
            font-weight: 500;
            font-size: 0.82rem;
            text-decoration: none;
            border: 1px solid #d4dbd2;
            transition: all 0.15s;
        }}
        .rel-badge:hover {{
            background: var(--c-secondary);
            color: #ffffff;
            border-color: var(--c-secondary);
        }}
        
        .sources-section {{
            font-size: 0.82rem;
            background: #f8fafc;
            border: 1px solid #eef2f6;
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            margin-top: 0.8rem;
        }}
        .source-entry {{
            margin-bottom: 0.3rem;
            color: var(--c-text);
        }}
        .source-entry strong {{
            color: var(--c-primary);
            font-weight: 600;
        }}
        .source-entry a {{
            color: var(--c-primary);
            text-decoration: none;
            font-weight: 500;
        }}
        .source-entry a:hover {{
            color: var(--c-accent-red);
            text-decoration: underline;
        }}
        
        .card-footer {{
            border-top: 1px solid var(--c-border);
            padding-top: 0.85rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--c-text-muted);
            font-weight: 500;
        }}
        .btn-feedback {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: #ffffff;
            color: var(--c-accent-red);
            border: 1px solid var(--c-accent-red);
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.82rem;
            transition: all 0.2s;
        }}
        .btn-feedback:hover {{
            background: var(--c-accent-red);
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(121, 51, 39, 0.35);
        }}
        
        footer {{
            text-align: center;
            padding: 2.8rem 1.5rem;
            background: var(--c-primary-dark);
            color: #cbd3ca;
            font-size: 0.92rem;
            margin-top: 4rem;
            border-top: 4px solid var(--c-accent-olive);
        }}
        footer p {{
            margin-bottom: 0.4rem;
        }}
        footer strong {{
            color: #ffffff;
            font-weight: 600;
        }}
        footer a {{
            color: var(--c-accent-olive);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.15s;
        }}
        footer a:hover {{
            color: #ffffff;
            text-decoration: underline;
        }}
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
                    <a href="thesaurus.json" download class="btn-toggle btn-download" style="text-decoration:none; display:inline-block;">Scarica Dataset JSON</a>
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
                    target.style.outline = '3px solid var(--c-secondary)';
                    target.style.boxShadow = '0 0 16px var(--c-secondary-glow)';
                    setTimeout(() => {{ 
                        target.style.outline = ''; 
                        target.style.boxShadow = '';
                    }}, 2000);
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
    Crea la cartella di output 'dist/' se non esiste già;
    Carica e unifica tutti i termini Markdown da 'data/terms/';
    Esporta l'indice strutturato 'dist/thesaurus.json';
    Compila l'applicazione web interattiva 'dist/index.html' (pronta per GitHub Pages);
    Crea una copia sincronizzata in 'web_mockup/index.html' per consultazione locale.
    """
    print("=" * 70)
    print("COMPILAZIONE ARTEFATTI DEL TESAURO SULLA GOVERNANCE DELL'IA")
    print("=" * 70)
    
    # Crea 'dist/' in caso non ci sia
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # Data handling: caricamento e ingestione
    terms = load_terms()
    print(f"Caricati {len(terms)} termini sorgente.")
    
    # Porta tutto in JSON
    json_path = os.path.join(DIST_DIR, "thesaurus.json")
    with open(json_path, "w", encoding="utf-8") as f:
        # ensure_ascii=False preserva caratteri accentati ed emoticon UTF-8
        json.dump(terms, f, ensure_ascii=False, indent=2)
    print(f"[BUILD] Esportato Dataset JSON: {json_path}")
    
    # Compila GH Pages
    html_path = os.path.join(DIST_DIR, "index.html")
    build_web_portal(terms, html_path)
    
    # SAFEGUARD JEKYLL
    nojekyll_path = os.path.join(DIST_DIR, ".nojekyll")
    open(nojekyll_path, "w", encoding="utf-8").close()
    
    # backup locale
    web_mockup_dir = os.path.join(ROOT_DIR, "web_mockup")
    os.makedirs(web_mockup_dir, exist_ok=True)
    mockup_html_path = os.path.join(web_mockup_dir, "index.html")
    build_web_portal(terms, mockup_html_path)
    
    print("=" * 70)
    print("BUILD COMPLETATA CON SUCCESSO!")


if __name__ == "__main__":
    main()

