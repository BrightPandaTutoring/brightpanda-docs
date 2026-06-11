# Bright Panda — Session Log

Laatste sessie: 11 juni 2026

## Waar aan gewerkt

Scenario 21 (Intake Flow: Contact Status) omgezet van Watch Records polling naar event-driven via Salesforce Flow + webhook. Salesforce Flow `Scenario_21_Intake_Webhook` gebouwd en geactiveerd. Make Scenario 21 trigger moet nog handmatig omgezet worden van Watch Records naar Custom Webhook.

Daarnaast: scenario-intervallen geoptimaliseerd (6, 7, 8, 9) en geanalyseerd welke scenario's geschikt zijn voor webhook.

## Afgerond

**Scenario 21 — Intake Flow event-driven (Salesforce Flow actief, Make trigger nog te doen)**
- Salesforce Flow `Scenario_21_Intake_Webhook` (API-naam: `Scenario_21_Intake_Webhook`): IsActive true, object Account, RecordAfterSave
- Entry-condities: `Record Type ID` Equals `012KB000000ojZGYAY` AND `Contact Status` Does Not Equal (leeg)
- When to run: Only when a record is updated to meet the condition requirements
- Async pad AAN, Assignment `RequestBodyIntakeStatus` (11 velden), Action External Service `MakeIntakeContactStatusWebhook` → `SendIntakeContactStatusToMake`
- External Service `MakeIntakeContactStatusWebhook` aangemaakt met Complete Schema, alle 11 velden (6 string + 5 boolean)
- Webhook URL: `https://hook.eu1.make.com/wg18bd9j8vkf15rwi3p1d57msoq7smi9` (naam: BP-Intake-Contact-Status-Webhook)
- KEY LEARNING: `Is Changed` operator blokkeert het opslaan van een flow met async pad (Salesforce-fout `-63617461`, meerdere uren verloren). Oplossing: `Does Not Equal (leeg)` gebruiken. Vastgelegd als regel 27 in CLAUDE.md.

**Scenario-intervallen geoptimaliseerd:**
- Scenario 6: elke 2u → elke 4u
- Scenario 7: elke 15 min → elke 4u
- Scenario 8: elke 15 min → elke 30 min (niet verder vanwege 2u-tijdvensters in filters)
- Scenario 9: elke 15 min → elke 3u
- Raouf heeft dit zelf doorgevoerd in Make.

**Analyse scenario's 6, 7, 8, 9 voor webhook:**
Geen van de vier is een goede webhookkandiaat — ze triggeren op tijdsverstrijken zonder reactie, niet op een event. Polling blijft het juiste patroon voor reminders/escalaties.

## Wachten op / eerstvolgende acties

1. **Make Scenario 21 trigger handmatig omzetten:** open Scenario 21 in Make → verwijder Watch Records trigger → vervang door Custom Webhook `BP-Intake-Contact-Status-Webhook` (URL: `/wg18bd9j8vkf15rwi3p1d57msoq7smi9`) → voeg Webhook Response toe (status 200, body `{"accepted": true}`, Content-Type application/json) → verwijder oude filters die naar de Watch Records module verwijzen → activeer + Run once.
2. **Scenario 21 testen end-to-end:** zet Contact_Status__c van een testleerling op 'Called - 1st Attempt, No Answer' en controleer of Make de webhook ontvangt en de juiste route uitvoert.
3. **Scenario 23 test 2** nog te bevestigen (Trial Class → Pending Conversion). Testrecord Raouf Student (001P8000010CE5HIAW) staat mogelijk nog niet op Client — controleren en opruimen.
4. **Scenario 3** (Trial Lesson Scheduled): MailerLite-module + filter-fix nog open.
5. **Scenario 17** omzetten naar event-driven.

## Let op

- **Is Changed = VERBODEN in flows met async pad.** Geeft fout `-63617461` bij elke save-poging. Gebruik altijd `Does Not Equal (leeg)` als alternatief.
- **Salesforce blokkeert opslaan van incomplete flows** — tussentijds opslaan lukt niet als het async-pad leeg is. Altijd eerst volledig afbouwen (Assignment + Action), dan pas Save.
- **Scenario 21 Make-trigger staat nog op Watch Records** — de Salesforce Flow is actief maar Make ontvangt nog geen webhooks totdat de trigger in Make handmatig omgezet is.

## GitHub commits deze sessie
- CLAUDE.md: Scenario 21 event-driven toegevoegd (tabel + detailsectie), interval-updates scenario 6/7/8/9, regel 27 (Is Changed verboden), playbook bijgewerkt.
- SESSION_LOG.md: deze sessie.
