# Scenario 7 — Internal Alert Teacher No Response

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Stuurt een intern WhatsApp alert naar Bright Panda (`31613689666`) wanneer een docent na **24 uur** nog steeds geen beschikbaarheid heeft ingevuld. Wordt eenmalig verstuurd dankzij het `Teacher_Escalation_Sent__c` veld.

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
[2]  Salesforce → Get a Record (Teacher Account)
        ↓
[3]  Salesforce → Get a Record (Student Account)
        ↓
[4]  HTTP POST → 360dialog (internal_alert_teacher_no_availability → 31613689666)
        ↓
[5]  Salesforce → Update a Record (Teacher_Escalation_Sent__c = true)
```

---

## Module 1 — SOQL

```sql
SELECT Id, Teacher__c, Student__c, Name, Trial_Lesson_Status__c,
       Teacher_Invited_At__c, Teacher_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Teacher Invited'
AND Teacher_Invited_At__c < {{formatDate(addHours(now; -24); "YYYY-MM-DDTHH:mm:ss")}}Z
AND Teacher_Escalation_Sent__c = false
```

> ⚠️ De tijdsfilter zit in de SOQL WHERE clause — niet in de router. Dit is betrouwbaarder dan datetime-vergelijking in Make.com router.

## Module 2 — Get Teacher Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output:** `{{2.FirstName}}`, `{{2.LastName}}`, `{{2.Phone}}`

## Module 3 — Get Student Account
- **Record ID:** `{{1.Student__c}}`
- **Output:** `{{3.FirstName}}`

---

## Module 4 — HTTP POST → 360dialog

```json
{
  "messaging_product": "whatsapp",
  "to": "31613689666",
  "type": "template",
  "template": {
    "name": "internal_alert_teacher_no_availability",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{2.LastName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{2.Phone}}"},
        {"type": "text", "text": "{{1.Name}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{2.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{2.LastName}}` | Achternaam docent |
| `{{3}}` | `{{3.FirstName}}` | Voornaam leerling |
| `{{4}}` | `{{2.Phone}}` | Telefoon docent |
| `{{5}}` | `{{1.Name}}` | Matching number (bijv. "Matching Number 0016") |

---

## Module 5 — Salesforce Update

- **Record ID:** `{{1.Id}}`
- `Teacher_Escalation_Sent__c` = `true`

---

## Template Tekst

```
⚠️ Actie vereist — Bright Panda intern!

Docent {{1}} {{2}} heeft na 24 uur nog geen beschikbaarheid ingevuld voor leerling {{3}}.

Neem direct contact op met de docent.

Docent telefoon: {{4}}
Matching: {{5}}

Bel nu!
```

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 1](scenario-01-docent-uitnodiging-whatsapp.md) | Zet `Teacher_Invited_At__c` timestamp bij uitnodiging |
| [Scenario 6](scenario-06-teacher-availability-reminder.md) | Reminders aan docent (12u eerste, daarna elke 2u) |
