# Scenario 12 — Docent New Registration (Claude AI Analyse)

**Laatste update:** 10 april 2026
**Status:** 🔧 In aanbouw — Claude analyse werkend, bevestigingsmail en morning briefing nog te bouwen

---

## Doel

Analyseert automatisch nieuwe docent-aanmeldingen met **Claude AI** en schrijft een aanbeveling terug naar Salesforce. Bright Panda ziet in de ochtend via de morning briefing of een docent een interview verdient, een twijfelgeval is, of afgewezen moet worden.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Watch Records |
| Object | Account |
| Volgorde | By Created Time |
| Limit | 10 per run |
| Interval | Elke 15 minuten |
| Filter | `RecordTypeId = 012KB000000ojZLYAY` AND `Lifecycle_Stage__c = New` |

---

## Module Volgorde

```
[1]  Salesforce → Watch Records (Teacher Account filter)
        ↓
[2]  Salesforce → Get a Record (Teacher Account — volledige data)
        ↓
[3]  HTTP POST → Anthropic API (Claude analyse)
        ↓
[4]  Salesforce → Update a Record (Claude_Recommendation__c)

[Nog te bouwen]
        ↓
[5]  Email → Bevestiging naar docent
[6]  Morning briefing trigger
```

---

## Module 2 — Get Teacher Account

- **Record ID:** `{{1.Id}}`
- **Output:** `{{2.Name}}`, `{{2.Subject_s__c}}`, `{{2.Study__c}}`, `{{2.University__c}}`, `{{2.MailingCity}}`, `{{2.Birthdate}}`, `{{2.Comments_FromWebForm__c}}`, `{{2.ReferredToBPVia__c}}`

---

## Module 3 — HTTP POST → Anthropic API

**Endpoint:** `https://api.anthropic.com/v1/messages`
**Header:** `x-api-key: [Bright Panda Make.com API key]`
**Header:** `anthropic-version: 2023-06-01`

```json
{
  "model": "claude-opus-4-6",
  "max_tokens": 1024,
  "system": "{{zie system prompt hieronder}}",
  "messages": [{
    "role": "user",
    "content": "Naam: {{2.Name}}\nVakken: {{2.Subject_s__c}}\nStudie: {{2.Study__c}}\nUniversiteit: {{2.University__c}}\nLocatie: {{2.MailingCity}}\nGeboortedatum: {{2.Birthdate}}\nOpmerkingen: {{2.Comments_FromWebForm__c}}\nVia: {{2.ReferredToBPVia__c}}"
  }]
}
```

**Output:** `{{3.data.content[].text}}` → bevat de aanbeveling als tekst

---

## Claude Analyse System Prompt

```
Je bent een recruiter voor Bright Panda Bijles, een bijlesplatform dat leerlingen in het voortgezet onderwijs koppelt aan studenten die bijles geven.

Analyseer de volgende docent-aanmelding en geef een aanbeveling in het volgende format:

BESLISSING: [INTERVIEW AANRADEN / TWIJFELGEVAL / AFWIJZEN]

ONDERBOUWING:
[2-4 zinnen waarom]

AANDACHTSPUNTEN:
[Eventuele vragen of aandachtspunten voor het interview]

Gebruik de volgende criteria:

VAKKEN (prioriteit hoog):
- Hoge vraag: Wiskunde A, Wiskunde B, Scheikunde, Natuurkunde, Economie, Bedrijfseconomie, Nederlands, Engels, Frans
- Extra waardevol: Arabisch, Russisch, Turks, Italiaans (zeldzaam)
- Lage prioriteit: vakken met weinig aanvragen

OPLEIDING:
- Voorkeur: WO (universiteit)
- Prima: HBO
- Minder geschikt: MBO of lager

LEEFTIJD:
- Minimaal 18 jaar
- 18-26 jaar: ideaal (student-profiel)
- 26+ jaar: mogelijk als "Pro Docent" als ervaring dit rechtvaardigt

LOCATIE:
- Online geven is altijd mogelijk
- Grote steden (Amsterdam, Rotterdam, Den Haag, Utrecht) hebben meer leerlingen
- Kleine steden: meer kans op online

ERVARING:
- Bijleservaring: pluspunt, maar niet vereist
- Eerste bijles: prima als profiel verder sterk is

Wees beknopt maar concreet. Geef altijd een duidelijke beslissing.
```

---

## Module 4 — Salesforce Update

- **Record ID:** `{{1.Id}}`
- `Claude_Recommendation__c` = `{{3.data.content[].text}}`

---

## Salesforce Veld: Claude_Recommendation__c

| Eigenschap | Waarde |
|-----------|--------|
| **Type** | Text Area (Long) |
| **API naam** | `Claude_Recommendation__c` |
| **Object** | Account (Teacher) |
| **Zichtbaar voor** | Bright Panda intern |

**Voorbeeldwaarde:**
```
BESLISSING: INTERVIEW AANRADEN

ONDERBOUWING:
Sterke kandidaat — WO Wiskunde aan UvA, geeft bijles in Wiskunde A en B. 
Grote vraag naar Wiskunde in Amsterdam. Geen ervaring, maar sterk profiel.

AANDACHTSPUNTEN:
- Vraag naar beschikbaarheid per week
- Check of online of in-person voorkeur heeft
```

---

## Nog te bouwen

| Onderdeel | Status | Details |
|-----------|--------|---------|
| Bevestigingsmail docent | ❌ Nog te bouwen | Automatische ontvangstbevestiging na aanmelding |
| Morning briefing | ❌ Nog te bouwen | Dagelijks overzicht nieuwe aanmeldingen + Claude aanbevelingen via Claude.ai (Salesforce MCP) |
| Docent profielformulier | ❌ Nog te bouwen | Tally form met: adres, vakken+niveau, IBAN, AVG checkbox, optioneel paspoort |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 13](scenario-13-docent-lifecycle.md) | Verwerkt lifecycle updates (Interview Invited → Contracting → On-boarded) |
