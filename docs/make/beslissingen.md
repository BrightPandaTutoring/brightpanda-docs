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

### B36 — Checkbox velden in router: Text operators, niet Boolean
- **Keuze:** In Make.com router filters voor checkbox velden: operator **Text — Equal to** gebruiken met waarde `"false"` of `"true"` als tekst
- **Reden:** Boolean operators werken niet correct voor Salesforce checkbox velden in Make.com routers — de vergelijking geeft onverwachte resultaten
- **Bewijs:** `Trial_Class_Reminder_48h_Sent__c` filter werkte niet met Boolean → opgelost met Text operator
- **Geldt voor:** Alle checkbox velden in alle router filters (Scenarios 6, 8, enz.)

### B37 — SOQL tijdsfilter via formatDate(addHours()) patroon
- **Keuze:** Tijdsgebaseerde filters in SOQL WHERE clause: `{{formatDate(addHours(now; -X); "YYYY-MM-DDTHH:mm:ss")}}Z`
- **Reden:** Tijdsfiltering in Make.com router is onbetrouwbaar voor DateTime vergelijkingen — SOQL WHERE clause is nauwkeuriger en eenvoudiger
- **Patroon:** `AND Veld__c < {{formatDate(addHours(now; -24); "YYYY-MM-DDTHH:mm:ss")}}Z` voor "ouder dan 24 uur"
- **Gebruik:** Scenarios 6, 7, 8, 03 (Reminders & Escalatie)

### B38 — TinyURL Pro plan
- **Keuze:** TinyURL Pro plan ($13/maand, 250 links/maand) met branded domain `go.brightpanda.nl`
- **Reden:** Professionele verkorte URL's voor ouders en docenten; branded domain versterkt vertrouwen
- **DNS:** CNAME `go → hrj2vlx.customer.tinyurl.com` in Squarespace (brightpanda.nl DNS)
- **Status:** DNS propagatie in behandeling — tot activatie: geen `"domain"` parameter in JSON

### B39 — Squarespace beheert brightpanda.nl DNS
- **Keuze:** DNS records voor `brightpanda.nl` worden beheerd via Squarespace
- **Gevolg:** TinyURL CNAME (`go → hrj2vlx.customer.tinyurl.com`) toevoegen in Squarespace DNS panel
- **Propagatietijd:** Tot 4 uur — daarna "Check Now" klikken in TinyURL dashboard

### B40 — No Show + Stopped na parent_timeslot_final
- **Keuze:** Na versturen van `parent_timeslot_final` (72u zonder reactie): `Trial_Lesson_Status__c = No Show` en `Status__c = Stopped`
- **Reden:** Matching is definitief beëindigd — geen verdere automatisering actief
- **Toekomst:** Re-engagement flow na 30 dagen (WhatsApp + MailerLite) — nog te bouwen

### B41 — Picker v11: geen Tally Form 2 link bij no_match

- **Keuze:** De "geen tijdslot past" knop op de picker pagina toont in v11 geen Tally Form 2 link meer
- **Reden:** Tally Form 2 was verwarrend — ouder hoefde niets in te vullen. De docent neemt contact op en vult het tijdslot zelf in via Tally Form 3
- **Nieuwe tekst:** "Geen probleem! De docent van [leerlingnaam] neemt zo snel mogelijk contact met je op om samen een tijdslot af te spreken."
- **Gevolg:** Scenario 3b Pad B stuurt de docent automatisch alle benodigde info (ouder contactgegevens + Tally Form 3 link)

---

### B42 — Scenario 2 trigger: Immediately (niet elke minuut)
- **Keuze:** Webhook scenarios activeren op "Immediately" — geen polling interval nodig
- **Reden:** Webhook scenarios reageren op inkomende data — een polling interval voegt latency toe en is overbodig
- **Bewijs:** Scenario 2 stond op "Every 1 minute" → gewijzigd naar "Immediately" → snellere verwerking

### B43 — Default matching status: --None-- (niet Trial Class)
- **Keuze:** Nieuwe matchings aanmaken met `Status__c = --None--` of leeg, niet `Trial Class`
- **Reden:** `Trial Class` als standaardwaarde triggert Scenario 1 op historische/test-data. Scenario 1 filtert op `Trial_Lesson_Status__c = 'Trial Class' AND Teacher_Invited_At__c = NULL`

### B44 — Docent lifecycle via Make.com (Scenario 13) — geen Salesforce Flow
- **Keuze:** Lifecycle updates (MailerLite, DocuSeal, Offboarded_Date__c) via Make.com Watch Records
- **Reden:** Make.com is de centrale orchestratieplek — Salesforce Flows voegen complexiteit toe zonder voordeel
- **Gevolg:** `Offboarded_Date__c` wordt ingevuld via Scenario 13 Route 4

### B45 — DocuSeal voor contracten ($0.20/contract)
- **Keuze:** DocuSeal EU plan voor e-signatures
- **Reden:** Goedkoop ($0.20/contract via Make.com), EU-server, eenvoudige template-gebaseerde workflow
- **Template ID:** `485548`, **Endpoint:** `https://api.docuseal.eu/submissions`
- **Status:** Beslissing nog niet definitief — bevestig voor live gaan

### B46 — Contract verlenging: handmatige beoordeling
- **Keuze:** Geen automatische contractverlenging — Salesforce Flow triggert `Contract Expiring Soon` na 335 dagen (30 dagen voor einde), daarna handmatig beslissen
- **Reden:** Verlenging vereist beoordeling van prestaties docent

### B47 — IBAN in Tally formulier (AVG-compliant)
- **Keuze:** Docent vult IBAN in via Tally profielformulier met verplichte AVG toestemmingscheckbox
- **Reden:** Tally is acceptabel voor opslaan bankgegevens mits expliciete toestemming via checkbox
- **Gevolg:** Tally antwoorden via Make.com naar `IBAN__c` veld op Teacher Account

### B48 — Morning briefing via Claude.ai (Salesforce MCP)
- **Keuze:** Dagelijkse briefing voor Bright Panda team via Claude.ai met Salesforce MCP verbinding
- **Reden:** Centrale plek voor AI-analyses (Scenario 12 aanbevelingen) en overzicht nieuwe aanmeldingen
- **Status:** Salesforce MCP config aangemaakt (`~/.config/claude/claude_desktop_config.json`) — verbinding nog te testen
- **Geen aparte WhatsApp/email** voor interne briefings

### B49 — MailerLite merge tags: `{$field_name}` (niet `{field_name}`)
- **Keuze:** Merge tags in MailerLite e-mails schrijven als `{$naam}` met dollarteken
- **Reden:** `{naam}` (zonder `$`) werkt niet in MailerLite — variabelen worden dan niet ingevuld
- **Bewijs:** Student naam en docent naam in intro tekst automations hadden geen `$` → tekst toonde letterlijk `{naam}`

### B50 — Scenario 11 tijdzone: dynamisch na zomertijd
- **Keuze (tijdelijk):** `+01:00` hardcoded (wintertijd CET) in Scenario 11 SOQL
- **Fix (toekomst):** `{{formatDate(addMinutes(now; -60); "YYYY-MM-DDTHH:mm:ssZ"; "Europe/Amsterdam")}}` testen na zomertijd overgang
- **Impact:** In zomertijd (CEST, +02:00) wordt de les 1 uur te laat gedetecteerd

---

## Openstaande Acties (To-do)

| Actie | Prioriteit | Details |
|-------|-----------|---------|
| DocuSeal beslissing bevestigen | Hoog | Bevestig DocuSeal EU plan vóór live gaan (Scenario 13) |
| Scenario 11 tijdzone fix | Hoog | `+01:00` vervangen door dynamische tijdzone na zomertijd overgang |
| trial_lesson_confirmation_parent template | Medium | V4 pending — wacht op Meta goedkeuring als Utility zonder button |
| availability_conflict templates opnieuw indienen | Medium | Beide templates opnieuw indienen bij 360dialog met voorbeeldwaarden |
| Claude Desktop MCP testen | Medium | Salesforce MCP verbinding testen in Claude Desktop voor morning briefing |
| Scenario 12: bevestigingsmail docent bouwen | Medium | Automatische ontvangstbevestiging bij nieuwe docent aanmelding |
| Docent profielformulier bouwen | Medium | Tally form: adres, vakken+niveau, IBAN, AVG checkbox, optioneel paspoort |
| parent_timeslot_final video vs afbeelding | Medium | Video speelt niet automatisch af in WhatsApp — overweging: vervangen door afbeelding |
| Re-engagement flow bouwen | Laag | Na `No Show` + `Stopped - Never Converted`: WhatsApp + MailerLite na 30 dagen |
| Contract_Start_Date__c veld aanmaken | Laag | Date veld op Teacher Account — nodig voor Scenario 13 Route 2 |
| Picker hosten op brightpanda.nl | Laag | Webflow redirect — professionelere URL voor ouders |
| Meta Business Verificatie | Laag | KvK 84707577 — naam zichtbaar bij ontvanger |
| Morning briefing format uitwerken | Laag | Dagelijks overzicht via Claude.ai met Salesforce MCP |
