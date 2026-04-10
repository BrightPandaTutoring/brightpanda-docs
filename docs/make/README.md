# Make.com Scenario Documentatie

Overzicht van alle Make.com automatiserings-scenarios voor Bright Panda.

---

## Scenario Index

| # | Naam | Trigger | Status | Bestand |
|---|------|---------|--------|---------|
| 01 | Docent Uitnodiging via WhatsApp | Salesforce Watch (7 min) | ✅ Werkend — Aan | [scenario-01](scenario-01-docent-uitnodiging-whatsapp.md) |
| 02 | Tally Webhook → Ouder Planning | Custom Webhook (Tally Form 1) | ✅ Werkend — Aan | [scenario-02](scenario-02-tally-webhook-ouder-planning.md) |
| 03 | Trial Lesson Scheduled & Availability Conflict | Custom Webhook (GAS Picker) | ✅ Werkend — Pad A + Pad B | [scenario-3b](scenario-3b-ouder-tijdslot-verwerking.md) |
| 04 | Teacher Timeslot Submission | Custom Webhook (Tally Form 3) | ✅ Werkend — Aan | [scenario-04](scenario-04-teacher-timeslot-submission.md) |
| 05 | Availability Conflict Reminder | Schedule (elke 4 uur) | ✅ Werkend — Aan | [scenario-05](scenario-05-availability-conflict-reminder.md) |
| 06 | Teacher Availability Reminder | Schedule (elke 2 uur) | ✅ Werkend — Aan | [scenario-06](scenario-06-teacher-availability-reminder.md) |
| 07 | Internal Alert Teacher No Response | Schedule (elke 15 min) | ✅ Werkend | [scenario-07](scenario-07-internal-alert.md) |
| 08 | Lesson Date Reminder | Schedule (elke 15 min) | ✅ Werkend | [scenario-08](scenario-08-lesson-date-reminder.md) |
| 09 | Parent Timeslot Reminders & Escalatie | Schedule (elke 15 min) | ✅ Werkend | [scenario-09](scenario-09-parent-reminders.md) |
| 10 | Salesforce to MailerLite New Registration | Salesforce Watch (7 min) | ✅ Werkend — Aan | [scenario-10](scenario-10-salesforce-mailerlite.md) |

---

## Status Legenda

| Icoon | Betekenis |
|-------|-----------|
| ✅ | Actief en werkend |
| 🟡 | In ontwikkeling / gedeeltelijk werkend |
| 🔴 | Nog te bouwen |
| ⚫ | Inactief / gearchiveerd |

---

## Openstaande To-do's

| Item | Prioriteit | Details |
|------|-----------|---------|
| Post-proefles flow (Scenario 11+) | Medium | Statusupdates na proefles, MailerLite groep updates |
| Intern WhatsApp alert bij nieuwe aanmelding | Laag | Extra module in Scenario 10 |
| Claude API matching | Laag | Make.com → Claude API → top 3 docenten → intern WhatsApp |
| Footer logo welkomstmail | Laag | Zodra collega aanlevert |
| Picker hosten op brightpanda.nl (Webflow) | Laag | GAS URL vervangen door branded URL |
| Meta Business Verificatie | Laag | KvK 84707577 |
| Einde-tot-einde test volledige flow | Medium | Met echt matching record |

---

## Volledige Flow

```
[Salesforce: nieuw leerling account aangemaakt]
        ↓
  Scenario 10 ── MailerLite subscriber aanmaken
               ── Welkomstmail automatisch via MailerLite automation

[Salesforce: Status__c → Trial Class]
        ↓
  Scenario 01 ── WhatsApp docent met Tally Form 1 link
              ── Teacher_Invited_At__c = nu
              ── Status: Teacher Invited

  Scenario 06 ── Reminder docent na 12u
  Scenario 07 ── Intern alert na 24u
        ↓
  [Docent vult beschikbaarheid in via Tally Form 1]
        ↓
  Scenario 02 ── Verwerkt tijdsloten via GAS Script 2
              ── Slaat timeslotsRaw op in Available_Timeslots__c
              ── WhatsApp ouder met GAS Picker URL (via TinyURL)
              ── Parent_Invited_At__c = nu
              ── Status: Parent Invited

  Scenario 09 ── Reminder ouder 24u / escalatie 48u / No Show 72u
        ↓
  [Ouder klikt tijdslot op GAS Picker pagina]
        ↓
  Scenario 03 ──
    Pad A (chosen):
              ── Slaat Trial_Lesson_Date__c op (geen Z suffix)
              ── WhatsApp bevestiging naar ouder + docent (contactgegevens)
              ── Status: Trial Lesson Scheduled
    Pad B (no_match):
              ── TinyURL Tally Form 3
              ── WhatsApp docent: bel de ouder + link Form 3
              ── Status: Availability Conflict

  Scenario 05 ── Reminder docent elke 4u bij Availability Conflict
        ↓
  [Docent belt ouder → vult tijdslot in via Tally Form 3]
        ↓
  Scenario 04 ── Slaat tijdslot op
              ── WhatsApp bevestiging naar ouder + docent
              ── Status: Trial Lesson Scheduled

  Scenario 08 ── Reminders 48u / 24u / 2u voor proefles
```

---

## Referentie Documenten

| Document | Inhoud |
|----------|--------|
| [Gedeelde configuratie](gedeelde-configuratie.md) | 360dialog, TinyURL, MailerLite, GAS URLs, Salesforce velden, webhook URLs |
| [Google Apps Script](google-apps-script.md) | Script 1 (vakvertaling), Script 2 (tijdslotverwerking), Script 3 (picker v10) |
| [MailerLite inrichting](mailerlite.md) | Groepen, custom fields, automations, welkomstmail |
| [Beslissingen](beslissingen.md) | Alle technische en functionele beslissingen |

---

## Hoe deze docs te gebruiken

- Elk scenario heeft een eigen bestand in deze map
- Bestanden volgen de naamconventie: `scenario-[nr]-[korte-naam].md`
- Bij errors: open het relevante scenario-bestand → sectie "Foutmeldingen & Oplossingen"
- Bij bouwen nieuw scenario: check eerst [beslissingen.md](beslissingen.md) voor werkwijze afspraken
- JSON bodies altijd volledig kopiëren — nooit partial aanpassen
- API key altijd kopiëren van werkende module — nooit handmatig overtypen

---

> Documentatie gegenereerd via Claude Code — Bright Panda Tutoring
