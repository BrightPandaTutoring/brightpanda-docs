# Scenario 14 — DocuSeal Contract Signed Webhook

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Ontvangt automatisch een webhook van DocuSeal zodra een docent het contract heeft ondertekend. Zoekt het bijbehorende Teacher Account op in Salesforce via email, zet de lifecycle stage op `Pending Onboarding`, en voegt de docent toe aan de juiste MailerLite groep.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Afzender | DocuSeal (bij status: completed) |

---

## Module Volgorde

```
[1]  Webhooks → Custom Webhook (DocuSeal completion event)
        ↓
[2]  Salesforce → Search Records SOQL (lookup op email)
        ↓
[3]  Salesforce → Update a Record (Lifecycle_Stage__c = Pending Onboarding)
        ↓
[4]  MailerLite → Create/Update Subscriber + groep "Pending Onboarding"
```

---

## Module 2 — Salesforce SOQL (lookup op email)

```sql
SELECT Id, Name, Email, Lifecycle_Stage__c
FROM Account
WHERE PersonEmail = '{{1.submitters[].email}}'
AND RecordTypeId = '012KB000000ojZLYAY'
```

> DocuSeal stuurt het email adres van de ondertekenaar in de webhook payload. Hiermee zoeken we het Teacher Account op.

---

## Module 3 — Salesforce Update

- **Record ID:** `{{2.Id}}`
- `Lifecycle_Stage__c` = `Pending Onboarding`

---

## Module 4 — MailerLite

- **Actie:** Create/Update Subscriber
- **Email:** `{{1.submitters[].email}}`
- **Groep:** `Pending Onboarding`

---

## DocuSeal Configuratie

| Instelling | Waarde |
|-----------|--------|
| **Plan** | EU |
| **API Endpoint** | `https://api.docuseal.eu/submissions` |
| **API Key** | `kF6DXM8V8AEJcRhXshwE1RxdvarDx9NHwuYjd9FnZz3` |
| **Template ID** | `485548` |
| **Prijs** | $0.20 per contract (via Make.com integratie) |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 13](scenario-13-docent-lifecycle.md) | Verstuurt het contract bij `Contracting` lifecycle stage |
