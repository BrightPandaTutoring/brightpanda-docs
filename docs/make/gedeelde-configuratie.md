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
| `teacher_invitation` | ✅ Goedgekeurd | Scenario 01 + 03 (route 1) | 4 — naam docent, naam student, vak NL, Tally link |
| `parent_timeslot_invitation` | ✅ Goedgekeurd | Scenario 02 + 03 (route 3) | 5 — naam ouder, naam leerling, vak, tijdsloten, Form 2 link |
| `trial_lesson_confirmation` | ✅ Goedgekeurd | Scenario 3b modules 8 + 10 | Parameters ONBEKEND — template tekst ophalen uit 360dialog dashboard |
| Reminder template docent | 🔴 Niet aangemaakt | Scenario 03 (route 1) | — |
| Reminder template ouder | 🔴 Niet aangemaakt | Scenario 03 (route 3) | — |

> ⚠️ **Pas templates alleen aan na volledig testen.** Elke wijziging vereist opnieuw Meta goedkeuring (wachttijd: 2-7 werkdagen).

### Template teksten

> ⚠️ **`trial_lesson_confirmation`** template tekst is ONBEKEND — Raouf opent 360dialog dashboard → Message Templates → deelt de volledige tekst. Parameters kunnen pas bepaald worden na ontvangst.

**Disclaimer tekst (in alle templates):**
> "Dit nummer is alleen voor het inplannen van proeflessen. Voor andere vragen kun je ons bereiken via WhatsApp: +31613689666 of telefoon: 071-3031901."

---

## Salesforce Verbinding

| Instelling | Waarde |
|-----------|--------|
| **Verbindingsnaam in Make.com** | Bright Panda Salesforce |
| **Make.com omgeving** | eu1.make.com |

---

## Google Apps Script

| Instelling | Waarde |
|-----------|--------|
| **Script URL** | `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec` |
| **Versie** | 2 |
| **Functie A** | Bouw tijdsloten string (Scenario 02, module 31) |
| **Functie B** | Vertaal keuzenummer naar datetime (Scenario 3b, module 5) |

Zie [google-apps-script.md](google-apps-script.md) voor volledige documentatie.

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
| Intern escalatie WhatsApp | `31613689666` | Escalaties Scenario 03 + 04 |
| Intern telefoon | 071-3031901 | Vermeld in template disclaimer |
| Intern WhatsApp (zichtbaar) | +31613689666 | Vermeld in template disclaimer |

---

## Tally Formulieren

| Formulier | URL | Webhook URL | Doel |
|-----------|-----|-------------|------|
| Form 1 (docent) | `https://tally.so/r/2Ekaq9` | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` | Docent vult beschikbaarheid in |
| Form 2 (ouder) | `https://tally.so/r/WOozov` | Nog te koppelen | Ouder kiest tijdslot |

---

## Dataconventie Telefoonnummers

> ⚠️ **Kritiek** — verkeerd formaat leidt tot HTTP 100 "Invalid parameter" bij 360dialog

| ✅ Correct | ❌ Incorrect |
|-----------|------------|
| `31630892143` | `0630892143` (lokaal) |
| `31630892143` | `+31630892143` (met +) |
| `15557590811` | `+1 555-759-0811` (met spaties/+) |

**Geldt voor alle velden:** `Phone`, `PersonMobilePhone`, `ParentSPhone__c`

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
| `switch()` in JSON | ✅ Gebruik backticks voor string literals: `` `Mathematics A` `` |
| Backticks in `replace()` | ❌ Geeft "Module references non-existing module NaN" error |
| Formules met `"` in JSON | Altijd vooraf berekenen in Tools → Set Variable module |

**Stelregel:** Als een formule dubbele aanhalingstekens nodig heeft → Set Variable module gebruiken, resultaat als `{{X.variabelenaam}}` in JSON plaatsen.

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
| Resultaat | Naam zichtbaar, geen groen vinkje (dat is alleen voor grote merken) |

---

## Salesforce Custom Velden op Student_Teacher_Matching__c

| API Naam | Type | Beschrijving |
|----------|------|-------------|
| `Trial_Lesson_Date__c` | Date | Definitieve datum + tijd proefles |
| `Trial_Lesson_Status__c` | Picklist | Teacher Invited → Availability Received → Parent Invited → Trial Lesson Scheduled → Trial Lesson Completed → No Show |
| `Tally_Link_Teacher__c` | Text | Volledige Tally Form 1 URL verstuurd naar docent |
| `Available_Timeslots__c` | Long Text Area (10.000) | Genummerde tijdslotenlijst: `1=datum tijd\|2=datum tijd` |
| `Teacher_Reminder_Sent__c` | Checkbox | true na versturen 24u reminder docent |
| `Teacher_Escalation_Sent__c` | Checkbox | true na versturen 48u escalatie docent |
| `Parent_Reminder_Sent__c` | Checkbox | true na versturen 24u reminder ouder |
| `Parent_Escalation_Sent__c` | Checkbox | true na versturen 48u escalatie ouder |
| `Reminder_Sent__c` | Checkbox | Legacy algemene reminder vlag |
