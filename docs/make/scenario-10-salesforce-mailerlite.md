# Scenario 10 — Salesforce to MailerLite New Registration

**Make naam:** Salesforce to MailerLite New Registration
**Make Scenario ID:** 4969006 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** ⚠️ In debug — automatisch gedeactiveerd door Make.com na herhaalde fouten

---

## Doel

Detecteert automatisch wanneer een nieuwe leerling (Person Account) aangemaakt wordt in Salesforce, vertaalt het vak naar Nederlands, maakt/update de ouder als subscriber in MailerLite, en stuurt een intern WhatsApp alert naar Bright Panda.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Salesforce Watch Records |
| Object | Account |
| Watch Records by | Created Time (From now on) |
| Interval | **Elke 20 minuten** (was 7 min — te veel credits verbruik) |
| Limit | 10 records per run |

---

## Filter (tussen module 1 en module 3)

**Label:** Alleen Person Accounts (geen docenten)

| # | Veld | Operator | Waarde |
|---|------|----------|--------|
| 1 | `IsPersonAccount` | Equal to (case insensitive) | `true` |
| 2 | `RecordTypeId` | Not equal to (case insensitive) | `012KB000000ojZLYAY` |

> Conditie 2 sluit docenten uit op basis van Record Type ID. Alleen student Person Accounts worden verwerkt.

---

## Module Volgorde

```
[1]  Salesforce → Watch Records (Account — nieuwe registraties)
        ↓
     Filter: IsPersonAccount = true AND RecordTypeId ≠ Teacher Record Type
        ↓
[4]  HTTP GET → Google Apps Script (vakvertaling)
        ↓
[3]  MailerLite → Create/Update Subscriber
        ↓
[6]  HTTP POST → 360dialog (internal_alert_new_registration → intern)
        ↓
[7]  HTTP POST → 360dialog (intern Raouf)
        ↓
[8]  HTTP POST → 360dialog (intern Yasin)
```

> Module nummering: 1 → 4 → 3 → 6 → 7 → 8

---

## Modules Detail

### Module 1 — Salesforce Watch Records

- **Object:** Account
- **Watch Records by:** Created Time (From now on)
- **Limit:** 10
- **Output (gebruikte velden):**

| Veld | API naam | Gebruik |
|------|---------|---------|
| Account naam (leerling) | `1.Name` | → `student_name` custom field |
| Email ouder | `1.ParentSEmail__c` | MailerLite email address |
| Naam ouder | `1.ParentsName__c` | MailerLite name |
| Telefoon ouder | `1.ParentSPhone__c` | MailerLite phone |
| Stad | `1.MailingCity` | MailerLite city |
| Postcode | `1.MailingPostalCode` | intern alert |
| Vak(ken) | `1.Subjects__c` | → vakvertaling → `subjects` custom field |
| Niveau | `1.Education_Level__c` | → `education_level` custom field |
| Leerjaar | `1.SchoolYear__c` | → `school_year` custom field (Text) |
| Verwezen via | `1.ReferredToBPVia__c` | → `referred_by` custom field |
| Aanmaakdatum | `1.CreatedDate` | → `registration_date` custom field |
| Pro aanmelding | `1.Pro_Student_sign_up__c` | → `is_pro` custom field |

---

### Module 4 — HTTP GET → Google Apps Script (Vakvertaling)

> ⚠️ **BUG:** Module 4 gebruikte de verkeerde script URL en gaf HTTP 404 "Not Found" terug.

| | URL |
|-|-----|
| **❌ Oude/fout URL** | `https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec` |
| **✅ Correcte URL** | `https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec` |

- **Method:** GET
- **Input:** `?subject={{encodeURL(ifempty(1.Subjects__c; ""))}}`
- **Parse response:** NO
- **Output:** `{{4.data}}` — kommagescheiden Nederlandse vaknamen

> `ifempty(1.Subjects__c; "")` voorkomt crash als Subjects__c leeg is.

---

### Module 3 — MailerLite Create/Update Subscriber

- **Connectie:** MailerLite Bright Panda
- **Email address:** `{{1.ParentSEmail__c}}`
- **Name:** `{{1.ParentsName__c}}`
- **Phone:** `{{1.ParentSPhone__c}}`
- **City:** `{{1.MailingCity}}`
- **Group IDs:** Nieuwe Proefles Aanmelding
- **Status:** leeg (default = Active)

**Custom fields:**

| Custom field tag | Waarde | Bron |
|-----------------|--------|------|
| `{$student_name}` | `{{1.Name}}` | Account naam (leerling) |
| `{$subjects}` | `{{4.data}}` | Vakvertaling output |
| `{$school_year}` | `{{1.SchoolYear__c}}` | Leerjaar (Text type!) |
| `{$referred_by}` | `{{1.ReferredToBPVia__c}}` | Verwezen via |
| `{$registration_date}` | `{{1.CreatedDate}}` | Aanmaakdatum |
| `{$has_trial_lesson}` | `false` | Altijd false bij aanmelden |
| `{$is_active_client}` | `false` | Altijd false bij aanmelden |
| `{$total_matchings}` | `0` | Altijd 0 bij aanmelden |
| `{$is_pro}` | `{{1.Pro_Student_sign_up__c}}` | Pro aanmelding checkbox |

> **Waarom Create/Update (upsert)?** Als een ouder meerdere kinderen aanmeldt, wordt de subscriber bijgewerkt i.p.v. dubbel aangemaakt. MailerLite gebruikt email als unieke sleutel.

> ⚠️ **MailerLite merge tags:** Gebruik **altijd** `{$veldnaam}` (met dollarteken), nooit `{veldnaam}`.

---

### Modules 6, 7, 8 — Intern WhatsApp Alerts

**Template:** `internal_alert_new_registration` (9 params)

| Module | Naar | Nummer |
|--------|------|--------|
| 6 | Zakelijk | `31613689666` |
| 7 | Raouf | `31630892143` |
| 8 | Yasin | `31623325599` |

```json
{
  "messaging_product": "whatsapp",
  "to": "{{NUMMER}}",
  "type": "template",
  "template": {
    "name": "internal_alert_new_registration",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{1.Name}}"},
        {"type": "text", "text": "{{4.data}}"},
        {"type": "text", "text": "{{1.Education_Level__c}}"},
        {"type": "text", "text": "{{1.SchoolYear__c}}"},
        {"type": "text", "text": "{{1.ParentsName__c}}"},
        {"type": "text", "text": "{{1.ParentSPhone__c}}"},
        {"type": "text", "text": "{{1.ParentSEmail__c}}"},
        {"type": "text", "text": "{{1.MailingCity}}"},
        {"type": "text", "text": "{{1.MailingPostalCode}}"}
      ]
    }]
  }
}
```

> ⚠️ **BUG module 6:** Foutmelding `"(#131008) Required parameter is missing. Parameter of type text is missing text value"` — een specifiek record triggerde de module met een lege tekstvariabele. Fix: `ifempty()` fallback toevoegen voor elke parameter die leeg kan zijn.

---

## Bekende Fouten & Fixes

| Fout | Module | Oorzaak | Fix |
|------|--------|---------|-----|
| HTTP 404 "Not Found" | 4 | Verkeerde Google Apps Script URL | URL vervangen door `AKfycbyrP2jVtMak...` + `ifempty` fallback |
| `(#131008) Required parameter is missing` | 6 | Lege tekstvariabele in WhatsApp parameters | `ifempty(VELD; "onbekend")` wrapper toevoegen per parameter |
| Scenario automatisch gedeactiveerd | — | Make.com deactiveerde na herhaalde fouten | Na fixen A en B: scenario heractiveren |
| `school_year` crashte op "Groep 5" | 3 | MailerLite veld was Number type | MailerLite field type gewijzigd van Number → Text; module opnieuw mappen |
| Vakvertaling werkte niet op meerdere vakken | 4 | Script behandelde hele string als één sleutel | Script gebruikt nu split op `;`, vertaalt elk vak apart |
| Docenten worden verwerkt | — | Alle Person Accounts triggeren watch | Filter op RecordTypeId ≠ Teacher Record Type ID |

---

## Wat er daarna automatisch gebeurt

Na aanmaken subscriber in MailerLite:
1. MailerLite detecteert: subscriber joined group "Nieuwe Proefles Aanmelding"
2. Automation "Welkomstmail Proefles Aanmelding" wordt getriggerd
3. Welkomstmail wordt verstuurd naar ouder

> Zie [MailerLite inrichting](mailerlite.md) voor de volledige automation setup.

---

## Gerelateerde documenten

| Document | Beschrijving |
|----------|-------------|
| [MailerLite inrichting](mailerlite.md) | Groepen, custom fields, automation, welkomstmail |
| [Google Apps Script](google-apps-script.md) | Vakvertaling script |
| [Gedeelde configuratie](gedeelde-configuratie.md) | MailerLite connectie, API credentials |
