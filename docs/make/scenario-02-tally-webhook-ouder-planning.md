# Scenario 02 — Tally Webhook → Ouder Planning

**Make Scenario ID:** 4740354 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Ontvangt de beschikbaarheid van een docent via **Tally Form 1** webhook, verwerkt de tijdsloten via Google Apps Script, zoekt het matching record op in Salesforce, haalt docent- en studentgegevens op, maakt een TinyURL van de picker link, en stuurt een **WhatsApp naar de ouder** met de verkorte picker URL.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Docent Beschikbaarheid |
| Webhook URL | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` |
| Ingesteld in | Tally Form 1 → Settings → Integrations → Webhooks |

> ⚠️ Altijd eerst **Run once** → wachten op "Waiting for data" → dan Tally invullen. Webhook logs: linkermenu → **Webhooks** → **Logs** (niet via History tab).

---

## Module Volgorde

```
[1]  Webhooks → Custom Webhook (Tally Form 1)
        ↓
[31] HTTP POST → Google Apps Script (bouw tijdsloten strings)
        ↓
[3]  Salesforce → Search Records SOQL (matching ophalen)
        ↓
[32] Salesforce → Get a Record (Teacher Account)
        ↓
[4]  Salesforce → Get a Record (Student Account)
        ↓
[35] HTTP POST → TinyURL (picker link verkorten)
        ↓
[5]  HTTP POST → 360dialog (WhatsApp naar ouder)
        ↓
[6]  Salesforce → Update a Record
```

---

## Modules Detail

### Module 1 — Custom Webhook
- **Output:** Tally form data met `data.fields[]`
- `fields[1].value` = matching_number (bijv. `"0016"`)
- `fields[2].value` = student_name

### Module 31 — HTTP POST → Google Apps Script (Tijdslotverwerking)

- **URL:** `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`
- **Method:** POST
- **Parse response:** YES
- **Output:** `{{31.data.timeslots}}` (genummerd voor WhatsApp), `{{31.data.timeslotsRaw}}` (voor picker URL + Salesforce)

Zie [Google Apps Script](google-apps-script.md) voor de volledige JSON body en logica.

### Module 3 — Salesforce Search Records SOQL

```sql
SELECT Id, Student__c, Teacher__c, Available_Timeslots__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{1.data.fields[1].value}}'
```

> `fields[1].value` = matching_number (bijv. `"0016"`). Salesforce zoekt op de volledige naam "Matching Number 0016".

### Module 32 — Salesforce Get a Record (Teacher)
- **Type:** Account
- **Record ID:** `{{3.Teacher__c}}`
- **Output:** `{{32.FirstName}}`

### Module 4 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{3.Student__c}}`
- **Output:** `{{4.FirstName}}`, `{{4.ParentsName__c}}`, `{{4.ParentSPhone__c}}`

### Module 35 — HTTP POST → TinyURL

**JSON body:**
```json
{
  "url": "https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec?slots={{encodeURL(31.data.timeslotsRaw)}}&matching={{encodeURL(3.Name)}}&student_name={{encodeURL(4.FirstName)}}&parent_name={{encodeURL(4.ParentsName__c)}}"
}
```

- **API Endpoint:** `https://api.tinyurl.com/create`
- **Header:** `Authorization: Bearer azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji`
- **Output:** `{{35.data.data.tiny_url}}` ← let op: dubbel `.data.data`

> ⚠️ `go.brightpanda.nl` branded domain is nog niet actief (DNS propagatie). Zodra actief: voeg `"domain": "go.brightpanda.nl"` toe aan de JSON body.

### Module 5 — HTTP POST → 360dialog (WhatsApp naar ouder)

**Template:** `parent_timeslot_invitation` (4 parameters)

**JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{4.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "parent_timeslot_invitation",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{4.ParentsName__c}}"},
        {"type": "text", "text": "{{4.FirstName}}"},
        {"type": "text", "text": "{{32.FirstName}}"},
        {"type": "text", "text": "{{35.data.data.tiny_url}}"}
      ]
    }]
  }
}
```

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{4.ParentsName__c}}` | Naam ouder |
| `{{2}}` | `{{4.FirstName}}` | Voornaam student |
| `{{3}}` | `{{32.FirstName}}` | Voornaam docent |
| `{{4}}` | `{{35.data.data.tiny_url}}` | Verkorte picker URL |

### Module 6 — Salesforce Update a Record

- **Record ID:** `{{3.Id}}`

| Veld | Waarde |
|------|--------|
| `Available_Timeslots__c` | `{{31.data.timeslotsRaw}}` |
| `Trial_Lesson_Status__c` | `Parent Invited` |
| `Parent_Invited_At__c` | `{{now}}` |

---

## Tally Form 1 — Datastructuur

| Index | Veld | Type |
|-------|------|------|
| `fields[1]` | matching_number | HIDDEN — bijv. `"0016"` |
| `fields[2]` | student_name | HIDDEN |
| `fields[3]` | Datum 1 | INPUT_DATE (date object) |
| `fields[5-17]` | Checkboxes datum 1 | CHECKBOX (13 tijdsloten) |
| `fields[18]` | Datum 2 | INPUT_DATE |
| `fields[20-32]` | Checkboxes datum 2 | CHECKBOX |
| `fields[33]` | Datum 3 | INPUT_DATE |
| `fields[35-47]` | Checkboxes datum 3 | CHECKBOX |
| `fields[48]` | Datum 4 | INPUT_DATE |
| `fields[50-62]` | Checkboxes datum 4 | CHECKBOX |
| `fields[63]` | Datum 5 | INPUT_DATE |
| `fields[65-77]` | Checkboxes datum 5 | CHECKBOX |

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| TinyURL output leeg | Verkeerd output pad gebruikt | Correct pad: `{{35.data.data.tiny_url}}` (dubbel `.data`) |
| `go.brightpanda.nl` niet actief | DNS propagatie niet compleet | Wachten op propagatie → Check Now in TinyURL dashboard |
| Tally date objects niet concateneerbaar | Make.com date object incompatibel | Aanhalingstekens om datumchips in GAS JSON body |
| Ouder telefoon/naam leeg | Veldnaam inconsistentie | Check welke variant in module output staat: `ParentsName__c` of `ParentSName__c` |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Stuurt Tally Form 1 link naar docent |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Verwerkt picker response van ouder |
| [Reminders & Escalatie](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende ouder |
| [Google Apps Script](google-apps-script.md) | Tijdsloten verwerking (module 31) |
