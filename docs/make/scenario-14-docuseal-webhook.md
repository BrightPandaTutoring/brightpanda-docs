# Scenario 14 — DocuSeal Contract Signed Webhook

**Laatste update:** 19 april 2026
**Status:** ✅ Werkend — Aan
**Scenario ID:** 5133318

---

## Doel

Ontvangt automatisch een webhook van DocuSeal zodra een docent het contract heeft ondertekend. Zoekt het bijbehorende Teacher Account op in Salesforce via email, zet de lifecycle stage op `Pending Onboarding`, slaat de URL van de ondertekende PDF op in `Contract_URL__c`, en voegt de docent toe aan de juiste MailerLite groep.

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
[3]  HTTP → GET signed PDF (via documents[].url uit payload)
        ↓
[5]  Salesforce → Update a Record (lifecycle + datum + Contract_URL__c)
        ↓
[6]  MailerLite → Create/Update Subscriber + groep "Pending Onboarding"
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

## Module 5 — Salesforce Update Record

- **Record ID:** `{{2.Id}}`
- `Lifecycle_Stage__c` = `Pending Onboarding`
- `Pending_Onboarding_Date__c` = vandaag
- **`Contract_URL__c` = `{{1.data.documents[].url}}`** ← toegevoegd 19 april 2026

---

## Module 6 — MailerLite

- **Actie:** Create/Update Subscriber
- **Email:** `{{1.submitters[].email}}`
- **Groep:** `Pending Onboarding`

---

## History van wijzigingen

### 19 april 2026
- **Module 5 uitgebreid** met `Contract_URL__c` → `{{1.data.documents[].url}}`
- **Module 9 verwijderd** (`salesforce:makeApiCall` voor ContentVersion upload) — gaf [404] error ook met absolute URL
- **Modules 11 en 12 verwijderd** (tijdelijke HTTP modules voor OAuth token + ContentVersion via HTTP) — zelfde root cause
- Scenario is nu clean: Webhook → SOQL → HTTP GET PDF → Update Record → MailerLite

### Waarom geen PDF upload naar Salesforce?
Poging gedaan om de ondertekende PDF op te slaan als ContentVersion (bestand op het Account record):
- `salesforce:makeApiCall` in Make.com voegt de instance URL **niet** automatisch toe → altijd absolute URL gebruiken
- Ook met absolute URL (`https://brightpanda.my.salesforce.com/services/data/v62.0/sobjects/ContentVersion`) → [404] error
- Root cause: ontbrekende OAuth scopes in Make.com's gedeelde Salesforce app
- Eigen Salesforce Connected App aanmaken: mislukt door **Insufficient Privileges** op huidige licentie

**Tijdelijke oplossing:** URL naar de DocuSeal PDF opslaan in `Contract_URL__c`. Voor een permanente oplossing is een Salesforce licentie-upgrade nodig of een alternatieve opslaglocatie (Google Drive, Dropbox, S3).

---

## DocuSeal Configuratie

| Instelling | Waarde |
|-----------|--------|
| **Plan** | EU |
| **API Endpoint** | `https://api.docuseal.eu/submissions` |
| **API Key** | `kF6DXM8V8AEJcRhXshwE1RxdvarDx9NHwuYjd9FnZz3` |
| **Template ID** | `485548` |
| **Prijs** | $0.20 per contract (via Make.com integratie) |
| **Velden** | Readonly (docent tekent alleen) |
| **Reminders** | 3, 7 en 15 dagen |
| **Email templates** | signature request, reminder, document copy, completed notification |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 13](scenario-13-docent-lifecycle.md) | Verstuurt het contract bij `Contracting` lifecycle stage |
| Scenario 15 | Tally reminder voor Pending Onboarding docenten |
| Scenario 17 | Auto On-boarded zodra alle 3 velden ingevuld zijn |
| Scenario 19 | Documentation reminder voor Pending Onboarding docenten |
