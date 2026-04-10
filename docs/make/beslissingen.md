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

---

## Functionele Beslissingen

### B06 — Ouder kiest tijdslot via getal, niet via dropdown
- **Keuze:** Number invoerveld in Form 2 waarbij ouder een getal typt
- **Reden:** Dropdown werkt niet dynamisch in Tally zonder betaald plan; tekstveld geeft typefouten
- **Afgewezen:** Vrije tekstinvoer (typefouten), dropdown (niet dynamisch)

### B07 — Nummering per tijdslot (niet per datum)
- **Keuze:** Elke datum+tijdslot combinatie krijgt een uniek oplopend getal
- **Reden:** Ouder moet exact tijdslot kunnen kiezen, niet alleen een datum
- **Afgewezen:** Nummering per datum (te vaag voor definitieve afspraak)

### B08 — Alleen hele uren in tijdsloten (13 opties per datum)
- **Keuze:** 13 opties van 08:00-09:00 t/m 20:00-21:00
- **Reden:** 26 halve uren is te lang voor de form; in de praktijk volstaat dit
- **Uitbreidbaar** naar halve uren later

### B09 — Telefoonnummers uitwisselen pas bij bevestiging
- **Keuze:** Docent en ouder krijgen elkaars telefoonnummer pas in de `trial_lesson_confirmation`
- **Reden:** Privacy — alleen relevant als proefles definitief ingepland is

### B10 — Verzetten en annuleren gaat handmatig
- **Keuze:** Geen automatisering voor verzetten of annuleren van proeflessen
- **Reden:** Te complex, valt buiten scope. Contactgegevens staan in WhatsApp disclaimer.

### B11 — Escalaties via WhatsApp naar intern nummer
- **Keuze:** Escalatiemeldingen via WhatsApp naar `+31613689666`
- **Reden:** Redundantie — escalaties mogen niet gemist worden
- **Kanalen:** WhatsApp (alle scenario's), Gmail/email (Scenario 03 — ook via email voor redundantie)

### B12 — Inbound WhatsApp messaging niet bouwen
- **Keuze:** Geen automatische verwerking van inkomende WhatsApp berichten
- **Reden:** Te complex, valt buiten scope van dit project

### B13 — Scheduling Scenario 03 op 15 minuten
- **Keuze:** Elke 15 minuten draaien
- **Reden:** Make.com Free plan limiet (ideaal zou elk uur zijn)

---

## Template Beslissingen

### B14 — Templates pas aanpassen na volledig testen
- **Keuze:** `trial_lesson_confirmation` disclaimer toevoegen als allerlaatste stap
- **Reden:** Elke template aanpassing vereist opnieuw Meta goedkeuring (wachttijd: 2-7 dagen)

### B15 — Meta Business Verificatie later doen
- **Keuze:** Op to-do lijst gezet, niet urgent
- **Reden:** Eerst automatisering volledig werkend krijgen en testen
- **Wat het oplevert:** Naam "Bright Panda Bijles" zichtbaar bij ontvanger in plaats van +1 nummer

---

## Werkwijze Afspraken

| Afspraak | Detail |
|----------|--------|
| JSON aanlevering | Altijd volledige JSON geven bij HTTP module aanpassingen, nooit partial |
| Stappenbeschrijving | Als bulletpoints, niet als lange lappen tekst |
| Meerdere stappen tegelijk | Niet steeds 1 regel, maar meerdere stappen per keer |
| Webhook logs | Via linkermenu → Webhooks → Logs (niet via scenario History tab) |
| Formule met `"` in JSON | Stop → gebruik Set Variable module |
