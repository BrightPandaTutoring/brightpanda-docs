# Scenario 19 — Documentation Reminder Pending Onboarding

**Laatste update:** 19 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Herinnert docenten in Pending Onboarding via WhatsApp om het Tally akkoord-formulier in te vullen (Docent Gids gelezen). Vult `Documentation_Reminder_Sent__c` zodra de reminder is verstuurd, zodat er niet meerdere reminders worden verzonden.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Dagelijks |

---

## Module Volgorde

```
[1]  Salesforce → Search Records SOQL (Pending Onboarding docenten zonder reminder)
        ↓
  [FILTER: Docent found — 1.Total number of bundles > 0]  ← toegevoegd 19 april 2026
        ↓
[2]  Iterator (over SOQL resultaten)
        ↓
[3]  HTTP → POST 360dialog WhatsApp (documentation_reminder template)
        ↓
[4]  Salesforce → Update Record (Documentation_Reminder_Sent__c = vandaag)
```

---

## Filter "Docent found" (tussen module 1 en 2)

**Kritieke regel toegevoegd 19 april 2026 na fix:**

| Veld | Waarde |
|------|--------|
| **Label** | `Docent found` |
| **Conditie** | `1.Total number of bundles` |
| **Operator** | `Numeric operators: Greater than` |
| **Waarde** | `0` |

**Waarom dit filter nodig is:**
Bij 0 SOQL resultaten draaide de iterator toch een lege bundle door, waardoor de WhatsApp module een lege `to` parameter kreeg. 360dialog gaf dan:
```
DataError: The parameter to is required
```

De fix voorkomt dat downstream modules met lege bundles worden uitgevoerd.

> **Algemene regel voor alle Make.com scenarios:** bij een iterator die op SOQL of vergelijkbare resultaten draait, altijd een filter vóór de iterator toevoegen op `Total number of bundles > 0`. Zie ook CLAUDE.md regel 13.

---

## Module 1 — SOQL Query

```sql
SELECT Id, Name, FirstName, PersonMobilePhone, PersonEmail, Pending_Onboarding_Date__c
FROM Account
WHERE RecordTypeId = '012KB000000ojZLYAY'
AND LifecycleStage__c = 'Pending Onboarding'
AND Documentation_Agreed__c = NULL
AND Documentation_Reminder_Sent__c = NULL
AND Pending_Onboarding_Date__c <= [aantal dagen geleden]
```

---

## Module 3 — 360dialog WhatsApp (documentation_reminder)

- **Endpoint:** `https://waba-v2.360dialog.io/messages`
- **Template:** `documentation_reminder` (of hergebruikt bestaand template)
- **Phone:** `replace({{2.PersonMobilePhone}}; "+"; "")`

---

## Module 4 — Salesforce Update

- **Record ID:** `{{2.Id}}`
- `Documentation_Reminder_Sent__c` = vandaag

---

## Test (19 april 2026)

Getest met **Raouf Angudi Teacher** record:
- `Pending_Onboarding_Date__c` tijdelijk op 12 april gezet → viel binnen query window
- WhatsApp correct verstuurd ✅
- `Documentation_Reminder_Sent__c` correct gevuld ✅
- Na test: lifecycle teruggezet naar On-boarded

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 14](scenario-14-docuseal-webhook.md) | Zet docent naar Pending Onboarding |
| Scenario 15 | Tally reminder (andere reminder soort) |
| Scenario 17 | Auto On-boarded wanneer alle velden ingevuld zijn |
