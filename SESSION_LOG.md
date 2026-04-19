# Bright Panda — Session Log
*Doel van dit bestand: bij elke nieuwe Claude chat (Claude.ai of Claude Code) als eerste lezen om te weten waar Raouf en Yasin gebleven waren. Wordt bijgewerkt bij elke "Afsluiten".*

---

## Laatste sessie: 19 april 2026

### Waar werd aan gewerkt
- **Scenario 14 (DocuSeal Contract Signed)** uitgebreid met `Contract_URL__c` veld
- **Scenario 19 (Documentation Reminder Pending Onboarding)** fix: filter toegevoegd vóór iterator om lege bundles te voorkomen
- Nieuw Salesforce veld `Contract_URL__c` (URL, 500 chars) aangemaakt op Account object
- Uitgebreid onderzoek gedaan naar PDF upload als ContentVersion in Salesforce — niet mogelijk op huidige licentie

### Belangrijkste beslissingen deze sessie
- **PDF bestand uploaden naar Salesforce niet haalbaar**: zowel `salesforce:makeApiCall` (met en zonder absolute URL) als eigen Connected App geven problemen → tijdelijke oplossing: `Contract_URL__c` slaat DocuSeal PDF URL op
- **Make.com iterator regel geformaliseerd**: altijd filter `Total number of bundles > 0` vóór iterator plaatsen om downstream errors bij 0 resultaten te voorkomen
- **`salesforce:makeApiCall` regel geformaliseerd**: altijd absolute URL gebruiken, instance URL wordt niet automatisch toegevoegd

### Key learnings toegevoegd aan CLAUDE.md
- KRITIEKE REGEL 12: `salesforce:makeApiCall` vereist absolute URL, ContentVersion endpoint geeft nog steeds [404] door ontbrekende OAuth scopes
- KRITIEKE REGEL 13: Make.com iterator met 0 bundles → altijd filter vooraf
- Salesforce Connected App aanmaken vereist specifieke permissies — niet beschikbaar op huidige licentie

### Scenarios geüpdate in CLAUDE.md
- Scenario 14: beschrijving uitgebreid met "vult Contract_URL__c"
- Scenario 17: toegevoegd aan tabel (Auto On-boarded, dagelijks 08:00)
- Scenario 19: toegevoegd aan tabel (Documentation Reminder, met filter)

### Wachten op externe actie
- Template `pending_onboarding_tally_reminder` → wachten op Meta goedkeuring (Scenario 15)
- Templates `availability_conflict_teacher` + `_reminder` → opnieuw indienen met voorbeeldwaarden
- Templates `teacher_invitation` + `teacher_intro_message_parent` → wachten op Meta goedkeuring (Scenario 1)

### Eerstvolgende acties
1. End-to-end onboarding test met echte docent (geen testrecord meer)
2. Student Path guidance teksten in Salesforce instellen voor alle lifecycle stages
3. Scenario 1 testen zodra templates goedgekeurd zijn
4. Scenario 13 — Interview Invited WhatsApp testen
5. Licentie-upgrade onderzoeken voor PDF upload naar Salesforce (of alternatieve opslag: Google Drive / Dropbox / S3)

### Let op / context
- Scenarios 1-9 + 11 staan op **inactief** in Make.com (Raouf zet ze pas live na test)
- Scenario 10, 12, 13, 14, 15, 17, 19 zijn **actief**
- Nieuw veld `Contract_URL__c` staat nu in Teacher velden in CLAUDE.md
- Test op 19 april: Raouf Angudi Teacher record gebruikt voor Scenario 19 test, daarna weer op On-boarded gezet

### Volledige to-do lijst
Zie `TODO.md` in deze repo voor de actuele lijst per categorie.
