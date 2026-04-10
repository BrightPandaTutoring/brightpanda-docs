# Scenario 01 — Docent Uitnodiging via WhatsApp

**Make naam:** Integration Salesforce, HTTP
**Aangemaakt:** 10 april 2026
**Status:** 🟡 In ontwikkeling

---

## Doel

Detecteert wanneer een Student Teacher Matching record in Salesforce de status **"Teacher Invited"** krijgt, haalt de docentgegevens op, en stuurt automatisch een **WhatsApp bericht via 360dialog** met een gepersonaliseerde Tally-link zodat de docent zijn/haar beschikbaarheid kan invullen.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Watch Records (Salesforce polling) |
| Object | `Student_Teacher_Matching__c` |
| Sortering | Updated Time |
| Interval | Elke 15 minuten |
| Limit | 10 records |

---

## Modules / Stappen

```
[1] Salesforce → Watch Records
        ↓
    FILTER: Trial_Lesson_Status__c = "Teacher Invited"
        ↓
[3] Salesforce → Get a Record (Teacher)
        ↓
[5] (NOG TE BOUWEN) Salesforce → Get a Record (Student)
        ↓
[7] HTTP → Make a request → 360dialog WhatsApp API
        ↓
[9] (NOG TE BOUWEN) Salesforce → Update a Record
```

> ⚠️ Module nummering is 1, 3, 5... (niet oplopend 1,2,3) omdat tussenliggende modules verwijderd zijn tijdens de bouw.

### Module 1 — Salesforce Watch Records
- **Object:** `Student_Teacher_Matching__c`
- **Output velden:** `Name`, `Teacher__c`, `Student__c`, `Trial_Lesson_Status__c`, `Subject_s__c`

### Filter (tussen module 1 en 3)
- **Conditie:** `Trial_Lesson_Status__c` Equal to `Teacher Invited`

### Module 3 — Salesforce Get a Record (Docent)
- **Type:** Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output velden:** `FirstName`, `PersonMobilePhone`, `Subjects__c`

### Module 5 — Salesforce Get a Record (Student) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{1.Student__c}}`
- **Output velden:** `FirstName`, `ParentSPhone__c`

### Module 7 — HTTP Make a request (360dialog WhatsApp)
- **URL:** `https://waba-v2.360dialog.io/messages`
- **Method:** POST
- **Headers:**
  ```
  D360-API-KEY: xl6Aj3Gs66I40LQl7C6GbjlxAK
  Content-Type: application/json
  ```
- **Body:**
  ```json
  {
    "messaging_product": "whatsapp",
    "to": "{{3.PersonMobilePhone}}",
    "type": "template",
    "template": {
      "name": "teacher_invitation",
      "language": {"code": "nl"},
      "components": [{
        "type": "body",
        "parameters": [
          {"type": "text", "text": "{{3.FirstName}}"},
          {"type": "text", "text": "{{3.Related_Student_r.FirstName}}"},
          {"type": "text", "text": "{{1.Subject_s__c}}"},
          {"type": "text", "text": "https://tally.so/r/2Ekaq9?matching_number={{1.Name}}&student_name={{3.Related_Student_r.FirstName}}"}
        ]
      }]
    }
  }
  ```

### Module 9 — Salesforce Update a Record *(NOG TE BOUWEN)*
- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{1.Id}}`
- **Velden:**
  - `Tally_Link_Teacher__c` → samengestelde Tally URL
  - `Trial_Lesson_Status__c` → `"Availability Received"`

---

## Datastructuur

| Variabele | Bron | Waarde / Beschrijving |
|-----------|------|-----------------------|
| `{{1.Name}}` | Module 1 | Matching Number (bijv. BP-001) |
| `{{1.Teacher__c}}` | Module 1 | Salesforce ID van docent |
| `{{1.Student__c}}` | Module 1 | Salesforce ID van student |
| `{{1.Subject_s__c}}` | Module 1 | Vak(ken) |
| `{{3.FirstName}}` | Module 3 | Voornaam docent |
| `{{3.PersonMobilePhone}}` | Module 3 | WhatsApp nummer docent |
| Tally URL | Samengesteld | `https://tally.so/r/2Ekaq9?matching_number={{1.Name}}&student_name={{3.Related_Student_r.FirstName}}` |

---

## Gekoppelde Apps & Services

| Service | Gebruik |
|---------|---------|
| **Salesforce** | Bron van matching records + docent/student data |
| **360dialog** | WhatsApp Business API voor berichtenverzending |
| **Tally.so** | Formulier voor docent om beschikbaarheid in te vullen (extern, geen Make module) |

---

## Foutmeldingen & Oplossingen

| Fout | Oplossing |
|------|-----------|
| `[403] Forbidden resource` op 360Messenger for WhatsApp module | Vervangen door **HTTP Make a request** module met directe 360dialog API call |
| Tally heeft geen Watch Responses trigger in Make | Scenario 2 wordt een apart scenario met **Custom Webhook** als trigger |

---

## Speciale Opmerkingen

- ⚠️ WhatsApp template `teacher_invitation` moet **goedgekeurd zijn door Meta** voordat het scenario live kan
- ⚠️ 360dialog staat "under review" — max **5 berichten per 24u** tot goedkeuring
- 🧪 Testnummer: `+1 555-759-0811` (Amerikaans testnummer via 360dialog)

---

## Gerelateerde Scenario's

| Scenario | Status | Beschrijving |
|----------|--------|-------------|
| [Scenario 02 — Tally Webhook → Ouder Planning](scenario-02-tally-webhook-ouder-planning.md) | 🔴 Nog te bouwen | Ontvangt Tally form submission van docent → stuurt keuze naar ouder |
| [Scenario 03 — Reminders & Follow-up](scenario-03-reminders-followup.md) | 🔴 Nog te bouwen | Dagelijkse reminder naar ouder + docent voor proefles morgen |

---

## Scenario 02 — Tally Webhook → Ouder Planning *(Gepland)*

**Trigger:** Custom Webhook (ontvangt Tally form submission van docent)

**Geplande modules:**
1. Webhooks → Custom webhook → ontvangt beschikbaarheid docent
2. Salesforce → Get a Record → haal matching record op via `matching_number`
3. Salesforce → Get a Record → haal student/ouder gegevens op
4. HTTP → 360dialog → stuur WhatsApp naar ouder met tijdslot keuze link
5. Salesforce → Update Record → status → `"Availability Received"`

---

## Scenario 03 — Reminders & Follow-up *(Gepland)*

**Trigger:** Schedule (dagelijks 08:00)

**Geplande modules:**
1. Salesforce → Search Records → proeflessen van morgen
2. HTTP → 360dialog → reminder naar ouder
3. HTTP → 360dialog → reminder naar docent
4. Salesforce → Update Record → `Reminder_Sent__c = true`
