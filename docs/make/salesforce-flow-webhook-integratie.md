# Salesforce Flow → Make.com Webhook Integratie

## Overzicht

Scenario 10 wordt getriggerd via een real-time Salesforce Record-Triggered Flow zodra een nieuw student Account wordt aangemaakt. Dit vervangt de oude polling-trigger (Watch Records, elke 20 minuten).

---

## Architectuur

```
Nieuw Student Account in Salesforce
        ↓
Record-Triggered Flow (New Student Registration Webhook - V4)
        ↓
Set Request Body (Assignment)
        ↓
HTTP Callout → Make.com Webhook URL
        ↓
Scenario 10 triggert direct
```

---

## Salesforce Flow configuratie

**Flow naam:** New Student Registration Webhook  
**Type:** Record-Triggered Flow  
**Object:** Account  
**Trigger:** A record is created  
**Condition:** RecordTypeId = `012KB000000ojZGYAY` (Student)  
**Optimize for:** Actions and Related Records  
**Asynchronous Path:** Aan (verplicht voor externe callouts)

### Set Request Body (Assignment)

Vult de `RequestBody2` variabele (Apex-Defined, type `ExternalService__MakeNewStudentWebhook2_SendNewStudenttoMake`) met de volgende velden:

| Variable | Waarde |
|---|---|
| RequestBody2 > Id | `{!$Record.Id}` |
| RequestBody2 > FirstName | `{!$Record.FirstName}` |
| RequestBody2 > LastName | `{!$Record.LastName}` |
| RequestBody2 > PersonEmail | `{!$Record.PersonEmail}` |
| RequestBody2 > ParentSEmail__c | `{!$Record.ParentSEmail__c}` |
| RequestBody2 > ParentSName__c | `{!$Record.ParentSName__c}` |
| RequestBody2 > ParentSPhone__c | `{!$Record.ParentSPhone__c}` |
| RequestBody2 > Subjects__c | `{!$Record.Subjects__c}` |
| RequestBody2 > EducationLevel__c | `{!$Record.EducationLevel__c}` |
| RequestBody2 > SchoolYear__c | `{!$Record.SchoolYear__c}` |
| RequestBody2 > PersonMailingCity | `{!$Record.PersonMailingCity}` |
| RequestBody2 > PersonMailingPostalCode | `{!$Record.PersonMailingPostalCode}` |
| RequestBody2 > ReferredToBPVia__c | `{!$Record.ReferredToBPVia__c}` |

### HTTP Callout Action

**External Service:** MakeNewStudentWebhook2  
**Operation:** Send New Student to Make  
**Method:** POST  
**URL:** `https://hook.eu1.make.com/g6jv8nryuh3nffn3l7h2xpfcwn5b14ii`  
**Transaction Control:** Always continue in current transaction

---

## Salesforce Setup configuratie

### External Credential
- **Name:** MakeWebhookNoAuth
- **Authentication Protocol:** No Authentication
- **Principal:** No Auth (Named Principal, Configured)

### Named Credential
- **Name:** MakeNewStudentWebhook
- **URL:** `https://hook.eu1.make.com`
- **External Credential:** MakeWebhookNoAuth
- **Enabled for Callouts:** Aan
- **Generate Authorization Header:** Uit
- **Allow Formulas in HTTP Body:** Aan

### External Service
- **Name:** MakeNewStudentWebhook2
- **Named Credential:** MakeNewStudentWebhook
- **OpenAPI schema:** zie onderaan dit document

### Permission Set
- **Name:** Make Webhook Access
- **External Credential Principal Access:** MakeWebhookNoAuth - No Auth
- **Toegewezen aan:** Raouf Angudi

---

## Make.com Scenario 10 configuratie

**Trigger:** Custom Webhook (module 10) — Salesforce New Student Registration  
**Webhook URL:** `https://hook.eu1.make.com/g6jv8nryuh3nffn3l7h2xpfcwn5b14ii`

### Module volgorde

1. **Module 10** — Custom Webhook (trigger)
2. **Module 14** — Webhook Response (direct na module 10) → geeft JSON response terug aan Salesforce
3. **Filter** — Heeft vakken: `{{10.Subjects__c}}` is not empty
4. **Module 4** — HTTP GET → Google Apps Script vakken vertaling
5. **Module 3** — MailerLite → Create/Update Subscriber
6. **Module 6** — WhatsApp → Raouf (31630892143)
7. **Module 7** — WhatsApp → Yasin (31623325599)
8. **Module 8** — WhatsApp → Intern (31613689666)
9. **Module 9** — Slack → #nieuwe-aanmeldingen

### Webhook Response (module 14)

Status: `200`  
Body: `{"accepted": true}`  
Custom Headers: `Content-Type` = `application/json`

> **Belangrijk:** De Webhook Response module moet direct na de Custom Webhook trigger staan. Salesforce wacht op deze response — als die te laat komt of de verkeerde Content-Type heeft, faalt de Salesforce Flow.

---

## Veelvoorkomende fouten en oplossingen

### `MakeWebhookNoAuth might not exist`
**Oorzaak:** De Permission Set is niet toegewezen aan de gebruiker.  
**Oplossing:** Setup → Permission Sets → Make Webhook Access → Manage Assignments → voeg gebruiker toe.

### `Expected application/json, got text/plain`
**Oorzaak:** Make.com stuurt standaard `text/plain: Accepted` terug. Salesforce verwacht JSON.  
**Oplossing:** Voeg een Webhook Response module toe direct na de Custom Webhook trigger met `Content-Type: application/json`.

### `There is no scenario listening for this webhook`
**Oorzaak:** Scenario 10 staat niet actief of de Custom Webhook module is niet de trigger.  
**Oplossing:** Zet scenario actief en zorg dat de Custom Webhook module de eerste module is in de flow.

### `body = {!RequestBody2} (null)`
**Oorzaak:** De RequestBody2 variabele is leeg of incompatibel met de External Service.  
**Oplossing:** Open de Set Request Body assignment → klik Done → Save As New Version → Activate.

### `[422] subscriber is not active and cannot be imported`
**Oorzaak:** De ouder is al aanwezig in MailerLite met status unsubscribed/bounced.  
**Oplossing:** Geen actie nodig bij echte aanmeldingen. Dit treedt alleen op bij hergebruikte test-emailadressen.

---

## OpenAPI Schema (MakeNewStudentWebhook2)

```json
{
  "openapi": "3.0.1",
  "info": {"title": "MakeNewStudentWebhook2", "description": ""},
  "paths": {
    "/g6jv8nryuh3nffn3l7h2xpfcwn5b14ii": {
      "post": {
        "operationId": "Send New Student to Make",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "FirstName": {"type": "string"},
                  "LastName": {"type": "string"},
                  "PersonEmail": {"type": "string"},
                  "EducationLevel__c": {"type": "string"},
                  "ParentSPhone__c": {"type": "string"},
                  "ParentSEmail__c": {"type": "string"},
                  "ParentSName__c": {"type": "string"},
                  "SchoolYear__c": {"type": "string"},
                  "PersonMailingPostalCode": {"type": "string"},
                  "PersonMailingCity": {"type": "string"},
                  "Id": {"type": "string"},
                  "ReferredToBPVia__c": {"type": "string"},
                  "Subjects__c": {"type": "string"}
                }
              }
            }
          },
          "required": true
        },
        "responses": {
          "2XX": {
            "description": "",
            "content": {
              "text/plain": {
                "schema": {"type": "string"}
              }
            }
          }
        }
      }
    }
  }
}
```
