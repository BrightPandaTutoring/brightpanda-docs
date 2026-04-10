# Scenario 6 — Teacher Availability Reminder

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Stuurt automatisch een herinnerings-WhatsApp naar een docent die na 12 uur nog geen beschikbaarheid heeft ingevuld. Twee routes: eerste reminder (één keer) en herhaalde reminder (elke 2 uur daarna).

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 2 uur |

---

## Module Volgorde

```
[1]  Salesforce → Search Records SOQL
        ↓
[2]  Salesforce → Get a Record (Teacher Account) [Ignore error handler]
        ↓
[3]  Salesforce → Get a Record (Student Account)
        ↓
[Router]
    ├── Route 1 (First Reminder): Teacher_Reminder_Sent__c = false
    │   [8]  HTTP POST → TinyURL (Tally Form 1 link verkorten)
    │   [4]  HTTP POST 360dialog → teacher_availability_reminder
    │   Update: Teacher_Reminder_Sent__c = true
    │
    └── Route 2 (Repeat Reminder): Teacher_Reminder_Sent__c = true
        [9]  HTTP POST → TinyURL (Tally Form 1 link verkorten)
        [7]  HTTP POST 360dialog → teacher_availability_reminder_repeat
```

---

## Module 1 — SOQL

```sql
SELECT Id, Teacher__c, Student__c, Name,
       Tally_Link_Teacher__c, Teacher_Reminder_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Teacher Invited'
AND Teacher_Invited_At__c < {{formatDate(addHours(now; -12); "YYYY-MM-DDTHH:mm:ss")}}Z
```

## Module 2 — Get Teacher Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output:** `{{2.FirstName}}`, `{{2.Phone}}`

## Module 3 — Get Student Account
- **Record ID:** `{{1.Student__c}}`
- **Output:** `{{3.FirstName}}`

---

## Router Filters

> ⚠️ **Gebruik Text operators** — Boolean operators werken niet correct voor checkbox velden in Make.com router filters.

| Route | Conditie | Operator |
|-------|----------|----------|
| Route 1 (First Reminder) | `1.Teacher_Reminder_Sent__c` = `false` | Text — Equal to |
| Route 2 (Repeat Reminder) | `1.Teacher_Reminder_Sent__c` = `true` | Text — Equal to |

---

## Module 8 — Route 1: TinyURL (Tally Form 1 link)

```json
{
  "url": "{{1.Tally_Link_Teacher__c}}",
  "domain": "go.brightpanda.nl"
}
```

- **API Endpoint:** `https://api.tinyurl.com/create`
- **Header:** `Authorization: Bearer azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji`
- **Output:** `{{8.data.data.tiny_url}}`

## Module 4 — Route 1: teacher_availability_reminder

```json
{
  "messaging_product": "whatsapp",
  "to": "{{2.Phone}}",
  "type": "template",
  "template": {
    "name": "teacher_availability_reminder",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{8.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

**Update na Route 1:** `Teacher_Reminder_Sent__c = true`, Record ID: `{{1.Record ID}}`

---

## Module 9 — Route 2: TinyURL (Tally Form 1 link)

```json
{
  "url": "{{1.Tally_Link_Teacher__c}}",
  "domain": "go.brightpanda.nl"
}
```

- **Output:** `{{9.data.data.tiny_url}}`

## Module 7 — Route 2: teacher_availability_reminder_repeat

```json
{
  "messaging_product": "whatsapp",
  "to": "{{2.Phone}}",
  "type": "template",
  "template": {
    "name": "teacher_availability_reminder_repeat",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{9.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 1](scenario-01-docent-uitnodiging-whatsapp.md) | Zet status Teacher Invited + Teacher_Invited_At__c |
| [Scenario 7](scenario-07-internal-alert.md) | Intern alert na 24u geen reactie |
