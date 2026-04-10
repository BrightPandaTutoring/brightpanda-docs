# Scenario 3b — Trial Lesson Scheduled & Availability Conflict

**Make naam:** Scenario 3b (intern genummerd als Scenario 3)
**Make Scenario ID:** 4783259 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Pad A én Pad B werkend

---

## Doel

Ontvangt de keuze van een ouder via de **Google Apps Script picker pagina**. Bij Pad A: bevestigt de proefles naar ouder en docent. Bij Pad B (geen tijdslot past): stuurt de docent instructie om de ouder te bellen en geeft Tally Form 3 link om het afgesproken tijdslot in te vullen.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook URL | `https://hook.eu1.make.com/jgrnq4k8yob8txh5x0jn2ojxx94awnwr` |
| Afzender | Google Apps Script picker v11 (POST na klik) |

---

## Webhook Input — Velden van GAS Picker

| Veld | Inhoud | Voorbeeld |
|------|--------|-----------|
| `{{3.matching_number}}` | Volledige matching naam | `"Matching Number 0016"` |
| `{{3.student_name}}` | Voornaam student | `"Emma"` |
| `{{3.chosen}}` | Keuzenummer (Pad A) | `2` |
| `{{3.chosen_date}}` | Leesbare datum | `"15 mrt"` |
| `{{3.chosen_date_iso}}` | ISO datum | `"2026-03-15"` |
| `{{3.chosen_time}}` | Tijdslot string | `"10:00-11:00"` |
| `{{3.chosen_start_time}}` | Begintijd | `"10:00"` |
| `{{3.status}}` | `"chosen"` of `"no_match"` | `"chosen"` |

> ⚠️ Webhook is **module 3** — gebruik altijd `{{3.variabelenaam}}`, nooit `{{1.variabelenaam}}`.

---

## Module Volgorde

```
[3]  Webhooks → Custom Webhook (GAS Picker)
        ↓
[23] Router → splitst op 3.status
        │
        ├── Route 1: status = "chosen"  (Pad A)
        │   [4]  Salesforce Search Records SOQL
        │   [6]  Salesforce Update Record (datum + status)
        │   [8]  Salesforce Get a Record (Student Account)
        │   [9]  Salesforce Get a Record (Teacher Account)
        │   [7]  HTTP POST 360dialog → trial_lesson_confirmation_parent
        │   [12] HTTP POST 360dialog → trial_lesson_confirmed_teacher
        │
        └── Route 2: status = "no_match"  (Pad B)
            [25] Salesforce Search Records SOQL
            [26] Salesforce Get a Record (Student Account)
            [27] Salesforce Get a Record (Teacher Account)
            [28] Salesforce Update Record (Availability Conflict)
            [29] HTTP POST 360dialog → availability_conflict_teacher
```

---

## PAD A — Tijdslot Gekozen

### Module 4 — Salesforce Search Records SOQL

```sql
SELECT Id, Teacher__c, Student__c, Available_Timeslots__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{3.matching_number}}'
```

### Module 6 — Salesforce Update a Record

- **Record ID:** `{{4.Id}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Date__c` | `{{3.chosen_date_iso}}T{{3.chosen_start_time}}:00.000` |
| `Trial_Lesson_Status__c` | `Trial Lesson Scheduled` |

> ⚠️ **Geen Z suffix** — zonder Z gebruikt Salesforce Europe/Amsterdam tijdzone. Met Z toont de tijd 1 uur later.
> ⚠️ **`chosen_start_time`** gebruiken (niet `chosen_time`) — `chosen_time` = "10:00-11:00", `chosen_start_time` = "10:00" (begintijd).

### Module 8 — Salesforce Get a Record (Student)
- **Record ID:** `{{4.Student__c}}`
- **Output:** `{{8.ParentsName__c}}`, `{{8.ParentSPhone__c}}`, `{{8.FirstName}}`

### Module 9 — Salesforce Get a Record (Teacher)
- **Record ID:** `{{4.Teacher__c}}`
- **Output:** `{{9.FirstName}}`, `{{9.AccountPhone}}`

### Module 7 — HTTP POST → 360dialog (WhatsApp naar ouder)

```json
{
  "messaging_product": "whatsapp",
  "to": "{{8.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_confirmation_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{8.ParentsName__c}}"},
        {"type": "text", "text": "{{8.FirstName}}"},
        {"type": "text", "text": "{{3.chosen_date}}"},
        {"type": "text", "text": "{{3.chosen_time}}"},
        {"type": "text", "text": "{{9.FirstName}}"},
        {"type": "text", "text": "{{9.AccountPhone}}"}
      ]
    }]
  }
}
```

### Module 12 — HTTP POST → 360dialog (WhatsApp naar docent)

```json
{
  "messaging_product": "whatsapp",
  "to": "{{9.AccountPhone}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_confirmed_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{9.FirstName}}"},
        {"type": "text", "text": "{{8.FirstName}}"},
        {"type": "text", "text": "{{3.chosen_date}}"},
        {"type": "text", "text": "{{3.chosen_time}}"},
        {"type": "text", "text": "{{8.ParentsName__c}}"},
        {"type": "text", "text": "{{8.ParentSPhone__c}}"}
      ]
    }]
  }
}
```

---

## PAD B — Geen Tijdslot Past

### Module 25 — Salesforce Search Records SOQL

```sql
SELECT Id, Teacher__c, Student__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{3.matching_number}}'
```

### Module 26 — Salesforce Get a Record (Student)
- **Record ID:** `{{25.Student__c}}`
- **Output:** `{{26.FirstName}}`, `{{26.ParentsName__c}}`, `{{26.ParentSPhone__c}}`

### Module 27 — Salesforce Get a Record (Teacher)
- **Record ID:** `{{25.Teacher__c}}`
- **Output:** `{{27.FirstName}}`, `{{27.Phone}}`

### Module 28 — Salesforce Update a Record
- **Record ID:** `{{25.Id}}`
- `Trial_Lesson_Status__c` = `Availability Conflict`

### Module 30 — HTTP POST → TinyURL (Tally Form 3 link verkorten)

**JSON body:**
```json
{
  "url": "https://tally.so/r/q4PDV9?matching_number={{encodeURL(25.Name)}}",
  "domain": "go.brightpanda.nl"
}
```

- **API Endpoint:** `https://api.tinyurl.com/create`
- **Header:** `Authorization: Bearer azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji`
- **Output:** `{{30.data.data.tiny_url}}`

### Module 29 — HTTP POST → 360dialog (WhatsApp naar docent)

```json
{
  "messaging_product": "whatsapp",
  "to": "{{27.Phone}}",
  "type": "template",
  "template": {
    "name": "availability_conflict_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{27.FirstName}}"},
        {"type": "text", "text": "{{26.FirstName}}"},
        {"type": "text", "text": "{{26.ParentsName__c}}"},
        {"type": "text", "text": "{{26.ParentSPhone__c}}"},
        {"type": "text", "text": "{{30.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

---

## Wat er daarna gebeurt

**Pad A:** → Scenario 8 stuurt reminders 48u/24u/2u vóór de proefles

**Pad B:** → Docent belt ouder → vult tijdslot in via Tally Form 3 → Scenario 4 verwerkt dit

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `Trial_Lesson_Date__c` toonde 1 uur te laat | Z suffix → Salesforce UTC → 1u verschil NL | Zonder Z: `{{3.chosen_date_iso}}T{{3.chosen_start_time}}:00.000` |
| `chosen_start_time` pakte eindtijd | `chosen_time` = "10:00-11:00" | Picker stuurt `chosen_start_time` apart via `split("-")[0]` |
| Invalid API token module 12 | Typefout in API key (l vs I) | API key kopiëren van werkende module |
| SOQL 0 resultaten | Variabele als plain text ingevoerd | Chip selecteren uit variabele picker (blauwe chip) |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Stuurt picker URL naar ouder |
| [Scenario 04](scenario-04-teacher-timeslot-submission.md) | Verwerkt Tally Form 3 na Pad B |
| [Scenario 05](scenario-05-availability-conflict-reminder.md) | Reminder docent elke 4u bij Availability Conflict |
| [Scenario 08](scenario-08-lesson-date-reminder.md) | Reminders voor de proefles |
| [Google Apps Script](google-apps-script.md) | Script 3 — Picker v11 |
