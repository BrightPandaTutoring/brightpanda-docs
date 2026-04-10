# Google Apps Script

**Script URL (actief):**
`https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`

**Versie:** 2
**Beheer:** [script.google.com](https://script.google.com)
**Laatste update:** 10 april 2026

---

## Waarom Google Apps Script?

Na 3+ uur debuggen bleek dat Tally `INPUT_DATE` velden in Make.com worden omgezet naar **date objects**. Geen enkele Make.com functie kon de datum als string concateneren:

| Geprobeerd | Resultaat |
|-----------|---------|
| `{{1.data.fields[3].value}} & " - test"` | `" - test"` (datum leeg) |
| `toString(1.data.fields[3].value) & " - test"` | leeg |
| `formatDate(1.data.fields[3].value; "DD-MM-YYYY")` | leeg |
| `formatDate(1.data.fields[3].value; "YYYY-MM-DD")` | leeg |
| `parseDate(1.data.fields[3].value; "YYYY-MM-DD")` | leeg |

**Root cause:** Make.com's `&` concatenatie operator werkt niet op date objects. Bewijs: `{{1.data.fields[3].value}}` puur weergeven gaf `"2026-03-10"` correct, maar in een expressie met `&` was de waarde altijd leeg.

**Oplossing:** Datum als JSON string sturen naar Google Apps Script via aanhalingstekens om de chip: `"3": "{{1.data.fields[3].value}}"` — de aanhalingstekens forceren JSON serialisatie als string.

> Naast datum-problemen zijn ook lange Make.com formules (>13 geneste if-statements) onbetrouwbaar — tokens lijken correct maar geven lege output bij opslaan. Alle complexe logica staat daarom in dit script.

---

## Deploy Instellingen

| Instelling | Waarde |
|-----------|--------|
| Execute as | Me |
| Access | Anyone |
| Versie | 2 |

**Versie update deployen:**
1. Ga naar [script.google.com](https://script.google.com)
2. Open het script
3. Klik **Deploy** → **Manage deployments**
4. Klik op de bestaande deployment → **Edit** (potlood)
5. Kies **New version**
6. Klik **Deploy**
7. URL blijft hetzelfde — geen aanpassing nodig in Make.com

> ⚠️ Bij een **nieuwe** deployment (niet versie update) verandert de URL. Dan moet de URL bijgewerkt worden in Make.com Scenario 02 module 31 en Scenario 3b module 5.

---

## Architectuur

```
POST request binnenkomt
        ↓
  data.fields aanwezig?
  ├── YES → Functie A (Scenario 02: bouw tijdsloten string)
  └── NO  → data.timeslots + data.chosen aanwezig?
                └── YES → Functie B (Scenario 3b: vertaal keuzenummer)
```

---

## Functie A — Bouw Tijdsloten String (Scenario 02)

### Input
```json
{
  "fields": {
    "3": "2026-03-10",
    "18": "2026-03-12",
    "33": "",
    "48": "",
    "63": "",
    "5": false,
    "6": false,
    "7": true,
    "8": true,
    "9": false,
    "10": false,
    "11": false,
    "12": false,
    "13": false,
    "14": false,
    "15": false,
    "16": false,
    "17": false,
    "20": false,
    "21": false,
    "22": false,
    "23": false,
    "24": false,
    "25": true,
    ...
  }
}
```

### Datum- en Checkbox Mapping

| Datum veld | Checkbox range | Tijdsloten |
|-----------|---------------|-----------|
| `fields[3]` (Datum 1) | `fields[5]` t/m `fields[17]` | 08:00-09:00 t/m 20:00-21:00 |
| `fields[18]` (Datum 2) | `fields[20]` t/m `fields[32]` | 08:00-09:00 t/m 20:00-21:00 |
| `fields[33]` (Datum 3) | `fields[35]` t/m `fields[47]` | 08:00-09:00 t/m 20:00-21:00 |
| `fields[48]` (Datum 4) | `fields[50]` t/m `fields[62]` | 08:00-09:00 t/m 20:00-21:00 |
| `fields[63]` (Datum 5) | `fields[65]` t/m `fields[77]` | 08:00-09:00 t/m 20:00-21:00 |

**Tijdsloten array (index 0-12):**
```
08:00-09:00 | 09:00-10:00 | 10:00-11:00 | 11:00-12:00 | 12:00-13:00
13:00-14:00 | 14:00-15:00 | 15:00-16:00 | 16:00-17:00 | 17:00-18:00
18:00-19:00 | 19:00-20:00 | 20:00-21:00
```

### Output
```json
{"timeslots": "2026-03-10 - 10:00-11:00|2026-03-10 - 11:00-12:00|2026-03-12 - 17:00-18:00"}
```

**Gebruikt in Make.com als:** `{{31.data.timeslots}}`

---

## Functie B — Vertaal Keuzenummer naar Datetime (Scenario 3b)

### Input
```json
{
  "timeslots": "2026-03-10 - 10:00-11:00|2026-03-10 - 14:00-15:00|2026-03-12 - 09:00-10:00",
  "chosen": 2
}
```

### Logica
1. Split `timeslots` op `|` → array
2. Pak index `chosen - 1` (1-based → 0-based) → `"2026-03-10 - 14:00-15:00"`
3. Split op `" - "` → datum `"2026-03-10"`, tijdslot `"14:00-15:00"`
4. Split tijdslot op `"-"` → starttijd `"14:00"`
5. Bouw ISO datetime: `"2026-03-10T14:00:00.000Z"`

### Output
```json
{
  "timeslot": "2026-03-10 - 14:00-15:00",
  "datetime": "2026-03-10T14:00:00.000Z"
}
```

**Gebruikt in Make.com als:**
- `{{5.data.timeslot}}` → leesbaar tijdslot voor WhatsApp bericht
- `{{5.data.datetime}}` → ISO datetime voor `Trial_Lesson_Date__c`

> **Tijdzone:** Script genereert UTC (`Z`). Salesforce slaat UTC op en toont automatisch in lokale tijdzone van de gebruiker. Voor Nederland (UTC+1 winter) toont Salesforce `10:00 UTC` correct als `11:00`.

---

## Volledige Script Code (Versie 2)

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);

  // Scenario 2: verwerk docent beschikbaarheid
  if (data.fields) {
    const fields = data.fields;
    const times = [
      "08:00-09:00","09:00-10:00","10:00-11:00","11:00-12:00",
      "12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00",
      "16:00-17:00","17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00"
    ];
    const dateFields = [3, 18, 33, 48, 63];
    const slotStarts = [5, 20, 35, 50, 65];
    let result = [];

    for (let d = 0; d < 5; d++) {
      const datum = fields[dateFields[d]];
      if (!datum) continue;
      for (let t = 0; t < 13; t++) {
        if (fields[slotStarts[d] + t] === true) {
          result.push(datum + " - " + times[t]);
        }
      }
    }

    return ContentService
      .createTextOutput(JSON.stringify({ timeslots: result.join("|") }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  // Scenario 3b: ouder kiest tijdslot nummer
  if (data.timeslots && data.chosen) {
    const slots = data.timeslots.split("|");
    const index = parseInt(data.chosen) - 1;
    const chosen = slots[index];

    if (!chosen) {
      return ContentService
        .createTextOutput(JSON.stringify({ error: "Tijdslot niet gevonden" }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    const parts = chosen.split(" - ");
    const date = parts[0];
    const time = parts[1].split("-")[0];
    const datetime = date + "T" + time + ":00.000Z";

    return ContentService
      .createTextOutput(JSON.stringify({ timeslot: chosen, datetime: datetime }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

---

## Gebruik per Scenario

| Scenario | Module | Functie | Trigger in input | Output gebruikt |
|----------|--------|---------|-----------------|----------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | 31 | A | `data.fields` aanwezig | `{{31.data.timeslots}}` |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | 5 | B | `data.timeslots` + `data.chosen` | `{{5.data.timeslot}}`, `{{5.data.datetime}}` |
