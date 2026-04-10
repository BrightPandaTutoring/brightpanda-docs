# Scenario 02 — Tally Webhook → Ouder Planning

**Make naam:** Integration Webhooks
**Make Scenario ID:** 4740354 (eu1.make.com)
**Laatste update:** 10 april 2026
**Status:** 🟡 In ontwikkeling

> **Openstaande blokkades:**
> 1. Meta display name goedkeuring (fout 131037) blokkeert alle WhatsApp berichten
> 2. SOQL query nog hardcoded op `0016` — dynamisch maken is volgende stap
> 3. Parameter 3 tijdsloten nog niet correct geformatteerd — `join/map` formule testen
> 4. `ParentSPhone__c` invullen op testrecord Raouf Student in Salesforce

---

## Doel

Ontvangt de beschikbaarheid die een docent invult via **Tally Form 1** via een webhook, zoekt het matching record op in Salesforce, haalt de oudergegevens op, en stuurt een **WhatsApp bericht naar de ouder** met de beschikbare tijdsloten en een link naar Tally Form 2.

**Probleem dat het oplost:** Ouders moesten handmatig benaderd worden na ontvangst van docent beschikbaarheid.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook naam | Tally Docent Beschikbaarheid |
| Webhook URL | `https://hook.eu1.make.com/8mum1e8efh41uf7gdb91gvyrwsz0mexg` |
| Ingesteld in | Tally Form 1 → Settings → Integrations → Webhooks |
| Werking | Tally stuurt POST zodra docent beschikbaarheidsformulier indient |

> ⚠️ **Webhook tijdstip-instructie:** Altijd eerst **Run once** starten in Make.com en wachten op "Waiting for data" — dan pas Tally formulier invullen. Nooit andersom.

---

## Modules / Stappen

```
[1] Webhooks → Custom Webhook (Tally Docent Beschikbaarheid)
        ↓
[3] Salesforce → Search Records (SOQL op matching_number)
        ↓
[4] Salesforce → Get a Record (Student Account)
        ↓
[5] HTTP → POST 360dialog WhatsApp API (naar ouder)
        ↓
[6] Salesforce → Update a Record (status → Parent Invited)
```

---

### Module 1 — Custom Webhook
- **Naam:** Tally Docent Beschikbaarheid
- **Output:** Volledige Tally form response inclusief `data.fields[]` array

### Module 3 — Salesforce Search Records (SOQL)

**Huidige versie (hardcoded voor test):**
```sql
SELECT Id, Student__c, Teacher__c, Subject_s__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = 'Matching Number 0016'
```

**Definitieve versie (nog in te stellen):**
```sql
SELECT Id, Student__c, Teacher__c, Subject_s__c, Name
FROM Student_Teacher_Matching__c
WHERE Name = 'Matching Number {{1.data.fields[0].value}}'
```

> ⚠️ De pill-selector in de Make.com SOQL editor toont altijd het laatste element van de `fields[]` array. Gebruik workaround: typ `{{1.data.fields[0].value}}` handmatig in het SOQL veld in plaats van via dropdown.

### Module 4 — Salesforce Get a Record (Student)
- **Type:** Account
- **Record ID:** `{{3.Student__c}}`
- **Output velden:** `FirstName`, `ParentSPhone__c`

> Module 4 is noodzakelijk omdat de SOQL query alleen het `Student__c` ID teruggeeft, niet de volledige accountgegevens.

### Module 5 — HTTP Make a request (360dialog WhatsApp → Ouder)
Zie [Gedeelde 360dialog configuratie](gedeelde-configuratie.md) voor headers/auth.

**Body:**
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
        {"type": "text", "text": "{{1.data.fields[1].value}}"},
        {"type": "text", "text": "{{1.data.fields[2].value}}: {{join(map(1.data.fields[3].options; \"text\"; \"id\"; 1.data.fields[3].value[]); \", \")}}"},
        {"type": "text", "text": "https://tally.so/r/WOozov?matching_number={{1.data.fields[0].value}}&student_name={{1.data.fields[1].value}}"}
      ]
    }]
  }
}
```

> ⚠️ Parameter 3 (tijdsloten) is nog niet volledig getest. De `join/map` formule is de voorgestelde oplossing maar moet worden uitgebreid voor meerdere datums (fields[4..11]).

### Module 6 — Salesforce Update a Record
- **Type:** `Student_Teacher_Matching__c`
- **Record ID:** `{{3.Id}}`
- **Veld:** `Trial_Lesson_Status__c` → `Parent Invited`

---

## Datastructuur

### Tally Webhook data (bevestigd via testsubmissie matching_number=0016, student_name=Raouf)

| Index | Veld | Type | Voorbeeldwaarde |
|-------|------|------|----------------|
| `fields[0].value` | matching_number | HIDDEN_FIELDS | `"0016"` |
| `fields[1].value` | student_name | HIDDEN_FIELDS | `"Raouf"` |
| `fields[2].value` | Date 1 | INPUT_DATE | `"2026-03-09"` |
| `fields[3].options` | Date 1 Times | MULTI_SELECT array | `["10:00-11:00", "11:00-12:00", "14:00-15:00"]` |
| `fields[4].value` | Date 2 | INPUT_DATE | `"2026-03-10"` |
| `fields[5].options` | Date 2 Times | MULTI_SELECT array | `["12:00-13:00", "15:00-16:00"]` |
| `fields[6..9]` | Date 3 + Date 3 Times, Date 4 + Date 4 Times | — | leeg in test |
| `fields[10].options` | Date 5 Times | MULTI_SELECT array | `["18:00-19:00", "15:00-16:00"]` |

### Salesforce variabelen

| Variabele | Module | Beschrijving |
|-----------|--------|-------------|
| `{{3.Id}}` | Module 3 | ID van het matching record |
| `{{3.Student__c}}` | Module 3 | Salesforce ID van student |
| `{{4.FirstName}}` | Module 4 | Voornaam ouder (staat op Student Account) |
| `{{4.ParentSPhone__c}}` | Module 4 | Telefoonnummer ouder (internationaal formaat) |

---

## Filters / Condities

- Geen expliciete filter — scenario verwerkt alle inkomende webhook submissions
- De SOQL query filtert impliciet op de `matching_number` die Tally meestuurt

---

## Gekoppelde Apps & Services

| Service | Gebruik |
|---------|---------|
| **Webhooks / Tally.so** | Trigger via webhook na invullen Form 1 |
| **Salesforce** | SOQL lookup matching + ophalen student/ouder + update status |
| **360dialog** | WhatsApp bericht naar ouder |
| **Tally.so Form 2** | Link geconstrueerd in JSON body (`tally.so/r/WOozov`) |

---

## Foutmeldingen & Oplossingen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `map() finished with error — {object} is not a valid array` | `map()` werkt niet direct op `fields[]` structuur | Directe array indexes gebruikt: `fields[0].value` en `fields[1].value` |
| "Missing value of required parameter 'record'" in Module 4 | SOQL vond geen record, `Student__c` was leeg | SOQL werkend maken via hardcoded `"0016"` als test |
| SOQL: Total number of bundles: 0 | Make.com gebruikte oude webhook data waarbij `fields[0].value` leeg was | Run once opnieuw gestart met verse Tally submission |
| Dropdown filter werkte niet (Name veld niet vindbaar) | Dropdown toonde veldlabels, niet het `Name` veld | Search By omgezet van Filter naar **SOQL Query** |
| Webhook "The module is not set up" bij eerste Run once | Data structuur nog niet bepaald | Re-determine data structure → Run once → Tally invullen |
| Tally retry mislukt (Failed in history) | Make.com luisterde niet meer op moment van submission | Altijd eerst Run once starten, wachten op "Waiting for data", dan Tally invullen |
| HTTP "The parameter to is required" | `ParentSPhone__c` niet ingevuld op testrecord | Ingevuld met testnummer `31613689666` |
| OAuthException 100 "Invalid parameter" van 360dialog | Parameter 3 was leeg of bevatte verkeerde waarde | JSON body gecorrigeerd naar correcte `fields[]` indexen |

---

## Speciale Opmerkingen

- 🔑 Tally MULTI_SELECT data wordt geleverd als een `options` array — complexe parsing vereist
- 🔢 `join/map` formule voor tijdsloten is voorgesteld maar nog niet bevestigd werkend voor alle datumsloten
- ⚠️ Scenario was aanvankelijk genaamd "Scenario 2 - Tally Webhook Ouder", definitief hernoemd naar "Integration Webhooks"

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Stuurt Tally Form 1 link naar docent |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders + escalatie bij niet-reageren |
