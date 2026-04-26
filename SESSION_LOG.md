# Bright Panda — Session Log
*Doel van dit bestand: bij elke nieuwe Claude chat (Claude.ai of Claude Code) als eerste lezen om te weten waar Raouf en Yasin gebleven waren. Wordt bijgewerkt bij elke "Afsluiten".*

---

## Laatste sessie: 26 april 2026

### Waar werd aan gewerkt
- **Scenario 21 — Intake Flow: Contact Status** volledig gebouwd (ID: 5442970)
- **Scenario 22 — Daily Callbacks + Nieuwe aanmeldingen Slack 09:00** volledig gebouwd (ID: 5451841)
- **WhatsApp templates** geschreven en ingediend bij Meta
- **MailerLite automations** aangemaakt voor intake flow
- **Salesforce checkbox velden** aangemaakt voor duplicate prevention

### Belangrijkste beslissingen
- **Watch Records (polling)** gekozen als trigger voor Scenario 21 — CDC vereist Enterprise Edition, Flows beperkt tot 5 op Professional Edition
- **Checkbox velden per route** aangemaakt om dubbele berichten te voorkomen bij herhaalde record updates
- **Slack berichten per ouder apart** zodat jullie per bericht kunnen reageren en aangeven wie het oppakt
- **Scenario 22 Route 1** = nieuwe aanmeldingen (#nieuwe-aanmeldingen), **Route 2** = callbacks (#callbacks)
- **Template 3 ingediend als Marketing** — Meta categoriseert emotionele/urgente templates als Marketing, acceptabel voor 3e poging

### Scenario 21 — Intake Flow structuur
- **Route 1** (1st Attempt No Answer): WhatsApp + MailerLite "Intake - 1st Attempt" + SF checkbox
- **Route 2** (2nd Attempt No Answer): WhatsApp + MailerLite "Intake - 2nd Attempt No Answer" + SF checkbox
- **Route 3** (3rd Attempt No Answer): WhatsApp + MailerLite "Intake - 3rd Attempt No Answer" + SF update (Unreachable + checkbox)
- **Route 4** (Reached - Need to Call Back): SF checkbox + Slack direct naar #callbacks
- **Route 5** (Reached): MailerLite "Intake - Reached" + SF checkbox

### WhatsApp templates status
- `intake_parent_1st_attempt_no_answer` ✅ Goedgekeurd (Utility)
- `intake_parent_2nd_attempt_no_answer` ✅ Goedgekeurd (Utility)
- `intake_parent_3rd_attempt_no_answer_v3` ⏳ Ingediend (Marketing categorie)

### Nieuwe Salesforce velden
- `Intake_1st_Attempt_Sent_c__c`, `Intake_2nd_Attempt_Sent_c__c`, `Intake_3rd_Attempt_Sent_c__c`
- `Intake_Reached_Callback_Sent__c`, `Intake_Reached_Sent__c`
- Let op: API namen hebben dubbele `_c__c` suffix door fout bij aanmaken — werkt wel

### Wachten op
- `intake_parent_3rd_attempt_no_answer_v3` Meta goedkeuring
- Scenario 21 + 22 end-to-end test uitvoeren
- MailerLite email "Intake - Reached" nog schrijven en automation aanmaken

### Eerstvolgende acties
1. End-to-end test Scenario 21 + 22 uitvoeren met testrecord
2. MailerLite email "Intake - Reached" schrijven en automation aanmaken
3. Slack kanalen #proeflessen, #pending-conversie, #escalaties aanmaken + scenarios bouwen
4. Student Lifecycle stages toevoegen in Salesforce (Intake, Pending Conversion, Unreachable etc.)
5. Contact_Status__c waarden + kleuren instellen in Salesforce

### Let op / context
- Scenario 21 draait elke 15 minuten (polling) — niet real-time
- Salesforce Professional Edition: max 5 Flows, geen CDC
- Scenario 22 draait dagelijks om 09:00 (Europe/Amsterdam)
- Scenarios 1-9, 11 staan nog op inactief in Make.com

### Volledige to-do lijst
Zie `TODO.md` in deze repo voor de actuele lijst per categorie.
