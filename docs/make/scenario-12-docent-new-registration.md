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
        ↓
[5]  MailerLite → Create/Update Subscriber (groep: Nieuwe Docent Aanmelding)

[Nog te bouwen]
        ↓
[6]  Email → Bevestigingsmail naar docent
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

## Module 5 — MailerLite Create/Update Subscriber

- **Actie:** Create/Update Subscriber
- **Name:** `{{2.FirstName}}`
- **Last name:** `{{2.LastName}}`
- **Email:** `{{2.PersonEmail}}`
- **Groep:** `Nieuwe Docent Aanmelding`

---

## Bevestigingsmail (module 6 — nog te bouwen)

| Eigenschap | Waarde |
|-----------|--------|
| **Onderwerp** | `Welkom bij Bright Panda Bijles – we hebben je aanmelding ontvangen!` |
| **Afzender** | `teachers@brightpanda.nl` (alias van info@ — nog te regelen) |
| **Inhoud** | Ontvangstbevestiging + verwachte doorlooptijd |

---

## Nog te bouwen

| Onderdeel | Status | Details |
|-----------|--------|---------|
| Bevestigingsmail docent | ❌ Nog te bouwen | Module 6 — afzender teachers@brightpanda.nl (alias aanmaken) |
| Morning briefing | ❌ Nog te bouwen | Dagelijks overzicht via Claude.ai (Salesforce MCP verbinding) |
| Docent profielformulier | ❌ Nog te bouwen | Tally Form 3 uitbreiden: geboortedatum, vakken+niveau, IBAN, AVG checkbox |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 13](scenario-13-docent-lifecycle.md) | Verwerkt lifecycle updates (Interview Invited → Contracting → On-boarded) |
