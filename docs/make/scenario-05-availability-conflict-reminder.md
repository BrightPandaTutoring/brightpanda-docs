# Scenario 5 — Availability Conflict Reminder

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Stuurt elke 4 uur een herinnerings-WhatsApp naar een docent zolang de matching status `Availability Conflict` heeft en er nog geen definitieve datum is ingepland. De docent wordt herinnerd om de ouder te bellen en Tally Form 3 in te vullen.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 4 uur |

---

## Module Volgorde

```
[1]  Salesforce → Search Records SOQL
        ↓
[2]  Salesforce → Get a Record (Teacher Account) [Ignore error handler]
        ↓
[3]  Salesforce → Get a Record (Student Account)
        ↓
[5]  HTTP POST → TinyURL (Tally Form 3 link verkorten)
        ↓
[4]  HTTP POST → 360dialog (availability_conflict_teacher_reminder)
        ↓
[6]  Salesforce → Update Record (Teacher_Escalation_Sent__c = true)
```

---

## Module 1 — SOQL

```sql
SELECT Id, Teacher__c, Student__c, Name, Tally_Link_Teacher__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Availability Conflict'
AND Trial_Lesson_Date__c = NULL
```

## Module 2 — Get Teacher Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output:** `{{2.FirstName}}`, `{{2.Phone}}`

## Module 3 — Get Student Account
- **Record ID:** `{{1.Student__c}}`
- **Output:** `{{3.FirstName}}`, `{{3.ParentsName__c}}`, `{{3.ParentSPhone__c}}`

## Module 5 — HTTP POST → TinyURL

**JSON body:**
```json
{
  "url": "https://tally.so/r/q4PDV9?matching_number={{encodeURL(1.Name)}}",
  "domain": "go.brightpanda.nl"
}
```

- **API Endpoint:** `https://api.tinyurl.com/create`
- **Header:** `Authorization: Bearer azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji`
- **Output:** `{{5.data.data.tiny_url}}`

## Module 4 — HTTP POST → 360dialog

```json
{
  "messaging_product": "whatsapp",
  "to": "{{2.Phone}}",
  "type": "template",
  "template": {
    "name": "availability_conflict_teacher_reminder",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{3.ParentsName__c}}"},
        {"type": "text", "text": "{{3.ParentSPhone__c}}"},
        {"type": "text", "text": "{{5.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

## Module 5 — Salesforce Update
- **Record ID:** `{{1.Id}}`
- `Teacher_Escalation_Sent__c` = `true`

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Zet status op Availability Conflict (Pad B) |
| [Scenario 4](scenario-04-teacher-timeslot-submission.md) | Verwerkt Tally Form 3 wanneer docent reageert |
