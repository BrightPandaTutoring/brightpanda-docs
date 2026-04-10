# Beslissingen & Afspraken

Overzicht van alle technische en functionele beslissingen gemaakt tijdens de bouw van de Make.com automatisering.

---

## Technische Beslissingen

### B01 — Set Variable module buiten JSON voor `replace()` formule
- **Keuze:** Formules met aanhalingstekens altijd buiten JSON berekenen in een aparte Set Variable module
- **Reden:** Dubbele aanhalingstekens in Make.com formules conflicteren altijd met JSON string opmaak
- **Gevolg:** Gebruik `{{X.variabelenaam}}` in JSON, nooit de formule zelf
- **Zie ook:** [Scenario 01 module 8](scenario-01-docent-uitnodiging-whatsapp.md)

### B02 — Backticks in `switch()` binnen JSON, niet in `replace()`
- **Keuze:** `switch()` in JSON body gebruikt backticks: `` switch(x; `A`; `B`) ``
- **Reden:** Backticks conflicteren niet met JSON aanhalingstekens
- **Let op:** Backticks werken **alleen** in `switch()`, **niet** in `replace()` (geeft NaN error)

### B03 — Available_Timeslots__c als persistente opslag
- **Keuze:** Genummerde tijdslotenlijst opslaan in Salesforce veld op matching record
- **Reden:** Make.com heeft geen geheugen tussen scenario-runs. Scenario 04 heeft de lijst nodig die Scenario 02 bouwde.
- **Alternatief overwogen:** `timeslots_all` als URL hidden field in Form 2 (URL lengte berekend als voldoende bij max 65 opties, maar Salesforce is robuuster)
- **Veldformat:** `1=12 maart 13:00-14:00|2=12 maart 14:00-15:00`

### B04 — Checkboxes in plaats van Multi-select in Tally Form 1
- **Keuze:** Alle tijdsloten velden gewijzigd van Multi-select naar Checkboxes (10 maart 2026)
- **Reden:** Betere compatibiliteit met Make.com `map()` formule
- **Let op:** Checkboxes sturen ook UUIDs — de UUID→tekst mapping via `options` array blijft altijd nodig

### B05 — SOQL Query in plaats van Filter dropdown
- **Keuze:** Salesforce Search Records gebruikt SOQL Query mode, niet de Filter dropdown
- **Reden:** Filter dropdown toont veldlabels, niet het `Name` veld — `Name` was niet vindbaar via dropdown

### B06 — Ouders ophalen via Contact SOQL, niet via Account veld
- **Keuze:** `SELECT FirstName, Phone FROM Contact WHERE AccountId = '{{account_id}}'`
- **Reden:** Ontdekt dat ouders Contact records zijn in Salesforce, niet een veld (`ParentSPhone__c`) op het student Account
- **Impact:** Alle scenarios die ouder contactgegevens nodig hebben, moeten een aparte SOQL module hebben (Scenario 01 module 9, Scenario 02 module 32, Scenario 3b module 13)

### B07 — Google Apps Script voor vakvertaling (Scenario 01)
- **Keuze:** Aparte GET-aanroep naar Google Apps Script Script 1 voor vertaling Engelse → Nederlandse vaknaam
- **Reden:** `switch()` formule in Make.com JSON body conflicteert met aanhalingstekens; 31 vakcombinaties is te lang voor betrouwbare Make.com formule
- **Implementatie:** Module 10, GET request, Parse response: NO, output via `{{10.body}}`
- **Voordeel:** Vertaaltabel eenvoudig uitbreidbaar in GAS zonder Make.com aanpassing

### B08 — encodeURL() voor matching_number in Tally URL
- **Keuze:** `encodeURL(1.Name)` in plaats van `replace()` voor URL-encoding
- **Reden:** "Matching Number 0016" bevat spaties → URL breekt in WhatsApp. `encodeURL()` converteert naar `Matching%20Number%200016`
- **Gevolg:** Geen Set Variable module nodig voor URL-encoding

### B09 — Parse response: NO voor Google Apps Script aanroepen
- **Keuze:** Parse response uitgeschakeld voor beide GAS scripts
- **Reden Script 1:** Script retourneert plain text — Make.com geeft JSON parse error als Parse response aan staat. Output via `.body` chip.
- **Reden Script 2:** JSON output, maar Parse response kan instabiel zijn — gebruik `{{31.data.timeslots}}` chip direct.

### B10 — Tally field indexering is 0-based
- **Keuze:** Alle Tally field referenties beginnen bij 0: `fields[0]` = eerste veld
- **Reden:** Vastgesteld via analyse van daadwerkelijke webhook data — Make.com toonde initieel misleidende preview
- **Impact:** Scenario 01 SOQL en module 31 JSON body zijn bijgewerkt. `fields[0].value` in Tally Form 1 bevat de volledige matching naam "Matching Number 0016" (niet alleen het getal "0016")

### B11 — Trial_Lesson_Status__c filter voorkomt dubbele berichten (Scenario 01)
- **Keuze:** Filter op `Trial_Lesson_Status__c = leeg` in Scenario 01
- **Reden:** Zonder deze filter stuurt het scenario bij elke trigger opnieuw een WhatsApp naar de docent. Het veld wordt na versturen gevuld met "Teacher Invited", waardoor herhaling geblokkeerd wordt.

---

## Functionele Beslissingen

### B12 — Ouder kiest tijdslot via getal, niet via dropdown
- **Keuze:** Number invoerveld in Form 2 waarbij ouder een getal typt
- **Reden:** Dropdown werkt niet dynamisch in Tally zonder betaald plan; tekstveld geeft typefouten
- **Afgewezen:** Vrije tekstinvoer (typefouten), dropdown (niet dynamisch)

### B13 — Nummering per tijdslot (niet per datum)
- **Keuze:** Elke datum+tijdslot combinatie krijgt een uniek oplopend getal
- **Reden:** Ouder moet exact tijdslot kunnen kiezen, niet alleen een datum
- **Afgewezen:** Nummering per datum (te vaag voor definitieve afspraak)

### B14 — Alleen hele uren in tijdsloten (13 opties per datum)
- **Keuze:** 13 opties van 08:00-09:00 t/m 20:00-21:00
- **Reden:** 26 halve uren is te lang voor de form; in de praktijk volstaat dit
- **Uitbreidbaar** naar halve uren later

### B15 — Telefoonnummers uitwisselen pas bij bevestiging
- **Keuze:** Docent en ouder krijgen elkaars telefoonnummer pas in de `trial_lesson_confirmation`
- **Reden:** Privacy — alleen relevant als proefles definitief ingepland is

### B16 — Verzetten en annuleren gaat handmatig
- **Keuze:** Geen automatisering voor verzetten of annuleren van proeflessen
- **Reden:** Te complex, valt buiten scope. Contactgegevens staan in WhatsApp disclaimer.

### B17 — Escalaties via WhatsApp naar intern nummer
- **Keuze:** Escalatiemeldingen via WhatsApp naar `+31613689666`
- **Reden:** Redundantie — escalaties mogen niet gemist worden
- **Kanalen:** WhatsApp (alle scenario's), Gmail/email (Scenario 03 — ook via email voor redundantie)

### B18 — Inbound WhatsApp messaging niet bouwen
- **Keuze:** Geen automatische verwerking van inkomende WhatsApp berichten
- **Reden:** Te complex, valt buiten scope van dit project

### B19 — Scheduling Scenario 03 op 15 minuten
- **Keuze:** Elke 15 minuten draaien
- **Reden:** Make.com Free plan limiet (ideaal zou elk uur zijn)

### B20 — 360dialog gekozen boven Twilio
- **Keuze:** 360dialog (EUR 49/maand) in plaats van Twilio (pay-per-message)
- **Reden:** Break-even punt berekend op ~110 proeflessen/maand. Bij groei is 360dialog goedkoper. Simpler integratie via directe WhatsApp Business API.
- **Break-even:** Twilio kost ~€0,045 per bericht; bij 110 proeflessen × ~10 berichten per proefles ≈ 1.100 berichten × €0,045 = €49,50

---

## Template Beslissingen

### B21 — Templates pas aanpassen na volledig testen
- **Keuze:** Disclaimer toevoegen als allerlaatste stap
- **Reden:** Elke template aanpassing vereist opnieuw Meta goedkeuring (wachttijd: 2-7 dagen)

### B22 — Meta Business Verificatie later doen
- **Keuze:** Op to-do lijst gezet, niet urgent
- **Reden:** Eerst automatisering volledig werkend krijgen en testen
- **Wat het oplevert:** Naam "Bright Panda Bijles" zichtbaar bij ontvanger in plaats van +1 nummer

### B23 — Templates indienen zonder emoji, categorie Utility
- **Keuze:** Geen emoji's in template tekst, handmatig categorie "Utility" selecteren bij indiening
- **Reden:** Meta classificeert templates met emoji's of woorden als "proefles" automatisch als Marketing
- **Bewijs:** `teacher_invitation` werd initieel als Marketing geclassificeerd → opnieuw aangemaakt als Utility ✅. Zelfde probleem met `trial_lesson_confirmation_teacher` → hernoemd naar `trial_lesson_confirmed_teacher`, opnieuw ingediend als Utility.

---

### B24 — Webhook module 3 in Scenario 3b (niet 1)
- **Keuze:** Scenario 3b gebruikt `{{3.data.fields[...]}}` voor alle webhook referenties
- **Reden:** Scenario 3b is later aangemaakt — de webhook module heeft automatisch nummer 3 gekregen in dit scenario
- **Risico:** Fout modulenummer geeft "references non-existing module" waarschuwing in Make.com

### B25 — Aanhalingstekens om datumchips in JSON body
- **Keuze:** Tally datumvelden in JSON body altijd omringen met aanhalingstekens: `"3": "{{1.data.fields[3].value}}"`
- **Reden:** Tally `INPUT_DATE` velden arriveren als date objects in Make.com. Geen enkele Make.com functie (`toString`, `formatDate`, `&`) kan ze concateneren. Aanhalingstekens forceren JSON serialisatie als string.
- **Bewijs:** Meer dan 3 uur debuggen, alle Make.com opties geprobeerd. Google Apps Script heeft dit probleem niet.

### B26 — if() wrapper voor checkbox waarden in JSON
- **Keuze:** Alle checkbox velden wrappen: `{{if(1.data.fields[5].value; true; false)}}`
- **Reden:** Make.com checkbox velden zijn een intern boolean type dat niet als geldig JSON boolean geserialiseerd wordt. `if()` garandeert altijd de literale waarden `true` of `false`.

### B27 — Lange Make.com formules vermijden
- **Keuze:** Formules met meer dan ~13 geneste `if`-statements niet gebruiken in Make.com
- **Reden:** Lange formules raken corrupt bij opslaan — tokens lijken correct gekleurd maar geven lege output. Root causes: slimme aanhalingstekens bij paste, verlies van `{{ }}` wrappers, afkappen bij veel module referenties.
- **Alternatief:** Google Apps Script voor alle complexe logica

---

## Werkwijze Afspraken

| Afspraak | Detail |
|----------|--------|
| JSON aanlevering | Altijd volledige JSON geven bij HTTP module aanpassingen, nooit partial |
| Stappenbeschrijving | Als bulletpoints, niet als lange lappen tekst |
| Meerdere stappen tegelijk | Niet steeds 1 regel, maar meerdere stappen per keer |
| Webhook logs | Via linkermenu → Webhooks → Logs (niet via scenario History tab) |
| Formule met `"` in JSON | Stop → gebruik Set Variable module of Google Apps Script |
| Webhook queue | Altijd "Wait for new data" kiezen, nooit "Use existing data" — pakt oudste uit queue |
| Tally datum in JSON | Altijd aanhalingstekens om datumchips: `"2": "{{1.data.fields[2].value}}"` |
| Checkbox in JSON | Altijd `if()`-wrapper: `{{if(1.data.fields[5].value; true; false)}}` |
| Tally indexering | 0-based — `fields[0]` is het eerste veld |
| GAS Script 1 (vakvertaling) | Parse response: NO — output via `.body` chip |

---

## Openstaande Acties

| Actie | Door wie | Details |
|-------|---------|---------|
| `trial_lesson_confirmed_teacher` goedkeuring afwachten | Raouf | Meta melding afwachten → dan Scenario 3b modules 7-13 bouwen |
| Scenario 3b modules 7-13 bouwen | Raouf + Claude | Na goedkeuring template — JSON bodies staan klaar in scenario-3b.md |
| Einde-tot-einde test uitvoeren | Raouf | Na oplevering Scenario 3b — echt matching record gebruiken |
| Meta display name goedkeuring afwachten | Raouf | Wachten, dan Scenario 1 Run once opnieuw |
| Scenario 3b Pad B ontwerpen | Raouf + Claude | Wat gebeurt er als ouder "geen tijdslot past" aanvinkt? |
| Scenario 02 SOQL + indices testen | Raouf | Nieuwe 0-based field indices en `fields[0]` voor matching_number verifiëren |
| Disclaimer toevoegen aan templates | Raouf | Allerlaatste stap na volledig testen |
| Meta Business Verificatie | Raouf | KvK 84707577 — lage urgentie |
