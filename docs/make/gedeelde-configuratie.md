# Gedeelde Configuratie — Make.com Scenarios

Configuratie die van toepassing is op **alle** Bright Panda Make.com scenarios.

---

## 360dialog Configuratie

### HTTP Module Instellingen
| Instelling | Waarde |
|-----------|--------|
| **API Endpoint** | `https://waba-v2.360dialog.io/messages` |
| **Method** | POST |
| **Authentication** | No authentication (in Make.com) |
| **Header: D360-API-KEY** | `xl6Aj3Gs66I40LQl7C6GbjlxAK` |
| **Header: Content-Type** | `application/json` |
| **Body content type** | `application/json` |
| **Body input method** | JSON string |

> ⚠️ **API-key lettertypes:** De sleutel bevat zowel hoofdletters als kleine letters die op elkaar lijken. Kopieer de sleutel **altijd** van een werkende module — nooit handmatig overtypen. Fout: `I` (hoofdletter) versus `l` (kleine letter L) zijn niet te onderscheiden in sommige fonts.

### 360dialog Account Status
| Eigenschap | Waarde |
|-----------|--------|
| **Plan** | Starter EUR 49/maand |
| **Display name** | Bright Panda Bijles |
| **Status** | READY (groen bolletje) |
| **Quality Rating** | High |
| **Business Messaging Limit** | 250 unieke gebruikers per 24 uur |
| **WhatsApp Business nummer** | +1 555-759-0811 (API formaat: `15557590811`) |

---

## WhatsApp Templates

| Template | Status | Gebruikt in | Parameters |
|----------|--------|------------|-----------|
| `teacher_invitation` | ✅ Goedgekeurd | Scenario 01 module 5 | 6 — naam docent, naam student, vak NL, naam ouder, tel ouder, Tally link |
| `parent_timeslot_invitation` | ✅ Goedgekeurd | Scenario 02 module 5 | 4 — naam ouder, naam student, naam docent, picker URL |
| `trial_lesson_confirmation_parent` | ✅ Goedgekeurd | Scenario 3b module 7 | 6 — naam ouder, naam student, datum, tijd, naam docent, tel docent |
| `trial_lesson_confirmed_teacher` | ✅ Goedgekeurd | Scenario 3b module 12 | 6 — naam docent, naam student, datum, tijd, naam ouder, tel ouder |
| Availability Conflict template (docent) | 🔴 Nog te maken | Scenario 3b Pad B | — instructie om ouder te bellen + contactgegevens |
| Reminder template docent | 🔴 Niet aangemaakt | Scenario 03 | — |
| Reminder template ouder | 🔴 Niet aangemaakt | Scenario 03 | — |

> ⚠️ **Pas templates alleen aan na volledig testen.** Elke wijziging vereist opnieuw Meta goedkeuring (wachttijd: 2-7 werkdagen).
> ⚠️ **Template classificatie:** Vermijd emoji's in de template tekst — Meta classificeert dan als Marketing in plaats van Utility. Dien altijd handmatig in als categorie Utility.

---

## Salesforce Verbinding

| Instelling | Waarde |
|-----------|--------|
| **Verbindingsnaam in Make.com** | Bright Panda Salesforce |
| **Make.com omgeving** | eu1.make.com |
| **Instance URL** | `https://brightpanda.my.salesforce.com` |
| **Setup URL** | `https://brightpanda.my.salesforce-setup.com` |
| **Username** | `info@brightpanda.nl` |
| **Security Token** | `fQ1CK5nBYy8qpd5j05vHaFUnP` |
| **MCP Server** | `@tsmztech/mcp-server-salesforce` |
| **MCP Config pad** | `~/Library/Application Support/Claude/claude_desktop_config.json` |

> ⚠️ **MCP beperkingen:** @tsmztech MCP server ondersteunt geen LongTextArea of picklist waarden toevoegen via Metadata API. Workaround: Claude in Chrome voor browser automatisering, of handmatig via Setup UI.

> ⚠️ **Salesforce Setup iframes:** Claude in Chrome heeft problemen met klik-coördinaten in Salesforce Setup pagina's die in iframes laden. Sommige handelingen moeten handmatig worden uitgevoerd.

---

## Google Calendar & Gmail

| Service | Waarde |
|---------|--------|
| **Google Calendar scheduling link** | `https://calendar.app.google/ArBhdKvAnLR924Xa6` |
| **Gmail account** | `info@brightpanda.nl` |
| **Gmail MCP** | Read + draft only — **geen send capability** |
| **Gebruik** | Scenario 13 Route 1: Google Calendar link in interview uitnodiging email |

---

### Salesforce Record Structuur

| Entiteit | Object type | Record Type | Record Type ID |
|----------|-------------|-------------|----------------|
| Docenten | Account (Person Account) | Teacher | `012KB000000ojZLYAY` |
| Studenten/Ouders | Account (Person Account) | Student | — |

> **Ouder contactgegevens** zitten als custom velden op het **Student Account**. Gebruik `{{X.ParentsName__c}}` en `{{X.ParentSPhone__c}}` direct na een Get a Record op het Student Account.

---

### Teacher Account Velden

**Standaard velden:**
- `Id`, `Name`, `FirstName`, `LastName`
- `PersonEmail` — primaire email
- `Phone` — internationaal formaat met `+` (bijv. `+31630892143`)
- `BillingStreet`, `BillingCity`, `BillingPostalCode`, `BillingCountry`
- `RecordTypeId` = `012KB000000ojZLYAY`

**Custom velden:**

| API Naam | Type | Beschrijving |
|----------|------|-------------|
| `LifecycleStage__c` | Picklist | Huidige fase (zie lifecycle stages) |
| `Subjects__c` | Multipicklist | Vakken in het Engels (zie vakkenlijst) |
| `Can_Teach_Until_Education_Level__c` | Picklist | Max onderwijsniveau (Basisschool / VMBO-BBL,GL,KBL,TL / Havo / VWO / Gymnasium) |
| `Can_Teach_Until_School_Year__c` | Picklist | Max leerjaar (Groep 1-8, 1-6) |
| `Can_Give_Exam_Training__c` | Boolean | Examentraining mogelijk |
| `CanTeachElementarySchool__c` | Boolean | Kan basisschool geven |
| `Teaching_Level_Details__c` | LongTextArea (32768) | Gedetailleerde niveauinfo per onderwijsniveau |
| `Level_Details__c` | Text (255) | ⛔ Oud veld — verwijderen na datamigratate naar Teaching_Level_Details__c |
| `Claude_Recommendation__c` | LongTextArea | AI aanbeveling van Scenario 12 |
| `IBAN__c` | Text (255) | IBAN bankrekening (via Tally + AVG toestemming) |
| `NameOnBankCard__c` | Text (255) | Naam op bankpas |
| `HourlyRate__c` | Currency | Uurtarief |
| `Study__c` | Text (255) | Studie (vrij tekst) |
| `University__c` | Text (255) | Universiteit/hogeschool (vrij tekst fallback) |
| `University_WO__c` | Picklist | Universiteit WO (Global Value Set) |
| `University_HBO__c` | Picklist | Hogeschool HBO (Global Value Set "University (HBO)") |
| `HBO_WO__c` | Picklist | HBO (Bachelor) / WO Bachelor / WO Master |
| `OfficialName__c` | Text | Officiële naam voor contract |
| `Offboarded_Date__c` | Date | Datum offboarding (ingevuld door Scenario 13) |
| `Notes__c` | Rich Text Area (32768) | Interne notities |
| `Contract_Start_Date__c` | Date | Startdatum contract |
| `Contract_End_Date__c` | Date | Einddatum contract (= start + 365 dagen) |
| `Interview_Date__c` | Date | Datum interview |
| `Experience__c` | Picklist | Junior / Medior / Senior |
| `MaxStudentCapacity__c` | Number | Maximaal aantal leerlingen |

> ⚠️ **`LifecycleStage__c`** — géén underscore tussen "Lifecycle" en "Stage". Eerder gedocumenteerd als `Lifecycle_Stage__c` (fout).

**LifecycleStage__c waarden (Teacher):**
`New` → `Interview Invited` → `Interview Scheduled` → `Interview Completed` → `Contracting` → `Pending Onboarding` → `On-boarded` → `Contract Expiring Soon` → `Renew` → `Offboarded` → `Not a Match` → `Not Interested`

**Picklist: nieuwe waarden toevoegen:**
Nieuwe universiteiten/vakken die niet in de picklist staan, moeten via browser handmatig worden toegevoegd. Kortste pad:
`https://brightpanda.my.salesforce.com/setup/ui/recordtypefields.jsp?id=012KB000000ojZLYAY&type=Account&setupid=AccountRecordTypes`

---

### Student Account Velden

| API Naam | Type | Beschrijving |
|----------|------|-------------|
| `Name` | Text | Naam leerling |
| `FirstName` | Text | Voornaam leerling |
| `ParentsName__c` | Text | Naam ouder (let op: hoofdletter S) |
| `ParentSPhone__c` | Text | Telefoon ouder (internationaal formaat) |
| `ParentSEmail__c` | Text | Email ouder |
| `MailingCity` | Text | Woonplaats |
| `MailingPostalCode` | Text | Postcode |
| `LifecycleStage__c` | Picklist | Huidige fase student |
| `Subjects__c` | Multipicklist | Vak(ken) — zelfde Global Value Set als Teacher |
| `SchoolYear__c` | Text | Leerjaar (bijv. "Groep 5", "3 VWO") |
| `ReferredToBPVia__c` | Text | Hoe verwezen naar BP |
| `AnyConditions__c` | Text | Bijzonderheden leerling |
| `IssuesWithSubject__c` | Text | Problemen met het vak |

**LifecycleStage__c waarden (Student):**
`New` → `Enrollment` → `Matching Teacher` → `Trial Class` → `Client` → `Churned` → `Wrong Match` → `Stopped - Never Converted` → `Stopped - Existing Client`

### Salesforce Custom Object: Student_Teacher_Matching__c

| API Naam | Type | Beschrijving |
|----------|------|-------------|
| `Name` | Text | Matching naam, bijv. "Matching Number 0016" |
| `Teacher__c` | Lookup (Account) | Docent |
| `Student__c` | Lookup (Account) | Student |
| `Status__c` | Picklist | Trial Class, Active, Paused, Stopped |
| `Trial_Lesson_Status__c` | Picklist | zie tabel hieronder |
| `Available_Timeslots__c` | Long Text Area (10.000) | `timeslotsRaw` pipe-separated string |
| `Tally_Link_Teacher__c` | Text | Tally Form 1 URL verstuurd naar docent |
| `Trial_Lesson_Date__c` | DateTime | Definitieve datum + tijd proefles (zonder Z suffix) |
| `Subject_s__c` | Text | Vak (Engelse naam vanuit Salesforce) |
| `Teacher_Reminder_Sent__c` | Checkbox | true na versturen reminder docent (Scenario 6) |
| `Teacher_Escalation_Sent__c` | Checkbox | true na versturen intern alert (Scenario 7) + conflict reminder (Scenario 5) |
| `Parent_Reminder_Sent__c` | Checkbox | true na versturen 24u reminder ouder (Scenario 9) |
| `Parent_Escalation_Sent__c` | Checkbox | true na versturen 48u escalatie ouder (Scenario 9) |
| `Teacher_Invited_At__c` | DateTime | Timestamp wanneer docent uitgenodigd is (ingevuld door Scenario 1) |
| `Parent_Invited_At__c` | DateTime | Timestamp wanneer ouder uitgenodigd is (ingevuld door Scenario 2) |
| `Trial_Class_Reminder_48h_Sent__c` | Checkbox | true na 48u reminder (Scenario 8) |
| `Trial_Class_Reminder_24h_Sent__c` | Checkbox | true na 24u reminder (Scenario 8) |
| `Trial_Class_Reminder_2h_Sent__c` | Checkbox | true na 2u reminder (Scenario 8) |

### Trial_Lesson_Status__c Picklist Waarden

| Waarde | Trigger |
|--------|---------|
| `Teacher Invited` | Scenario 01 — na versturen WhatsApp docent |
| `Availability Received` | — (handmatig of toekomstig) |
| `Parent Invited` | Scenario 02 — na versturen picker URL naar ouder |
| `Trial Lesson Scheduled` | Scenario 3b Pad A — na bevestiging tijdslot |
| `Availability Conflict` | Scenario 3b Pad B — geen tijdslot past |
| `Trial Lesson Completed` | Scenario 11 — automatisch 60-75 min na lesstart |
| `No Show` | Scenario 9 Route 3 — na 72u geen tijdslot gekozen |

### Status__c Picklist Waarden

| Waarde | Gebruik |
|--------|---------|
| `Trial Class` | Default bij aanmaken matching |
| `Active` | Na succesvolle proefles — actieve bijles |
| `Paused` | Tijdelijk gepauzeerd |
| `Stopped - Never Converted` | Gestopt na Scenario 9 Route 3 (nooit proefles gehad) |
| `Stopped - Existing Client` | Gestopt na actieve bijles |
| `Wrong Match` | Mismatch docent-leerling |

---

## TinyURL Configuratie

| Instelling | Waarde |
|-----------|--------|
| **Plan** | Pro ($13/maand, 250 links/maand) |
| **API Endpoint** | `https://api.tinyurl.com/create` |
| **API Token** | `azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji` |
| **Branded domain** | `go.brightpanda.nl` |
| **CNAME waarde** | `hrj2vlx.customer.tinyurl.com` |
| **DNS beheer** | Squarespace (brightpanda.nl domein) |
| **DNS status** | ✅ ACTIEF |

**JSON body voor Make.com:**
```json
{
  "url": "https://...",
  "domain": "go.brightpanda.nl"
}
```

> ⚠️ `"domain": "go.brightpanda.nl"` alleen toevoegen nadat DNS propagatie bevestigd is. Tot die tijd weglaten — TinyURL geeft dan een `tinyurl.com` link terug.

**Output in Make.com:** `{{MODULE.data.data.tiny_url}}` — let op: **dubbel `.data.data`**

**Gebruik in Make.com:** HTTP POST naar TinyURL endpoint vóór het versturen van de WhatsApp — de verkorte URL wordt meegestuurd in het bericht.

**Geïntegreerd:**
- ✅ Scenario 2 module 35 (picker link naar ouder)

**Nog te integreren (TO DO):**
- ⚠️ Scenario 3b Pad B module 29 (Tally Form 3 link naar docent)
- ⚠️ Scenario 5 module 4 (Tally Form 3 reminder link)
- ⚠️ Scenario 6 modules 4 + 7 (Tally Form 1 link in reminders)
- ⚠️ Scenario 03 Routes 1 + 2 (picker link in ouder reminders)

---

## Anthropic API Configuratie

| Instelling | Waarde |
|-----------|--------|
| **API Key naam** | `Bright Panda Make.com` |
| **Endpoint** | `https://api.anthropic.com/v1/messages` |
| **Model** | `claude-opus-4-6` |
| **Header** | `x-api-key: [API key]` |
| **Header** | `anthropic-version: 2023-06-01` |
| **Gebruikt in** | Scenario 12 module 3 (docent analyse) |

**Output pad in Make.com:** `{{MODULE.data.content[].text}}`

---

## DocuSeal Configuratie

| Instelling | Waarde |
|-----------|--------|
| **Plan** | EU |
| **API Endpoint** | `https://api.docuseal.eu/submissions` |
| **API Key** | `kF6DXM8V8AEJcRhXshwE1RxdvarDx9NHwuYjd9FnZz3` |
| **Template ID** | `485548` |
| **Prijs** | $0.20 per contract (via Make.com) |
| **Gebruikt in** | Scenario 13 Route 2 (contract versturen bij Contracting) |
| **Webhook** | Scenario 14 (bij contract getekend) |

**Template velden (exact lowercase):** `name`, `street`, `city`, `start_date`, `hourly_rate`, `signing_date`, `signature`

> ⚠️ Veldnamen zijn case-sensitive en exact lowercase. `Name` geeft error — moet `name` zijn.

---

## MailerLite Configuratie

| Instelling | Waarde |
|-----------|--------|
| **URL** | app.mailerlite.com |
| **Account** | Bright Panda Bijles |
| **Plan** | Growing Business |
| **Connectienaam in Make.com** | MailerLite Bright Panda |
| **API Token** | Opgeslagen door gebruiker (niet gedocumenteerd) |

**Custom Fields (merge tags):**

| Merge tag | Type | Beschrijving |
|-----------|------|-------------|
| `{$student_name}` | Text | Voornaam leerling |
| `{$teacher_name}` | Text | Voornaam docent |
| `{$subjects}` | Text | Vakken (kommagescheiden NL) |
| `{$school_year}` | **Text** (niet Number!) | Leerjaar — bijv. "Groep 5", "3 VWO" |
| `{$registration_date}` | Text | Datum aanmelding |
| `{$referred_by}` | Text | Via welk kanaal verwezen |
| `{$trial_lesson_outcome}` | Text | Resultaat proefles |
| `{$total_matchings}` | Text | Totaal aantal matchings |
| `{$is_pro}` | Text | Pro aanmelding (true/false) |
| `{$is_active_client}` | Text | Actieve klant (true/false) |
| `{$has_trial_lesson}` | Text | Heeft proefles gehad (true/false) |
| `{$name}` | Text | Standaard veld — voornaam |
| `{$last_name}` | Text | Standaard veld — achternaam |
| `{$phone}` | Text | Standaard veld — telefoon |

> ⚠️ **Merge tag format:** Gebruik **altijd** `{$veldnaam}` (met dollarteken). `{veldnaam}` (zonder `$`) werkt niet — variabele wordt niet ingevuld in de email.
>
> ⚠️ **`school_year` is Text type** — als Number type ingesteld wordt "Groep 5" afgewezen. Veld type wijzigen via MailerLite → Subscribers → Fields.

Zie [mailerlite.md](mailerlite.md) voor volledige inrichting (groepen, custom fields, automations).

---

## Google Apps Script URLs

| Script | URL | Methode | Gebruikt in |
|--------|-----|---------|------------|
| **Script 1 — Vakvertaling** | `https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec` | GET | Scenario 01 module 10 |
| **Script 2 — Tijdslotverwerking** | `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec` | POST | Scenario 02 module 31 |
| **Script 3 — Picker v11** | `https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec` | GET (HTML) | Scenario 02 → ouder klikt → POST naar Scenario 3b |

---

## Make.com Omgeving

| Instelling | Waarde |
|-----------|--------|
| **Regio** | eu1 (Europa) |
| **URL** | eu1.make.com |
| **Organisatie ID** | 1179486 |

---

## Contactgegevens

| Contact | Waarde | Gebruik |
|---------|--------|---------|
| WhatsApp Business (Bright Panda) | `15557590811` | Verzendend nummer |
| Zakelijk WhatsApp (intern) | `31613689666` | Escalaties, intern alerts |
| Raouf | `31630892143` | Intern alert Scenario 11 |
| Yasin | `31623325599` | Intern alert Scenario 11 |
| Intern telefoon | 071-3031901 | Vermeld in template disclaimer |
| Intern WhatsApp (zichtbaar) | +31613689666 | Vermeld in template disclaimer |

---

## Tally Formulieren

| Formulier | URL | Webhook URL | Doel |
|-----------|-----|-------------|------|
| Form 1 (docent beschikbaarheid) | `https://tally.so/r/2Ekaq9` | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` | Docent vult beschikbaarheid in |
| Form 2 (fallback ouder) | `https://tally.so/r/WOozov` | — | ⛔ Niet meer gebruikt — vervangen door GAS picker (v11 toont Form 2 link niet meer) |
| Form 3 (docent tijdslot na conflict) | `https://tally.so/r/q4PDV9` | `https://hook.eu1.make.com/1aa2q2bnkvxodps6errjs6pxs3j4v4d9` | Docent vult afgesproken tijdslot in na Availability Conflict |

> Tally Form 2 is **vervangen** door de Google Apps Script picker pagina (Script 3 v11). De no_match knop toont nu geen Tally Form 2 link meer — de docent belt de ouder en vult het tijdslot in via Tally Form 3.

### Tally Form 1 Webhook Data (Scenario 02)

| Index | Veld | Waarde |
|-------|------|--------|
| `fields[1]` | matching_number | `"0016"` (alleen getal) |
| `fields[2]` | student_name | `"Emma"` |
| `fields[3]` | Datum 1 | Date object |
| `fields[5-17]` | Checkboxes datum 1 | true/false (13 tijdsloten) |
| `fields[18]` | Datum 2 | Date object |
| ... | ... | ... |

---

## Webhook URLs

| Scenario | Webhook URL |
|----------|-------------|
| Scenario 02 (Tally Form 1) | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` |
| Scenario 3b (GAS Picker) | `https://hook.eu1.make.com/jgrnq4k8yob8txh5x0jn2ojxx94awnwr` |
| Scenario 4 (Tally Form 3) | `https://hook.eu1.make.com/1aa2q2bnkvxodps6errjs6pxs3j4v4d9` |

---

## Dataconventie Telefoonnummers

> ⚠️ **Kritiek** — verkeerd formaat leidt tot HTTP 100 "Invalid parameter" bij 360dialog

| ✅ Correct | ❌ Incorrect |
|-----------|------------|
| `31630892143` | `0630892143` (lokaal) |
| `31630892143` | `+31630892143` (met +) |
| `15557590811` | `+1 555-759-0811` (met spaties/+) |

**Geldt voor alle velden:** `Phone` (Account), `AccountPhone`, `ParentSPhone__c`

---

## Tally Webhook Instructie

> ⚠️ Verkeerde volgorde leidt tot mislukte webhook ontvangst

1. Open het scenario in Make.com
2. Klik **Run once**
3. Wacht op **"Waiting for data"** melding
4. Vul dan pas het Tally formulier in

**Webhook logs bekijken:**
- Ga **uit** het scenario (sluit het scenario)
- Klik links in het menu op **Webhooks**
- Klik op **Logs** bij de naam van de webhook
- ❌ Niet via de scenario **History tab**

---

## Make.com Formule Regels

| Regel | Detail |
|-------|--------|
| `replace()` in JSON | ❌ Conflicteert met JSON aanhalingstekens → gebruik Set Variable module |
| `switch()` in JSON | ✅ Gebruik backticks: `` `Mathematics A` `` |
| Backticks in `replace()` | ❌ Geeft "Module references non-existing module NaN" error |
| `and()` functie | ❌ Bestaat niet in Make.com → gebruik `if(x; if(y; ...))` |
| `encodeURL()` | ✅ Gebruik voor strings met spaties in URL parameters |
| `&` in JSON body URL | ✅ Literal `&` werken in JSON body — gebruik niet `%26` |
| Tally datum in JSON | Altijd aanhalingstekens: `"3": "{{1.data.fields[3].value}}"` |
| Checkbox in JSON | Altijd `if()`-wrapper: `{{if(x; true; false)}}` |
| Lange formules (>13 if) | ❌ Corrupt bij opslaan → gebruik Google Apps Script |

---

## Meta Business Verificatie (To-do)

**Doel:** "Bright Panda Bijles" als naam zichtbaar bij ontvanger (in plaats van +1 nummer)
**Status:** Nog te doen — lage urgentie

| Stap | Detail |
|------|--------|
| Locatie | Meta Business Manager → Settings → Security center → Start verification |
| KvK nummer | 84707577 |
| Kosten | Gratis |
| Doorlooptijd | 2-7 werkdagen |
