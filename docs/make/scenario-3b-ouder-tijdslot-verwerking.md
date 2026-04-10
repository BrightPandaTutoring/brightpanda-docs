# Scenario 3b — Ouder Tijdslot Verwerking

**Make naam:** Scenario 3b (intern genummerd als Scenario 3)
**Make Scenario ID:** 4783259 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Pad A én Pad B werkend

---

## Doel

Ontvangt de tijdslot keuze van een ouder via de **Google Apps Script picker pagina**. Slaat de definitieve datum op in Salesforce, en stuurt een bevestiging naar zowel ouder als docent met elkaars contactgegevens.

Bij **Pad B** (geen tijdslot past): stuurt WhatsApp naar docent met instructie om de ouder te bellen, update status naar `Availability Conflict`.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Ouder Tijdslot |
| Webhook URL | `https://hook.eu1.make.com/jgrnq4k8yob8txh5x0jn2ojxx94awnwr` |
| Afzender | Google Apps Script picker pagina (POST na klik op tijdslot of "geen tijdslot" knop) |

> ⚠️ **Webhook is module 3** in dit scenario. Gebruik **altijd** `{{3.data.fields[...]}}` of `{{3.variabelenaam}}` — nooit module 1.

---

## Webhook Input — Velden van GAS Picker

| Veld | Inhoud | Voorbeeld |
|------|--------|-----------|
| `{{3.matching_number}}` | Volledige matching naam | `"Matching Number 0016"` |
| `{{3.student_name}}` | Voornaam student | `"Emma"` |
| `{{3.chosen}}` | Keuzenummer (alleen bij Pad A) | `2` |
| `{{3.chosen_date}}` | Leesbare datum | `"15 mrt"` |
| `{{3.chosen_date_iso}}` | ISO datum | `"2026-03-15"` |
| `{{3.chosen_time}}` | Tijdslot string | `"10:00-11:00"` |
| `{{3.chosen_start_time}}` | Begintijd alleen | `"10:00"` |
| `{{3.status}}` | `"chosen"` of `"no_match"` | `"chosen"` |

---

## Module Volgorde

```
[3]  Webhooks → Custom Webhook (GAS Picker)       ✅ Werkend
        ↓
[23] Router → splitst op basis van 3.status
        │
        ├── Route 1: status = "chosen"  (Pad A — tijdslot gekozen)
        │       ↓
        │   [4]  Salesforce → Search Records SOQL (matching)      ✅
        │       ↓
        │   [6]  Salesforce → Update a Record (datum + status)     ✅
        │       ↓
        │   [8]  Salesforce → Get a Record (Student Account)       ✅
        │       ↓
        │   [9]  Salesforce → Get a Record (Teacher Account)       ✅
        │       ↓
        │   [7]  HTTP → 360dialog (WhatsApp naar ouder)            ✅
        │       ↓
        │   [12] HTTP → 360dialog (WhatsApp naar docent)           ✅
        │
        └── Route 2: status = "no_match"  (Pad B — geen tijdslot past)
                ← NOG TE BOUWEN
```

---

## Modules Detail — Pad A

### Module 3 — Custom Webhook ✅
- **Naam:** Tally Ouder Tijdslot
- **Ontvangt:** JSON POST van Google Apps Script picker pagina

### Module 23 — Router
- **Route 1 filter:** `{{3.status}}` equal to `chosen`
- **Route 2 filter:** `{{3.status}}` equal to `no_match`

### Module 4 — Salesforce Search Records (SOQL) ✅

```sql
SELECT Id, Teacher__c, Student__c, Available_Timeslots__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{3.matching_number}}'
```

> `{{3.matching_number}}` bevat de **volledige** matching naam "Matching Number 0016" — direct gebruiken als chip, geen prefix toevoegen.

**Output:** `{{4.Id}}`, `{{4.Teacher__c}}`, `{{4.Student__c}}`

### Module 6 — Salesforce Update a Record ✅

- **Record ID:** `{{4.Id}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Date__c` | `{{3.chosen_date_iso}}T{{3.chosen_start_time}}:00.000` |
| `Trial_Lesson_Status__c` | `Trial Lesson Scheduled` |

> ⚠️ **Geen `Z` suffix** — datum opslaan als `2026-03-15T10:00:00.000` (zonder Z). Met Z gebruikt Salesforce UTC, waardoor de tijd 1 uur later lijkt in Europe/Amsterdam tijdzone.
>
> ⚠️ **`chosen_start_time` gebruiken, niet `chosen_time`** — `chosen_time` bevat het volledige bereik "10:00-11:00". `chosen_start_time` bevat alleen "10:00" (begintijd, gesplitst via `selectedTime.split("-")[0]` in de picker).

### Module 8 — Salesforce Get a Record (Student) ✅
- **Type:** Account
- **Record ID:** `{{4.Student__c}}`
- **Output:** `{{8.ParentsName__c}}`, `{{8.ParentSPhone__c}}`, `{{8.FirstName}}`

### Module 9 — Salesforce Get a Record (Teacher) ✅
- **Type:** Account
- **Record ID:** `{{4.Teacher__c}}`
- **Output:** `{{9.FirstName}}`, `{{9.AccountPhone}}`

> Docenten zijn Account records. Telefoonnummer = `AccountPhone` veld in Make.com module output.

### Module 7 — HTTP POST → 360dialog (WhatsApp naar ouder) ✅

**Template:** `trial_lesson_confirmation_parent` (6 parameters)

**JSON body:**
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

**Parameter mapping:**

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{8.ParentsName__c}}` | Naam ouder |
| `{{2}}` | `{{8.FirstName}}` | Voornaam student |
| `{{3}}` | `{{3.chosen_date}}` | Leesbare datum, bijv. "15 mrt" |
| `{{4}}` | `{{3.chosen_time}}` | Tijdslot, bijv. "10:00-11:00" |
| `{{5}}` | `{{9.FirstName}}` | Voornaam docent |
| `{{6}}` | `{{9.AccountPhone}}` | Telefoonnummer docent |

### Module 12 — HTTP POST → 360dialog (WhatsApp naar docent) ✅

**Template:** `trial_lesson_confirmed_teacher` (6 parameters)

**JSON body:**
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

**Parameter mapping:**

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{9.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{8.FirstName}}` | Voornaam student |
| `{{3}}` | `{{3.chosen_date}}` | Leesbare datum |
| `{{4}}` | `{{3.chosen_time}}` | Tijdslot |
| `{{5}}` | `{{8.ParentsName__c}}` | Naam ouder |
| `{{6}}` | `{{8.ParentSPhone__c}}` | Telefoonnummer ouder |

> **Privacyprincipe:** Docent en ouder krijgen **elkaars contactgegevens pas in de bevestiging** — niet eerder.

---

## Pad B — Geen Tijdslot Past ✅ WERKEND

**Trigger:** Router Route 2 — `{{3.status}}` = `"no_match"`

**Stappen:**

| Module | Actie |
|--------|-------|
| Module 30 | HTTP → TinyURL (korte URL van Tally Form 3) |
| Module 29 | HTTP → 360dialog (WhatsApp `availability_conflict_teacher` naar docent) |
| Salesforce Update | `Trial_Lesson_Status__c = Availability Conflict` |

**Inhoud WhatsApp naar docent:**
- Instructie om de ouder te bellen
- Contactgegevens ouder (naam + telefoon)
- Link naar Tally Form 3 om het afgesproken tijdslot in te vullen (via TinyURL → `go.brightpanda.nl`)

**Wat daarna:**
- Docent belt ouder en spreekt tijdslot af
- Docent vult het tijdslot in via Tally Form 3
- Scenario 4 verwerkt de Tally Form 3 submission → bevestiging naar ouder en docent

**Inhoud WhatsApp naar docent (concept):**
- Naam docent, naam student
- Contactgegevens ouder (naam + telefoon)
- Instructie: "Geen tijdslot paste voor de ouder. Neem contact op om een datum te plannen."

---

## WhatsApp Templates

### `trial_lesson_confirmation_parent`
**Status:** ✅ Approved | **Categorie:** Utility | **Parameters:** 6

```
Hoi {{1}},

De proefles is bevestigd!

Leerling: {{2}}
Datum: {{3}}
Tijd: {{4}}

Contactgegevens docent:
Naam: {{5}}
Telefoon: {{6}}

Tot dan!
```

### `availability_conflict_teacher`
**Status:** ✅ Approved | **Categorie:** Utility
**Gebruik:** Pad B — instructie aan docent om ouder te bellen + link Tally Form 3

### `trial_lesson_confirmed_teacher`
**Status:** ✅ Approved | **Categorie:** Utility | **Parameters:** 6

```
Hoi {{1}},

De proefles is bevestigd.

Leerling: {{2}}
Datum: {{3}}
Tijd: {{4}}

Contactgegevens ouder:
Naam: {{5}}
Telefoon: {{6}}

Tot dan!
```

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| Trial_Lesson_Date__c toonde 1 uur te laat | Z suffix → Salesforce gebruikte UTC → 1 uur verschil NL | Zonder Z opslaan: `{{3.chosen_date_iso}}T{{3.chosen_start_time}}:00.000` |
| `chosen_start_time` pakte eindtijd | `chosen_time` bevat "10:00-11:00", niet "10:00" | Picker stuurt `chosen_start_time` apart via `selectedTime.split("-")[0]` |
| Invalid API token module 12 | Typefout in API key (kleine l vs hoofdletter I) | API key kopiëren van werkende module 7 |
| SOQL 0 resultaten | Variabele als plain text ingevoerd | Chip selecteren vanuit variabele picker (blauwe chip) |
| `Trial Lesson Scheduled` bad value | Exacte picklist waarde verkeerd gespeld | Exacte waarde: `Trial Lesson Scheduled` (met spaties) |

---

## Speciale Opmerkingen

- ⚠️ Einde-tot-einde test is **nog nooit volledig uitgevoerd** met een echt matching record
- 📋 Verzetten/annuleren gaat handmatig — contactgegevens staan in WhatsApp berichten
- 🔄 Picker pagina toont "geen tijdslot" knop → POST naar webhook met `status=no_match`

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Stuurt picker URL naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende ouder |
| [Google Apps Script](google-apps-script.md) | Script 3 — Picker pagina (v10) |
