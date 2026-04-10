# Scenario 01 — Docent Uitnodiging via WhatsApp

**Make naam:** Integration Salesforce, HTTP
**Laatste update:** 10 april 2026
**Status:** 🟡 In ontwikkeling

> **Blokkade:** Meta propagatie vertraging na display name wijziging naar "Bright Panda Bijles" (fout #131037). 360dialog toont READY + groen bolletje. Wacht 24-48u, daarna Run once opnieuw proberen.

---

## Doel

Detecteert automatisch wanneer een nieuwe matching de status **"Teacher Invited"** krijgt in Salesforce, haalt docent- en studentgegevens op, en stuurt een **WhatsApp bericht via 360dialog** met een gepersonaliseerde Tally-link zodat de docent zijn/haar beschikbaarheid kan invullen. Slaat daarna de Tally-link op in het Salesforce matching record.

**Probleem dat het oplost:** Bright Panda moest handmatig docenten benaderen voor proeflesplanning.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Watch Records (Salesforce polling) |
| Object | `Student_Teacher_Matching__c` |
| Watch type | Watch by Updated Time |
| Interval | Elke 15 minuten |
| Limit | 10 records per run |

---

## Module Volgorde

```
[1] Salesforce → Watch Records
        ↓
[2] Filter: Trial_Lesson_Status__c = "Teacher Invited"
        ↓
[3] Salesforce → Get a Record (Teacher Account)
        ↓
[6] Salesforce → Get a Record (Student Account)
        ↓
[8] Tools → Set Variable (matching_number_clean)
        ↓
[5] HTTP → POST 360dialog WhatsApp API
        ↓
[7] Salesforce → Update a Record (Matching)
```

> ⚠️ Module nummering volgt toevoegvolgorde in Make.com, niet de visuele positie. Volgorde: 1 → 2 → 3 → 6 → 8 → 5 → 7

---

## Modules Detail

### Module 1 — Salesforce Watch Records
- **Object:** `Student_Teacher_Matching__c`
- **Output velden:** `Id`, `Student__c`, `Teacher__c`, `Subject_s__c`, `Name`, `Trial_Lesson_Status__c`

### Module 2 — Filter
- **Conditie:** `Trial_Lesson_Status__c` Equal to `Teacher Invited`
- **Bij niet voldoen:** scenario stopt volledig

### Module 3 — Salesforce Get a Record (Docent)
- **Type:** Account
- **Record ID:** `{{1.Teacher__c}}`
- **Gebruikte output:** `{{3.FirstName}}`, `{{3.Phone}}`

### Module 6 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{1.Student__c}}`
- **Gebruikte output:** `{{6.FirstName}}`

### Module 8 — Tools Set Variable ⚠️ Kritiek
- **Variable name:** `matching_number_clean`
- **Variable value:** `{{replace(1.Name; "Matching Number "; "")}}`
- **Resultaat:** bijv. `"0016"` (alleen het getal, zonder prefix en spatie)
- **Gebruik in volgende modules:** `{{8.matching_number_clean}}`

> **Waarom een aparte module?** De `replace()` formule gebruikt dubbele aanhalingstekens die conflicteren met JSON string opmaak in de HTTP module. Backticks werken **niet** in `replace()` — dit geeft "Module references non-existing module NaN" error. Dubbele aanhalingstekens werken alleen in een Set Variable module buiten de JSON.

### Module 5 — HTTP Make a request (360dialog WhatsApp)
- **URL:** `https://waba.360dialog.io/v1/messages`
- **Method:** POST
- Zie [Gedeelde configuratie](gedeelde-configuratie.md) voor headers

**Volledige JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.Phone}}",
  "type": "template",
  "template": {
    "name": "teacher_invitation",
    "language": {"code": "nl"},
    "components": [
      {
        "type": "body",
        "parameters": [
          {"type": "text", "text": "{{3.FirstName}}"},
          {"type": "text", "text": "{{6.FirstName}}"},
          {"type": "text", "text": "{{switch(1.Subject_s__c; `Mathematics A`; `Wiskunde A`; `Mathematics B`; `Wiskunde B`; `Mathematics C`; `Wiskunde C`; `Mathematics D`; `Wiskunde D`; `Physics`; `Natuurkunde`; `Chemistry`; `Scheikunde`; `Biology`; `Biologie`; `Dutch`; `Nederlands`; `English`; `Engels`; `French`; `Frans`; `German`; `Duits`; `Spanish`; `Spaans`; `Latin`; `Latijn`; `Greek`; `Grieks`; `Arabic`; `Arabisch`; `Chinese`; `Chinees`; `Italian`; `Italiaans`; `Russian`; `Russisch`; `Turkish`; `Turks`; `Computer Science`; `Informatica`; `Geography`; `Aardrijkskunde`; `History`; `Geschiedenis`; `Economics`; `Economie`; `Business Economics`; `Bedrijfseconomie`; `Philosophy`; `Filosofie`; `Social Studies`; `Maatschappijleer`; `Music`; `Muziek`; `Art`; `Kunst`; `Cito Test`; `Cito Test`; `Coding`; `Coderen`; `Calculations`; `Rekenen`; 1.Subject_s__c)}}"},
          {"type": "text", "text": "https://tally.so/r/2Ekaq9?matching_number={{8.matching_number_clean}}&student_name={{6.FirstName}}"}
        ]
      }
    ]
  }
}
```

> **Backtick regel:** Backticks werken in `switch()` binnen JSON strings om conflict met JSON aanhalingstekens te vermijden. Ze werken **niet** in `replace()`.

**Template parameters:**
| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{3.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{6.FirstName}}` | Voornaam student |
| `{{3}}` | `switch(...)` | Vak vertaald naar Nederlands |
| `{{4}}` | URL | Tally Form 1 link met matching_number en student_name |

### Module 7 — Salesforce Update a Record
- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{1.Id}}`

| Veld | Waarde |
|------|--------|
| `Tally_Link_Teacher__c` | `https://tally.so/r/2Ekaq9?matching_number={{replace(1.Name; "Matching Number "; "")}}&student_name={{6.FirstName}}` |
| `Trial_Lesson_Status__c` | `Availability Received` |

> `BundleValidationError: Missing value of required parameter 'record'` bij lege tests is **normaal gedrag** — treedt op als er geen records zijn met status "Teacher Invited".

---

## Datastructuur

| Variabele | Module | Beschrijving |
|-----------|--------|-------------|
| `{{1.Id}}` | 1 | ID van het matching record |
| `{{1.Teacher__c}}` | 1 | Salesforce ID van docent |
| `{{1.Student__c}}` | 1 | Salesforce ID van student |
| `{{1.Subject_s__c}}` | 1 | Vak (Engelse picklist waarde) |
| `{{1.Name}}` | 1 | Matching naam: "Matching Number 0016" |
| `{{3.FirstName}}` | 3 | Voornaam docent |
| `{{3.Phone}}` | 3 | WhatsApp nummer docent (internationaal: `31XXXXXXXXX`) |
| `{{6.FirstName}}` | 6 | Voornaam student |
| `{{8.matching_number_clean}}` | 8 | Alleen het getal uit de matching naam, bijv. `"0016"` |

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `[403] Forbidden resource` | 360Messenger for WhatsApp module | Vervangen door HTTP Make a request module |
| HTTP 100 "The parameter to is required" | `PersonMobilePhone` bestaat niet op Person Account | Gewijzigd naar `{{3.Phone}}` |
| HTTP 100 "Invalid parameter" | Nummer als `0630892143` (lokaal) | Gewijzigd naar `31630892143` (internationaal) |
| HTTP 132001 "Template does not exist in nl" | Template nog Pending bij Meta | Gewacht op Meta goedkeuring |
| HTTP 131037 "Display name needs approval" | Display name gewijzigd in 360dialog | Wachten 24-48u op Meta propagatie |
| URL afgebroken in WhatsApp | `{{1.Name}}` bevat "Matching Number 0016" met spaties | Set Variable module (module 8) toegevoegd met `replace()` |
| `InvalidConfigurationError: Bad control character in string` | `replace()` met aanhalingstekens in JSON body | `replace()` verplaatst naar Set Variable module buiten JSON |
| `Module references non-existing module 'NaN'` | Backticks gebruikt in `replace()` formule | Backticks werken alleen in `switch()`, niet in `replace()` |
| `BundleValidationError: Missing value of required parameter 'record'` | Geen records met "Teacher Invited" bij test | Normaal gedrag, geen fix nodig |
| Vakken in het Engels in WhatsApp | `Subject_s__c` opgeslagen in Engels | `switch()` vertaaltabel met backticks in JSON |
| JSON "Bad Request" | JSON had 6 parameters, template accepteert er 4 | JSON teruggebracht naar 4 parameters |

---

## Speciale Opmerkingen

- 📱 Telefoonnummers **altijd** opslaan als `31XXXXXXXXX` (zonder `+`, met landcode)
- 🔢 Backticks in `switch()` binnen JSON = OK. Backticks in `replace()` = FOUT
- ✅ Template `teacher_invitation` goedgekeurd door Meta
- ⚠️ Disclaimer in template: "Dit nummer is alleen voor het inplannen van proeflessen. Voor andere vragen: WhatsApp +31613689666 of telefoon: 071-3031901"

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Ontvangt Tally Form 1 response van docent → stuurt tijdsloten naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders + escalatie bij niet-reageren |
