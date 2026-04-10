# Scenario 10 — Salesforce to MailerLite New Registration

**Make naam:** Salesforce to MailerLite New Registration
**Make Scenario ID:** 4969006 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Live, interval 7 minuten

---

## Doel

Detecteert automatisch wanneer een nieuwe leerling (Person Account) aangemaakt wordt in Salesforce, vertaalt het vak naar Nederlands, en maakt/update de ouder als subscriber in MailerLite met alle relevante gegevens. De welkomstmail wordt automatisch getriggerd door de MailerLite automation.

**Probleem dat het oplost:** Ouders moesten handmatig worden toegevoegd aan de emaillijst na een nieuwe aanmelding.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Salesforce Watch Records |
| Object | Account |
| Watch Records by | Created Time (From now on) |
| Interval | Elke 7 minuten |
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
```

> Volgorde: 1 → 4 → 3

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
| Email ouder | `1.Parent_s_Email__c` | MailerLite email address |
| Naam ouder | `1.Parent_s_Name__c` | MailerLite name + custom field |
| Telefoon ouder | `1.Parent_s_Phone__c` | MailerLite phone |
| Stad | `1.MailingCity` | MailerLite city |
| Vak(ken) | `1.Subject_s__c` | → vakvertaling → `subjects` custom field |
| Niveau | `1.Education_Level__c` | → `education_level` custom field |
| Leerjaar | `1.School_Year__c` | → `school_year` custom field |
| Verwezen via | `1.Referred_to_BP_Via__c` | → `referred_by` custom field |
| Geslachtsvoorkeur | `1.Gender_Preference__c` | → `gender_preference` custom field |
| Opmerkingen | `1.Comments_From_Web_Form__c` | → `comments` custom field |
| Aanmaakdatum | `1.CreatedDate` | → `registration_date` custom field |
| Pro aanmelding | `1.Pro_Student_sign_up__c` | → `is_pro` custom field |

### Module 4 — HTTP GET → Google Apps Script (Vakvertaling)

- **URL:** `https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec?subject={{encodeURL(1.Subject_s__c)}}`
- **Method:** GET
- **Parse response:** NO
- **Output:** `{{4.data}}` — kommagescheiden Nederlandse vaknamen, bijv. `"Wiskunde A, Biologie"`

> `Subject_s__c` bevat puntkomma-gescheiden Engelse vaknamen (bijv. `"Mathematics A;Biology"`). Het script splitst deze, vertaalt elk vak apart, en retourneert een kommagescheiden Nederlandse string.

### Module 3 — MailerLite Create/Update Subscriber

- **Connectie:** MailerLite Bright Panda
- **Email address:** `{{1.Parent_s_Email__c}}`
- **Name:** `{{1.Parent_s_Name__c}}`
- **Phone:** `{{1.Parent_s_Phone__c}}`
- **City:** `{{1.MailingCity}}`
- **Group IDs:** Nieuwe Proefles Aanmelding
- **Status:** leeg (default = Active)

**Custom fields:**

| Custom field tag | Waarde | Bron |
|-----------------|--------|------|
| `student_name` | `{{1.Name}}` | Account naam (leerling) |
| `subjects` | `{{4.data}}` | Vakvertaling output |
| `education_level` | `{{1.Education_Level__c}}` | Niveau |
| `school_year` | `{{1.School_Year__c}}` | Leerjaar |
| `referred_by` | `{{1.Referred_to_BP_Via__c}}` | Verwezen via |
| `gender_preference` | `{{1.Gender_Preference__c}}` | Geslachtsvoorkeur |
| `comments` | `{{1.Comments_From_Web_Form__c}}` | Opmerkingen |
| `registration_date` | `{{1.CreatedDate}}` | Aanmaakdatum |
| `has_trial_lesson` | `false` | Altijd false bij aanmelden |
| `is_active_client` | `false` | Altijd false bij aanmelden |
| `total_matchings` | `0` | Altijd 0 bij aanmelden |
| `is_pro` | `{{1.Pro_Student_sign_up__c}}` | Pro aanmelding checkbox |

> **Waarom Create/Update (upsert)?** Als een ouder meerdere kinderen aanmeldt, wordt de subscriber bijgewerkt i.p.v. dubbel aangemaakt. MailerLite gebruikt email als unieke sleutel.

---

## Wat er daarna automatisch gebeurt

Na aanmaken subscriber in MailerLite:
1. MailerLite detecteert: subscriber joined group "Nieuwe Proefles Aanmelding"
2. Automation "Welkomstmail Proefles Aanmelding" wordt getriggerd
3. Welkomstmail wordt verstuurd naar ouder

> Zie [MailerLite inrichting](mailerlite.md) voor de volledige automation setup.

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| Vakvertaling werkte niet op meerdere vakken | Script behandelde de hele string als één sleutel | Script aangepast: splitst op `;`, vertaalt elk vak apart, retourneert kommagescheiden string |
| MailerLite HTML editor sloeg niet op | Growing Business plan heeft geen custom HTML editor | HTML via drag & drop content block in email editor — werkt op Growing Business |
| Docenten worden ook verwerkt | Alle Person Accounts triggeren de watch | Filter op RecordTypeId ≠ Teacher Record Type ID toegevoegd |

---

## To-do

| Actie | Detail |
|-------|--------|
| Intern WhatsApp alert bij nieuwe aanmelding | Extra module toevoegen aan dit scenario — WhatsApp naar intern nummer bij elke nieuwe registratie |

---

## Gerelateerde documenten

| Document | Beschrijving |
|----------|-------------|
| [MailerLite inrichting](mailerlite.md) | Groepen, custom fields, automation, welkomstmail |
| [Google Apps Script](google-apps-script.md) | Script 1 — vakvertaling |
| [Gedeelde configuratie](gedeelde-configuratie.md) | MailerLite connectie, API credentials |
