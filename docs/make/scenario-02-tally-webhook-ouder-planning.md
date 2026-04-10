# Scenario 02 — Tally Webhook → Ouder Planning

**Make naam:** Integration Webhooks
**Make Scenario ID:** 4740354 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** ✅ Compleet

---

## Doel

Ontvangt de beschikbaarheid van een docent via **Tally Form 1** webhook, verwerkt de tijdsloten via Google Apps Script, zoekt het matching record op in Salesforce, haalt oudergegevens op, stuurt een **WhatsApp bericht naar de ouder** met genummerde tijdsloten en Tally Form 2 link, en slaat de tijdslotenlijst op in `Available_Timeslots__c`.

**Probleem dat het oplost:** Ouders moesten handmatig benaderd worden na ontvangst van docent beschikbaarheid.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Docent Beschikbaarheid |
| Webhook URL | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` |
| Ingesteld in | Tally Form 1 → Settings → Integrations → Webhooks |

> ⚠️ **Webhook timing:** Altijd eerst **Run once** starten → wachten op "Waiting for data" → dan pas Tally invullen. Webhook logs bekijken: ga **uit** het scenario → linkermenu → **Webhooks** → **Logs** (NIET via History tab).

---

## Module Volgorde

```
[1]  Webhooks → Custom Webhook (Tally Form 1)
        ↓
[31] HTTP → Google Apps Script (bouw tijdsloten string)
        ↓
[3]  Salesforce → Search Records (SOQL op matching_number)
        ↓
[4]  Salesforce → Get a Record (Student Account)
        ↓
[5]  HTTP → 360dialog (WhatsApp naar ouder)
        ↓
[6]  Salesforce → Update a Record (Available_Timeslots__c + status)
```

> Volgorde: 1 → 31 → 3 → 4 → 5 → 6

---

## Modules Detail

### Module 1 — Custom Webhook
- **Naam:** Tally Docent Beschikbaarheid
- **Output:** Volledige Tally form response met `data.fields[]` array (1-based indexing)

### Module 31 — HTTP → Google Apps Script

**Doel:** Alle Tally checkbox- en datumvelden verwerken tot een pipe-separated tijdsloten string. Complexe logica buiten Make.com om problemen met lange formules te vermijden.

- **URL:** `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`
- **Method:** POST
- **Body:** Alle 65+ velden als JSON

**Body structuur:**
```json
{
  "fields": {
    "3": "{{1.data.fields[3].value}}",
    "5": "{{if(1.data.fields[5].value; true; false)}}",
    "6": "{{if(1.data.fields[6].value; true; false)}}",
    "7": "{{if(1.data.fields[7].value; true; false)}}",
    ...
  }
}
```

> Datumvelden als JSON string doorgeven (geen datum object — Tally date objects zijn niet direct concateneerbaar in Make.com).
> Checkboxvelden als `if(x.value; true; false)` doorgeven.

**Output:** `{{31.data.timeslots}}` — pipe-separated string, bijv:
```
2026-03-10 - 10:00-11:00|2026-03-10 - 11:00-12:00|2026-03-12 - 14:00-15:00
```

Zie [Google Apps Script documentatie](google-apps-script.md) voor de volledige logica.

### Module 3 — Salesforce Search Records (SOQL)

```sql
SELECT Id, Teacher__c, Student__c, Subject_s__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = 'Matching Number {{1.data.fields[1].value}}'
```

> ⚠️ Typ de pill handmatig — pill-selector toont altijd het laatste `fields[]` element.

### Module 4 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{3.Student__c}}`
- **Gebruikte output:** `{{4.FirstName}}`, `{{4.ParentSPhone__c}}`

### Module 5 — HTTP → 360dialog (WhatsApp naar ouder)

Zie [Gedeelde configuratie](gedeelde-configuratie.md) voor headers/auth.

**Template:** `parent_timeslot_invitation` (5 parameters)

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{4.FirstName}}` | Voornaam ouder |
| `{{2}}` | `{{1.data.fields[2].value}}` | Naam leerling |
| `{{3}}` | `{{3.Subject_s__c}}` | Vak |
| `{{4}}` | `{{31.data.timeslots}}` | Pipe-separated tijdsloten string |
| `{{5}}` | Tally Form 2 URL | `https://tally.so/r/WOozov?matching_number={{1.data.fields[1].value}}&student_name={{1.data.fields[2].value}}` |

**JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{4.ParentSPhone__c}}",
  "type": "template",
  "template": {
    "name": "parent_timeslot_invitation",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{4.FirstName}}"},
        {"type": "text", "text": "{{1.data.fields[2].value}}"},
        {"type": "text", "text": "{{3.Subject_s__c}}"},
        {"type": "text", "text": "{{31.data.timeslots}}"},
        {"type": "text", "text": "https://tally.so/r/WOozov?matching_number={{1.data.fields[1].value}}&student_name={{1.data.fields[2].value}}"}
      ]
    }]
  }
}
```

### Module 6 — Salesforce Update a Record

- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{3.Id}}`

| Veld | Waarde |
|------|--------|
| `Available_Timeslots__c` | `{{31.data.timeslots}}` |
| `Trial_Lesson_Status__c` | `Parent Invited` |

---

## Tally Form 1 — Webhook Datastructuur

> Gebaseerd op daadwerkelijke JSON ontvangen op 10 maart 2026. Make.com gebruikt **1-based indexing**.

| Index | Veldnaam | Type | Voorbeeldwaarde |
|-------|----------|------|----------------|
| `fields[1]` | matching_number | HIDDEN | `"0016"` |
| `fields[2]` | student_name | HIDDEN | `"Raouf"` |
| `fields[3]` | Datum 1 | INPUT_DATE | Date object ⚠️ |
| `fields[4]` | Tijdsloten datum 1 | CHECKBOXES groep | options + value array |
| `fields[5-17]` | Individuele checkboxes datum 1 | CHECKBOX | `true` of `false` (13 tijdsloten) |
| `fields[18]` | Datum 2 | INPUT_DATE | Date object |
| `fields[19]` | Tijdsloten datum 2 | CHECKBOXES groep | options + value array |
| `fields[20-32]` | Individuele checkboxes datum 2 | CHECKBOX | `true` of `false` |
| `fields[33]` | Datum 3 | INPUT_DATE | — |
| `fields[34]` | Tijdsloten datum 3 | CHECKBOXES groep | — |
| `fields[35-47]` | Individuele checkboxes datum 3 | CHECKBOX | — |
| `fields[48]` | Datum 4 | INPUT_DATE | — |
| `fields[49]` | Tijdsloten datum 4 | CHECKBOXES groep | — |
| `fields[50-62]` | Individuele checkboxes datum 4 | CHECKBOX | — |
| `fields[63]` | Datum 5 | INPUT_DATE | — |
| `fields[64]` | Tijdsloten datum 5 | CHECKBOXES groep | — |
| `fields[65-77]` | Individuele checkboxes datum 5 | CHECKBOX | — |

**13 tijdsloten per datum:** 08:00-09:00 t/m 20:00-21:00

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `and(x; y)` bestaat niet in Make.com | Make.com ondersteunt geen `and()` functie | Gebruik geneste `if(x; if(y; ...))` |
| Tally date objects niet concateneerbaar | Datum object uit Tally kan niet direct als string gebruikt worden | Datum als JSON string doorgeven aan Google Apps Script |
| Lange formules raken corrupt | Make.com formules zijn onbetrouwbaar bij complexiteit | Alle complexe logica naar Google Apps Script verplaatst |
| Make.com pakt oudste webhook uit queue | Oude webhook data wordt verwerkt | Altijd "Wait for new data" klikken, dan direct nieuw formulier submitten |
| `newline` / `char(10)` werken niet als separator | Make.com ondersteunt newlines niet betrouwbaar | Pipe `\|` gebruiken als separator |
| Variabele referenties onbetrouwbaar | Computed variabelen kunnen corrupt raken | Altijd originele databron gebruiken, bijv. `{{1.data.fields[3].value}}` |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Stuurt Tally Form 1 link naar docent |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders + escalatie bij niet-reageren |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Verwerkt Form 2 submission van ouder |
| [Google Apps Script](google-apps-script.md) | Tijdsloten verwerking (module 31) |
