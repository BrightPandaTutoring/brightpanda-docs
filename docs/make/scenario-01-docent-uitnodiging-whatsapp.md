# Scenario 01 — Docent Uitnodiging via WhatsApp

**Make naam:** Scenario 1 — Teacher Invitation
**Make scenario ID:** 4729958
**Laatste update:** 9 juni 2026
**Status:** ✅ Werkend — event-driven via Salesforce webhook

---

## Doel

Wanneer een matching klaarstaat voor een proefles, stuurt dit scenario een **WhatsApp naar de docent** met alle benodigde info (leerling, vak in het Nederlands, contactgegevens ouder, Tally Form 1 link), daarna een introductiebericht aan de ouder, voegt de ouder toe aan MailerLite, en zet de status in Salesforce op "Teacher Invited".

**Probleem dat het oplost:** Bright Panda moest handmatig docenten benaderen voor proeflesplanning.

---

## Trigger — event-driven webhook (sinds 9 juni 2026)

Dit scenario draait **niet meer op polling**. Het wordt direct getriggerd door een Salesforce Record-Triggered Flow zodra `Start_Trial_Class_Process__c` op een matching wordt aangevinkt.

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Hook ID | 3197287 |
| Aangeroepen door | Salesforce Flow "Scenario 1 — Teacher Invitation Webhook" (V10) |
| Payload | `studentId`, `teacherId`, `subjects`, `name`, `status`, `matchingId` |

**Workflow voor de gebruiker:** zet Status = Trial Class, vul Teacher/Student/Subject(s), vink **Start_Trial_Class_Process__c** aan. De Salesforce Flow vuurt dan asynchroon de webhook af.

Zie [Salesforce Flow → Make Webhook Integratie](salesforce-flow-webhook-integratie.md) voor de volledige flow-configuratie, de anti-loop-opzet en troubleshooting.

**Filter na de webhook:** `{{14.status}}` gelijk aan `Trial Class`.

---

## Module Volgorde

```
[14] Custom Webhook (payload uit Salesforce Flow)
         ↓
[18] Webhook Response — 200 + {"accepted": true} + Content-Type: application/json
         ↓
     Filter: {{14.status}} = "Trial Class"
         ↓
[3]  Salesforce → Get a Record (Teacher Account, {{14.teacherId}})
         ↓
[6]  Salesforce → Get a Record (Student Account, {{14.studentId}})
         ↓
[9]  Salesforce → SOQL Contacts (loopt mee, output ongebruikt)
         ↓
[10] HTTP GET → Google Apps Script (vakvertaling NL, {{14.subjects}})
         ↓
[5]  HTTP POST → 360dialog (WhatsApp naar docent — teacher_invitation)
         ↓
[11] Sleep 180 seconden
         ↓
[12] HTTP POST → 360dialog (WhatsApp naar ouder — teacher_intro_message_parent)
         ↓
[13] MailerLite → Create/Update Subscriber (groep "Teacher Found - Parent Email")
         ↓
[7]  Salesforce → Update a Record (Trial_Lesson_Status, Teacher_Invited_At, Tally link)
```

> Volgorde: 14 → 18 → 3 → 6 → 9 → 10 → 5 → 11 → 12 → 13 → 7

> **Belangrijk:** module 18 (Webhook Response) moet direct na de trigger staan, mét `Content-Type: application/json`. Zonder die header kan Salesforce het antwoord niet parsen, faalt de async flow-run, en plant Salesforce automatische retries in die later als "spook-webhooks" terugkomen. Zie de integratie-doc.

---

## Modules Detail

### Module 14 — Custom Webhook
- **Hook ID:** 3197287
- **Payload velden:** `{{14.studentId}}`, `{{14.teacherId}}`, `{{14.subjects}}`, `{{14.name}}` (Matching Number), `{{14.status}}`, `{{14.matchingId}}`

### Module 18 — Webhook Response
- **Status:** 200
- **Body:** `{"accepted": true}`
- **Header:** `Content-Type: application/json`

### Module 3 — Salesforce Get a Record (Docent)
- **Type:** Account
- **Record ID:** `{{14.teacherId}}`
- **Output:** `{{3.FirstName}}`, `{{3.Phone}}`

> ⚠️ Docenten zijn **Account** records in Salesforce (geen Contact). Telefoon = `Phone` veld op Account, in Make.com zichtbaar als "Business Phone".

### Module 6 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{14.studentId}}`
- **Output:** `{{6.FirstName}}`, `{{6.ParentSName__c}}`, `{{6.ParentSPhone__c}}`, `{{6.ParentSEmail__c}}`

> Ouder naam, telefoon en e-mail zitten als custom velden op het **Student Account**: `ParentSName__c`, `ParentSPhone__c`, `ParentSEmail__c`. Let op de hoofdletter S (`ParentS...`).

### Module 9 — Salesforce SOQL (Contacts)
- **Query:** `SELECT Id, FirstName, Phone FROM Contact WHERE AccountId = '{{6.Id}}'`
- Loopt mee in de keten maar de output wordt niet gebruikt (oudergegevens komen rechtstreeks van het Student Account in module 6). Kan bij een opschoonronde verwijderd worden.

### Module 10 — HTTP GET → Google Apps Script (Vakvertaling)
- **URL:** `https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec?subject={{encodeURL(14.subjects)}}`
- **Method:** GET
- **Parse response:** NO
- **Output:** `{{10.data}}` — plain text Nederlandse vaknaam, bijv. `"Wiskunde B"`

> Gebruik altijd `{{10.data}}` voor Nederlandstalige communicatie, nooit het ruwe `{{14.subjects}}` / `Subjects__c`. Zie [Google Apps Script — Vakvertaling](google-apps-script.md#script-1--vakvertaling).

### Module 5 — HTTP POST → 360dialog (WhatsApp naar docent)

**Template:** `teacher_invitation` (6 parameters). Zie [Gedeelde configuratie](gedeelde-configuratie.md) voor headers.

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
        {"type": "text", "text": "{{6.ParentSName__c}}"},
        {"type": "text", "text": "{{6.ParentSPhone__c}}"},
        {"type": "text", "text": "https://tally.so/r/2Ekaq9?matching_number={{encodeURL(14.name)}}&student_name={{6.FirstName}}"}
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
| `{{4}}` | `{{6.ParentSName__c}}` | Naam ouder (custom veld op Student Account) |
| `{{5}}` | `{{6.ParentSPhone__c}}` | Telefoonnummer ouder (custom veld op Student Account) |
| `{{6}}` | Tally URL | `https://tally.so/r/2Ekaq9?matching_number={{encodeURL(14.name)}}&student_name={{6.FirstName}}` |

> `encodeURL(14.name)` converteert "Matching Number 0016" naar "Matching%20Number%200016" zodat de URL niet breekt in WhatsApp.

### Module 11 — Sleep
- **Duur:** 180 seconden. Geeft de docent even tijd voordat de ouder een bericht krijgt.

### Module 12 — HTTP POST → 360dialog (WhatsApp naar ouder)

**Template:** `teacher_intro_message_parent` (4 parameters).

```json
{
  "messaging_product": "whatsapp",
  "to": "{{replace(3.Phone; \"+\"; )}}",
  "type": "template",
  "template": {
    "name": "teacher_intro_message_parent",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{6.ParentSPhone__c}}"},
        {"type": "text", "text": "{{6.ParentSName__c}}"},
        {"type": "text", "text": "{{3.FirstName}}"},
        {"type": "text", "text": "{{6.FirstName}}"}
      ]
    }]
  }
}
```

> Module 12 strikt het plusteken uit het nummer via `replace(3.Phone; "+"; )`. Module 5 gebruikt het nummer mét plus.

### Module 13 — MailerLite Create/Update Subscriber
- **Email:** `{{6.ParentSEmail__c}}`
- **Groep:** `189010938726188387` ("Teacher Found - Parent Email")
- **Velden:** `name` = `{{6.ParentSName__c}}`, `student_name` = `{{6.FirstName}}`, `teacher_name` = `{{3.FirstName}}`, `subjects` = `{{10.data}}`

> Een subscriber toevoegen aan een groep triggert de bijbehorende MailerLite-automation; geen aparte "Add to Group" module nodig.

### Module 7 — Salesforce Update a Record
- **Record ID:** `{{14.matchingId}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Status__c` | `Teacher Invited` |
| `Teacher_Invited_At__c` | `{{now}}` |
| `Tally_Link_Teacher__c` | `https://tally.so/r/2Ekaq9?matching_number={{encodeURL(14.name)}}&student_name={{6.FirstName}}` |

> Module 7 raakt `Start_Trial_Class_Process__c` bewust niet aan. Het zetten van `Trial_Lesson_Status__c` haalt het record uit de qualifying-staat van de flow, wat de loop voorkomt (in combinatie met "Only when a record is updated to meet the condition requirements" in de flow).

---

## WhatsApp Template — `teacher_invitation`

**Status:** ✅ Approved · **Categorie:** Utility · **Taal:** nl · **Parameters:** 6

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
| Tally URL afgekapt na spatie | "Matching Number 0016" bevat spaties | `encodeURL(14.name)` gebruikt |
| `switch()` brak JSON | Aanhalingstekens conflicteerden | Aparte HTTP module met Google Apps Script |
| Template door Meta als Marketing geclassificeerd | Emoji + woord "proefles" | Opnieuw aangemaakt zonder emoji, categorie Utility |
| Webhook vuurt herhaaldelijk / loop (elke ~3 min) | Actieve flow-versie mist `Trial_Lesson_Status Is Null`-guard of staat op "Every time" | Flow V10: conditie `Trial_Lesson_Status Is Null` + "Only when a record is updated to meet the condition requirements"; geen Is Changed |
| Spook-webhooks ~29 min later, ongevraagd | Mislukte async flow-run (verkeerde Content-Type) → Salesforce retryt automatisch tot 2x met de oude context | Module 18 Webhook Response → `Content-Type: application/json`; geslaagde run laat 0 errored interviews achter |
| Aanpassingen aan flow hadden geen effect | Bewerkte versie was InvalidDraft, oudere versie nog actief | Via `FlowVersionView` controleren welke versie Active is; juiste versie activeren |

> Volledige uitleg en diagnostische SOQL-queries in [Salesforce Flow → Make Webhook Integratie](salesforce-flow-webhook-integratie.md#veelvoorkomende-fouten-en-oplossingen).

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Verwerkt Form 1 response van docent |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende docent |
| [Salesforce Flow Webhook Integratie](salesforce-flow-webhook-integratie.md) | Trigger-mechaniek, anti-loop, troubleshooting |
| [Google Apps Script](google-apps-script.md) | Script 1 Vakvertaling |
