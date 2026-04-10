# Google Apps Script

**Script URL:** `https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`
**Versie:** 2
**Laatste update:** 10 april 2026

---

## Waarom Google Apps Script?

Make.com formules zijn onbetrouwbaar bij complexe logica (lange formules raken corrupt, `and()` bestaat niet, datum objecten zijn niet concateneerbaar). Alle complexe verwerking is daarom naar Google Apps Script verplaatst.

---

## Architectuur

Eén `doPost` handler met twee functies, bepaald op basis van de input:

```
POST request binnenkomt
        ↓
  data.fields aanwezig?
  ├── YES → Functie A (Scenario 2: bouw tijdsloten string)
  └── NO  → data.timeslots + data.chosen aanwezig?
                └── YES → Functie B (Scenario 3b: vertaal keuzenummer)
```

---

## Functie A — Bouw Tijdsloten String (Scenario 2)

**Trigger:** Input bevat `data.fields`

### Input
```json
{
  "fields": {
    "3": "2026-03-10",
    "5": false,
    "6": false,
    "7": true,
    "8": true,
    "9": false,
    ...
  }
}
```

- Sleutel `"3"`, `"18"`, `"33"`, `"48"`, `"63"` → datum strings (INPUT_DATE)
- Sleutels voor tijdsloten → `true` of `false` checkboxwaarden

### Tijdsloten mapping (per datum)

| Field index offset | Tijdslot |
|-------------------|---------|
| +2 (bijv. `fields[5]` voor datum 1) | 08:00-09:00 |
| +3 | 09:00-10:00 |
| +4 | 10:00-11:00 |
| +5 | 11:00-12:00 |
| +6 | 12:00-13:00 |
| +7 | 13:00-14:00 |
| +8 | 14:00-15:00 |
| +9 | 15:00-16:00 |
| +10 | 16:00-17:00 |
| +11 | 17:00-18:00 |
| +12 | 18:00-19:00 |
| +13 | 19:00-20:00 |
| +14 | 20:00-21:00 |

**Datum blokken:**
| Datum veld | Checkbox range |
|-----------|---------------|
| `fields[3]` | `fields[5]` t/m `fields[17]` |
| `fields[18]` | `fields[20]` t/m `fields[32]` |
| `fields[33]` | `fields[35]` t/m `fields[47]` |
| `fields[48]` | `fields[50]` t/m `fields[62]` |
| `fields[63]` | `fields[65]` t/m `fields[77]` |

### Logica
1. Loop over 5 datums
2. Als datum ingevuld: loop over 13 tijdsloten
3. Als checkbox `true` → voeg `"datum - tijdslot"` toe aan array
4. Join array met `|` separator

### Output
```json
{
  "timeslots": "2026-03-10 - 10:00-11:00|2026-03-10 - 11:00-12:00|2026-03-12 - 14:00-15:00"
}
```

**Gebruikt in Make.com als:** `{{31.data.timeslots}}`

---

## Functie B — Vertaal Keuzenummer naar Datetime (Scenario 3b)

**Trigger:** Input bevat `data.timeslots` en `data.chosen`

### Input
```json
{
  "timeslots": "2026-03-10 - 10:00-11:00|2026-03-10 - 14:00-15:00|2026-03-12 - 09:00-10:00",
  "chosen": 2
}
```

### Logica
1. Split `timeslots` op `|` → array van strings
2. Pak index `chosen - 1` (1-based → 0-based)
3. Resultaat: `"2026-03-10 - 14:00-15:00"`
4. Split op `" - "` → datum: `"2026-03-10"`, tijdslot: `"14:00-15:00"`
5. Split tijdslot op `"-"` → starttijd: `"14:00"`
6. Bouw ISO datetime: `"2026-03-10T14:00:00.000Z"`

### Output
```json
{
  "timeslot": "2026-03-10 - 14:00-15:00",
  "datetime": "2026-03-10T14:00:00.000Z"
}
```

**Gebruikt in Make.com als:**
- `{{5.data.timeslot}}` → leesbaar tijdslot voor WhatsApp bericht
- `{{5.data.datetime}}` → ISO datetime voor `Trial_Lesson_Date__c` in Salesforce

---

## Hoe aanpassen / opnieuw deployen

1. Ga naar [script.google.com](https://script.google.com)
2. Open het script
3. Maak aanpassingen
4. Klik **Deploy** → **Manage deployments**
5. Klik op de bestaande deployment → **Edit** (potlood icoon)
6. Kies **New version**
7. Klik **Deploy**
8. De URL blijft hetzelfde — geen aanpassing nodig in Make.com

> ⚠️ Bij een nieuwe deployment (niet versie update) verandert de URL. Dan moet de URL in Make.com module 31 en module 5 (Scenario 3b) bijgewerkt worden.

---

## Gebruik per Scenario

| Scenario | Module | Functie | Input | Output gebruikt |
|----------|--------|---------|-------|----------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Module 31 | Functie A | Tally fields[] | `{{31.data.timeslots}}` |
| [Scenario 3b](scenario-3b-ouder-tijdslot-verwerking.md) | Module 5 | Functie B | Available_Timeslots__c + keuzenummer | `{{5.data.timeslot}}`, `{{5.data.datetime}}` |
