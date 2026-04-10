# Scenario 11 — Post-Proefles Flow

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — ⚠️ tijdzone tijdelijk hardcoded (+01:00 wintertijd)

---

## Doel

Detecteert automatisch wanneer een proefles heeft plaatsgevonden (60-75 minuten na `Trial_Lesson_Date__c`) en:
1. Zet status op `Trial Lesson Completed`
2. Stuurt bevestiging naar ouder en docent
3. Stuurt intern alert naar Raouf, Yasin en zakelijk nummer
4. Voegt ouder toe aan MailerLite groep "Proefles Afgelopen"

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 15 minuten |

---

## Module Volgorde

```
[1]  Salesforce → Search Records SOQL
        ↓
[2]  Salesforce → Get a Record (Teacher Account) [Ignore error handler]
        ↓
[3]  Salesforce → Get a Record (Student Account) [Ignore error handler]
        ↓
[4]  Salesforce → Update a Record (Trial_Lesson_Status__c = Trial Lesson Completed)
        ↓
[5]  HTTP POST → 360dialog (trial_lesson_completed_parent → ouder)
        ↓
[7]  MailerLite → Create/Update Subscriber + groep "Proefles Afgelopen"
        ↓
[10] HTTP POST → 360dialog (intern alert → Raouf)
        ↓
[11] HTTP POST → 360dialog (intern alert → Yasin)
        ↓
[12] HTTP POST → 360dialog (intern alert → zakelijk)
        ↓
[15] HTTP POST → 360dialog (trial_lesson_completed_teacher → docent)
```

---

## Module 1 — SOQL

```sql
SELECT Id, Name, Teacher__c, Student__c, Trial_Lesson_Status__c, Trial_Lesson_Date__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Trial Lesson Scheduled'
AND Trial_Lesson_Date__c < {{formatDate(addMinutes(now; -60); "YYYY-MM-DDTHH:mm:ss"; "Europe/Amsterdam")}}+01:00
AND Trial_Lesson_Date__c > {{formatDate(addMinutes(now; -75); "YYYY-MM-DDTHH:mm:ss"; "Europe/Amsterdam")}}+01:00
```

> ⚠️ **Tijdzone tijdelijk hardcoded:** `+01:00` is wintertijd (CET). In zomertijd (CEST, +02:00) klopt dit niet — de les wordt dan 1 uur te laat gedetecteerd.
> **Fix:** `{{formatDate(addMinutes(now; -60); "YYYY-MM-DDTHH:mm:ssZ"; "Europe/Amsterdam")}}` — testen na zomertijd overgang.

**Logica:** Detecteert lessen die 60-75 minuten geleden begonnen zijn. Tijdvenster van 15 minuten matcht het scenario-interval.

## Module 2 — Get Teacher Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output:** `{{2.FirstName}}`, `{{2.Phone}}`
- **Ignore error handler:** ✅ (voorkomt crash bij ontbrekend account)

## Module 3 — Get Student Account
- **Record ID:** `{{1.Student__c}}`
- **Output:** `{{3.FirstName}}`, `{{3.ParentsName__c}}`, `{{3.ParentSPhone__c}}`, `{{3.ParentSEmail__c}}`
- **Ignore error handler:** ✅

---

## Module 4 — Salesforce Update

- **Record ID:** `{{1.Id}}`
- `Trial_Lesson_Status__c` = `Trial Lesson Completed`

---

## Module 5 — trial_lesson_completed_parent

```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_completed_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.ParentsName__c}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{2.FirstName}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{3.ParentsName__c}}` | Naam ouder |
| `{{2}}` | `{{3.FirstName}}` | Voornaam leerling |
| `{{3}}` | `{{2.FirstName}}` | Voornaam docent |

---

## Module 7 — MailerLite Update

- **Actie:** Create/Update Subscriber
- **Email:** `{{3.ParentSEmail__c}}`
- **Groep:** `Proefles Afgelopen`

> ⚠️ Scenario crashte tijdens test omdat `ParentSEmail__c` leeg was in testmatching. Fix: zorg dat testrecords volledig zijn, of voeg error handler toe.

---

## Modules 10, 11, 12 — Interne Alerts

**Template:** `internal_alert_trial_lesson_completed` (5 params)

| Module | Naar | Nummer |
|--------|------|--------|
| 10 | Raouf | `31630892143` |
| 11 | Yasin | `31623325599` |
| 12 | Zakelijk | `31613689666` |

```json
{
  "messaging_product": "whatsapp",
  "to": "{{NUMMER}}",
  "type": "template",
  "template": {
    "name": "internal_alert_trial_lesson_completed",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{1.Name}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"HH:mm\"; \"Europe/Amsterdam\")}}"}
      ]
    }]
  }
}
```

---

## Module 15 — trial_lesson_completed_teacher

```json
{
  "messaging_product": "whatsapp",
  "to": "{{2.Phone}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_completed_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{2.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{3.FirstName}}` | Voornaam leerling |

> Template heeft een **phone button** — docent kan direct bellen.

---

## Openstaande Verbeteringen

> ⚠️ **Tijdzone fix:** `+01:00` vervangen door dynamische tijdzone. Fix na zomertijd overgang testen.
> ⚠️ **ParentSEmail__c:** Error handler toevoegen bij lege emailadressen voor MailerLite module.

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 8](scenario-08-lesson-date-reminder.md) | Reminders 48u/24u/2u vóór de proefles |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Zet status op Trial Lesson Scheduled |
| [Scenario 4](scenario-04-teacher-timeslot-submission.md) | Alternatieve weg naar Trial Lesson Scheduled |
