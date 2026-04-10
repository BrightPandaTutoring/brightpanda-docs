# Scenario 4 — Teacher Timeslot Submission

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Verwerkt het tijdslot dat een docent indient via **Tally Form 3** (na een Availability Conflict). Slaat de definitieve datum op in Salesforce en stuurt bevestigings-WhatsApp naar ouder en docent.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook URL | `https://hook.eu1.make.com/1aa2q2bnkvxodps6errjs6pxs3j4v4d9` |
| Afzender | Tally Form 3 (`https://tally.so/r/q4PDV9`) |

---

## Tally Form 3 — Veldstructuur

| Index | Veld | Format |
|-------|------|--------|
| `fields[1].value` | matching_number (hidden) | `"Matching Number 0016"` |
| `fields[2].value` | datum | `"2026-03-15"` |
| `fields[3].value` | starttijd | `"10:00"` (HH:mm) |

---

## Module Volgorde

```
[1]  Webhook → Custom Webhook (Tally Form 3)
        ↓
[2]  Salesforce → Search Records SOQL (matching ophalen)
        ↓
[3]  Salesforce → Get a Record (Student Account)
        ↓
[4]  Salesforce → Get a Record (Teacher Account)
        ↓
[5]  Salesforce → Update a Record (datum + status)
        ↓
[6]  HTTP POST → 360dialog (WhatsApp naar ouder)
        ↓
[7]  HTTP POST → 360dialog (WhatsApp naar docent)
```

---

## Modules Detail

### Module 2 — Salesforce Search Records SOQL

```sql
SELECT Id, Teacher__c, Student__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{1.data.fields[1].value}}'
```

### Module 3 — Salesforce Get a Record (Student)
- **Record ID:** `{{2.Student__c}}`
- **Output:** `{{3.FirstName}}`, `{{3.ParentsName__c}}`, `{{3.ParentSPhone__c}}`

> ⚠️ Veldnaam inconsistentie: controleer in module output of het veld `ParentSName__c` of `ParentsName__c` heet.

### Module 4 — Salesforce Get a Record (Teacher)
- **Record ID:** `{{2.Teacher__c}}`
- **Output:** `{{4.FirstName}}`, `{{4.Phone}}`

### Module 5 — Salesforce Update a Record
- **Record ID:** `{{2.Id}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Date__c` | `{{1.data.fields[2].value}}T{{1.data.fields[3].value}}:00.000` |
| `Trial_Lesson_Status__c` | `Trial Lesson Scheduled` |

> Geen Z suffix — zie [beslissing B10](beslissingen.md).

### Module 6 — HTTP POST → 360dialog (WhatsApp naar ouder)

```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_confirmation_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.ParentSName__c}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{formatDate(1.data.fields[2].value; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{1.data.fields[3].value}}"},
        {"type": "text", "text": "{{4.FirstName}}"},
        {"type": "text", "text": "{{4.Phone}}"}
      ]
    }]
  }
}
```

### Module 7 — HTTP POST → 360dialog (WhatsApp naar docent)

```json
{
  "messaging_product": "whatsapp",
  "to": "{{4.Phone}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_confirmed_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{4.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{formatDate(1.data.fields[2].value; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{1.data.fields[3].value}}"},
        {"type": "text", "text": "{{3.ParentSName__c}}"},
        {"type": "text", "text": "{{3.ParentSPhone__c}}"}
      ]
    }]
  }
}
```

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Triggert Availability Conflict (Pad B) |
| [Scenario 5](scenario-05-availability-conflict-reminder.md) | Reminder docent elke 4u zolang conflict open staat |
| [Scenario 8](scenario-08-lesson-date-reminder.md) | Reminders vóór de proefles |
