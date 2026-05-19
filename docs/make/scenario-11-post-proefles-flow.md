# Scenario 11 — Post-Proefles Flow

**Laatste update:** 19 mei 2026
**Status:** ✅ Werkend — event-driven via Salesforce Flow

---

## Doel

Wordt automatisch getriggerd 70 minuten nadat de proefles heeft plaatsgevonden en:
1. Zet status op `Trial Lesson Completed`
2. Stuurt bevestiging naar ouder en docent
3. Stuurt intern alert naar Raouf, Yasin en zakelijk nummer
4. Voegt ouder toe aan MailerLite groep "Proefles Afgelopen"

---

## Architectuur

```
Status wijzigt naar Trial Lesson Scheduled in Salesforce
        ↓
Record-Triggered Flow (Post-Proefles Flow Trigger)
        ↓
Wacht 70 minuten na Trial_Lesson_Date__c
        ↓
Vul Request Body (Assignment)
        ↓
HTTP Callout → Make.com Webhook (Stuur Post Proefles naar Make)
        ↓
Scenario 11 triggert direct
```

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Salesforce Record-Triggered Flow + Custom Webhook |
| Salesforce Flow | Post-Proefles Flow Trigger |
| Webhook URL | `https://hook.eu1.make.com/pk888u999ewnnksom71zqatslfyhow8z` |
| Timing | 70 minuten na `Trial_Lesson_Date__c` |

> **Vervangt:** de oude polling trigger (elke 15 minuten, 96 onnodige runs per dag).

---

## Salesforce Flow configuratie

**Flow naam:** Post-Proefles Flow Trigger
**Type:** Record-Triggered Flow
**Object:** Student Teacher Matching
**Trigger:** A record is created or updated
**Condition:** `Trial_Lesson_Status__c` Equals `Trial Lesson Scheduled`
**When to Run:** Only when a record is updated to meet the condition requirements
**Optimize for:** Actions and Related Records

### Scheduled Path: 70 minuten na proefles

| Instelling | Waarde |
|---|---|
| Time Source | Student Teacher Matching: Trial Lesson Date |
| Offset Number | 70 |
| Offset Options | Minutes After |

### Assignment: Vul Request Body

Vult de `RequestBodyPostProefles` variabele (Apex-Defined, type `ExternalService__MakePostProeflesWebhook_SendPostProeflesToMake_IN_body`) met:

| Variable | Waarde |
|---|---|
| RequestBodyPostProefles > Id | `{!$Record.Id}` |
| RequestBodyPostProefles > Student__c | `{!$Record.Student__c}` |
| RequestBodyPostProefles > Teacher__c | `{!$Record.Teacher__c}` |
| RequestBodyPostProefles > Trial_Lesson_Date__c | `{!$Record.Trial_Lesson_Date__c}` |
| RequestBodyPostProefles > Trial_Lesson_Status__c | `{!$Record.Trial_Lesson_Status__c}` |

### Action: Stuur Post Proefles naar Make

**External Service:** MakePostProeflesWebhook
**Operation:** SendPostProeflesToMake
**Body:** `RequestBodyPostProefles`

---

## Salesforce Setup configuratie

### External Service
- **Name:** MakePostProeflesWebhook
- **Named Credential:** MakeNewStudentWebhook (hergebruikt van scenario 10)
- **OpenAPI schema:** zie onderaan dit document

### Permission Set
- **Name:** Make Webhook Access (hergebruikt van scenario 10)
- **Toegewezen aan:** Raouf Angudi

---

## Make.com Scenario 11 configuratie

**Trigger:** Custom Webhook (module 17)
**Webhook URL:** `https://hook.eu1.make.com/pk888u999ewnnksom71zqatslfyhow8z`

### Module volgorde

```
[17] Custom Webhook (trigger)
        ↓
[18] Webhook Response → {"accepted": true} + Content-Type: application/json
        ↓
[2]  Salesforce → Get a Record (Teacher Account)
        ↓
[3]  Salesforce → Get a Record (Student Account)
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

### Webhook data (module 17)

| Veld | Inhoud |
|---|---|
| `17.Id` | Matching record ID |
| `17.Student__c` | Student record ID |
| `17.Teacher__c` | Teacher record ID |
| `17.Trial_Lesson_Date__c` | Datum en tijd proefles |
| `17.Trial_Lesson_Status__c` | `Trial Lesson Scheduled` |

### Webhook Response (module 18)

Status: `200`
Body: `{"accepted": true}`
Custom Headers: `Content-Type` = `application/json`

---

## Module 2 — Get Teacher Account
- **Record ID:** `{{17.Teacher__c}}`

## Module 3 — Get Student Account
- **Record ID:** `{{17.Student__c}}`

## Module 4 — Salesforce Update
- **Record ID:** `{{17.Id}}`
- `Trial_Lesson_Status__c` = `Trial Lesson Completed`

---

## Slack module — Interne alert

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "Proefles afgerond — bel de ouder op!"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Leerling:* {{3.FirstName}} {{3.LastName}}"},
        {"type": "mrkdwn", "text": "*Ouder:* {{3.ParentSName__c}}"},
        {"type": "mrkdwn", "text": "*Telefoon:* {{3.ParentSPhone__c}}"},
        {"type": "mrkdwn", "text": "*Docent:* {{2.FirstName}} {{2.LastName}}"},
        {"type": "mrkdwn", "text": "*Vakken:* {{3.Subjects__c}}"},
        {"type": "mrkdwn", "text": "*Datum:* {{formatDate(17.Trial_Lesson_Date__c; \"DD-MM-YYYY\")}}"}
      ]
    }
  ]
}
```

---

## OpenAPI Schema (MakePostProeflesWebhook)

```json
{
  "openapi": "3.0.1",
  "info": {"title": "MakePostProeflesWebhook", "description": ""},
  "servers": [{"url": "https://hook.eu1.make.com"}],
  "paths": {
    "/pk888u999ewnnksom71zqatslfyhow8z": {
      "post": {
        "operationId": "SendPostProeflesToMake",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "Id": {"type": "string"},
                  "Student__c": {"type": "string"},
                  "Teacher__c": {"type": "string"},
                  "Trial_Lesson_Date__c": {"type": "string"},
                  "Trial_Lesson_Status__c": {"type": "string"}
                }
              }
            }
          },
          "required": true
        },
        "responses": {
          "2XX": {"description": "", "content": {"text/plain": {"schema": {"type": "string"}}}}
        }
      }
    }
  }
}
```

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 8](scenario-08-lesson-date-reminder.md) | Reminders 48u/24u/2u vóór de proefles |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Zet status op Trial Lesson Scheduled |
| [Scenario 4](scenario-04-teacher-timeslot-submission.md) | Alternatieve weg naar Trial Lesson Scheduled |
| [salesforce-flow-webhook-integratie.md](salesforce-flow-webhook-integratie.md) | Patroon voor Salesforce Flow naar Make.com webhook |
