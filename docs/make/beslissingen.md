# Beslissingen & Afspraken

Overzicht van alle technische en functionele beslissingen gemaakt tijdens de bouw van de Make.com automatisering.

---

## Technische Beslissingen

### B01 — Set Variable module buiten JSON voor `replace()` formule
- **Keuze:** Formules met aanhalingstekens altijd buiten JSON berekenen in een aparte Set Variable module
- **Reden:** Dubbele aanhalingstekens in Make.com formules conflicteren altijd met JSON string opmaak
- **Gevolg:** Gebruik `{{X.variabelenaam}}` in JSON, nooit de formule zelf

### B02 — Backticks in `switch()` binnen JSON, niet in `replace()`
- **Keuze:** `switch()` in JSON body gebruikt backticks: `` switch(x; `A`; `B`) ``
- **Let op:** Backticks werken **alleen** in `switch()`, **niet** in `replace()` (geeft NaN error)

### B03 — Available_Timeslots__c als persistente opslag
- **Keuze:** `timeslotsRaw` string opslaan in Salesforce veld op matching record
- **Reden:** Make.com heeft geen geheugen tussen scenario-runs. Scenario 3b heeft de lijst nodig die Scenario 02 bouwde.
- **Veldformat:** `2026-03-10 - 10:00-11:00|2026-03-10 - 11:00-12:00`

### B04 — Checkboxes in Tally Form 1
- **Keuze:** Tijdsloten als Checkboxes (niet Multi-select)
- **Reden:** Betere compatibiliteit met Make.com processing

### B05 — SOQL Query in plaats van Filter dropdown
- **Keuze:** Salesforce Search Records gebruikt SOQL Query mode, niet de Filter dropdown
- **Reden:** Filter dropdown toont veldlabels, niet het `Name` veld

### B06 — Ouder contactgegevens van Student Account (niet Contact SOQL)
- **Keuze:** `ParentsName__c` en `ParentSPhone__c` custom velden direct van het Student Account
- **Reden:** Ouders zijn geen Contact records in Salesforce — custom velden op Account zijn de correcte bron
- **Impact:** Geen aparte Contact SOQL module nodig in Scenario 01, 02 en 3b

### B07 — Google Apps Script voor vakvertaling (Scenario 01)
- **Keuze:** Aparte GET-aanroep naar Script 1 voor vertaling Engelse → Nederlandse vaknaam
- **Reden:** `switch()` in Make.com JSON conflicteert; 31 vakken is te lang voor betrouwbare formule
- **Implementatie:** Module 10, GET, Parse response: NO, output via `{{10.data}}` chip

### B08 — encodeURL() voor spaties in URL parameters
- **Keuze:** `encodeURL()` gebruiken voor alle strings met spaties in URL parameters
- **Reden:** "Matching Number 0016" bevat spaties → URL breekt in WhatsApp
- **Gebruik:** `encodeURL(1.Name)` in Tally links, `encodeURL(31.data.timeslotsRaw)` in picker URL

### B09 — & als literal in JSON body URL (niet %26)
- **Keuze:** `&` gebruiken in JSON body URL parameter strings
- **Reden:** `%26` gaf JSON coderingsproblemen; literal `&` in een JSON string-waarde werkt correct

### B10 — Trial_Lesson_Date__c opslaan zonder Z suffix
- **Keuze:** DateTime opslaan als `{{3.chosen_date_iso}}T{{3.chosen_start_time}}:00.000` — zonder `Z`
- **Reden:** Met `Z` interpreteert Salesforce de tijd als UTC → toont 1 uur later in Europe/Amsterdam
- **Bewijs:** Proefles om 10:00 werd weergegeven als 11:00 → Z verwijderd → correct

### B11 — chosen_start_time apart meesturen vanuit picker
- **Keuze:** Picker stuurt `chosen_start_time` als apart veld via `selectedTime.split("-")[0]`
- **Reden:** `chosen_time` bevat "10:00-11:00" — voor DateTime opslag is alleen "10:00" nodig
- **Zonder dit:** `Trial_Lesson_Date__c` bevatte "11:00" (eindtijd) in plaats van "10:00"

### B12 — Tally Form 2 vervangen door Google Apps Script picker
- **Keuze:** Picker pagina (Script 3) in plaats van Tally Form 2 voor ouder tijdslot keuze
- **Reden:** Betere UX — ouder klikt op tijdslot knop in plaats van getal typen; geen Tally Pro plan nodig
- **Gevolg:** Scenario 3b ontvangt nu van GAS picker via webhook, niet meer van Tally Form 2
- **Tally Form 2 URL:** Blijft beschikbaar als fallback bij no_match knop op picker pagina

### B13 — Trial_Lesson_Status__c filter voorkomt dubbele berichten (Scenario 01)
- **Keuze:** Filter op `Trial_Lesson_Status__c = leeg` in Scenario 01
- **Reden:** Zonder filter stuurt het scenario elke 15 minuten een nieuwe WhatsApp naar de docent

### B14 — API key altijd kopiëren van werkende module
- **Keuze:** API key nooit handmatig overtypen — altijd copy-paste van bestaande werkende module
- **Reden:** Typefout tussen `I` (hoofdletter i) en `l` (kleine letter L) is onzichtbaar in Make.com editor
- **Bewijs:** Module 12 in Scenario 3b gaf "Invalid API token" door typefout in handmatig overgetypte key

### B15 — Lange Make.com formules vermijden
- **Keuze:** Formules met meer dan ~13 geneste `if`-statements niet gebruiken in Make.com
- **Reden:** Lange formules raken corrupt bij opslaan — tokens lijken correct maar geven lege output
- **Alternatief:** Google Apps Script voor alle complexe logica

### B16 — timeslotsRaw vs timeslots (twee outputs van Script 2)
- **Keuze:** Script 2 geeft twee outputs: genummerd voor WhatsApp (`timeslots`), ruw voor opslag (`timeslotsRaw`)
- **Reden:** WhatsApp template toonde genummerde lijst "1. ma 10 mrt 10:00-11:00". Picker pagina heeft ISO datumnotatie nodig voor correcte verwerking.
- **Salesforce opslag:** `Available_Timeslots__c` = `timeslotsRaw`

---

## Functionele Beslissingen

### B17 — Ouder kiest tijdslot via klikbare knop op picker pagina
- **Keuze:** Google Apps Script HTML pagina met klikbare tijdsloten (Script 3)
- **Reden:** Dropdown werkt niet dynamisch in Tally zonder betaald plan; tekstveld geeft typefouten; picker is professioneler
- **Afgewezen:** Vrije tekstinvoer, dropdown (Tally Pro), Tally Number field

### B18 — Nummering per tijdslot (niet per datum)
- **Keuze:** Elke datum+tijdslot combinatie krijgt een uniek oplopend getal
- **Reden:** Ouder moet exact tijdslot kunnen kiezen, niet alleen een datum

### B19 — Alleen hele uren in tijdsloten (13 opties per datum)
- **Keuze:** 13 opties van 08:00-09:00 t/m 20:00-21:00
- **Uitbreidbaar** naar halve uren later

### B20 — Telefoonnummers uitwisselen pas bij bevestiging
- **Keuze:** Docent en ouder krijgen elkaars telefoonnummer pas in de `trial_lesson_confirmation` berichten
- **Reden:** Privacy — alleen relevant als proefles definitief ingepland is

### B21 — Verzetten en annuleren gaat handmatig
- **Keuze:** Geen automatisering voor verzetten of annuleren van proeflessen
- **Reden:** Te complex, valt buiten scope. Contactgegevens staan in WhatsApp berichten.

### B22 — Escalaties via WhatsApp naar intern nummer
- **Keuze:** Escalatiemeldingen via WhatsApp naar `+31613689666`
- **Reden:** Redundantie — escalaties mogen niet gemist worden

### B23 — Reminder naar docent elke 3 uur bij Availability Conflict
- **Keuze:** Polling scenario elke 15 min — bij `Availability Conflict` + `Trial_Lesson_Date__c` leeg → reminder elke 3 uur
- **Reden:** Docent moet snel actie ondernemen door ouder te bellen
- **Status:** Nog te bouwen

### B24 — Bij no_match belt docent de ouder
- **Keuze:** Bij Pad B (geen tijdslot past) instrueert Bright Panda de docent om de ouder te bellen
- **Reden:** Ouder geeft alternatieve beschikbaarheid op in Tally Form 2 (link staat op picker pagina) — maar afgesproken datum wordt handmatig bevestigd
- **Docent vult daarna:** Via een nieuw form het afgesproken tijdslot in → Salesforce update

### B25 — 360dialog gekozen boven Twilio
- **Keuze:** 360dialog (EUR 49/maand flat) in plaats van Twilio (pay-per-message)
- **Break-even:** ~110 proeflessen/maand bij ~10 berichten per proefles

### B26 — Picker later hosten op brightpanda.nl
- **Keuze:** Webflow redirect van brightpanda.nl naar GAS URL
- **Reden:** GAS URL is lang en onprofessioneel voor ouders
- **Status:** Toekomstige verbetering — lage urgentie

---

## Template Beslissingen

### B27 — Templates indienen als Utility, zonder emoji
- **Keuze:** Geen emoji's in template tekst, handmatig categorie "Utility" selecteren bij indiening
- **Reden:** Meta classificeert templates met emoji's als Marketing — langere wachttijd + hogere kosten
- **Bewijs:** `teacher_invitation` → Marketing → opnieuw aangemaakt als Utility ✅

### B28 — Disclaimer toevoegen als allerlaatste stap
- **Keuze:** Disclaimer ("Dit nummer is alleen voor...") toevoegen na volledig testen
- **Reden:** Elke template aanpassing vereist opnieuw Meta goedkeuring (wachttijd: 2-7 dagen)

### B29 — Meta Business Verificatie later
- **Keuze:** Op to-do lijst, niet urgent
- **Wat het oplevert:** "Bright Panda Bijles" naam zichtbaar bij ontvanger (KvK 84707577)

---

## Webhook Module Nummering

| Scenario | Webhook module | Gebruik in formules |
|----------|---------------|---------------------|
| Scenario 02 | Module 1 | `{{1.data.fields[...]}}` |
| Scenario 3b | Module 3 | `{{3.variabelenaam}}` |

> ⚠️ Fout modulenummer geeft "references non-existing module" waarschuwing in Make.com.

---

## Werkwijze Afspraken

| Afspraak | Detail |
|----------|--------|
| JSON aanlevering | Altijd volledige JSON geven bij HTTP module aanpassingen, nooit partial |
| Stappenbeschrijving | Als bulletpoints, niet als lange lappen tekst |
| Webhook logs | Via linkermenu → Webhooks → Logs (niet via scenario History tab) |
| Formule met `"` in JSON | Stop → gebruik Set Variable module of Google Apps Script |
| Webhook queue | Altijd "Wait for new data" kiezen, nooit "Use existing data" |
| Tally datum in JSON | Aanhalingstekens om datumchips: `"3": "{{1.data.fields[3].value}}"` |
| Checkbox in JSON | `if()`-wrapper: `{{if(1.data.fields[5].value; true; false)}}` |
| API key | Altijd kopiëren van werkende module — nooit handmatig typen |
| DateTime in Salesforce | Zonder Z suffix: `{{chosen_date_iso}}T{{chosen_start_time}}:00.000` |
| URL parameters in JSON | `&` literal gebruiken — niet `%26` |

---

### B30 — MailerLite is geen CRM
- **Keuze:** Salesforce blijft bron van waarheid. MailerLite alleen voor emailcommunicatie.
- **Gevolg:** Docent-specifieke info (naam, matchingdetails) niet opgeslagen in MailerLite — wordt per email meegegeven via Make.com op het moment van versturen.

### B31 — Scenario 10 filter op RecordTypeId voor docenten
- **Keuze:** Filter `RecordTypeId ≠ 012KB000000ojZLYAY` om docenten uit te sluiten van MailerLite
- **Reden:** Docenten zijn ook Person Accounts — zonder filter worden zij als subscriber aangemaakt
- **Aanvulling:** Filter `IsPersonAccount = true` voor alle Company Accounts

### B32 — Vakvertaling splitst op puntkomma
- **Keuze:** Script 1 splitst `Subject_s__c` op `;`, vertaalt elk vak apart, geeft kommagescheiden NL string terug
- **Reden:** Leerling kan meerdere vakken hebben. Eerdere versie behandelde de hele string als één sleutel → geen match.
- **Impact:** Output in MailerLite `subjects` field: `"Wiskunde A, Biologie"` i.p.v. `"Mathematics A;Biology"`

### B33 — TinyURL voor alle externe links in WhatsApp
- **Keuze:** Alle externe URLs (picker, Tally Form 3) eerst verkorten via TinyURL branded domain `go.brightpanda.nl`
- **Reden:** Lange GAS URLs zijn onprofessioneel; branded domain versterkt vertrouwen bij ouders/docenten
- **API token:** `azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji`

### B34 — Geen double opt-in voor MailerLite
- **Keuze:** Ouder wordt direct als Active subscriber aangemaakt — geen bevestigingsmail
- **Reden:** Ouder meldt zich aan via Salesforce web-to-lead (actieve opt-in handeling) — extra bevestiging is niet nodig

### B35 — Teacher_Invited_At__c en Parent_Invited_At__c als timestamp
- **Keuze:** Aparte DateTime velden voor wanneer uitnodiging verstuurd is
- **Reden:** `LastModifiedDate` is onbetrouwbaar voor timing (record kan om andere redenen gewijzigd zijn)
- **Gebruik:** Scenarios 6, 7, 9 berekenen tijdsverschil op basis van deze velden

---

## Openstaande Acties (To-do)

| Actie | Prioriteit | Details |
|-------|-----------|---------|
| Scenario 3b Pad B afbouwen | Hoog | SOQL + Get Student/Teacher + Update `Availability Conflict` + WhatsApp docent |
| Template maken: Availability Conflict docent | Hoog | Instructie om ouder te bellen + contactgegevens — indienen bij Meta als Utility |
| Nieuw polling scenario bouwen | Medium | Elke 15 min — check `Availability Conflict` + `Trial_Lesson_Date__c` leeg → reminder docent elke 3 uur |
| Nieuw scenario: docent vult tijdslot in | Medium | Form → Salesforce update `Trial_Lesson_Date__c` + `Trial Lesson Scheduled` + bevestiging WhatsApp |
| Filter dubbele submissions Scenario 3b | Medium | Voorkomt dat dezelfde submission twee keer verwerkt wordt |
| Reminders 24u en 1u voor proefles | Laag | Herinnering aan ouder en docent vlak voor de proefles |
| Einde-tot-einde test | Hoog | Na Pad B — volledig testen met echt matching record |
| Picker hosten op brightpanda.nl | Laag | Webflow redirect — professionelere URL voor ouders |
| Meta Business Verificatie | Laag | KvK 84707577 — naam zichtbaar bij ontvanger |
| Help tekst bij Trial_Lesson_Status__c | Laag | Tooltip in Salesforce met uitleg wat elke status triggert |
