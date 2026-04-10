# Scenario 02 — Tally Webhook → Ouder Planning

**Make naam:** Integration Webhooks
**Make Scenario ID:** 4740354 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** 🟡 In ontwikkeling — gestopt bij module 8 (Set Variable timeslots formule)

> **Openstaande blokkades:**
> - **A:** Module 8 Set Variable formule werkt alleen voor datum 1 — uitbreiden naar datum 2-5
> - **B:** HTTP module 5 nog niet geconfigureerd (`parent_timeslot_invitation` call)
> - **C:** Salesforce Update module 6 nog niet geconfigureerd (status + `Available_Timeslots__c`)
> - **D:** Meta display name goedkeuring blokkeert testen (fout #131037)

---

## Doel

Ontvangt de beschikbaarheid die een docent invult via **Tally Form 1** via een webhook, zoekt het matching record op in Salesforce, haalt de oudergegevens op, stuurt een **WhatsApp bericht naar de ouder** met genummerde tijdsloten en een link naar Tally Form 2, en slaat de genummerde tijdslotenlijst op in `Available_Timeslots__c`.

**Probleem dat het oplost:** Ouders moesten handmatig benaderd worden na ontvangst van docent beschikbaarheid.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Docent Beschikbaarheid |
| Webhook URL | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` |
| Ingesteld in | Tally Form 1 → Settings → Integrations → Webhooks |

> ⚠️ **Webhook timing:** Altijd eerst **Run once** starten → wachten op "Waiting for data" → dan pas Tally invullen. Webhook logs bekijken: ga **uit** het scenario naar het linkermenu → klik op **Webhooks** → klik op **Logs** bij de webhook naam (NIET via de scenario History tab).

---

## Module Volgorde

```
[1] Webhooks → Custom Webhook
        ↓
[8] Tools → Set Variable (timeslots_numbered_list)   ← HIER GESTOPT
        ↓
[3] Salesforce → Search Records (SOQL)
        ↓
[4] Salesforce → Get a Record (Student Account)
        ↓
[5] HTTP → POST 360dialog (naar ouder)               ← NOG TE CONFIGUREREN
        ↓
[6] Salesforce → Update a Record                     ← NOG TE CONFIGUREREN
```

> Volgorde: 1 → 8 → 3 → 4 → 5 → 6

---

## Modules Detail

### Module 1 — Custom Webhook
- **Naam:** Tally Docent Beschikbaarheid
- **Output:** Volledige Tally form response met `data.fields[]` array (1-based indexing in Make.com)

### Module 8 — Tools Set Variable (timeslots_numbered_list)
- **Variable name:** `timeslots_numbered_list`
- **Status:** Module aangemaakt, werkt voor datum 1, uitbreiden naar datum 2-5 nodig

**Werkende gedeeltelijke formule (datum 1):**
```
{{join(map(1.data.fields[4].options; "text"; "id"; 1.data.fields[4].value[]); "\n")}}
```

**Gewenste eindformule** (geeft genummerd overzicht over alle 5 datums):
```
1. 11 maart 13:00-14:00
2. 11 maart 14:00-15:00
3. 25 maart 10:00-11:00
```

> ⚠️ Verifieer de exacte field indices voor datum 2-5 via de webhook logs voordat je de formule uitbreidt. De berekende indices staan in de Tally datastructuur hieronder.

**Opslagformat in `Available_Timeslots__c`:**
```
1=12 maart 13:00-14:00|2=12 maart 14:00-15:00|3=25 maart 10:00-11:00
```

### Module 3 — Salesforce Search Records (SOQL)

**Definitieve versie:**
```sql
SELECT Id, Student__c, Teacher__c, Subject_s__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = 'Matching Number {{1.data.fields[1].value}}'
```

> ⚠️ **Pill-selector bug:** De dropdown in de SOQL editor toont altijd het laatste element van `fields[]`. Typ `{{1.data.fields[1].value}}` handmatig in het SOQL veld.

**Tijdelijke testversie (hardcoded):**
```sql
WHERE Name = 'Matching Number 0016'
```

### Module 4 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{3.Student__c}}`
- **Gebruikte output:** `{{4.FirstName}}`, `{{4.ParentSPhone__c}}`

> Module 4 is noodzakelijk omdat SOQL alleen het `Student__c` ID teruggeeft, niet de volledige accountgegevens.

### Module 5 — HTTP Make a request (360dialog → Ouder) *(NOG TE CONFIGUREREN)*

**Beoogde JSON body:**
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
        {"type": "text", "text": "{{8.timeslots_numbered_list}}"},
        {"type": "text", "text": "https://tally.so/r/WOozov?matching_number={{1.data.fields[1].value}}&student_name={{1.data.fields[2].value}}"}
      ]
    }]
  }
}
```

> ⚠️ Parameter 3 (genummerde tijdsloten) is afhankelijk van de voltooide Set Variable formule in module 8.

### Module 6 — Salesforce Update a Record *(NOG TE CONFIGUREREN)*
- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{3.Id}}`

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Status__c` | `Parent Invited` |
| `Available_Timeslots__c` | `{{8.timeslots_numbered_list}}` (in pipe-formaat) |

---

## Tally Form 1 — Webhook Datastructuur

> Gebaseerd op daadwerkelijke JSON ontvangen op 10 maart 2026. Make.com gebruikt **1-based indexing**.

| Index | Veldnaam | Type | Voorbeeldwaarde |
|-------|----------|------|----------------|
| `fields[1]` | matching_number | HIDDEN_FIELDS | `"0016"` |
| `fields[2]` | student_name | HIDDEN_FIELDS | `"Raouf"` |
| `fields[3]` | Date 1 | INPUT_DATE | `"2026-03-12"` |
| `fields[4]` | Tijdsloten datum 1 | CHECKBOXES | options array + value array van UUIDs |
| `fields[5-17]` | Individuele checkboxes datum 1 | CHECKBOXES | `true` of `false` (13 tijdsloten) |
| `fields[18]` | Date 2 | INPUT_DATE | `"2026-03-13"` |
| `fields[19]` | Tijdsloten datum 2 | CHECKBOXES | options + value array |
| `fields[20-32]` | Individuele checkboxes datum 2 | CHECKBOXES | `true` of `false` |
| `fields[33]` | Date 3 | INPUT_DATE | — |
| `fields[34]` | Tijdsloten datum 3 | CHECKBOXES | — |
| `fields[35-47]` | Individuele checkboxes datum 3 | CHECKBOXES | — |
| `fields[48]` | Date 4 | INPUT_DATE | — |
| `fields[49]` | Tijdsloten datum 4 | CHECKBOXES | — |
| `fields[50-62]` | Individuele checkboxes datum 4 | CHECKBOXES | — |
| `fields[63]` | Date 5 | INPUT_DATE | — |
| `fields[64]` | Tijdsloten datum 5 | CHECKBOXES | — |
| `fields[65-77]` | Individuele checkboxes datum 5 | CHECKBOXES | — |

> ⚠️ Indices datum 2-5 zijn berekend op basis van 13 tijdsloten per datum = 14 fields per datumblok. **Verifieer via webhook logs** voor de exacte indices.

**Checkboxes UUID→tekst formule:**
```
{{join(map(1.data.fields[4].options; "text"; "id"; 1.data.fields[4].value[]); " | ")}}
```
> Tally Checkboxes sturen geselecteerde opties als **UUID strings** in `value[]`. De leesbare tekst staat in `options[]` als objecten met `id` en `text`. De `map()` formule is altijd nodig.

**13 tijdsloten opties (identiek per datum):**
```
08:00-09:00  |  09:00-10:00  |  10:00-11:00  |  11:00-12:00  |  12:00-13:00
13:00-14:00  |  14:00-15:00  |  15:00-16:00  |  16:00-17:00  |  17:00-18:00
18:00-19:00  |  19:00-20:00  |  20:00-21:00
```

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `map() finished with error — not a valid array` | Directe aanroep op `fields[]` structuur | Directe array indexes: `fields[1].value` |
| "Missing value of required parameter 'record'" (module 4) | SOQL vond geen record, `Student__c` was leeg | SOQL hardcoded op `"0016"` als test |
| SOQL: Total number of bundles: 0 | Oude webhook data had lege `fields[1].value` | Run once opnieuw gestart met verse Tally submission |
| Dropdown filter werkte niet voor Name veld | Dropdown toonde veldlabels, niet `Name` | Search By omgezet van Filter naar **SOQL Query** |
| Webhook "The module is not set up" bij Run once | Data structuur nog niet bepaald | Re-determine data structure → Run once → Tally invullen |
| Tally retry mislukt (Failed in history) | Make.com luisterde niet meer op moment van submission | Altijd eerst Run once → wachten → dan Tally invullen |
| HTTP "The parameter to is required" | `ParentSPhone__c` niet ingevuld op testrecord | Ingevuld met testnummer `31613689666` |
| OAuthException 100 "Invalid parameter" van 360dialog | Verkeerde `fields[]` index in JSON body | JSON gecorrigeerd naar bevestigde field indices |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Stuurt Tally Form 1 link naar docent |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders + escalatie bij niet-reageren |
| [Scenario 04](scenario-04-ouder-tijdslot-verwerking.md) | Verwerkt Form 2 submission van ouder |
