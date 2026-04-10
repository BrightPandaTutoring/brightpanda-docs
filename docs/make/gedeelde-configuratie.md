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
| **Header: D360-API-KEY** | `xl6Aj3Gs66I40LQI7C6GbjIxAK` |
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
| **URL** | brightpanda.lightning.force.com |

### Salesforce Record Structuur

| Entiteit | Object type | Relevante velden |
|----------|-------------|-----------------|
| Docenten | **Account** | `Phone` (= Business Phone in Make.com), `FirstName` |
| Studenten | **Account** | `FirstName`, `Name`, `ParentsName__c`, `ParentSPhone__c` |
| Ouders | Custom velden op Student Account | `ParentsName__c`, `ParentSPhone__c` |

> **Ouder contactgegevens** zitten als custom velden op het **Student Account** (niet als Contact record). Gebruik `{{X.ParentsName__c}}` en `{{X.ParentSPhone__c}}` direct na een Get a Record op het Student Account.

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
| `Teacher_Reminder_Sent__c` | Checkbox | true na versturen 24u reminder docent |
| `Teacher_Escalation_Sent__c` | Checkbox | true na versturen 48u escalatie docent |
| `Parent_Reminder_Sent__c` | Checkbox | true na versturen 24u reminder ouder |
| `Parent_Escalation_Sent__c` | Checkbox | true na versturen 48u escalatie ouder |

### Trial_Lesson_Status__c Picklist Waarden

| Waarde | Trigger |
|--------|---------|
| `Teacher Invited` | Scenario 01 — na versturen WhatsApp docent |
| `Availability Received` | — (handmatig of toekomstig) |
| `Parent Invited` | Scenario 02 — na versturen picker URL naar ouder |
| `Trial Lesson Scheduled` | Scenario 3b Pad A — na bevestiging tijdslot |
| `Availability Conflict` | Scenario 3b Pad B — geen tijdslot past |
| `Trial Lesson Completed` | Handmatig |
| `No Show` | Handmatig |

---

## Google Apps Script URLs

| Script | URL | Methode | Gebruikt in |
|--------|-----|---------|------------|
| **Script 1 — Vakvertaling** | `https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec` | GET | Scenario 01 module 10 |
| **Script 2 — Tijdslotverwerking** | `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec` | POST | Scenario 02 module 31 |
| **Script 3 — Picker v10** | `https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec` | GET (HTML) | Scenario 02 → ouder klikt → POST naar Scenario 3b |

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
| Intern escalatie WhatsApp | `31613689666` | Escalaties Scenario 03 |
| Intern telefoon | 071-3031901 | Vermeld in template disclaimer |
| Intern WhatsApp (zichtbaar) | +31613689666 | Vermeld in template disclaimer |

---

## Tally Formulieren

| Formulier | URL | Webhook URL | Doel |
|-----------|-----|-------------|------|
| Form 1 (docent beschikbaarheid) | `https://tally.so/r/2Ekaq9` | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` | Docent vult beschikbaarheid in |
| Form 2 (fallback ouder) | `https://tally.so/r/WOozov` | — | Niet meer primair gebruikt — fallback bij no_match knop op picker pagina |

> Tally Form 2 is **vervangen** door de Google Apps Script picker pagina (Script 3). Betere UX: ouder klikt op tijdslot in plaats van getal typen.

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
