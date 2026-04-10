# Scenario 3b — Ouder Tijdslot Verwerking

**Make naam:** Scenario 3b
**Make Scenario ID:** 4783259 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** 🟡 In aanbouw — modules 3-6 ✅ werkend, modules 7-13 nog te bouwen/testen

---

## Doel

Verwerkt de tijdslot keuze van een ouder via **Tally Form 2**. Vertaalt het gekozen getal naar een concreet tijdslot via Google Apps Script, slaat de definitieve datum op in Salesforce, en stuurt een bevestiging naar zowel ouder als docent met elkaars contactgegevens.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Ouder Tijdslot |
| Formulier | Tally Form 2 (`https://tally.so/r/WOozov`) |
| Webhook | Geconfigureerd in Make.com Scenario 3b |

---

## Module Volgorde

```
[3]  Webhooks → Custom Webhook (Tally Form 2)         ✅ Werkend
        ↓
[4]  Salesforce → Search Records (SOQL)               ✅ Werkend
        ↓
[5]  HTTP → Google Apps Script (keuze → datetime)     ✅ Getest en werkend
        ↓
[6]  Salesforce → Update a Record                     ✅ Werkend
        ↓
[8]  Salesforce → Get a Record (Student Account)      ← NOG TE BOUWEN
        ↓
[13] Salesforce → Search Records SOQL (Ouder Contact) ← NOG TE BOUWEN
        ↓
[7]  HTTP → 360dialog (WhatsApp naar ouder)           ← NOG TE BOUWEN
        ↓
[9]  Salesforce → Get a Record (Teacher Account)      ← NOG TE BOUWEN
        ↓
[12] HTTP → 360dialog (WhatsApp naar docent)          ← NOG TE BOUWEN
```

> ⚠️ **Kritiek:** De webhook is module **3** in dit scenario (niet 1 zoals in Scenario 02). Gebruik **altijd** `{{3.data.fields[...]}}` — nooit `{{1.data.fields[...]}}`. Fout modulenummer geeft "references non-existing module" waarschuwing.

> ⚠️ **Wacht op template goedkeuring:** `trial_lesson_confirmed_teacher` is ingediend bij Meta als Utility, goedkeuring afwachten. `trial_lesson_confirmation_parent` is al goedgekeurd.

---

## Modules Detail

### Module 3 — Custom Webhook ✅
- **Naam:** Tally Ouder Tijdslot
- **Output:** Tally Form 2 data

### Module 4 — Salesforce Search Records (SOQL) ✅

```sql
SELECT Id, Teacher__c, Student__c, Available_Timeslots__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{3.data.fields[1].value}}'
```

**Gebruikte output:** `{{4.Id}}`, `{{4.Teacher__c}}`, `{{4.Student__c}}`, `{{4.Available_Timeslots__c}}`

> **Opmerking:** Tally Form 2 gebruikt `matching_number` als `fields[1]` — dit bevat het matching nummer als getal (bijv. `"0016"`), niet de volledige naam. De SOQL voegt het prefix `Matching Number ` toe.

### Module 5 — HTTP → Google Apps Script ✅ Getest

**Getest met:** matching_number=0016 en handmatig gevulde `Available_Timeslots__c`

- **URL:** `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`
- **Method:** POST
- **Body type:** Raw
- **Content type:** application/json

**JSON body:**
```json
{"timeslots":"{{4.Available_Timeslots__c}}","chosen":{{3.data.fields[4].value}}}
```

**Output:**

| Variabele | Inhoud | Voorbeeld |
|-----------|--------|-----------|
| `{{5.data.timeslot}}` | Leesbaar tijdslot | `"2026-03-10 - 14:00-15:00"` |
| `{{5.data.datetime}}` | ISO datetime | `"2026-03-10T14:00:00.000Z"` |

Zie [Google Apps Script documentatie](google-apps-script.md) voor Functie B logica.

### Module 6 — Salesforce Update a Record ✅ Werkend

- **Record ID:** `{{4.Id}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Date__c` | `{{5.data.datetime}}` |
| `Trial_Lesson_Status__c` | `Lesson Scheduled` |

### Module 8 — Salesforce Get a Record (Student) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{4.Student__c}}`
- **Benodigde output:** `{{8.FirstName}}`, `{{8.Account ID}}`

### Module 13 — Salesforce Search Records SOQL (Ouder Contact) *(NOG TE BOUWEN)*

```sql
SELECT Id, FirstName, Phone FROM Contact WHERE AccountId = '{{8.Account ID}}'
```

- **Limit:** 10
- **Output:** `{{13.FirstName}}`, `{{13.Phone}}`

> Ouders zijn **Contact** records in Salesforce, gekoppeld via `AccountId` aan het student Account.

### Module 7 — HTTP → 360dialog (WhatsApp naar ouder) *(NOG TE BOUWEN)*

- **Template:** `trial_lesson_confirmation_parent`
- **Status template:** ✅ Goedgekeurd
- **Naar:** `{{13.Phone}}`

**JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{13.Phone}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_confirmation_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{13.FirstName}}"},
        {"type": "text", "text": "{{8.Name}}"},
        {"type": "text", "text": "{{3.data.fields[2].value}}"},
        {"type": "text", "text": "{{3.data.fields[3].value}}"},
        {"type": "text", "text": "{{9.FirstName}}"},
        {"type": "text", "text": "{{9.Phone}}"}
      ]
    }]
  }
}
```

**Parameter mapping:**

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{13.FirstName}}` | Voornaam ouder |
| `{{2}}` | `{{8.Name}}` | Volledige naam student (Account.Name) |
| `{{3}}` | `{{3.data.fields[2].value}}` | Leesbaar tijdslot (bijv. "2026-03-10 - 14:00-15:00") |
| `{{4}}` | `{{3.data.fields[3].value}}` | Extra datuminfo (Form 2 veld) |
| `{{5}}` | `{{9.FirstName}}` | Voornaam docent |
| `{{6}}` | `{{9.Phone}}` | Telefoonnummer docent |

### Module 9 — Salesforce Get a Record (Teacher) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{4.Teacher__c}}`
- **Benodigde output:** `{{9.Phone}}`, `{{9.FirstName}}`

### Module 12 — HTTP → 360dialog (WhatsApp naar docent) *(NOG TE BOUWEN)*

- **Template:** `trial_lesson_confirmed_teacher`
- **Status template:** 🟡 Ingediend bij Meta — wacht op goedkeuring
- **Naar:** `{{9.Phone}}`

**JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{9.Phone}}",
  "type": "template",
  "template": {
    "name": "trial_lesson_confirmed_teacher",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{9.FirstName}}"},
        {"type": "text", "text": "{{8.Name}}"},
        {"type": "text", "text": "{{3.data.fields[2].value}}"},
        {"type": "text", "text": "{{3.data.fields[3].value}}"},
        {"type": "text", "text": "{{13.FirstName}}"},
        {"type": "text", "text": "{{13.Phone}}"}
      ]
    }]
  }
}
```

**Parameter mapping:**

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{9.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{8.Name}}` | Volledige naam student |
| `{{3}}` | `{{3.data.fields[2].value}}` | Leesbaar tijdslot |
| `{{4}}` | `{{3.data.fields[3].value}}` | Extra datuminfo |
| `{{5}}` | `{{13.FirstName}}` | Voornaam ouder |
| `{{6}}` | `{{13.Phone}}` | Telefoonnummer ouder |

> **Privacyprincipe (B09):** Docent en ouder krijgen **elkaars contactgegevens pas in de bevestiging** — niet eerder. Dit is bewuste keuze.

---

## Tally Form 2 — Datastructuur

**URL:** `https://tally.so/r/WOozov`
**Link formaat:** `https://tally.so/r/WOozov?matching_number=0016&student_name=Emma+de+Vries`

| Index | Type | Inhoud |
|-------|------|--------|
| `fields[1]` | HIDDEN | matching_number (bijv. `"0016"`) |
| `fields[2]` | HIDDEN | student_name |
| `fields[3]` | HIDDEN | timeslots_all (backup, niet gebruikt in huidige opzet) |
| `fields[4]` | INPUT_NUMBER | Keuzenummer van de ouder |
| `fields[5]` | CHECKBOXES | "Past geen van de tijdsloten?" → Pad B |
| `fields[7]` | INPUT_DATE | Datum 1 (alternatieve beschikbaarheid) |
| `fields[8]` | MULTI_SELECT | Tijdsloten datum 1 (alternatief) |
| `fields[9]` | INPUT_DATE | Datum 2 (alternatief) |
| `fields[10]` | MULTI_SELECT | Tijdsloten datum 2 (alternatief) |
| ... | ... | Datum 3, 4, 5 (alternatief) |

---

## Pad B — Geen Tijdslot Past *(NOG TE ONTWERPEN)*

**Trigger:** `fields[5]` = aangevinkt (ouder vinkt "Past geen van de tijdsloten?" aan)

**Geplande acties:**
- Status update → bijv. `"No Match"` (statuswaarde nog te bepalen)
- WhatsApp naar intern team `+31613689666` voor handmatige opvolging

---

## Speciale Opmerkingen

- 📱 Docent en ouder krijgen **elkaars contactgegevens pas in de bevestiging** (privacy)
- ⚠️ Einde-tot-einde test is **nog nooit uitgevoerd** met een echt matching record
- 🕐 Test gedaan met handmatig gevuld `Available_Timeslots__c` en matching_number=0016
- 📋 Verzetten/annuleren gaat handmatig — contactgegevens in WhatsApp disclaimer
- ⚠️ Bouwen modules 7-13 wacht op goedkeuring `trial_lesson_confirmed_teacher` template

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Vult `Available_Timeslots__c` en stuurt Form 2 link naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende ouder |
| [Google Apps Script](google-apps-script.md) | Functie B — tijdslot vertaling |
