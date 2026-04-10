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
[32] Salesforce → Search Records SOQL (Parent Contact)
        ↓
[5]  HTTP → 360dialog (WhatsApp naar ouder)
        ↓
[6]  Salesforce → Update a Record (Available_Timeslots__c + status)
```

> Volgorde: 1 → 31 → 3 → 4 → 32 → 5 → 6

---

## Modules Detail

### Module 1 — Custom Webhook
- **Naam:** Tally Docent Beschikbaarheid
- **Output:** Volledige Tally form response met `data.fields[]` array

> ⚠️ **Tally gebruikt 0-based indexering** — `fields[0]` is het eerste veld (matching_number), niet `fields[1]`. Dit is afwijkend van eerdere aanname en is bevestigd via daadwerkelijke webhook data.

### Module 31 — HTTP → Google Apps Script

**Doel:** Alle Tally checkbox- en datumvelden verwerken tot een pipe-separated tijdsloten string. Complexe logica buiten Make.com om problemen met lange formules te vermijden.

- **URL:** `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`
- **Method:** POST
- **Body:** Alle 65+ velden als JSON (0-based indices)

**Volledige body (kopieer exact — aanhalingstekens om datumchips zijn kritiek):**
```json
{
  "fields": {
    "2": "{{1.data.fields[2].value}}",
    "17": "{{1.data.fields[17].value}}",
    "32": "{{1.data.fields[32].value}}",
    "47": "{{1.data.fields[47].value}}",
    "62": "{{1.data.fields[62].value}}",
    "4": {{if(1.data.fields[4].value; true; false)}},
    "5": {{if(1.data.fields[5].value; true; false)}},
    "6": {{if(1.data.fields[6].value; true; false)}},
    "7": {{if(1.data.fields[7].value; true; false)}},
    "8": {{if(1.data.fields[8].value; true; false)}},
    "9": {{if(1.data.fields[9].value; true; false)}},
    "10": {{if(1.data.fields[10].value; true; false)}},
    "11": {{if(1.data.fields[11].value; true; false)}},
    "12": {{if(1.data.fields[12].value; true; false)}},
    "13": {{if(1.data.fields[13].value; true; false)}},
    "14": {{if(1.data.fields[14].value; true; false)}},
    "15": {{if(1.data.fields[15].value; true; false)}},
    "16": {{if(1.data.fields[16].value; true; false)}},
    "19": {{if(1.data.fields[19].value; true; false)}},
    "20": {{if(1.data.fields[20].value; true; false)}},
    "21": {{if(1.data.fields[21].value; true; false)}},
    "22": {{if(1.data.fields[22].value; true; false)}},
    "23": {{if(1.data.fields[23].value; true; false)}},
    "24": {{if(1.data.fields[24].value; true; false)}},
    "25": {{if(1.data.fields[25].value; true; false)}},
    "26": {{if(1.data.fields[26].value; true; false)}},
    "27": {{if(1.data.fields[27].value; true; false)}},
    "28": {{if(1.data.fields[28].value; true; false)}},
    "29": {{if(1.data.fields[29].value; true; false)}},
    "30": {{if(1.data.fields[30].value; true; false)}},
    "31": {{if(1.data.fields[31].value; true; false)}},
    "34": {{if(1.data.fields[34].value; true; false)}},
    "35": {{if(1.data.fields[35].value; true; false)}},
    "36": {{if(1.data.fields[36].value; true; false)}},
    "37": {{if(1.data.fields[37].value; true; false)}},
    "38": {{if(1.data.fields[38].value; true; false)}},
    "39": {{if(1.data.fields[39].value; true; false)}},
    "40": {{if(1.data.fields[40].value; true; false)}},
    "41": {{if(1.data.fields[41].value; true; false)}},
    "42": {{if(1.data.fields[42].value; true; false)}},
    "43": {{if(1.data.fields[43].value; true; false)}},
    "44": {{if(1.data.fields[44].value; true; false)}},
    "45": {{if(1.data.fields[45].value; true; false)}},
    "46": {{if(1.data.fields[46].value; true; false)}},
    "49": {{if(1.data.fields[49].value; true; false)}},
    "50": {{if(1.data.fields[50].value; true; false)}},
    "51": {{if(1.data.fields[51].value; true; false)}},
    "52": {{if(1.data.fields[52].value; true; false)}},
    "53": {{if(1.data.fields[53].value; true; false)}},
    "54": {{if(1.data.fields[54].value; true; false)}},
    "55": {{if(1.data.fields[55].value; true; false)}},
    "56": {{if(1.data.fields[56].value; true; false)}},
    "57": {{if(1.data.fields[57].value; true; false)}},
    "58": {{if(1.data.fields[58].value; true; false)}},
    "59": {{if(1.data.fields[59].value; true; false)}},
    "60": {{if(1.data.fields[60].value; true; false)}},
    "61": {{if(1.data.fields[61].value; true; false)}},
    "64": {{if(1.data.fields[64].value; true; false)}},
    "65": {{if(1.data.fields[65].value; true; false)}},
    "66": {{if(1.data.fields[66].value; true; false)}},
    "67": {{if(1.data.fields[67].value; true; false)}},
    "68": {{if(1.data.fields[68].value; true; false)}},
    "69": {{if(1.data.fields[69].value; true; false)}},
    "70": {{if(1.data.fields[70].value; true; false)}},
    "71": {{if(1.data.fields[71].value; true; false)}},
    "72": {{if(1.data.fields[72].value; true; false)}},
    "73": {{if(1.data.fields[73].value; true; false)}},
    "74": {{if(1.data.fields[74].value; true; false)}},
    "75": {{if(1.data.fields[75].value; true; false)}},
    "76": {{if(1.data.fields[76].value; true; false)}}
  }
}
```

> **Waarom aanhalingstekens om datumchips?** Tally `INPUT_DATE` velden arriveren als date objects in Make.com. Direct samenvoegen met `&` of `formatDate()` geeft leeg resultaat. De aanhalingstekens forceren JSON serialisatie als string — Google Apps Script ontvangt dan gewoon tekst.
>
> **Waarom `if(x; true; false)` voor checkboxes?** Make.com checkbox velden zijn een intern boolean type dat niet als geldig JSON boolean geserialiseerd wordt. De `if()`-wrapper garandeert altijd de letterlijke waarden `true` of `false`.

**Output:** `{{31.data.timeslots}}` — pipe-separated string, bijv:
```
2026-03-10 - 10:00-11:00|2026-03-10 - 11:00-12:00|2026-03-12 - 14:00-15:00
```

Zie [Google Apps Script documentatie](google-apps-script.md) voor de volledige logica.

### Module 3 — Salesforce Search Records (SOQL)

```sql
SELECT Id, Teacher__c, Student__c, Subject_s__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = '{{1.data.fields[0].value}}'
```

> ⚠️ **Kritiek — 0-based indexering:** `fields[0]` is het matching_number veld (niet `fields[1]`). Het veld bevat de **volledige naam** "Matching Number 0016" — geen prefix toevoegen in de SOQL.
>
> ⚠️ **Chip selectie:** Selecteer de chip handmatig als blauwe chip. Als de waarde leeg lijkt in de output, sluit het scenario en heropen het — soms geeft Make.com een verouderde preview.

**Debug:** Als module 3 0 bundles retourneert:
1. Controleer in Salesforce: `SELECT Id, Name FROM Student_Teacher_Matching__c WHERE Name = 'Matching Number 0016'`
2. Controleer of `fields[0]` waarde correct is in de webhook log (Webhooks → Logs)
3. Verwijder de chip in de SOQL en selecteer opnieuw als blauwe chip

### Module 4 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{3.Student__c}}`
- **Gebruikte output:** `{{4.FirstName}}`, `{{4.Account ID}}`

> ⚠️ `ParentSPhone__c` is **niet bruikbaar** — ouders zijn Contact records in Salesforce, niet een veld op het Account. Gebruik module 32 (SOQL) om de ouder Contact op te halen.

### Module 32 — Salesforce Search Records SOQL (Ouder Contact)

```sql
SELECT Id, FirstName, Phone FROM Contact WHERE AccountId = '{{4.Account ID}}'
```

- **Limit:** 10
- **Output:** `{{32.FirstName}}`, `{{32.Phone}}`

> Ouders zijn **Contact** records in Salesforce, gekoppeld via `AccountId` aan het student Account.

### Module 5 — HTTP → 360dialog (WhatsApp naar ouder)

Zie [Gedeelde configuratie](gedeelde-configuratie.md) voor headers/auth.

**Template:** `parent_timeslot_invitation` (5 parameters)

| Parameter | Variabele | Inhoud |
|-----------|-----------|--------|
| `{{1}}` | `{{32.FirstName}}` | Voornaam ouder |
| `{{2}}` | `{{1.data.fields[1].value}}` | Naam leerling (fields[1] = student_name) |
| `{{3}}` | `{{3.Subject_s__c}}` | Vak |
| `{{4}}` | `{{31.data.timeslots}}` | Pipe-separated tijdsloten string |
| `{{5}}` | Tally Form 2 URL | `https://tally.so/r/WOozov?matching_number={{encodeURL(1.data.fields[0].value)}}&student_name={{1.data.fields[1].value}}` |

**JSON body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "{{32.Phone}}",
  "type": "template",
  "template": {
    "name": "parent_timeslot_invitation",
    "language": {"code": "nl"},
    "components": [{
      "type": "body",
      "parameters": [
        {"type": "text", "text": "{{32.FirstName}}"},
        {"type": "text", "text": "{{1.data.fields[1].value}}"},
        {"type": "text", "text": "{{3.Subject_s__c}}"},
        {"type": "text", "text": "{{31.data.timeslots}}"},
        {"type": "text", "text": "https://tally.so/r/WOozov?matching_number={{encodeURL(1.data.fields[0].value)}}&student_name={{1.data.fields[1].value}}"}
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

> **0-based indexering** — bevestigd via daadwerkelijke webhook data. `fields[0]` = eerste veld.

| Index | Veldnaam | Type | Voorbeeldwaarde |
|-------|----------|------|----------------|
| `fields[0]` | matching_number | HIDDEN | `"Matching Number 0016"` ⚠️ volledige naam! |
| `fields[1]` | student_name | HIDDEN | `"Raouf"` |
| `fields[2]` | Datum 1 | INPUT_DATE | Date object ⚠️ |
| `fields[3]` | Tijdsloten datum 1 | CHECKBOXES groep | options + value array |
| `fields[4-16]` | Individuele checkboxes datum 1 | CHECKBOX | `true` of `false` (13 tijdsloten) |
| `fields[17]` | Datum 2 | INPUT_DATE | Date object |
| `fields[18]` | Tijdsloten datum 2 | CHECKBOXES groep | options + value array |
| `fields[19-31]` | Individuele checkboxes datum 2 | CHECKBOX | `true` of `false` |
| `fields[32]` | Datum 3 | INPUT_DATE | — |
| `fields[33]` | Tijdsloten datum 3 | CHECKBOXES groep | — |
| `fields[34-46]` | Individuele checkboxes datum 3 | CHECKBOX | — |
| `fields[47]` | Datum 4 | INPUT_DATE | — |
| `fields[48]` | Tijdsloten datum 4 | CHECKBOXES groep | — |
| `fields[49-61]` | Individuele checkboxes datum 4 | CHECKBOX | — |
| `fields[62]` | Datum 5 | INPUT_DATE | — |
| `fields[63]` | Tijdsloten datum 5 | CHECKBOXES groep | — |
| `fields[64-76]` | Individuele checkboxes datum 5 | CHECKBOX | — |

**13 tijdsloten per datum:** 08:00-09:00 t/m 20:00-21:00

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| Module 3 retourneert 0 bundles | SOQL gebruikt `fields[1]` (oud) i.p.v. `fields[0]` (0-based) | Update chip naar `{{1.data.fields[0].value}}` — geen prefix toevoegen |
| Module 3 retourneert 0 bundles | Chip niet correct geselecteerd als blauwe chip | Verwijder chip, hertype `{{` en selecteer opnieuw |
| `and(x; y)` bestaat niet in Make.com | Make.com ondersteunt geen `and()` functie | Gebruik geneste `if(x; if(y; ...))` |
| Tally date objects niet concateneerbaar | Datum object uit Tally kan niet direct als string gebruikt worden | Datum als JSON string doorgeven aan Google Apps Script |
| Lange formules raken corrupt | Make.com formules zijn onbetrouwbaar bij complexiteit | Alle complexe logica naar Google Apps Script verplaatst |
| Make.com pakt oudste webhook uit queue | Oude webhook data wordt verwerkt | Altijd "Wait for new data" klikken, dan direct nieuw formulier submitten |
| `newline` / `char(10)` werken niet als separator | Make.com ondersteunt newlines niet betrouwbaar | Pipe `\|` gebruiken als separator |
| `ParentSPhone__c` leeg of niet gevonden | Ouders zijn Contact records, niet een veld op Account | Gebruik SOQL: `SELECT Phone FROM Contact WHERE AccountId = '{{4.Account ID}}'` |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Stuurt Tally Form 1 link naar docent |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders + escalatie bij niet-reageren |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Verwerkt Form 2 submission van ouder |
| [Google Apps Script](google-apps-script.md) | Tijdsloten verwerking (module 31) |
