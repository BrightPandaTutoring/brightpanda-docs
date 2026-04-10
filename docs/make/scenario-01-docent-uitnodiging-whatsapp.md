# Scenario 01 — Docent Uitnodiging via WhatsApp

**Make naam:** Integration Salesforce, HTTP
**Laatste update:** 10 april 2026
**Status:** 🟡 In ontwikkeling

> **Blokkade:** Meta goedkeuring `teacher_invitation` template (fout 131037 display name + fout 132001 template review)

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

## Modules / Stappen

```
[1] Salesforce → Watch Records
        ↓
    FILTER: Trial_Lesson_Status__c = "Teacher Invited"
        ↓
[3] Salesforce → Get a Record (Teacher Account)
        ↓
[6] Salesforce → Get a Record (Student Account)
        ↓
[5] HTTP → POST 360dialog WhatsApp API
        ↓
[7] Salesforce → Update a Record (Matching)
```

> ⚠️ Module nummering volgt toevoegvolgorde in Make.com, niet de visuele positie in de flow. Module 6 staat visueel vóór Module 5 omdat hij later is toegevoegd.

---

### Module 1 — Salesforce Watch Records
- **Object:** `Student_Teacher_Matching__c`
- **Output velden:** `Id`, `Student__c`, `Teacher__c`, `Subject_s__c`, `Name`, `Trial_Lesson_Status__c`

### Filter (na Module 1)
- **Conditie:** `Trial_Lesson_Status__c` Equal to `Teacher Invited`
- **Bij niet voldoen:** scenario stopt, geen bericht verstuurd

### Module 3 — Salesforce Get a Record (Docent)
- **Type:** Account
- **Record ID:** `{{1.Teacher__c}}`
- **Output velden:** `FirstName`, `Phone`

### Module 6 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{1.Student__c}}`
- **Output velden:** `FirstName`, `ParentSPhone__c`

### Module 5 — HTTP Make a request (360dialog WhatsApp)
Zie [Gedeelde 360dialog configuratie](gedeelde-configuratie.md) voor headers/auth.

**Body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.Phone}}",
  "type": "template",
  "template": {
    "name": "teacher_invitation",
    "language": { "code": "nl" },
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{6.FirstName}}"},
        {"type": "text", "text": "{{switch(1.Subject_s__c; \"Mathematics A\"; \"Wiskunde A\"; \"Mathematics B\"; \"Wiskunde B\"; \"Mathematics C\"; \"Wiskunde C\"; \"Mathematics D\"; \"Wiskunde D\"; \"Physics\"; \"Natuurkunde\"; \"Chemistry\"; \"Scheikunde\"; \"Biology\"; \"Biologie\"; \"Dutch\"; \"Nederlands\"; \"English\"; \"Engels\"; \"French\"; \"Frans\"; \"German\"; \"Duits\"; \"Spanish\"; \"Spaans\"; \"Latin\"; \"Latijn\"; \"Greek\"; \"Grieks\"; \"Arabic\"; \"Arabisch\"; \"Chinese\"; \"Chinees\"; \"Italian\"; \"Italiaans\"; \"Russian\"; \"Russisch\"; \"Turkish\"; \"Turks\"; \"Computer Science\"; \"Informatica\"; \"Geography\"; \"Aardrijkskunde\"; \"History\"; \"Geschiedenis\"; \"Economics\"; \"Economie\"; \"Business Economics\"; \"Bedrijfseconomie\"; \"Philosophy\"; \"Filosofie\"; \"Social Studies\"; \"Maatschappijleer\"; \"Music\"; \"Muziek\"; \"Art\"; \"Kunst\"; \"Cultural & Artistic Education (CKV)\"; \"Culturele en Kunstzinnige Vorming (CKV)\"; \"Cito Test\"; \"Cito Test\"; \"Coding\"; \"Coderen\"; \"Calculations\"; \"Rekenen\"; 1.Subject_s__c)}}"},
        {"type": "text", "text": "https://tally.so/r/2Ekaq9?matching_number={{replace(1.Name; \"Matching Number \"; \"\")}}&student_name={{6.FirstName}}"}
      ]
    }]
  }
}
```

> `switch()` heeft een fallback: als het vak niet in de lijst staat wordt de Engelse naam getoond.

### Module 7 — Salesforce Update a Record
- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{1.Id}}`
- **Velden:**

| Veld | Waarde |
|------|--------|
| `Tally_Link_Teacher__c` | `https://tally.so/r/2Ekaq9?matching_number={{replace(1.Name; "Matching Number "; "")}}&student_name={{6.FirstName}}` |
| `Trial_Lesson_Status__c` | `Availability Received` |

---

## Datastructuur

| Variabele | Module | Beschrijving |
|-----------|--------|-------------|
| `{{1.Id}}` | Module 1 | ID van het matching record |
| `{{1.Teacher__c}}` | Module 1 | Salesforce ID van docent |
| `{{1.Student__c}}` | Module 1 | Salesforce ID van student |
| `{{1.Subject_s__c}}` | Module 1 | Vak (Engelse waarde uit picklist) |
| `{{1.Name}}` | Module 1 | Matching record naam (bijv. "Matching Number 0016") |
| `{{3.FirstName}}` | Module 3 | Voornaam docent |
| `{{3.Phone}}` | Module 3 | WhatsApp nummer docent (internationaal formaat) |
| `{{6.FirstName}}` | Module 6 | Voornaam student |
| `{{6.ParentSPhone__c}}` | Module 6 | Telefoonnummer ouder (niet gebruikt in dit scenario) |
| `replace(1.Name; "Matching Number "; "")` | Berekend | Alleen het nummer, bijv. "0016" |

---

## Gekoppelde Apps & Services

| Service | Gebruik |
|---------|---------|
| **Salesforce** | Watch matching records + ophalen docent/student + updaten record |
| **360dialog** | WhatsApp Business API voor berichtenverzending |
| **Tally.so** | Formulier voor beschikbaarheid (extern, geen Make module) |

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `[403] Forbidden resource` | 360Messenger for WhatsApp module | Vervangen door **HTTP Make a request** met directe 360dialog API |
| HTTP fout 100 "The parameter to is required" | `{{3.PersonMobilePhone}}` bestaat niet op Person Account | Gewijzigd naar `{{3.Phone}}` |
| HTTP fout 100 "Invalid parameter" | Nummer opgeslagen als `0630892143` (lokaal formaat) | Nummer in Salesforce gewijzigd naar `31630892143` |
| HTTP fout 132001 "Template does not exist in nl" | Template stond bij Meta op Pending | Gewacht op Meta goedkeuring |
| HTTP fout 131037 "Display name needs approval" | Display name gewijzigd in 360dialog | Gewacht op Meta hergoedkeuring |
| URL gebroken in WhatsApp (spatie in matching_number) | `{{1.Name}}` geeft "Matching Number 0016" terug | `replace(1.Name; "Matching Number "; "")` gebruikt |
| Vakken verschenen in het Engels | `Subject_s__c` opgeslagen in het Engels | `switch()` vertaaltabel ingebouwd in HTTP parameter 3 |
| "Bad Request" bij eerste test | JSON had 6 parameters, template accepteert er 4 | JSON teruggebracht naar 4 parameters |

---

## Speciale Opmerkingen

- ⚠️ Template `teacher_invitation` opnieuw ingediend bij Meta op 8 maart na tekstwijzigingen — stond daarna in review
- 📱 Telefoonnummers **altijd** in Salesforce opslaan als `31XXXXXXXXX` (zonder `+`, met landcode)
- 🔢 Module nummering volgt toevoegvolgorde, niet visuele positie in de flow

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Ontvangt Tally response van docent → stuurt tijdsloten naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders + escalatie bij niet-reageren |
