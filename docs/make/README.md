# Make.com Scenario Documentatie

Overzicht van alle Make.com automatiserings-scenarios voor Bright Panda.

---

## Scenario Index

| # | Naam | Trigger | Status | Bestand |
|---|------|---------|--------|---------|
| 01 | Docent Uitnodiging via WhatsApp | Salesforce Watch (15 min) | 🟡 In ontwikkeling | [scenario-01](scenario-01-docent-uitnodiging-whatsapp.md) |
| 02 | Tally Webhook → Ouder Planning | Custom Webhook (Tally Form 1) | 🟡 In ontwikkeling | [scenario-02](scenario-02-tally-webhook-ouder-planning.md) |
| 03 | Reminders & Escalatie | Schedule (elke 15 min) | ✅ Gebouwd | [scenario-03](scenario-03-reminders-escalatie.md) |
| 04 | Ouder Tijdslot Verwerking | Custom Webhook (Tally Form 2) | 🔴 Nog te bouwen | [scenario-04](scenario-04-ouder-tijdslot-verwerking.md) |
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
| 01 | Meta propagatie na display name wijziging (fout #131037) | Wacht 24-48u → Run once opnieuw |
| 02 | Module 8 Set Variable formule werkt alleen voor datum 1 | Uitbreiden naar datum 2-5 |
| 02 | HTTP module 5 nog niet geconfigureerd | `parent_timeslot_invitation` call bouwen |
| 02 | Salesforce Update module 6 nog niet geconfigureerd | Status + `Available_Timeslots__c` invullen |

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
| [Gedeelde configuratie](gedeelde-configuratie.md) | 360dialog headers, API endpoint, Salesforce velden, telefoonnummer conventie, Tally webhook instructie, Meta Business Verificatie |
| [Beslissingen](beslissingen.md) | Alle technische en functionele beslissingen met onderbouwing |

---

## Hoe deze docs te gebruiken

- Elk scenario heeft een eigen bestand in deze map
- Bestanden volgen de naamconventie: `scenario-[nr]-[korte-naam].md`
- Bij errors: open het relevante scenario-bestand → sectie "Foutmeldingen & Oplossingen"
- Bij bouwen nieuw scenario: check eerst [beslissingen.md](beslissingen.md) voor werkwijze afspraken

---

> Documentatie gegenereerd via Claude Code — Bright Panda Tutoring
