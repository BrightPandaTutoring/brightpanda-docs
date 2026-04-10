# Make.com Scenario Documentatie

Overzicht van alle Make.com automatiserings-scenarios voor Bright Panda.

---

## Scenario Index

| # | Naam | Trigger | Status | Bestand |
|---|------|---------|--------|---------|
| 01 | Docent Uitnodiging via WhatsApp | Salesforce Watch (15 min) | ✅ Werkend — getest 12 maart 2026 | [scenario-01](scenario-01-docent-uitnodiging-whatsapp.md) |
| 02 | Tally Webhook → Ouder Planning | Custom Webhook (Tally Form 1) | 🟡 Compleet — SOQL 0-based indices hertesten | [scenario-02](scenario-02-tally-webhook-ouder-planning.md) |
| 03 | Reminders & Escalatie | Schedule (elke 15 min) | ✅ Compleet | [scenario-03](scenario-03-reminders-escalatie.md) |
| 3b | Ouder Tijdslot Verwerking | Custom Webhook (Tally Form 2) | 🟡 In aanbouw (modules 3-6 ✅, 7-13 wacht op template) | [scenario-3b](scenario-3b-ouder-tijdslot-verwerking.md) |
| 05 | Koppelingsbevestiging | Onbekend | 🔴 Backlog | [scenario-05](scenario-05-koppelingsbevestiging.md) |

---

## Status Legenda

| Icoon | Betekenis |
|-------|-----------|
| ✅ | Actief en werkend |
| 🟡 | In ontwikkeling / geblokkeerd |
| 🔴 | Nog te bouwen |
| ⚫ | Inactief / gearchiveerd |

---

## Huidige Blokkades

| Scenario | Blokkade | Actie |
|----------|---------|-------|
| 01 | Meta display name goedkeuring (laag prioriteit) | Wacht → dan naam "Bright Panda Bijles" zichtbaar bij ontvanger |
| 02 | SOQL module 3 gebruikte fields[1] i.p.v. fields[0] (0-based) | Gecorrigeerd in docs — hertesten met echt Tally formulier |
| 02 | Module 4 gebruikte `ParentSPhone__c` (niet bruikbaar) | Vervangen door module 32 Contact SOQL — nog testen |
| 3b | Template `trial_lesson_confirmed_teacher` wacht op Meta goedkeuring | Goedkeuring afwachten → dan modules 7-13 bouwen |
| 3b | Einde-tot-einde test nog niet gedaan | Na oplevering modules 7-13 uitvoeren met echt matching record |

---

## Volledige Flow

```
[Salesforce: status → Teacher Invited]
        ↓
  Scenario 01 ─── WhatsApp docent met Tally Form 1 link
        ↓
  [Docent vult beschikbaarheid in via Tally Form 1]
        ↓
  Scenario 02 ─── Bouwt genummerde tijdslotenlijst
               ─── Slaat op in Available_Timeslots__c
               ─── WhatsApp ouder met tijdsloten + Tally Form 2 link
        ↓
  [Ouder kiest tijdslot getal via Tally Form 2]
        ↓
  Scenario 04 ─── Zoekt tijdslot op in Available_Timeslots__c
               ─── Slaat op in Trial_Lesson_Date__c
               ─── WhatsApp bevestiging naar ouder + docent
               ─── Status → Trial Lesson Scheduled

  Scenario 03 ─── Draait elk kwartier
               ─── Route 1: Reminder docent na 24u
               ─── Route 2: Escalatie docent na 48u
               ─── Route 3: Reminder ouder na 24u
               ─── Route 4: Escalatie ouder na 48u

  Scenario 05 ─── Koppelingsbevestiging (buiten proefles flow) [Backlog]
```

---

## Referentie Documenten

| Document | Inhoud |
|----------|--------|
| [Gedeelde configuratie](gedeelde-configuratie.md) | 360dialog headers, API endpoint, Google Apps Script URL, templates overzicht, Salesforce velden, telefoonnummer conventie |
| [Google Apps Script](google-apps-script.md) | Functie A (tijdsloten string) + Functie B (keuzenummer → datetime), deploy instructies |
| [Beslissingen](beslissingen.md) | Alle technische en functionele beslissingen met onderbouwing |

---

## Hoe deze docs te gebruiken

- Elk scenario heeft een eigen bestand in deze map
- Bestanden volgen de naamconventie: `scenario-[nr]-[korte-naam].md`
- Bij errors: open het relevante scenario-bestand → sectie "Foutmeldingen & Oplossingen"
- Bij bouwen nieuw scenario: check eerst [beslissingen.md](beslissingen.md) voor werkwijze afspraken

---

> Documentatie gegenereerd via Claude Code — Bright Panda Tutoring
