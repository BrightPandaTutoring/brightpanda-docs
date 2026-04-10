# Make.com Scenario Documentatie

Overzicht van alle Make.com automatiserings-scenarios voor Bright Panda.

---

## Scenario Index

| # | Naam | Trigger | Status | Bestand |
|---|------|---------|--------|---------|
| 01 | Docent Uitnodiging via WhatsApp | Salesforce Watch (15 min) | ✅ Werkend | [scenario-01](scenario-01-docent-uitnodiging-whatsapp.md) |
| 02 | Tally Webhook → Ouder Planning | Custom Webhook (Tally Form 1) | ✅ Werkend | [scenario-02](scenario-02-tally-webhook-ouder-planning.md) |
| 03 | Reminders & Escalatie | Schedule (elke 15 min) | ✅ Werkend | [scenario-03](scenario-03-reminders-escalatie.md) |
| 3b | Ouder Tijdslot Verwerking | Custom Webhook (GAS Picker) | 🟡 Pad A ✅ werkend — Pad B nog te bouwen | [scenario-3b](scenario-3b-ouder-tijdslot-verwerking.md) |
| 05 | Koppelingsbevestiging | Onbekend | 🔴 Backlog | [scenario-05](scenario-05-koppelingsbevestiging.md) |

---

## Status Legenda

| Icoon | Betekenis |
|-------|-----------|
| ✅ | Actief en werkend |
| 🟡 | In ontwikkeling / gedeeltelijk werkend |
| 🔴 | Nog te bouwen |
| ⚫ | Inactief / gearchiveerd |

---

## Huidige Blokkades & Openstaande Werk

| Scenario | Item | Status |
|----------|------|--------|
| 3b | Pad B bouwen (no_match route) | 🔴 Nog te bouwen |
| 3b | Availability Conflict WhatsApp template | 🔴 Template nog te maken + Meta indienen |
| Nieuw | Polling scenario (reminder docent bij Availability Conflict) | 🔴 Nog te bouwen |
| Nieuw | Scenario: docent vult afgesproken tijdslot in | 🔴 Nog te bouwen |
| Alle | Einde-tot-einde test met echt matching record | ⏳ Na Pad B |
| Alle | Disclaimer toevoegen aan templates | ⏳ Na volledig testen |
| Laag | Picker hosten op brightpanda.nl (Webflow) | 🔴 Toekomstig |
| Laag | Meta Business Verificatie (KvK 84707577) | 🔴 Toekomstig |

---

## Volledige Flow

```
[Salesforce: Status__c → Trial Class]
        ↓
  Scenario 01 ─── WhatsApp docent met Tally Form 1 link
                   Status: Teacher Invited
        ↓
  [Docent vult beschikbaarheid in via Tally Form 1]
        ↓
  Scenario 02 ─── Verwerkt tijdsloten via GAS Script 2
               ─── Slaat timeslotsRaw op in Available_Timeslots__c
               ─── WhatsApp ouder met GAS Picker URL
                   Status: Parent Invited
        ↓
  [Ouder klikt tijdslot op GAS Picker pagina]
        ↓
  Scenario 3b ─── Ontvangt keuze van GAS Picker via webhook
     Pad A:    ─── Slaat Trial_Lesson_Date__c op (geen Z suffix)
               ─── WhatsApp bevestiging naar ouder + docent (met elkaars contactgegevens)
                   Status: Trial Lesson Scheduled
     Pad B:    ─── [NOG TE BOUWEN] Update Availability Conflict
               ─── WhatsApp docent: bel de ouder
                   Status: Availability Conflict

  Scenario 03 ─── Draait elk kwartier
               ─── Route 1: Reminder docent na 24u (Teacher Invited)
               ─── Route 2: Escalatie docent na 48u
               ─── Route 3: Reminder ouder na 24u (Parent Invited)
               ─── Route 4: Escalatie ouder na 48u

  Nieuw polling scenario ─── [NOG TE BOUWEN]
               ─── Check Availability Conflict + Trial_Lesson_Date__c leeg
               ─── Reminder docent elke 3 uur

  Nieuw scenario ─── [NOG TE BOUWEN]
               ─── Docent vult afgesproken tijdslot in via form
               ─── Salesforce update + bevestiging WhatsApp
```

---

## Referentie Documenten

| Document | Inhoud |
|----------|--------|
| [Gedeelde configuratie](gedeelde-configuratie.md) | 360dialog headers, API key, GAS URLs, templates overzicht, Salesforce velden, webhook URLs |
| [Google Apps Script](google-apps-script.md) | Script 1 (vakvertaling), Script 2 (tijdslotverwerking), Script 3 (picker v10) |
| [Beslissingen](beslissingen.md) | Alle technische en functionele beslissingen met onderbouwing |

---

## Hoe deze docs te gebruiken

- Elk scenario heeft een eigen bestand in deze map
- Bestanden volgen de naamconventie: `scenario-[nr]-[korte-naam].md`
- Bij errors: open het relevante scenario-bestand → sectie "Foutmeldingen & Oplossingen"
- Bij bouwen nieuw scenario: check eerst [beslissingen.md](beslissingen.md) voor werkwijze afspraken
- JSON bodies altijd volledig kopiëren — nooit partial aanpassen

---

> Documentatie gegenereerd via Claude Code — Bright Panda Tutoring
