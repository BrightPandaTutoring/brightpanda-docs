# Salesforce Flow → Make.com Webhook Integratie

## Overzicht

Dit document beschrijft het patroon voor het triggeren van Make.com scenario's via een Salesforce Record-Triggered Flow. Dit patroon vervangt polling-triggers en zorgt voor event-driven automatisering.

Geïmplementeerd voor:
- **Scenario 10** — Nieuwe student aanmelding (direct bij aanmaken)
- **Scenario 11** — Post-proefles flow (70 minuten na Trial_Lesson_Date__c)

---

## Scenario 10 — Nieuwe Student Aanmelding

### Architectuur

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

### Salesforce Flow configuratie

**Flow naam:** New Student Registration Webhook
**Type:** Record-Triggered Flow
**Object:** Account
**Trigger:** A record is created
**Condition:** RecordTypeId = `012KB000000ojZGYAY` (Student)
**Optimize for:** Actions and Related Records
**Asynchronous Path:** Aan (verplicht voor externe callouts)

#### Set Request Body (Assignment)

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

#### HTTP Callout Action

**External Service:** MakeNewStudentWebhook2
**Operation:** Send New Student to Make
**Method:** POST
**URL:** `https://hook.eu1.make.com/g6jv8nryuh3nffn3l7h2xpfcwn5b14ii`

---

## Scenario 11 — Post-Proefles Flow

### Architectuur

```
Status wijzigt naar Trial Lesson Scheduled in Salesforce
        ↓
Record-Triggered Flow (Post-Proefles Flow Trigger)
        ↓
Wacht 70 minuten na Trial_Lesson_Date__c
        ↓
Vul Request Body (Assignment)
        ↓
HTTP Callout → Make.com Webhook
        ↓
Scenario 11 triggert direct
```

### Salesforce Flow configuratie

**Flow naam:** Post-Proefles Flow Trigger
**Type:** Record-Triggered Flow
**Object:** Student Teacher Matching
**Trigger:** A record is created or updated
**Condition:** `Trial_Lesson_Status__c` Equals `Trial Lesson Scheduled`
**When to Run:** Only when a record is updated to meet the condition requirements
**Optimize for:** Actions and Related Records

#### Scheduled Path: 70 minuten na proefles

| Instelling | Waarde |
|---|---|
| Time Source | Student Teacher Matching: Trial Lesson Date |
| Offset Number | 70 |
| Offset Options | Minutes After |

#### Assignment: Vul Request Body

Vult de `RequestBodyPostProefles` variabele (Apex-Defined, type `ExternalService__MakePostProeflesWebhook_SendPostProeflesToMake_IN_body`) met:

| Variable | Waarde |
|---|---|
| RequestBodyPostProefles > Id | `{!$Record.Id}` |
| RequestBodyPostProefles > Student__c | `{!$Record.Student__c}` |
| RequestBodyPostProefles > Teacher__c | `{!$Record.Teacher__c}` |
| RequestBodyPostProefles > Trial_Lesson_Date__c | `{!$Record.Trial_Lesson_Date__c}` |
| RequestBodyPostProefles > Trial_Lesson_Status__c | `{!$Record.Trial_Lesson_Status__c}` |

#### HTTP Callout Action

**External Service:** MakePostProeflesWebhook
**Operation:** SendPostProeflesToMake
**Body:** `RequestBodyPostProefles`

---

## Salesforce Setup configuratie (gedeeld)

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

### External Services

| Naam | Named Credential | Gebruikt voor |
|---|---|---|
| MakeNewStudentWebhook2 | MakeNewStudentWebhook | Scenario 10 |
| MakePostProeflesWebhook | MakeNewStudentWebhook | Scenario 11 |

### Permission Set
- **Name:** Make Webhook Access
- **External Credential Principal Access:** MakeWebhookNoAuth - No Auth
- **Toegewezen aan:** Raouf Angudi

---

## Make.com configuratie (patroon)

Voor beide scenario's geldt:

1. **Trigger:** Custom Webhook module
2. **Direct na trigger:** Webhook Response module met `{"accepted": true}` en `Content-Type: application/json`

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
**Oorzaak:** Scenario staat niet actief of de Custom Webhook module is niet de trigger.
**Oplossing:** Zet scenario actief en zorg dat de Custom Webhook module de eerste module is.

### `body = {!RequestBody} (null)`
**Oorzaak:** De RequestBody variabele is leeg of incompatibel met de External Service.
**Oplossing:** Open de Assignment → klik Done → Save As New Version → Activate.

### `[422] subscriber is not active and cannot be imported`
**Oorzaak:** De ouder is al aanwezig in MailerLite met status unsubscribed/bounced.
**Oplossing:** Geen actie nodig bij echte aanmeldingen. Dit treedt alleen op bij hergebruikte test-emailadressen.

---

## OpenAPI Schema — MakeNewStudentWebhook2 (Scenario 10)

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
          "2XX": {"description": "", "content": {"text/plain": {"schema": {"type": "string"}}}}
        }
      }
    }
  }
}
```

## OpenAPI Schema — MakePostProeflesWebhook (Scenario 11)

```json
{
  "openapi": "3.0.1",
  "info": {"title": "MakePostProeflesWebhook", "description": ""},
  "servers": [{"url": "https://hook.eu1.make.com"}],
  "paths": {
    "/pk888u999ewnnksom71zqatslfyhow8z": {
      "post": {
        "operationId": "SendPostProeflesToMake",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "Id": {"type": "string"},
                  "Student__c": {"type": "string"},
                  "Teacher__c": {"type": "string"},
                  "Trial_Lesson_Date__c": {"type": "string"},
                  "Trial_Lesson_Status__c": {"type": "string"}
                }
              }
            }
          },
          "required": true
        },
        "responses": {
          "2XX": {"description": "", "content": {"text/plain": {"schema": {"type": "string"}}}}
        }
      }
    }
  }
}
```
