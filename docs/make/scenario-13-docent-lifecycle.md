# Scenario 13 — Docent Lifecycle Automation

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Automatiseert de volledige docent-lifecycle op basis van wijzigingen in `Lifecycle_Stage__c` op het Teacher Account. Stuurt WhatsApp berichten, beheert MailerLite groepen, verstuurt contracten via DocuSeal, en schrijft offboarding datum terug naar Salesforce.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Watch Records |
| Object | Account (Teacher) |
| Filter | `RecordTypeId = 012KB000000ojZLYAY` |

---

## Lifecycle Stages

| Stage | Trigger door | Make.com actie |
|-------|-------------|----------------|
| `New` | Nieuwe aanmelding | → Scenario 12 (Claude analyse) |
| `Interview Invited` | Handmatig in Salesforce | → Route 1: MailerLite + WhatsApp |
| `Interview Scheduled` | Handmatig | — |
| `Interview Completed` | Handmatig | — |
| `Contracting` | Handmatig na positief interview | → Route 2: DocuSeal contract |
| `Pending Onboarding` | Scenario 14 (contract getekend) | — |
| `On-boarded` | Handmatig | → Route 3: MailerLite groep update |
| `Contract Expiring Soon` | Salesforce Flow (335 dagen na start) | — (handmatige beoordeling) |
| `Renew` | Handmatig | — |
| `Not a Match` | Handmatig | → Route 4: verwijder MailerLite |
| `Not Interested` | Handmatig | → Route 4: verwijder MailerLite |
| `Offboarded` | Handmatig | → Route 4: verwijder MailerLite + `Offboarded_Date__c` |
| `Churned` | Handmatig | — |

---

## Module Volgorde

```
[Watch Records — Teacher Account]
        ↓
[Router] — splitst op Lifecycle_Stage__c
    │
    ├── Route 1 (Interview Invited)
    │   [MailerLite] → Voeg toe aan groep "Interview Invited"
    │   [MailerLite] → Start automation "Interview Uitnodiging"
    │   [HTTP POST] → WhatsApp naar docent (interview uitnodiging)
    │
    ├── Route 2 (Contracting)
    │   [Bereken] Contract_End_Date = Contract_Start_Date + 365 dagen
    │   [Salesforce Update] → Contract_End_Date__c
    │   [HTTP POST] → DocuSeal contract versturen
    │
    ├── Route 3 (On-boarded)
    │   [MailerLite] → Voeg toe aan groep "On-boarded Docenten"
    │
    └── Route 4 (Not a Match / Not Interested / Offboarded)
        [MailerLite] → Verwijder subscriber (of markeer als unsubscribed)
        [Salesforce Update] → Offboarded_Date__c = {{now}} (alleen bij Offboarded)
```

---

## Route 2 — Contracting: DocuSeal Contract

**Endpoint:** `https://api.docuseal.eu/submissions`
**Header:** `X-Auth-Token: kF6DXM8V8AEJcRhXshwE1RxdvarDx9NHwuYjd9FnZz3`

```json
{
  "template_id": 485548,
  "send_email": true,
  "submitters": [{
    "role": "First Party",
    "email": "{{TEACHER_EMAIL}}",
    "fields": [
      {"name": "name", "default_value": "{{TEACHER_OFFICIALNAME}}"},
      {"name": "street", "default_value": "{{TEACHER_STREET}}"},
      {"name": "city", "default_value": "{{TEACHER_CITY}}"},
      {"name": "start_date", "default_value": "{{CONTRACT_START_DATE}}"},
      {"name": "hourly_rate", "default_value": "{{TEACHER_HOURLYRATE}}"},
      {"name": "signing_date", "default_value": "{{TODAY}}"}
    ]
  }]
}
```

**DocuSeal Template velden (exact lowercase):**

| Veld naam | Salesforce bron | Beschrijving |
|-----------|----------------|-------------|
| `name` | `OfficialName__c` | Officiële naam voor contract |
| `street` | `MailingStreet` | Straat + huisnummer |
| `city` | `MailingCity` | Woonplaats |
| `start_date` | `Contract_Start_Date__c` | Startdatum contract |
| `hourly_rate` | `HourlyRate__c` | Uurtarief docent |
| `signing_date` | `{{now}}` | Datum ondertekening |
| `signature` | — | Wordt door docent ingevuld |

> ⚠️ **Veldnamen zijn exact lowercase** — `Name` geeft error, moet `name` zijn.
> ⚠️ **Prijs:** $0.20 per contract via Make.com + DocuSeal EU plan.

**Contract_End_Date berekening:**
- `Contract_End_Date__c` = `Contract_Start_Date__c` + 365 dagen
- Berekend via `formatDate(addDays(X.Contract_Start_Date__c; 365); "YYYY-MM-DD")`

**Contract verlenging:**
- Salesforce Flow triggert `Lifecycle_Stage__c = Contract Expiring Soon` na 335 dagen (30 dagen voor einde)
- Verlenging: **handmatige beoordeling** — geen automatische verlenging
- Daarna: handmatig `Lifecycle_Stage__c = Renew` of `Offboarded` zetten

---

## Route 4 — Offboarding

**MailerLite:** Verwijder subscriber of markeer als unsubscribed

**Salesforce Update** (alleen bij `Offboarded`):
- `Offboarded_Date__c` = `{{now}}`

> ⚠️ `Offboarded_Date__c` wordt via Make.com gevuld — geen Salesforce Flow nodig.

---

## Salesforce Teacher Account Velden

| Veld | Type | Beschrijving |
|------|------|-------------|
| `Lifecycle_Stage__c` | Picklist | Huidige fase in docent lifecycle |
| `Claude_Recommendation__c` | Text Area Long | AI aanbeveling (Scenario 12) |
| `OfficialName__c` | Text | Naam voor contract (officieel) |
| `HourlyRate__c` | Number | Uurtarief |
| `Contract_Start_Date__c` | Date | Startdatum contract |
| `Contract_End_Date__c` | Date | Einddatum contract (start + 365) |
| `Offboarded_Date__c` | Date | Datum offboarding |
| `IBAN__c` | Text | IBAN bankrekening (via Tally Form AVG-compliant) |
| `Teaching_Level_Details__c` | Text | Niveaudetails per vak |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 12](scenario-12-docent-new-registration.md) | Claude analyse bij nieuwe aanmelding |
| [Scenario 14](scenario-14-docuseal-webhook.md) | Verwerkt getekend contract → Pending Onboarding |
