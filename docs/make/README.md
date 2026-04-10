# Make.com Scenario Documentatie

Overzicht van alle Make.com automatiserings-scenarios voor Bright Panda.

---

## Scenario Index

| # | Naam | Trigger | Status | Bestand |
|---|------|---------|--------|---------|
| 01 | Docent Uitnodiging via WhatsApp | Salesforce Watch (15 min) | 🟡 In ontwikkeling | [scenario-01](scenario-01-docent-uitnodiging-whatsapp.md) |
| 02 | Tally Webhook → Ouder Planning | Custom Webhook (Tally Form 1) | 🟡 In ontwikkeling | [scenario-02](scenario-02-tally-webhook-ouder-planning.md) |
| 03 | Reminders & Escalatie | Schedule (elk uur) | 🔴 Nog te bouwen | [scenario-03](scenario-03-reminders-escalatie.md) |
| 04 | Koppelingsbevestiging | Onbekend | 🔴 Nog te bouwen | [scenario-04](scenario-04-koppelingsbevestiging.md) |

---

## Status Legenda

| Icoon | Betekenis |
|-------|-----------|
| ✅ | Actief en werkend |
| 🟡 | In ontwikkeling / geblokkeerd |
| 🔴 | Nog te bouwen |
| ⚫ | Inactief / gearchiveerd |

---

## Gedeelde Configuratie

- [Gedeelde configuratie](gedeelde-configuratie.md) — 360dialog HTTP headers, Salesforce verbinding, telefoonnummer conventie, Tally webhook instructie

---

## Huidige Blokkades

| Scenario | Blokkade |
|----------|---------|
| 01 + 02 | Meta goedkeuring `teacher_invitation` template (fout 131037 + 132001) |
| 02 | SOQL query nog hardcoded op `0016` — dynamisch maken |
| 02 | `join/map` formule tijdsloten nog niet getest |
| 03 | WhatsApp reminder template nog niet aangemaakt bij 360dialog/Meta |

---

## Flow Overzicht

```
[Salesforce: status → Teacher Invited]
        ↓
  Scenario 01: WhatsApp naar docent met Tally Form 1 link
        ↓
  [Docent vult beschikbaarheid in via Tally Form 1]
        ↓
  Scenario 02: WhatsApp naar ouder met tijdsloten + Tally Form 2 link
        ↓
  [Ouder kiest tijdslot via Tally Form 2]
        ↓
  (Scenario 0X: verwerk keuze ouder → bevestiging naar beide partijen)

  Scenario 03: Reminders (24u) + Escalaties (48u) voor niet-reagerende docenten/ouders
  Scenario 04: Koppelingsbevestiging bij definitieve match (buiten proefles flow)
```

---

## Hoe deze docs te gebruiken

- Elk scenario heeft een eigen bestand in deze map
- Bestanden volgen de naamconventie: `scenario-[nr]-[korte-naam].md`
- Bij errors: open het relevante scenario-bestand voor troubleshooting info
- Gedeelde instellingen staan in `gedeelde-configuratie.md`

---

> Documentatie gegenereerd via Claude Code — Bright Panda Tutoring
