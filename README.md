# Bright Panda Docs

Deze repository bevat de content en documentatie van Bright Panda Bijles.

## Repo structuur

```
/
├── CLAUDE.md             ← Instructies voor Claude (single source of truth: credentials, scenario statussen, regels)
├── TODO.md               ← Actuele to-do lijst
├── SESSION_LOG.md        ← Laatste sessie samenvatting (wordt bijgewerkt bij "Afsluiten")
├── README.md             ← Dit bestand
└── docs/
    ├── docent-gids/      ← Docent Gids (nl.md, en.md)
    ├── make/             ← Technische detail-documentatie per Make.com scenario
    └── archive-website-content/  ← Oud archief website/marketing content (geen ops, niet bijwerken)
```

## Docent Gids

De volledige tekst van de Docent Gids staat in:
- `docs/docent-gids/nl.md` — Nederlandse versie
- `docs/docent-gids/en.md` — Engelse versie (nog aan te maken)

### Hoe werkt de workflow?

1. Tekst aanpassen: vertel Claude in de chat wat er moet veranderen
2. Claude haalt nl.md op uit deze repo, past het aan en pusht het terug
3. Claude genereert daarna automatisch de nieuwe PDF

### Structuur van nl.md

- Paragraaftitels beginnen met `##`
- Subparagrafen beginnen met `###`
- `[icon: naam]` geeft aan welk pictogram bij een paragraaf hoort
- `[intro]` markeert de cursieve introtekst
- `[waarschuwing]` markeert een waarschuwingsblok
- `[info]` markeert een infoblok

## Sleutelwoorden tussen Claude sessies

- **"Pak op"** (begin nieuwe chat) — Claude leest SESSION_LOG.md, CLAUDE.md, TODO.md en geeft een korte status
- **"Update"** (tussentijds) — korte stand-van-zaken samenvatting
- **"Afsluiten"** (einde chat) — complete samenvatting, schrijft SESSION_LOG.md bij voor de volgende sessie
