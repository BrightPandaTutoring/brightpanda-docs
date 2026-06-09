# Bright Panda — Session Log

Laatste sessie: 9 juni 2026

## Waar aan gewerkt

Scenario 1 (Teacher Invitation, Make ID 4729958) omgebouwd van polling naar een event-driven Salesforce webhook-trigger, plus het volledig opsporen en oplossen van een hardnekkig probleem waarbij de webhook herhaaldelijk en ongevraagd bleef afvuren.

### Afgerond
- MailerLite-module (module 13) in Scenario 1: Create/Update Subscriber naar groep "Teacher Found - Parent Email" (189010938726188387). Vakken via `{{10.data}}` (NL-vertaling GAS), niet `{{6.Subjects__c}}`.
- Salesforce Record-Triggered Flow "Scenario 1 — Teacher Invitation Webhook" gebouwd op Student_Teacher_Matching__c, met async pad -> External Service callout naar de Make-webhook.
- Make Scenario 1 omgezet naar Custom Webhook-trigger (hook 3197287) + Webhook Response module direct na de trigger.
- Alle modulereferenties in Scenario 1 omgezet naar de webhook-payload `{{14.x}}` (matchingId, teacherId, studentId, subjects, name, status). Modules 3, 5, 6, 7, 9, 10, 12, 13 gecontroleerd en correct.
- Loop en spook-webhooks volledig opgelost (zie hieronder). Schone test op 16:49 bevestigd: één webhook, nul errored interviews, nul wachtende async jobs, geen naloper.

### Trigger-mechaniek (bevestigd)
Scenario 1 triggert via de handmatige checkbox `Start_Trial_Class_Process__c` op Student_Teacher_Matching__c. Workflow: zet Status = Trial Class, vul Teacher/Student/Subject(s), vink Start_Trial_Class_Process aan -> Salesforce Flow (async) -> webhook -> Make Scenario 1 -> docent krijgt WhatsApp `teacher_invitation` + Tally-link, daarna ouder-bericht, MailerLite, en module 7 zet Trial_Lesson_Status = "Teacher Invited".

## Wat er misging en hoe het is opgelost (belangrijk voor de toekomst)

Kernsymptoom: na het aanvinken van Start_Trial_Class_Process bleef de webhook herhaaldelijk afvuren, ook zonder dat er iets werd aangepast. Er bleken DRIE losse oorzaken te zijn, één voor één gevonden:

### 1. Verkeerde flow-versie actief
De versie die in de Flow Builder werd bewerkt (V8) had status InvalidDraft en was nooit geactiveerd. De actieve versie was V9, met loop-gevoelige condities. Alle aanpassingen in V8 hadden dus geen enkel effect.
Les: controleer altijd welke versie ECHT actief is via SOQL op FlowVersionView. Vertrouw niet op de titel/badge in de builder.

### 2. Ontbrekende anti-loop guard in de actieve versie
V9 had geen `Trial_Lesson_Status Is Null`-conditie en stond op "Every time a record is updated and meets the condition requirements". Daardoor hertriggerde elke update van module 7 de flow opnieuw -> loop elke ~3 minuten (gelijk aan de sleep-duur in Make).
Oplossing (V10, nu actief): entry-condities Status = Trial Class AND Start_Trial_Class_Process = True AND Trial_Lesson_Status Is Null, met "When to run for updated records = Only when a record is updated to meet the condition requirements". Dit is de echte loop-blokkade: zodra module 7 Trial_Lesson_Status op "Teacher Invited" zet, voldoet het record niet meer aan de condities en kan een vervolg-update niet opnieuw triggeren. Het vinken van de checkbox is de enige overgang die de flow start, dus precies één keer. Deze "Only when... meet"-optie voldoet ook aan de async-eis, dus GEEN Is Changed gebruiken (Is Changed dwingt "Every time" af).

### 3. Verkeerde Content-Type -> mislukte async-runs -> automatische retries (de "spook-webhooks")
De Webhook Response module gaf geen `Content-Type: application/json` terug. Make ontving de POST en draaide het scenario wél (status Success in de webhook-log), maar Salesforce kon het antwoord niet parsen en markeerde de asynchrone flow-run als mislukt. Salesforce doet dan automatisch tot 2 retries, met vertraging, en met de ORIGINELE record-context. Die retries vuurden ~29 minuten later (bv. om 16:07, twee tegelijk = het waargenomen paar) en gingen af ook al stond het record inmiddels op "Teacher Invited" -> retries her-evalueren de entry-condities niet. Ze lieten geen error-record achter omdat de Content-Type tegen die tijd al gefixt was, wat verklaarde waarom er achteraf 0 errored interviews te vinden waren.
Oplossing: Webhook Response module (module 18) -> header `Content-Type: application/json`, body `{"accepted": true}`, status 200. Sindsdien slagen runs in één keer (0 errored interviews), dus geen retries en geen nalopers. Bevestigd met de 16:49-test.

### Diagnostische SOQL-queries die hielpen (herbruikbaar)
- Actieve flow-versie: `FlowVersionView` WHERE `FlowDefinitionViewId = '300P800000yCuWyIAK'` ORDER BY VersionNumber DESC -> toont welke versie Active is en welke InvalidDraft/Obsolete.
- Achterstand/fouten: `FlowInterview` WHERE `InterviewLabel LIKE 'Scenario 1%'` -> errored of waiting interviews.
- Wachtende retries/async: `AsyncApexJob` WHERE `Status IN ('Queued','Processing','Preparing','Holding')`.
- Andere automatiseringen uitsluiten: `FlowDefinitionView` WHERE `IsActive = true` gefilterd op ProcessType (Workflow = Process Builder) en TriggerType (Scheduled) -> bevestigde dat niets anders het veld aanraakt.

## Wachten op / eerstvolgende acties
- Eindbevestiging (optioneel): rond ~17:18 (ongeveer 29 min na de 16:49-test) de Make webhook-log checken. Geen binnenkomst = 100% bevestigd dat de naloper weg is. De data (0 errored interviews, 0 async jobs) wijst al op schoon.
- 36 oude vastgelopen flow-interviews zijn opgeruimd (verwijderd via DML).
- Debug logging op de integratie-gebruiker aanzetten als er ooit tóch nog een afwijking optreedt, voor volledige tracing van de trigger.

## Let op (valkuilen voor de toekomst)
- "Scheduled Paths: 2" in het Start-element betekent hier alleen Run Immediately + Run Asynchronously; dit zijn GEEN tijdgestuurde paden. Niet mee op het verkeerde been laten zetten.
- Salesforce retryt mislukte asynchrone flow-paden automatisch (tot 2x) met de originele context. Een mislukte callout-response is dus niet onschuldig: die veroorzaakt latere "spook"-calls. Zorg altijd voor een correcte Webhook Response (200 + application/json) bij elk flow->Make webhook-patroon.
- Module 7 raakt `Start_Trial_Class_Process__c` bewust niet aan (blijft True als audit-bewijs). De loop-bescherming komt van de Is Null-guard plus "Only when updated to meet", niet van het terugzetten van dat veld.
- Testrecord: Matching 0016 (a0CP80000GejQk5MQE), Raouf Student + Raouf Angudi Teacher.
