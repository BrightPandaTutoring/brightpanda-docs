# Scenario 8 — Lesson Date Reminder

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Stuurt automatische herinneringen aan docent en ouder voor een geplande proefles op **48 uur**, **24 uur** en **2 uur** van tevoren. Aparte checkbox velden voorkomen dubbele berichten.

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
[Router] — 4 routes op basis van tijdvenster + checkbox
    ├── Route 1 (48u — docent)
    │   [4]  HTTP POST 360dialog → lesson_reminder_48h_teacher
    │   [5]  Salesforce Update → Trial_Class_Reminder_48h_Sent__c = true
    │
    ├── Route 2 (24u — ouder)
    │   [6]  HTTP POST 360dialog → lesson_reminder_24h_parent
    │   [7]  Salesforce Update → Trial_Class_Reminder_24h_Sent__c = true
    │
    ├── Route 3 (2u — docent)
    │   [8]  HTTP POST 360dialog → lesson_reminder_2h_teacher
    │   [9]  Salesforce Update → Trial_Class_Reminder_2h_Sent__c = true
    │
    └── Route 4 (2u — ouder)
        [10] HTTP POST 360dialog → lesson_reminder_2h_parent
        (geen aparte update — Route 3 zet al 2h checkbox)
```

---

## Module 1 — SOQL

```sql
SELECT Id, Teacher__c, Student__c, Name, Trial_Lesson_Date__c,
       Trial_Class_Reminder_48h_Sent__c, Trial_Class_Reminder_24h_Sent__c,
       Trial_Class_Reminder_2h_Sent__c, Trial_Lesson_Status__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Trial Lesson Scheduled'
```

## Module 2 — Get Teacher Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output:** `{{2.FirstName}}`, `{{2.Phone}}`

## Module 3 — Get Student Account
- **Record ID:** `{{1.Student__c}}`
- **Output:** `{{3.FirstName}}`, `{{3.ParentsName__c}}`, `{{3.ParentSPhone__c}}`

---

## Router Filters

> ⚠️ **Gebruik Text operators** — Boolean operators werken niet correct voor checkbox velden in Make.com router filters.

### Route 1 — 48u Reminder (docent)

| Conditie | Operator | Waarde |
|---------|----------|--------|
| `1.Trial_Lesson_Date__c` | Greater than or equal to | `{{formatDate(addHours(now; 47); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Lesson_Date__c` | Less than or equal to | `{{formatDate(addHours(now; 49); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Class_Reminder_48h_Sent__c` | Text — Equal to | `false` |

### Route 2 — 24u Reminder (ouder)

| Conditie | Operator | Waarde |
|---------|----------|--------|
| `1.Trial_Lesson_Date__c` | Greater than or equal to | `{{formatDate(addHours(now; 23); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Lesson_Date__c` | Less than or equal to | `{{formatDate(addHours(now; 25); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Class_Reminder_24h_Sent__c` | Text — Equal to | `false` |

### Route 3 — 2u Reminder (docent)

| Conditie | Operator | Waarde |
|---------|----------|--------|
| `1.Trial_Lesson_Date__c` | Greater than or equal to | `{{formatDate(addHours(now; 1); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Lesson_Date__c` | Less than or equal to | `{{formatDate(addHours(now; 3); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Class_Reminder_2h_Sent__c` | Text — Equal to | `false` |

### Route 4 — 2u Reminder (ouder)

| Conditie | Operator | Waarde |
|---------|----------|--------|
| `1.Trial_Lesson_Date__c` | Greater than or equal to | `{{formatDate(addHours(now; 1); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Lesson_Date__c` | Less than or equal to | `{{formatDate(addHours(now; 3); "YYYY-MM-DDTHH:mm:ss")}}Z` |
| `1.Trial_Class_Reminder_2h_Sent__c` | Text — Equal to | `false` |

> ⚠️ Routes 3 en 4 hebben dezelfde filterconditie. Route 3 zet `Trial_Class_Reminder_2h_Sent__c = true` — daarna triggert Route 4 niet meer. Zorg dat Route 3 vóór Route 4 staat in de router.

---

## Module 4 — Route 1: lesson_reminder_48h_teacher

```json
{
  "messaging_product": "whatsapp",
  "to": "{{2.Phone}}",
  "type": "template",
  "template": {
    "name": "lesson_reminder_48h_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"HH:mm\"; \"Europe/Amsterdam\")}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{2.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{3.FirstName}}` | Voornaam leerling |
| `{{3}}` | `{{formatDate(...)}}` | Datum (DD-MM-YYYY, Amsterdam tijdzone) |
| `{{4}}` | `{{formatDate(...)}}` | Tijd (HH:mm, Amsterdam tijdzone) |

**Update na Route 1:** `Trial_Class_Reminder_48h_Sent__c = true`, Record ID: `{{1.Id}}`

---

## Module 6 — Route 2: lesson_reminder_24h_parent

```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "lesson_reminder_24h_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.ParentsName__c}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"HH:mm\"; \"Europe/Amsterdam\")}}"}
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
| `{{4}}` | `{{formatDate(...)}}` | Datum (DD-MM-YYYY, Amsterdam tijdzone) |
| `{{5}}` | `{{formatDate(...)}}` | Tijd (HH:mm, Amsterdam tijdzone) |

**Update na Route 2:** `Trial_Class_Reminder_24h_Sent__c = true`, Record ID: `{{1.Id}}`

---

## Module 8 — Route 3: lesson_reminder_2h_teacher

```json
{
  "messaging_product": "whatsapp",
  "to": "{{2.Phone}}",
  "type": "template",
  "template": {
    "name": "lesson_reminder_2h_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"HH:mm\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{3.ParentsName__c}}"},
        {"type": "text", "text": "{{3.ParentSPhone__c}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{2.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{3.FirstName}}` | Voornaam leerling |
| `{{3}}` | `{{formatDate(...)}}` | Datum (DD-MM-YYYY, Amsterdam tijdzone) |
| `{{4}}` | `{{formatDate(...)}}` | Tijd (HH:mm, Amsterdam tijdzone) |
| `{{5}}` | `{{3.ParentsName__c}}` | Naam ouder |
| `{{6}}` | `{{3.ParentSPhone__c}}` | Telefoon ouder |

**Update na Route 3:** `Trial_Class_Reminder_2h_Sent__c = true`, Record ID: `{{1.Id}}`

---

## Module 10 — Route 4: lesson_reminder_2h_parent

```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "lesson_reminder_2h_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.ParentsName__c}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{2.FirstName}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"DD-MM-YYYY\"; \"Europe/Amsterdam\")}}"},
        {"type": "text", "text": "{{formatDate(1.Trial_Lesson_Date__c; \"HH:mm\"; \"Europe/Amsterdam\")}}"}
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
| `{{4}}` | `{{formatDate(...)}}` | Datum (DD-MM-YYYY, Amsterdam tijdzone) |
| `{{5}}` | `{{formatDate(...)}}` | Tijd (HH:mm, Amsterdam tijdzone) |

> Route 4 zet geen aparte checkbox — `Trial_Class_Reminder_2h_Sent__c` is al `true` gezet door Route 3.

---

## Salesforce Velden

| Veld | Type | Gebruik |
|------|------|---------|
| `Trial_Class_Reminder_48h_Sent__c` | Checkbox | Voorkomt dubbele 48u reminder |
| `Trial_Class_Reminder_24h_Sent__c` | Checkbox | Voorkomt dubbele 24u reminder |
| `Trial_Class_Reminder_2h_Sent__c` | Checkbox | Voorkomt dubbele 2u reminder (docent + ouder) |

---

## formatDate Timezone

> ⚠️ **Gebruik altijd `"Europe/Amsterdam"` als derde argument** in `formatDate()` voor `Trial_Lesson_Date__c`. Zonder tijdzone toont de tijd 1 uur vroeger (UTC).

```
{{formatDate(1.Trial_Lesson_Date__c; "DD-MM-YYYY"; "Europe/Amsterdam")}}  → "15-03-2026"
{{formatDate(1.Trial_Lesson_Date__c; "HH:mm"; "Europe/Amsterdam")}}       → "10:00"
```

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Zet status op Trial Lesson Scheduled (Pad A) |
| [Scenario 4](scenario-04-teacher-timeslot-submission.md) | Zet status op Trial Lesson Scheduled (na Availability Conflict) |
