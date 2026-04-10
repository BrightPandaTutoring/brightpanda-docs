# Scenario 03 — Reminders & Escalatie (Ouder)

**Make naam:** Bright Panda - Reminders & Escalatie
**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Verstuurt automatische **reminders en escalaties aan ouders** die na een `Parent Invited` status nog geen tijdslot hebben gekozen voor de proefles.

| Route | Trigger | Actie |
|-------|---------|-------|
| Route 1 | 24u na `Parent_Invited_At__c` | `parent_timeslot_reminder` → ouder |
| Route 2 | 48u na `Parent_Invited_At__c` | `parent_timeslot_escalation` → ouder + `internal_alert_parent_no_timeslot` → intern |
| Route 3 | 72u na `Parent_Invited_At__c` | `parent_timeslot_final` → ouder + status → No Show + Stopped |

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 15 minuten |

---

## Module Volgorde

```
[Schedule Trigger]
        ↓
    ┌── Route 1 (24u — Reminder)
    │   [16] Salesforce → Search Records SOQL
    │   [7]  Salesforce → Get a Record (Teacher Account)
    │   [12] Salesforce → Get a Record (Student Account)
    │   [TinyURL module] → verkorte picker link
    │   [HTTP POST] → 360dialog (parent_timeslot_reminder)
    │   [Update] → Parent_Reminder_Sent__c = true
    │
    ├── Route 2 (48u — Escalatie)
    │   [17] Salesforce → Search Records SOQL
    │   [Teacher Account]
    │   [Student Account]
    │   [TinyURL module] → verkorte picker link
    │   [HTTP POST] → 360dialog (parent_timeslot_escalation → ouder)
    │   [HTTP POST] → 360dialog (internal_alert_parent_no_timeslot → 31613689666)
    │   [Update] → Parent_Escalation_Sent__c = true
    │
    └── Route 3 (72u — Finale)
        [20] Salesforce → Search Records SOQL
        [Teacher Account]
        [Student Account]
        [HTTP POST] → 360dialog (parent_timeslot_final → ouder)
        [Update] → Trial_Lesson_Status__c = No Show, Status__c = Stopped
```

> ⚠️ **Module nummering:** In dit scenario is module **7 = Teacher** en module **12 = Student** — omgekeerd van de meeste andere scenario's. Gebruik altijd de juiste chipnummers bij het aanpassen.

---

## Route 1 — SOQL (Module 16)

```sql
SELECT Id, Teacher__c, Student__c, Name, Available_Timeslots__c,
       Parent_Invited_At__c, Parent_Reminder_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Parent Invited'
AND Parent_Invited_At__c < {{formatDate(addHours(now; -24); "YYYY-MM-DDTHH:mm:ss")}}Z
AND Parent_Reminder_Sent__c = false
```

### Module 7 — Get Teacher Account
- **Record ID:** `{{16.Teacher__c}}`
- **Output:** `{{7.FirstName}}`

### Module 12 — Get Student Account
- **Record ID:** `{{16.Student__c}}`
- **Output:** `{{12.FirstName}}`, `{{12.ParentsName__c}}`, `{{12.ParentSPhone__c}}`

### TinyURL Module
> ⚠️ **TO DO:** TinyURL module toevoegen vóór de WhatsApp module.
> Picker URL: `https://script.google.com/macros/s/AKfycbyrP2j.../exec?slots={{encodeURL(16.Available_Timeslots__c)}}&matching={{encodeURL(16.Name)}}&student_name={{encodeURL(12.FirstName)}}&parent_name={{encodeURL(12.ParentsName__c)}}`
> Output: `{{TINYURL_MODULE.data.data.tiny_url}}`

### HTTP POST — parent_timeslot_reminder

```json
{
  "messaging_product": "whatsapp",
  "to": "{{12.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "parent_timeslot_reminder",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{12.ParentsName__c}}"},
        {"type": "text", "text": "{{12.FirstName}}"},
        {"type": "text", "text": "{{7.FirstName}}"},
        {"type": "text", "text": "{{TINYURL_MODULE.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{12.ParentsName__c}}` | Naam ouder |
| `{{2}}` | `{{12.FirstName}}` | Voornaam leerling |
| `{{3}}` | `{{7.FirstName}}` | Voornaam docent |
| `{{4}}` | `{{TINYURL_MODULE.data.data.tiny_url}}` | Verkorte picker link |

**Update:** `Parent_Reminder_Sent__c = true`, Record ID: `{{16.Id}}`

---

## Route 2 — SOQL (Module 17)

```sql
SELECT Id, Teacher__c, Student__c, Name, Available_Timeslots__c,
       Parent_Invited_At__c, Parent_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Parent Invited'
AND Parent_Invited_At__c < {{formatDate(addHours(now; -48); "YYYY-MM-DDTHH:mm:ss")}}Z
AND Parent_Escalation_Sent__c = false
```

### HTTP POST — parent_timeslot_escalation

```json
{
  "messaging_product": "whatsapp",
  "to": "{{12.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "parent_timeslot_escalation",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{12.ParentsName__c}}"},
        {"type": "text", "text": "{{12.FirstName}}"},
        {"type": "text", "text": "{{7.FirstName}}"},
        {"type": "text", "text": "{{TINYURL_MODULE.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

### HTTP POST — internal_alert_parent_no_timeslot (naar 31613689666)

```json
{
  "messaging_product": "whatsapp",
  "to": "31613689666",
  "type": "template",
  "template": {
    "name": "internal_alert_parent_no_timeslot",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{12.FirstName}}"},
        {"type": "text", "text": "{{7.FirstName}}"},
        {"type": "text", "text": "{{7.LastName}}"},
        {"type": "text", "text": "{{12.ParentsName__c}}"},
        {"type": "text", "text": "{{12.ParentSPhone__c}}"},
        {"type": "text", "text": "{{17.Name}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{12.FirstName}}` | Voornaam leerling |
| `{{2}}` | `{{7.FirstName}}` | Voornaam docent |
| `{{3}}` | `{{7.LastName}}` | Achternaam docent |
| `{{4}}` | `{{12.ParentsName__c}}` | Naam ouder |
| `{{5}}` | `{{12.ParentSPhone__c}}` | Telefoon ouder |
| `{{6}}` | `{{17.Name}}` | Matching number |

**Update:** `Parent_Escalation_Sent__c = true`, Record ID: `{{17.Id}}`

---

## Route 3 — SOQL (Module 20)

```sql
SELECT Id, Teacher__c, Student__c, Name
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Parent Invited'
AND Parent_Invited_At__c < {{formatDate(addHours(now; -72); "YYYY-MM-DDTHH:mm:ss")}}Z
```

### HTTP POST — parent_timeslot_final (video header)

> ⚠️ Template heeft een **video header** — `https://media.tenor.com/AHr4JyE49zMAAAPo/x4ndrr-jake-gyllenhaal.mp4`
> Video speelt niet automatisch af in WhatsApp — overweging: vervangen door afbeelding.

```json
{
  "messaging_product": "whatsapp",
  "to": "{{12.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "parent_timeslot_final",
    "language": {"code": "nl"},
    "components": [
      {
        "type": "header",
        "parameters": [{
          "type": "video",
          "video": {"link": "https://media.tenor.com/AHr4JyE49zMAAAPo/x4ndrr-jake-gyllenhaal.mp4"}
        }]
      },
      {
        "type": "body",
        "parameters": [
          {"type": "text", "text": "{{12.ParentsName__c}}"},
          {"type": "text", "text": "{{12.FirstName}}"},
          {"type": "text", "text": "{{7.FirstName}}"}
        ]
      }
    ]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{12.ParentsName__c}}` | Naam ouder |
| `{{2}}` | `{{12.FirstName}}` | Voornaam leerling |
| `{{3}}` | `{{7.FirstName}}` | Voornaam docent |

**Update na Route 3:**

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Status__c` | `No Show` |
| `Status__c` | `Stopped` |

Record ID: `{{20.Id}}`

---

## Salesforce Velden

| Veld | Type | Wanneer `true` |
|------|------|---------------|
| `Parent_Reminder_Sent__c` | Checkbox | Na versturen 24u reminder (Route 1) |
| `Parent_Escalation_Sent__c` | Checkbox | Na versturen 48u escalatie (Route 2) |
| `Parent_Invited_At__c` | DateTime | Ingevuld door Scenario 2 bij versturen picker URL |

---

## Openstaande Verbeteringen

> ⚠️ **TinyURL nog niet geïntegreerd** in Routes 1 en 2. Picker link wordt momenteel niet meegestuurd.
> Zodra `go.brightpanda.nl` actief is: TinyURL module toevoegen vóór elke WhatsApp module die de picker link nodig heeft.

> ⚠️ **parent_timeslot_final video header** — Overweging: video vervangen door afbeelding (video speelt niet automatisch af in WhatsApp).

> ⚠️ **Re-engagement flow** na Route 3 — Na No Show + Stopped kan een re-engagement flow starten: WhatsApp + MailerLite na 30 dagen.

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Zet `Parent_Invited_At__c` en stuurt picker URL naar ouder |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Verwerkt ouder keuze — zet status Trial Lesson Scheduled of Availability Conflict |
