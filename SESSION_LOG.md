# Bright Panda — Session Log

Laatste sessie: 10 juni 2026

## Waar aan gewerkt

Twee automatiseringen omgezet naar event-driven / Salesforce-natief: Scenario 25 (Client Welkomstmail) via het Salesforce Flow → Make webhook-playbook, en Scenario 23 (Active Matching → Pending Conversion) volledig herbouwd als Salesforce-natieve Record-Triggered Flow (zonder Make). Daarnaast de tips-mail (aftercare) opgeschoond.

### Afgerond

**Scenario 25 — Client Welkomstmail (event-driven) — GETEST WERKEND**
- Make Scenario 25 (ID 5497116) omgezet van polling naar Custom Webhook (module 3, pad `/l6owd25tp5nachw2b075w7cvperjvdh7`) + Webhook Response (module 5, `{"accepted": true}`, Content-Type application/json). Oude filter (verwees naar niet-bestaande module) verwijderd — Salesforce-flow filtert al.
- MailerLite-module: `{{3.ParentSEmail__c}}`, `{{3.ParentSName__c}}`, `{{3.FirstName}}` → groep "Actieve Klanten" (182829305032606767).
- External Service `MakeClientWelcomeWebhook` (Complete Schema, Named Credential `MakeNewStudentWebhook`), operation `SendClientWelcomeToMake`, Apex-type `MakeClientWelcomeWebhook_SendClientWelcomeToMake_IN_body` met 4 velden (Id, ParentSEmail__c, ParentSName__c, FirstName).
- Record-Triggered Flow op Account: condities `LifecycleStage__c` = Client AND `RecordTypeId` = Student (012KB000000ojZGYAY), "Only when updated to meet", async pad. Geen anti-loop-guard nodig (scenario schrijft niets terug naar Account). Flow-label "Scenario 25 — Client Welcome Webhook", API-naam werd `Send_to_Make`.
- End-to-end getest: tips-mail kwam binnen. ✓

**Scenario 23 — Active Matching → Pending Conversion (Salesforce-NATIEF) — 1 van 2 tests bevestigd**
- Bewust GEEN Make/webhook: pure Salesforce-update, dus sneller/betrouwbaarder als native flow.
- Record-Triggered Flow op Student Teacher Matching, entry-conditie `Status__c` = Active, "Only when updated to meet", geen async (interne DML).
- Eén Update Records op Account met DUBBELE guard: `Id` = `{!$Record.Student__c}` AND `LifecycleStage__c` = `Trial Class`. Zet `LifecycleStage__c` = Pending Conversion + `Pending_Conversion_Date__c` = `{!Vandaag}` (Formula-resource, Date, `TODAY()`).
- Flow geverifieerd actief: `Scenario_23_Active_Matching_to_Pending_Conversion`, IsActive true, RecordAfterSave, object Student Teacher Matching.

**Tips-mail (aftercare) opgeschoond**
- `docs/mailerlite/emails/6-tips-voor-de-bijles.html`: alle `{$teacher_name}` verwijderd, vervangen door "de docent"/"the tutor" (bewuste keuze om Scenario 25 simpel te houden — geen docent-lookup). Resterende merge tags: {$name}, {$student_name}, {$unsubscribe}.

## Belangrijkste beslissing (business-logica)

De guard `LifecycleStage = Trial Class` op de Scenario 23-flow is cruciaal. "Matching wordt Active" is op zichzelf een te breed signaal: een bestaande klant (Client) die een extra vak/proefles aanvraagt, of een migratie van bestaande klanten, mag NIET teruggezet worden naar Pending Conversion. Door alleen om te zetten als het account op dat moment op Trial Class staat, worden migratie-matchings, extra-vak-matchings en bestaande klanten beschermd. Dit is getest en bevestigd (zie hieronder).

## Tests

**Scenario 23 — Test 1 (guard blokkeert) — GESLAAGD**
Testrecord: Matching 0016 (a0CP80000GejQk5MQE), student "Raouf Student" (001P8000010CE5HIAW), stond op Client. Matching → Active gezet. Resultaat: Raouf bleef Client, Pending_Conversion_Date leeg. De guard werkt: een bestaande klant wordt niet teruggezet. ✓

**Scenario 23 — Test 2 (wordt wél omgezet) — NIET BEVESTIGD, handmatig afmaken**
Opzet: Raouf op Trial Class zetten + matching terug naar Pending → dan matching → Active. Verwachting: Raouf → Pending Conversion + Pending_Conversion_Date = vandaag. De verificatie-query liep vast op Salesforce MCP-timeouts (meerdere keren geen respons na 4 min), dus NIET bevestigd of de omzetting daadwerkelijk plaatsvond.

## Wachten op / eerstvolgende acties

1. **Scenario 23 test 2 handmatig afmaken:** check dat account Raouf Student (001P8000010CE5HIAW) op Trial Class staat → zet matching 0016 op Pending → dan op Active → controleer of leerling op Pending Conversion komt + Pending_Conversion_Date__c = vandaag. Daarna testrecord opruimen (Raouf terug naar Client).
2. **Make Scenario 23 (ID 5495257) DEACTIVEREN** zodra test 2 bevestigd is — anders draaien de native flow en het Make-scenario dubbel.
3. **Scenario 3** (Trial Lesson Scheduled & Availability Conflict): MailerLite-module bouwen + filter-fix (`status` = tekst `chosen`) + end-to-end test. Nog open uit eerdere sessie.
4. **Scenario 17** (Auto On-boarded) nog omzetten van polling (dagelijks 08:00) naar event-driven.
5. **Picklist-discrepantie student-lifecycle** uitzoeken: documentatie noemt waarden die afwijken van de feitelijke picklist (o.a. "Matching Teacher", "Enrollment").

## Let op (valkuilen voor de toekomst)

- **External Service nooit achteraf wijzigen:** zodra die in een flow gebruikt wordt kan het schema niet meer aangepast worden ("referenced in a flow") → delete-loop. Stel alle payload-velden vooraf vast en zet ze in één keer goed (Complete Schema). Dit was gisteren de grootste tijdvreter.
- **Volgorde event-driven bouwen:** Make eerst (webhook-URL) → External Service met ALLE velden → Flow.
- **Pure Salesforce-update?** Bouw dan een Salesforce-natieve flow zonder webhook (zoals Scenario 23), niet via Make.
- **Datumveld in flow:** "Current Date" staat niet in de resource-picker. Gebruik Formula-resource (Data Type Date, `TODAY()`).
- **Flow-limiet:** Enterprise Edition = max 2.000 flows per type. De oude "max 5"-regel (Professional) is NIET van toepassing. CLAUDE.md regel 20 gecorrigeerd.
- **Salesforce MCP timeouts** komen voor (deze sessie meermaals bij verificatie-queries). Verifieer dan via de Setup UI of probeer opnieuw; een timeout betekent niet automatisch dat de DML mislukte.
- **Assignment-valkuil:** bij het vullen van de Apex-variabele Id koppelen aan Account ID, niet aan Record Type ID (deze fout is gisteren gemaakt en gecorrigeerd).

## GitHub commits deze sessie
- `6-tips-voor-de-bijles.html`: teacher_name verwijderd (hosted versie).
- CLAUDE.md: Scenario 25 event-driven toegevoegd; daarna Scenario 23 → Salesforce-natieve flow (nieuwe sectie "SALESFORCE-NATIEVE FLOWS"), flow-limiet gecorrigeerd (Enterprise max 2000), regels 24/25 toegevoegd (External Service niet achteraf wijzigen; datum-formula `TODAY()`), Scenario 23 in tabel = "⛔️ VERVANGEN — deactiveren". Laatste commit `3d0b2533`.
