# Scenario 10 — Student New Registration → MailerLite + WhatsApp Alert

**Make Scenario ID:** 4969006 (eu1.make.com)  
**Laatste update:** 11 mei 2026  
**Status:** ✅ Actief

---

## Doel

Wordt real-time getriggerd via een Salesforce Record-Triggered Flow zodra een nieuw student Account wordt aangemaakt. Vertaalt het vak naar Nederlands, maakt/update de ouder als subscriber in MailerLite, en stuurt intern een WhatsApp alert en Slack bericht naar Bright Panda.

> ⚠️ **Let op:** De trigger is gewijzigd van Salesforce Watch Records (polling elke 20 minuten) naar een real-time Salesforce Flow webhook. Zie [salesforce-flow-webhook-integratie.md](salesforce-flow-webhook-integratie.md) voor de volledige Salesforce Flow configuratie.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook (module 10) |
| Webhook naam | Salesforce New Student Registration |
| Webhook URL | `https://hook.eu1.make.com/g6jv8nryuh3nffn3l7h2xpfcwn5b14ii` |
| Getriggerd door | Salesforce Record-Triggered Flow (New Student Registration Webhook) |
| Timing | Real-time, zodra nieuw student Account wordt aangemaakt |

---

## Module Volgorde

```
[10] Custom Webhook (trigger — Salesforce New Student Registration)
        ↓
[14] Webhook Response → {"accepted": true} + Content-Type: application/json
        ↓
     Filter: Heeft vakken — {{10.Subjects__c}} is not empty
        ↓
[4]  HTTP GET → Google Apps Script (vakvertaling)
        ↓
[3]  MailerLite → Create/Update Subscriber
        ↓
[6]  HTTP POST → 360dialog WhatsApp (Raouf — 31630892143)
        ↓
[7]  HTTP POST → 360dialog WhatsApp (Yasin — 31623325599)
        ↓
[8]  HTTP POST → 360dialog WhatsApp (Intern — 31613689666)
        ↓
[9]  Slack → #nieuwe-aanmeldingen
```

---

## Modules Detail

### Module 10 — Custom Webhook

- **Webhook naam:** Salesforce New Student Registration
- **Webhook URL:** `https://hook.eu1.make.com/g6jv8nryuh3nffn3l7h2xpfcwn5b14ii`
- **Data structuur (velden):**

| Veld | Type |
|------|------|
| `FirstName` | text |
| `LastName` | text |
| `PersonEmail` | text |
| `ParentSEmail__c` | text |
| `ParentSName__c` | text |
| `ParentSPhone__c` | text |
| `Subjects__c` | text |
| `EducationLevel__c` | text |
| `SchoolYear__c` | text |
| `PersonMailingCity` | text |
| `PersonMailingPostalCode` | text |
| `ReferredToBPVia__c` | text |
| `Id` | text |

---

### Module 14 — Webhook Response

> ⚠️ **Verplicht direct na module 10.** Salesforce wacht op deze response. Zonder JSON Content-Type faalt de Salesforce Flow.

- **Status:** `200`
- **Body:** `{"accepted": true}`
- **Custom Headers:** `Content-Type` = `application/json`

---

### Filter — Heeft vakken

- **Condition:** `{{10.Subjects__c}}` is not empty

---

### Module 4 — HTTP GET → Google Apps Script (Vakvertaling)

- **Method:** GET
- **URL:** `https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec?subject={{encodeURL(10.Subjects__c)}}`
- **Parse response:** NO
- **Output:** `{{4.data}}` — kommagescheiden Nederlandse vaknamen

---

### Module 3 — MailerLite Create/Update Subscriber

- **Email address:** `{{10.ParentSEmail__c}}`
- **Name:** `{{10.ParentSName__c}}`
- **Phone:** `{{10.ParentSPhone__c}}`
- **City:** `{{10.PersonMailingCity}}`
- **Group IDs:** Nieuwe Proefles Aanmelding (182829161192097282)

**Custom fields:**

| Custom field | Waarde |
|-------------|--------|
| `student_name` | `{{10.FirstName}} {{10.LastName}}` |
| `subjects` | `{{4.data}}` |
| `school_year` | `{{10.SchoolYear__c}}` |
| `referred_by` | `{{10.ReferredToBPVia__c}}` |
| `has_trial_lesson` | `false` |
| `is_active_client` | `false` |
| `total_matchings` | `0` |

---

### Modules 6, 7, 8 — Intern WhatsApp Alerts

**Template:** `internal_alert_new_registration`

| Module | Naar | Nummer |
|--------|------|--------|
| 6 | Raouf | `31630892143` |
| 7 | Yasin | `31623325599` |
| 8 | Intern | `31613689666` |

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
        {"type": "text", "text": "{{10.FirstName}}"},
        {"type": "text", "text": "{{4.data}}"},
        {"type": "text", "text": "{{10.EducationLevel__c}}"},
        {"type": "text", "text": "{{10.SchoolYear__c}}"},
        {"type": "text", "text": "{{10.ParentSName__c}}"},
        {"type": "text", "text": "{{10.ParentSPhone__c}}"},
        {"type": "text", "text": "{{10.ParentSEmail__c}}"},
        {"type": "text", "text": "{{10.PersonMailingCity}}"},
        {"type": "text", "text": "{{10.PersonMailingPostalCode}}"}
      ]
    }]
  }
}
```

---

### Module 9 — Slack → #nieuwe-aanmeldingen

```
🆕 Nieuwe aanmelding
Leerling: {{10.FirstName}} {{10.LastName}}
Vak: {{4.data}}
Niveau: {{10.EducationLevel__c}} — Jaar {{10.SchoolYear__c}}
Ouder: {{10.ParentSName__c}}
Tel: {{10.ParentSPhone__c}}
Email: {{10.ParentSEmail__c}}
Stad: {{10.PersonMailingCity}}
```

---

## Bekende Fouten & Fixes

| Fout | Oorzaak | Fix |
|------|---------|-----|
| `MakeWebhookNoAuth might not exist` | Permission Set niet toegewezen | Setup → Permission Sets → Make Webhook Access → gebruiker toevoegen |
| `Expected application/json, got text/plain` | Make.com stuurt text/plain terug | Webhook Response module toevoegen direct na trigger met Content-Type: application/json |
| `There is no scenario listening` | Scenario inactief of webhook niet als trigger ingesteld | Scenario activeren, webhook als eerste module instellen |
| `[422] subscriber is not active` | Ouder bestaat al in MailerLite met status unsubscribed | Geen actie nodig bij echte aanmeldingen, treedt alleen op bij hergebruikte test-emailadressen |

---

## Gerelateerde documenten

| Document | Beschrijving |
|----------|-------------|
| [salesforce-flow-webhook-integratie.md](salesforce-flow-webhook-integratie.md) | Volledige Salesforce Flow + credentials configuratie |
| [MailerLite inrichting](mailerlite.md) | Groepen, custom fields, automation, welkomstmail |
| [Google Apps Script](google-apps-script.md) | Vakvertaling script |
| [Gedeelde configuratie](gedeelde-configuratie.md) | MailerLite connectie, API credentials |
