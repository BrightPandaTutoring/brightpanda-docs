# Scenario 3b — Ouder Tijdslot Verwerking

**Make naam:** Scenario 3b
**Make Scenario ID:** 4783259 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** 🟡 In aanbouw — module 6 ✅, module 7 onbekend, modules 8-11 nog te bouwen

> **Huidige blokkade:** Templates `trial_lesson_confirmation_parent` en `trial_lesson_confirmation_teacher` wachten op Meta goedkeuring. Daarna modules 8-11 bouwen.
> ⚠️ **Module 7** zichtbaar in Make.com screenshot maar inhoud onbekend — eerst openklikken en controleren voor je verdergaat.

---

## Doel

Verwerkt de tijdslot keuze die een ouder maakt via **Tally Form 2**. Vertaalt het gekozen getal naar een concreet tijdslot via Google Apps Script, slaat de definitieve datum op in Salesforce, en stuurt een bevestiging naar zowel ouder als docent met elkaars contactgegevens.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Ouder Tijdslot |
| Formulier | Tally Form 2 (`https://tally.so/r/WOozov`) |
| Webhook | Nog te koppelen in Tally Form 2 → Settings → Integrations → Webhooks |

---

## Module Volgorde

```
[3]  Webhooks → Custom Webhook (Tally Form 2)
        ↓
[4]  Salesforce → Search Records (SOQL op matching_number)
        ↓
[5]  HTTP → Google Apps Script (vertaal keuzenummer → datetime)
        ↓
[6]  Salesforce → Update a Record ✅ Werkend
        ↓
[7]  HTTP → ? (inhoud onbekend — controleren!)
        ↓
[8]  Salesforce → Get a Record (Student Account)    ← NOG TE BOUWEN
        ↓
[9]  HTTP → 360dialog (WhatsApp naar ouder)          ← NOG TE BOUWEN
        ↓
[10] Salesforce → Get a Record (Teacher Account)     ← NOG TE BOUWEN
        ↓
[11] HTTP → 360dialog (WhatsApp naar docent)         ← NOG TE BOUWEN
```

---

## Modules Detail

### Module 3 — Custom Webhook
- **Naam:** Tally Ouder Tijdslot
- **Output:** Tally Form 2 data

> ⚠️ De webhook is module **3** in dit scenario, dus alle referenties zijn `{{3.data.fields[...]}}` (niet `{{1.data...}}`).

### Module 4 — Salesforce Search Records (SOQL)

```sql
SELECT Id, Teacher__c, Student__c, Available_Timeslots__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = 'Matching Number {{3.data.fields[1].value}}'
```

### Module 5 — HTTP → Google Apps Script

**Doel:** Keuzenummer van ouder vertalen naar een concreet tijdslot en ISO datetime.

- **URL:** `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`
- **Method:** POST

**JSON body:**
```json
{
  "timeslots": "{{4.Available_Timeslots__c}}",
  "chosen": {{3.data.fields[4].value}}
}
```

**Output:**

| Variabele | Inhoud | Voorbeeld |
|-----------|--------|-----------|
| `{{5.data.timeslot}}` | Leesbaar tijdslot | `"2026-03-10 - 14:00-15:00"` |
| `{{5.data.datetime}}` | ISO datetime | `"2026-03-10T14:00:00.000Z"` |

Zie [Google Apps Script documentatie](google-apps-script.md) voor de Functie B logica.

### Module 6 — Salesforce Update a Record ✅ Werkend

- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{4.Id}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Date__c` | `{{5.data.datetime}}` |
| `Trial_Lesson_Status__c` | `Lesson Scheduled` |

### Module 7 — Onbekend
> ⚠️ Zichtbaar in Make.com screenshot maar inhoud nog niet bekeken. **Eerst controleren voor verdergaan.**

### Module 8 — Salesforce Get a Record (Student) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{4.Student__c}}`
- **Benodigde output:** `{{8.ParentSPhone__c}}`, `{{8.FirstName}}`

### Module 9 — HTTP → 360dialog (WhatsApp naar ouder) *(NOG TE BOUWEN)*

**Template:** `trial_lesson_confirmation_parent` (6 parameters)

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{8.FirstName}}` | Voornaam ouder |
| `{{2}}` | Naam leerling | Via matching of student account |
| `{{3}}` | Datum | Datum deel uit `{{5.data.timeslot}}` |
| `{{4}}` | Tijd | Tijd deel uit `{{5.data.timeslot}}` |
| `{{5}}` | Naam docent | Via Teacher Account (module 10) |
| `{{6}}` | Telefoonnummer docent | Via Teacher Account (module 10) |

> ⚠️ Template nog Pending bij Meta — bouwen nadat goedkeuring ontvangen is.

### Module 10 — Salesforce Get a Record (Teacher) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{4.Teacher__c}}`
- **Benodigde output:** `{{10.Phone}}`, `{{10.FirstName}}`

### Module 11 — HTTP → 360dialog (WhatsApp naar docent) *(NOG TE BOUWEN)*

**Template:** `trial_lesson_confirmation_teacher` (6 parameters)

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{10.FirstName}}` | Voornaam docent |
| `{{2}}` | Naam leerling | Via matching of student account |
| `{{3}}` | Datum | Datum deel uit `{{5.data.timeslot}}` |
| `{{4}}` | Tijd | Tijd deel uit `{{5.data.timeslot}}` |
| `{{5}}` | Naam ouder | `{{8.FirstName}}` |
| `{{6}}` | Telefoonnummer ouder | `{{8.ParentSPhone__c}}` |

> ⚠️ Template nog Pending bij Meta — bouwen nadat goedkeuring ontvangen is.

---

## Tally Form 2 — Datastructuur

**URL:** `https://tally.so/r/WOozov`
**Link formaat:** `https://tally.so/r/WOozov?matching_number=0016&student_name=Emma+de+Vries`

| Index | Type | Inhoud |
|-------|------|--------|
| `fields[1]` | HIDDEN | matching_number (bijv. `"0016"`) |
| `fields[2]` | HIDDEN | student_name |
| `fields[3]` | HIDDEN | timeslots_all (backup) |
| `fields[4]` | INPUT_NUMBER | Keuzenummer van de ouder |
| `fields[5]` | CHECKBOXES | "Past geen van de tijdsloten?" |

---

## Salesforce Veld Updates

| Veld | Waarde | Module |
|------|--------|--------|
| `Trial_Lesson_Date__c` | `{{5.data.datetime}}` | Module 6 ✅ |
| `Trial_Lesson_Status__c` | `Lesson Scheduled` | Module 6 ✅ |

---

## Speciale Opmerkingen

- 📱 Docent en ouder krijgen **elkaars contactgegevens pas in de bevestiging** (privacy)
- ⚠️ Als checkbox "Past geen tijdslot" aangevinkt → escalatie naar `+31613689666` (nog te bouwen)
- 📋 Verzetten en annuleren gaat **handmatig** — contactgegevens staan in de WhatsApp disclaimer

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Vult `Available_Timeslots__c` en stuurt Form 2 link naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende ouder |
| [Google Apps Script](google-apps-script.md) | Functie B — tijdslot vertaling |
