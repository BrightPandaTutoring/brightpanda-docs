# Bright Panda — Session Log
*Doel van dit bestand: bij elke nieuwe Claude chat (Claude.ai of Claude Code) als eerste lezen om te weten waar Raouf en Yasin gebleven waren. Wordt bijgewerkt bij elke "Afsluiten".*

---

## Laatste sessie: 16 april 2026

### Waar werd aan gewerkt
- **Repo reorganisatie**: `docent-gids/` verplaatst naar `docs/docent-gids/`. Marketing/website content (leerlingen, ouders, over-ons, faq, platform, administratie, technisch, docenten) verplaatst naar `docs/archive-website-content/`. Duplicaten verwijderd (oude gedragscode, scenario-05-koppelingsbevestiging). `docs/make/README.md` vereenvoudigd — verwijst nu naar CLAUDE.md voor scenario statussen (single source of truth).
- Docent Gids `docs/docent-gids/nl.md` — Hoofdstuk 1 (13 paragrafen) en Hoofdstuk 2 (Gedragscode, 7 paragrafen) volledig uitgeschreven
- Scenario 1 (Teacher Invitation) uitgebreid: 2 berichten met 180s sleep + nieuw template `teacher_intro_message_parent`
- Sleutelwoorden gedefinieerd: **Afsluiten**, **Update**, **Pak op**
- SESSION_LOG.md aangemaakt voor sessie-continuiteit tussen Claude chats

### Belangrijkste beslissingen deze sessie
- Hoofdstuk 2 Gedragscode opgesplitst in 7 paragrafen (i.p.v. 2 met "wordt nog uitgewerkt")
- Scenario 1 stuurt nu 2 berichten naar docent: invitation + 180s pauze + kant-en-klare doorstuurtekst voor ouder
- Drie sleutelwoorden vastgelegd in CLAUDE.md sectie "KRITIEKE REGELS"

### Wachten op externe actie
- Templates `teacher_invitation` (aangepast) + `teacher_intro_message_parent` (nieuw) → wachten op Meta goedkeuring via 360dialog
- Template `pending_onboarding_tally_reminder` → wachten op Meta goedkeuring (Scenario 15 hangt hierop)
- Templates `availability_conflict_teacher` + `_reminder` → opnieuw indienen met voorbeeldwaarden

### Eerstvolgende acties
1. Zodra `teacher_invitation` + `teacher_intro_message_parent` zijn goedgekeurd → Scenario 1 testen
2. End-to-end onboarding test met echte docent (geen testrecord)
3. Student Path guidance teksten in Salesforce instellen voor alle stages
4. MX record check in MailerLite zodra DNS gepropageerd

### Let op / context
- Scenarios 1-9 + 11 staan op **inactief** in Make.com (Raouf zet ze pas live na test)
- Scenario 10, 12, 13, 14, 15 zijn **actief**
- Docent Gids workflow: aanpassen in `docent-gids/nl.md` → committen → daarna PDF opnieuw genereren
- DocuSeal velden zijn readonly, reminders staan op 3/7/15 dagen
- Tally form NpY9RW heeft conditional formatting bug — staat op TODO

### Volledige to-do lijst
Zie `TODO.md` in deze repo voor de actuele lijst per categorie.
