# Gedeelde Configuratie — Make.com Scenarios

Configuratie die van toepassing is op **alle** Bright Panda Make.com scenarios.

---

## 360dialog HTTP Configuratie

Gebruik deze instellingen in elke HTTP module die naar de 360dialog WhatsApp API stuurt.

| Instelling | Waarde |
|-----------|--------|
| **URL** | `https://waba-v2.360dialog.io/messages` |
| **Method** | POST |
| **Authentication** | No authentication (in Make.com) |
| **Header 1** | `D360-API-KEY: xl6Aj3Gs66I40LQl7C6GbjlxAK` |
| **Header 2** | `Content-Type: application/json` |
| **Body content type** | `application/json` |
| **Body input method** | JSON string |

---

## Salesforce Verbinding

| Instelling | Waarde |
|-----------|--------|
| **Verbindingsnaam in Make.com** | Bright Panda Salesforce |
| **Make.com omgeving** | eu1.make.com |

---

## Dataconventie Telefoonnummers

> ⚠️ **Kritiek** — verkeerde opslag leidt tot HTTP fout 100 "Invalid parameter" bij 360dialog

- Alle nummers opslaan **zonder `+`** en **met landcode**: `31XXXXXXXXX`
- **Nooit** lokaal formaat gebruiken: `0XXXXXXXXX`
- Geldt voor alle velden: `Phone`, `PersonMobilePhone`, `ParentSPhone__c`, etc.

**Voorbeeld:**
```
✅ Correct:   31630892143
❌ Incorrect: 0630892143
❌ Incorrect: +31630892143
```

---

## Tally Webhook Instructie

> ⚠️ Timing is kritiek — verkeerde volgorde leidt tot mislukte webhook ontvangst

**Altijd in deze volgorde:**
1. Open het scenario in Make.com
2. Klik **Run once**
3. Wacht op de melding **"Waiting for data"**
4. Vul dan pas het Tally formulier in
5. Nooit andersom

---

## WhatsApp Templates (360dialog / Meta)

| Template | Status | Gebruik |
|----------|--------|---------|
| `teacher_invitation` | ⏳ In review bij Meta (opnieuw ingediend 8 maart) | Scenario 01 |
| `parent_timeslot_invitation` | ❓ Status onbekend | Scenario 02 |
| Reminder template docent | 🔴 Nog niet aangemaakt | Scenario 03 |
| Reminder template ouder | 🔴 Nog niet aangemaakt | Scenario 03 |

> Templates moeten eerst goedgekeurd zijn door Meta voordat ze live gebruikt kunnen worden.
> Zolang 360dialog "under review" staat: max **5 berichten per 24 uur**.

---

## Interne Contactgegevens

| Contact | Nummer / Adres | Gebruik |
|---------|---------------|---------|
| Bright Panda intern | `31613689666` | Escalatiemeldingen Scenario 03 |
| Testrecord Raouf Student | `31613689666` | Testen Scenario 02 |

---

## Make.com Omgeving

- **Regio:** eu1 (Europa)
- **URL:** eu1.make.com
- **Organisatie:** Bright Panda
