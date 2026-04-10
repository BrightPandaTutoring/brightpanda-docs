# Scenario 01 — Docent Uitnodiging via WhatsApp

**Make naam:** Scenario 1 Integration Salesforce HTTP
**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — getest en in productie

---

## Doel

Detecteert automatisch wanneer een matching de status **"Trial Class"** krijgt in Salesforce (en nog geen `Trial_Lesson_Status__c` heeft), haalt docent- en studentgegevens op, vertaalt het vak naar Nederlands via Google Apps Script, en stuurt een **WhatsApp naar de docent** met alle benodigde info inclusief contactgegevens van de ouder en de Tally Form 1 link.

**Probleem dat het oplost:** Bright Panda moest handmatig docenten benaderen voor proeflesplanning.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Salesforce Watch Records |
| Object | `Student_Teacher_Matching__c` |
| Watch type | By Updated Time |
| Interval | Elke 15 minuten |
| Limit | 10 records per run |

**Filter na module 1:**
- `Status__c` gelijk aan `Trial Class`
- `Trial_Lesson_Status__c` gelijk aan **leeg** (voorkomt herhaling — veld wordt na versturen gevuld)

---

## Module Volgorde

```
[1]  Salesforce → Watch Records
         ↓
     Filter: Status__c = "Trial Class" EN Trial_Lesson_Status__c = leeg
         ↓
[3]  Salesforce → Get a Record (Teacher Account)
         ↓
[6]  Salesforce → Get a Record (Student Account)
         ↓
[10] HTTP GET → Google Apps Script (vakvertaling NL)
         ↓
[5]  HTTP POST → 360dialog (WhatsApp naar docent)
         ↓
[7]  Salesforce → Update a Record (status + Tally link)
```

> Volgorde: 1 → 3 → 6 → 10 → 5 → 7

> **Module 9 (Contact SOQL) is niet meer actief.** Ouder naam en telefoonnummer worden direct van het Student Account opgehaald via custom velden `ParentsName__c` en `ParentSPhone__c`.

---

## Modules Detail

### Module 1 — Salesforce Watch Records
- **Object:** `Student_Teacher_Matching__c`
- **Output:** `Teacher__c`, `Student__c`, `Name`, `Subject_s__c`, `Record ID`

### Module 3 — Salesforce Get a Record (Docent)
- **Type:** Account
- **Record ID:** `{{1.Teacher__c}}` (blauwe chip)
- **Output:** `{{3.FirstName}}`, `{{3.Phone}}`

> ⚠️ Docenten zijn **Account** records in Salesforce (geen Contact). Telefoon = `Phone` veld op Account, zichtbaar in Make.com als "Business Phone".

### Module 6 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{1.Student__c}}` (blauwe chip)
- **Output:** `{{6.FirstName}}`, `{{6.ParentsName__c}}`, `{{6.ParentSPhone__c}}`

> Ouder naam en telefoonnummer zitten als custom velden op het **Student Account**: `ParentsName__c` en `ParentSPhone__c`. Geen aparte Contact SOQL nodig.

### Module 10 — HTTP GET → Google Apps Script (Vakvertaling)

- **URL:** `https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec?subject={{encodeURL(1.Subject_s__c)}}`
- **Method:** GET
- **Parse response:** NO (uitgeschakeld)
- **Output:** `{{10.data}}` — plain text Nederlandse vaknaam, bijv. `"Wiskunde B"`

> Zie [Google Apps Script — Script 1 Vakvertaling](google-apps-script.md#script-1--vakvertaling) voor de volledige vertaaltabel.

### Module 5 — HTTP POST → 360dialog (WhatsApp naar docent)

Zie [Gedeelde configuratie](gedeelde-configuratie.md) voor headers.

**Template:** `teacher_invitation` (6 parameters)

**Volledige JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{3.Phone}}",
  "type": "template",
  "template": {
    "name": "teacher_invitation",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{6.FirstName}}"},
        {"type": "text", "text": "{{10.data}}"},
        {"type": "text", "text": "{{6.ParentsName__c}}"},
        {"type": "text", "text": "{{6.ParentSPhone__c}}"},
        {"type": "text", "text": "https://tally.so/r/2Ekaq9?matching_number={{encodeURL(1.Name)}}&student_name={{6.FirstName}}"}
      ]
    }]
  }
}
```

**Parameter mapping:**

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{3.FirstName}}` | Voornaam docent |
| `{{2}}` | `{{6.FirstName}}` | Voornaam student |
| `{{3}}` | `{{10.data}}` | Vak in het Nederlands |
| `{{4}}` | `{{6.ParentsName__c}}` | Naam ouder (custom veld op Student Account) |
| `{{5}}` | `{{6.ParentSPhone__c}}` | Telefoonnummer ouder (custom veld op Student Account) |
| `{{6}}` | Tally URL | `https://tally.so/r/2Ekaq9?matching_number={{encodeURL(1.Name)}}&student_name={{6.FirstName}}` |

> `encodeURL(1.Name)` converteert "Matching Number 0016" naar "Matching%20Number%200016" zodat de URL niet breekt in WhatsApp.

### Module 7 — Salesforce Update a Record
- **Record ID:** `{{1.Record ID}}` ← **blauwe chip, nooit als platte tekst typen!**

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Status__c` | `Teacher Invited` |
| `Tally_Link_Teacher__c` | `https://tally.so/r/2Ekaq9?matching_number={{encodeURL(1.Name)}}&student_name={{6.FirstName}}` |

---

## WhatsApp Template — `teacher_invitation`

**Status:** ✅ Approved
**Categorie:** Utility
**Taal:** nl
**Parameters:** 6

**Volledige tekst:**
```
Hoi {{1}},

Je bent gematcht met een nieuwe leerling via Bright Panda Bijles.

Leerling: *{{2}}*
Vak: *{{3}}*

Contactgegevens ouder:
Naam: *{{4}}*
Telefoon: *{{5}}*

Vul zo snel mogelijk je beschikbaarheid in via deze link:

{{6}}

Neem daarna contact op met de ouder via WhatsApp of telefoon om jezelf voor te stellen.
Dit maakt een goede eerste indruk en biedt de kans om alvast belangrijke details te bespreken.

Hoe sneller jij reageert, hoe groter de kans dat wij deze leerling aan jou kunnen koppelen!

Dit nummer is alleen voor het inplannen van proeflessen en wordt niet gebruikt voor communicatie.
Voor andere vragen kun je ons bereiken via WhatsApp of telefoon: +31613689666.

Bedankt!
```

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `[403] Forbidden resource` | Native 360dialog module | Vervangen door HTTP Make a request |
| Tally URL afgekapt na spatie | "Matching Number 0016" bevat spaties | `encodeURL(1.Name)` gebruikt |
| `Missing value of required parameter 'record'` | Record ID als platte tekst ingevoerd | Vervangen door blauwe chip `1.Record ID` |
| `switch()` brak JSON | Aanhalingstekens conflicteerden | Aparte HTTP module met Google Apps Script |
| Template door Meta als Marketing geclassificeerd | Emoji + woord "proefles" triggerde classificatie | Opnieuw aangemaakt zonder emoji, categorie Utility |
| Scenario stuurde elke 15 min bericht | Geen filter op Trial_Lesson_Status__c | Filter toegevoegd: Trial_Lesson_Status__c = leeg |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Verwerkt Form 1 response van docent |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende docent |
| [Google Apps Script](google-apps-script.md) | Script 1 Vakvertaling |
