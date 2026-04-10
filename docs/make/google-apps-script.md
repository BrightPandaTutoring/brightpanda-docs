# Google Apps Script

Drie scripts voor de Bright Panda automatisering.

---

## Overzicht

| Script | Naam | URL | Methode | Gebruikt in |
|--------|------|-----|---------|------------|
| Script 1 | Vakvertaling | `AKfycbyfkKu...` | GET | Scenario 01 module 10 |
| Script 2 | Tijdslotverwerking | `AKfycbxJDpq...` | POST | Scenario 02 module 31 |
| Script 3 | Tijdslot Picker v10 | `AKfycbyrP2j...` | GET (HTML pagina) + POST (webhook) | Scenario 02 → ouder → Scenario 3b |

---

## Script 1 — Vakvertaling (Scenario 01 module 10)

**Volledige URL:**
`https://script.google.com/macros/s/AKfycbyfkKuHurbErhMZkl_GAAtDImsd9SzLyc9qi3-qYdm3kuf7m1kylo5joO_DfbijH1M-0Q/exec`

**Methode:** GET
**Parse response in Make.com:** NO (uitgeschakeld)
**Output chip:** `{{10.data}}`

**Aanroep in Make.com:**
```
GET [URL]?subject={{encodeURL(1.Subject_s__c)}}
```

> ⚠️ **Parse response: NO** — het script retourneert plain text. Als je Parse response aanzet, geeft Make.com een parse error.

> **Meerdere vakken:** `Subject_s__c` kan puntkomma-gescheiden vakken bevatten (bijv. `"Mathematics A;Biology"`). Het script splitst automatisch op `;`, vertaalt elk vak apart, en retourneert een kommagescheiden Nederlandse string (bijv. `"Wiskunde A, Biologie"`). Output chip: `{{MODULE_NUMMER.data}}`.

### Vertaaltabel (31 vakken)

| Engels (Salesforce) | Nederlands (WhatsApp) |
|--------------------|-----------------------|
| Mathematics A | Wiskunde A |
| Mathematics B | Wiskunde B |
| Mathematics C | Wiskunde C |
| Mathematics D | Wiskunde D |
| Physics | Natuurkunde |
| Chemistry | Scheikunde |
| Biology | Biologie |
| Economics | Economie |
| Business Economics | Bedrijfseconomie |
| Accounting | Bedrijfseconomie |
| Geography | Aardrijkskunde |
| History | Geschiedenis |
| Dutch | Nederlands |
| English | Engels |
| French | Frans |
| German | Duits |
| Spanish | Spaans |
| Latin | Latijn |
| Greek | Grieks |
| Computer Science | Informatica |
| General Science | Natuur- en Scheikunde 1 |
| Nature & Technology | Natuur & Technologie |
| Philosophy | Filosofie |
| Art | Tekenen/CKV |
| Social Studies | Maatschappijleer |
| Economics & Society | Maatschappijwetenschappen |
| Physical Education | Lichamelijke opvoeding |
| Music | Muziek |
| Drama | Drama |
| Management & Organization | M&O |
| Care & Welfare | Zorg & Welzijn |

> Onbekend vak: script retourneert de originele naam ongewijzigd.

### Script Code (Script 1 — met meerdere vakken ondersteuning)

```javascript
function doGet(e) {
  const subject = e.parameter.subject || "";
  const subjects = subject.split(";").map(s => s.trim());
  const translations = {
    "Mathematics A": "Wiskunde A",
    "Mathematics B": "Wiskunde B",
    "Mathematics C": "Wiskunde C",
    "Mathematics D": "Wiskunde D",
    "Physics": "Natuurkunde",
    "Chemistry": "Scheikunde",
    "Biology": "Biologie",
    "Economics": "Economie",
    "Business Economics": "Bedrijfseconomie",
    "Accounting": "Bedrijfseconomie",
    "Geography": "Aardrijkskunde",
    "History": "Geschiedenis",
    "Dutch": "Nederlands",
    "English": "Engels",
    "French": "Frans",
    "German": "Duits",
    "Spanish": "Spaans",
    "Latin": "Latijn",
    "Greek": "Grieks",
    "Computer Science": "Informatica",
    "General Science": "Natuur- en Scheikunde 1",
    "Nature & Technology": "Natuur & Technologie",
    "Philosophy": "Filosofie",
    "Art": "Tekenen/CKV",
    "Social Studies": "Maatschappijleer",
    "Economics & Society": "Maatschappijwetenschappen",
    "Physical Education": "Lichamelijke opvoeding",
    "Music": "Muziek",
    "Drama": "Drama",
    "Management & Organization": "M&O",
    "Care & Welfare": "Zorg & Welzijn"
  };
  const results = subjects.map(s => translations[s] || s);
  return ContentService.createTextOutput(results.join(", ")).setMimeType(ContentService.MimeType.TEXT);
}
```

---

## Script 2 — Tijdslotverwerking (Scenario 02 module 31)

**Volledige URL:**
`https://script.google.com/macros/s/AKfycbxJDpq3i4b7kafFE3Sc1ZFUck2ii7zTCBpXrbrVKlMGYfsyjeMURYXkCAy8SDxigk4f/exec`

**Methode:** POST
**Parse response in Make.com:** YES
**Output chips:** `{{31.data.timeslots}}` en `{{31.data.timeslotsRaw}}`

### Waarom Google Apps Script?

Na 3+ uur debuggen bleek dat Tally `INPUT_DATE` velden in Make.com worden omgezet naar **date objects**. Geen enkele Make.com functie kon de datum als string concateneren (`toString`, `formatDate`, `&`).

**Oplossing:** Datum als JSON string sturen met aanhalingstekens om de chip: `"3": "{{1.data.fields[3].value}}"` — de aanhalingstekens forceren JSON serialisatie als string.

### Deploy Instellingen

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
5. Kies **New version** → **Deploy**
7. URL blijft hetzelfde — geen aanpassing nodig in Make.com

### Functie A — Input (Scenario 02)

```json
{
  "fields": {
    "3": "2026-03-10",
    "18": "2026-03-12",
    "33": "",
    "48": "",
    "63": "",
    "5": false,
    "6": true,
    "7": true,
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

### Functie A — Output

| Variabele | Inhoud | Gebruik |
|-----------|--------|---------|
| `{{31.data.timeslots}}` | Genummerde string voor WhatsApp | Informatief in bericht (niet opgeslagen) |
| `{{31.data.timeslotsRaw}}` | Ruwe datumnotatie pipe-separated | Opgeslagen in `Available_Timeslots__c`, gebruikt door Picker |

```json
{
  "timeslots": "1. ma 10 mrt 10:00-11:00|2. ma 10 mrt 11:00-12:00|3. vr 14 mrt 09:00-10:00",
  "timeslotsRaw": "2026-03-10 - 10:00-11:00|2026-03-10 - 11:00-12:00|2026-03-14 - 09:00-10:00"
}
```

### Volledige Script Code (Script 2 — Versie 2)

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);

  if (data.fields) {
    const fields = data.fields;
    const times = [
      "08:00-09:00","09:00-10:00","10:00-11:00","11:00-12:00",
      "12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00",
      "16:00-17:00","17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00"
    ];
    const dateFields = [3, 18, 33, 48, 63];
    const slotStarts = [5, 20, 35, 50, 65];
    const dagNamen = ["zo","ma","di","wo","do","vr","za"];
    const maandNamen = ["jan","feb","mrt","apr","mei","jun","jul","aug","sep","okt","nov","dec"];

    let timeslotsArr = [];
    let timeslotsRawArr = [];

    for (let d = 0; d < 5; d++) {
      const datum = fields[dateFields[d]];
      if (!datum) continue;
      const dateObj = new Date(datum);
      const dagNaam = dagNamen[dateObj.getUTCDay()];
      const dag = dateObj.getUTCDate();
      const maand = maandNamen[dateObj.getUTCMonth()];

      for (let t = 0; t < 13; t++) {
        if (fields[slotStarts[d] + t] === true) {
          timeslotsArr.push(dagNaam + " " + dag + " " + maand + " " + times[t]);
          timeslotsRawArr.push(datum + " - " + times[t]);
        }
      }
    }

    const numbered = timeslotsArr.map((s, i) => (i+1) + ". " + s).join("|");

    return ContentService
      .createTextOutput(JSON.stringify({
        timeslots: numbered,
        timeslotsRaw: timeslotsRawArr.join("|")
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

---

## Script 3 — Tijdslot Picker v10 (Scenario 02 → Scenario 3b)

**Volledige URL:**
`https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec`

**Bestandsnaam:** `BrightPanda_TimeslotPicker_v10.gs`
**Type:** Web App — geeft HTML pagina terug
**Versie:** 10

### Doel

Vervangt Tally Form 2. De ouder opent een HTML pagina met alle beschikbare tijdsloten van de docent als klikbare knoppen. Bij klik stuurt de pagina een POST naar het Scenario 3b webhook.

### URL Parameters (input)

| Parameter | Inhoud | Bron |
|-----------|--------|------|
| `slots` | URL-encoded `timeslotsRaw` string | `{{encodeURL(31.data.timeslotsRaw)}}` |
| `matching` | URL-encoded matching naam | `{{encodeURL(3.Name)}}` |
| `student_name` | URL-encoded voornaam student | `{{encodeURL(4.FirstName)}}` |
| `parent_name` | URL-encoded naam ouder | `{{encodeURL(4.ParentsName__c)}}` |

**Voorbeeld URL:**
```
https://script.google.com/macros/s/AKfycbyrP2j.../exec?slots=2026-03-10%20-%2010%3A00-11%3A00%7C2026-03-10%20-%2011%3A00-12%3A00&matching=Matching%20Number%200016&student_name=Emma&parent_name=Miriam
```

### Output — POST naar Scenario 3b Webhook

Bij klik op tijdslot (Pad A):
```json
{
  "matching_number": "Matching Number 0016",
  "student_name": "Emma",
  "chosen": 2,
  "chosen_date": "ma 10 mrt",
  "chosen_date_iso": "2026-03-10",
  "chosen_time": "10:00-11:00",
  "chosen_start_time": "10:00",
  "status": "chosen"
}
```

Bij klik op "Geen tijdslot past" (Pad B):
```json
{
  "matching_number": "Matching Number 0016",
  "student_name": "Emma",
  "status": "no_match"
}
```

### Architect beslissingen

| Beslissing | Reden |
|------------|-------|
| `chosen_start_time` apart sturen | `chosen_time` bevat "10:00-11:00" — voor `Trial_Lesson_Date__c` is alleen "10:00" nodig |
| Datum zonder Z opslaan in Salesforce | Met Z (UTC) toont Salesforce de tijd 1 uur later in NL tijdzone |
| `chosen_date` als leesbare string | "ma 10 mrt" is vriendelijker in WhatsApp dan "2026-03-10" |
| Toekomstig: hosten op brightpanda.nl | GAS URL is lang en onprofessioneel — Webflow redirect aanmaken |

---

## Deploy Instellingen (alle scripts)

| Instelling | Waarde |
|-----------|--------|
| Execute as | Me |
| Access | Anyone (geen login vereist) |

> ⚠️ Bij een **nieuwe** deployment verandert de URL. Dan moeten alle Make.com modules die de URL gebruiken bijgewerkt worden.
