# Bright Panda — Session Log
*Doel van dit bestand: bij elke nieuwe Claude chat als eerste lezen. Wordt bijgewerkt bij elke "Afsluiten".*

---

## Laatste sessie: 14 mei 2026

### Waar werd aan gewerkt
1. **Brand identity gedocumenteerd** — Montserrat font, kleuren (#1d467f, #f59e0c, #f4f8fd, #1D2930), tone of voice
2. **Salesforce KPI Reports** — 9 reports aangemaakt via Analytics REST API
3. **Salesforce Dashboards** — 3 dashboards gebouwd en op Home pagina gezet
4. **Claude Design** — progress bar prototype uitgewerkt, brand info ingevoerd
5. **Volledige student flow geanalyseerd** — gaps geïdentificeerd

### KPI Reports aangemaakt (via Analytics REST API)
| Report | ID |
|---|---|
| [KPI] Student Funnel Overview | 00OP800000AfCPFMA3 |
| [KPI] New Registrations This Month | 00OP800000Af40JMAR |
| [KPI] Unreachable Contact Status | 00OP800000AfDLJMA3 |
| [KPI] Rejection Reason Breakdown | 00OP800000AfDMvMAN |
| [KPI] Pending Conversion Days | 00OP800000AfCgzMAF |
| [KPI] Trial Completed Awaiting Followup | 00OP800000AfDQ9MAN |
| [KPI] Open Actions Bsport To Create | 00OP800000AfEajMAF |
| [KPI] Conversion Rates Summary | 00OP800000AfDRlMAN |
| [KPI] Monthly Registration Trend | 00OP800000AfOBtMAN |

**Kritieke fix toegepast op alle reports:** `standardDateFilter` was automatisch op `CUSTOM startDate=vandaag` gezet door de API — gefixed naar `CUSTOM 2020-01-01 t/m 2027-12-31` zodat alle historische data zichtbaar is. Scope gezet op `organization`.

### Dashboards gebouwd
- **Student Funnel & Growth** — Monthly Trend, Funnel Overview, New Registrations, Unreachable, Rejection
- **Speed & Quality KPIs** — Pending Conversion Days, Trial Completed, Conversion Rates
- **Open Acties Team** — Bsport To Create, Pending Conversion Days

### Salesforce Home pagina
- Lightning App Builder → `Bright Panda Home` aangemaakt (Home Template One Region)
- Alle 3 dashboards toegevoegd als componenten
- Geactiveerd als App Default voor Sales app
- Dashboards verplaatst naar `Home Page Dashboards` folder zodat ze vindbaar zijn

### Student flow analyse
Volledige flow doorgelopen — gaps geïdentificeerd:
- Scenario 1 trigger klopt niet — moet `Start_Process__c` veld gebruiken
- Geen "Docent gevonden" email naar ouder
- Geen No Show flow
- Geen Unreachable re-engagement
- Geen churn win-back
- Slack #proeflessen en #escalaties nog te bouwen

### Matching Teacher beslissing
- Huidig: Scenario 1 triggert op `Trial_Lesson_Status__c` leeg — klopt niet
- Nieuw: `Start_Process__c` checkbox aanmaken op `Student_Teacher_Matching__c`
- Scenario 1 splitsen in 2 routes: Route 1 = email ouder, Route 2 = WhatsApp docent
- Nog te bouwen!

### Progress bar design
- 5 stappen: Aanvraag → Op zoek naar geschikte docent → Docent gevonden → Proefles → Bijles van start!
- Prototype gebouwd in claude.ai/design (High Fidelity)
- Brand: Montserrat, #1d467f blauw, #f59e0c amber
- Plan: GIF exporteren via ScreenToGif → uploaden in MailerLite

### Eerstvolgende acties
1. `Start_Process__c` veld aanmaken op Student_Teacher_Matching__c
2. Scenario 1 aanpassen + nieuw scenario "Docent gevonden" email bouwen
3. Progress bar GIF exporteren en in emails verwerken
4. Pending Conversion emails schrijven (dag 2, 5, 9)
5. Client welkomstmail schrijven
6. Scenario 21 + 22 end-to-end testen

### Let op
- KPI Reports hebben `standardDateFilter CUSTOM 2020-2027` — elk jaar updaten naar 2028 etc.
- Dashboard scope is `organization` — alle gebruikers zien alle data
- Formula velden nog handmatig aanmaken in Setup voor tijdberekeningen
- Rejection_Reason__c is nog leeg — chart toont pas data als gevuld
