# Scenario 3b — Ouder Tijdslot Verwerking

**Make naam:** Scenario 3b
**Make Scenario ID:** 4783259 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** 🟡 In aanbouw — modules 3-6 ✅ werkend, modules 7-10 nog te bouwen

> **Huidige blokkade:** Template `trial_lesson_confirmation` parameters onbekend — Raouf moet de volledige template tekst ophalen uit het 360dialog dashboard. Modules 8 en 10 kunnen pas gebouwd worden daarna.

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
[3]  Webhooks → Custom Webhook (Tally Form 2)      ✅ Werkend
        ↓
[4]  Salesforce → Search Records (SOQL)            ✅ Werkend
        ↓
[5]  HTTP → Google Apps Script (keuze → datetime)  ✅ Getest en werkend
        ↓
[6]  Salesforce → Update a Record                  ✅ Werkend
        ↓
[7]  Salesforce → Get a Record (Student Account)   ← NOG TE BOUWEN
        ↓
[8]  HTTP → 360dialog (WhatsApp naar ouder)         ← NOG TE BOUWEN (wacht op template tekst)
        ↓
[9]  Salesforce → Get a Record (Teacher Account)   ← NOG TE BOUWEN
        ↓
[10] HTTP → 360dialog (WhatsApp naar docent)        ← NOG TE BOUWEN (wacht op template tekst)
```

> ⚠️ **Kritiek:** De webhook is module **3** in dit scenario (niet 1 zoals in Scenario 02). Gebruik **altijd** `{{3.data.fields[...]}}` — nooit `{{1.data.fields[...]}}`. Fout modulenummer geeft "references non-existing module" waarschuwing.

---

## Modules Detail

### Module 3 — Custom Webhook ✅
- **Naam:** Tally Ouder Tijdslot
- **Output:** Tally Form 2 data

### Module 4 — Salesforce Search Records (SOQL) ✅

```sql
SELECT Id, Teacher__c, Student__c, Available_Timeslots__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = 'Matching Number {{3.data.fields[1].value}}'
```

**Gebruikte output:** `{{4.Id}}`, `{{4.Teacher__c}}`, `{{4.Student__c}}`, `{{4.Available_Timeslots__c}}`

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

### Module 7 — Salesforce Get a Record (Student) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{4.Student__c}}`
- **Benodigde output:** `{{7.ParentSPhone__c}}`, `{{7.FirstName}}`

### Module 8 — HTTP → 360dialog (WhatsApp naar ouder) *(NOG TE BOUWEN)*

> ⚠️ **Actie vereist:** Raouf opent 360dialog dashboard → Message Templates → `trial_lesson_confirmation` → deelt de volledige template tekst. Parameters kunnen pas bepaald worden na ontvangst.

- **Template:** `trial_lesson_confirmation`
- **Naar:** `{{7.ParentSPhone__c}}`
- **Parameters:** ONBEKEND — afhankelijk van template tekst

### Module 9 — Salesforce Get a Record (Teacher) *(NOG TE BOUWEN)*
- **Type:** Account
- **Record ID:** `{{4.Teacher__c}}`
- **Benodigde output:** `{{9.Phone}}`, `{{9.FirstName}}`

### Module 10 — HTTP → 360dialog (WhatsApp naar docent) *(NOG TE BOUWEN)*

> ⚠️ Zelfde template tekst nodig als module 8 — wacht op template informatie.

- **Template:** `trial_lesson_confirmation`
- **Naar:** `{{9.Phone}}`
- **Parameters:** ONBEKEND — afhankelijk van template tekst

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

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Vult `Available_Timeslots__c` en stuurt Form 2 link naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende ouder |
| [Google Apps Script](google-apps-script.md) | Functie B — tijdslot vertaling |
