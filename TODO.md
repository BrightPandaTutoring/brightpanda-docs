# Bright Panda — TODO
Laatst bijgewerkt: 26 juni 2026

---

## ✅ Afgerond (recent)
- **✅ GEDAAN: Gmail logo aangepast** (26 juni 2026) — pulserende versie van het Bright Panda logo ingesteld als Gmail-profielfoto / verzendlogo
- **✅ GEDAAN: Scenario 21 + 22 end-to-end getest** (26 juni 2026)
- **✅ GEDAAN: Scenario 21 polling vervangen door Salesforce webhook** (26 juni 2026)
- **✅ GEDAAN: Scenario 17 (Auto On-boarded) omgezet naar event-driven webhook** (26 juni 2026)
- **✅ GEDAAN: Email Design (Progress Bar) volledig afgerond** (26 juni 2026) — progress bar HiFi uitgewerkt, GIF geëxporteerd en verwerkt in intake emails, Intake - Reached email + automation aangemaakt, Pending Conversion emails dag 2/5/9 geschreven, Client welkomstmail geschreven, Progress bar stap 3 in "Docent gevonden" email afgerond
- **✅ GEDAAN: MailerLite flows afgerond** (26 juni 2026) — Post-proefles email flow ingericht, Client welkomstmail aangemaakt, Intake - Reached email + automation aangemaakt
- **✅ GEDAAN: Ashna Rajaram profiel volledig ingevuld** (26 juni 2026)
- **✅ GEDAAN: Student Path guidance teksten ingesteld in Salesforce** (26 juni 2026) — teksten + key fields voor alle lifecycle stages (New, Enrollment, Matching Teacher, Trial Class, Client, Stopped - Never Converted, Stopped - Existing Client, Wrong Match, Churned)
- **✅ GEDAAN: Scenario 1 omgebouwd naar event-driven webhook** (9 juni 2026) — trigger via `Start_Trial_Class_Process__c` checkbox + Salesforce Flow "Scenario 1 — Teacher Invitation Webhook" (V10), polling vervalt. Inclusief "Docent gevonden" notificatie naar ouder via MailerLite (module 13, groep "Teacher Found - Parent Email"). Loop + retry-"spook-webhooks" opgelost (Webhook Response Content-Type: application/json + anti-loop guard `Trial_Lesson_Status Is Null` met "Only when updated to meet"). Schone test bevestigd: 1 webhook, 0 errored interviews, 0 wachtende async jobs. Zie SESSION_LOG.md + docs/make/salesforce-flow-webhook-integratie.md.
- **✅ GEDAAN: WhatsApp templates goedgekeurd door Meta** (20 april 2026)
- **✅ GEDAAN: Docent Gids NL v1.0 + Teacher Guide EN v1.0 volledig afgerond**
- **✅ GEDAAN: Scenario 21 — Intake Flow gebouwd** (26 april 2026)
- **✅ GEDAAN: Scenario 22 — Daily Callbacks + Nieuwe aanmeldingen Slack 09:00 gebouwd** (26 april 2026)
- **✅ GEDAAN: MailerLite automations aangemaakt** (26 april 2026): Intake 1st/2nd/3rd Attempt No Answer, Intake Reached
- **✅ GEDAAN: Brand identity gedocumenteerd** (13 mei 2026) — Montserrat font, kleuren, tone of voice
- **✅ GEDAAN: 9 Salesforce KPI Reports aangemaakt** (14 mei 2026)
- **✅ GEDAAN: 3 Salesforce Dashboards gebouwd** (14 mei 2026): Student Funnel & Growth, Speed & Quality KPIs, Open Acties Team
- **✅ GEDAAN: Salesforce Home pagina ingericht** (14 mei 2026) — Bright Panda Home via Lightning App Builder met dashboards
- **~~TutorCruncher gekozen als Bsport-vervanger~~** (28 mei 2026) — beslissing teruggedraaid op 26 juni 2026, niet doorgegaan met TutorCruncher.

---

## 🔴 Hoge prioriteit

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: juridisch laten beoordelen

---

## 📊 Salesforce Dashboards

- **Formula velden aanmaken** voor tijdberekeningen:
  - `Days_in_Pending_Conversion__c` → `IF(ISBLANK(Pending_Conversion_Date__c), 0, TODAY() - Pending_Conversion_Date__c)`
  - `Days_Since_Registration__c` → `TODAY() - DATEVALUE(CreatedDate)`
- **Rejection_Reason__c gaan vullen** zodat Rejection Reason chart data toont
- **Dashboard 2 uitbreiden** zodra meer data beschikbaar is

---

## 💬 Slack

- **Persoonlijk Slack account aanmaken voor Raouf** (eigen email, bv. raouf@brightpanda.nl) → joinen in Brightpanda workspace → User ID doorgeven zodat @mention in Make scenario 10 toegevoegd kan worden → dan krijgt Raouf ook badge notificaties bij nieuwe aanmeldingen
- **Escalatie alert bouwen** → #escalaties

---

## ⚙️ Make.com / Automations

- **Scenario 13 — Contract Expiring Soon route bouwen** — huidige situatie: Salesforce Flow zet stage correct op `Contract Expiring Soon` na 335 dagen, maar Scenario 13 heeft geen route die hierop reageert. Bouwen: WhatsApp of Slack alert naar Raouf/Yasin met docent naam + einddatum contract → handmatige beoordeling
- **Scenario 13 — Renew route bouwen** — huidige situatie: route bestaat maar is een lege placeholder. Bouwen: nieuw DocuSeal contract versturen met bijgewerkte `Contract_Start_Date__c` (= vandaag) en `Contract_End_Date__c` (= vandaag + 365 dagen), zelfde flow als de Contracting route
- **Re-engagement flow bouwen voor No Show matchings**
- **AVG/GDPR data verwijdering automatiseren** (2 scenarios)

---

## 📧 MailerLite

- **Pending Conversion emails schrijven** (dag 2, 5, 9)

---

## 📈 Groei & Marketing

- **Marketingpositionering uitwerken** — inspelen op de emotie van de klant om hogere lesprijs te rechtvaardigen en sterkere merkbeleving te creëren
- **Vergoedingsframework uitwerken voor docenten** — duidelijke richtlijnen voor aankomend schooljaar: wat bieden we docenten, hoe blijven we competitief op de markt én eerlijk richting docent
- **Financieel plan maken** — volledige kostenanalyse: waar gaat het geld naartoe, welke kosten kunnen omlaag, waar laten we kansen liggen, en hoe verbeteren we dit radicaal voor aankomend schooljaar

---

## 🔒 GDPR / Compliance

- **Verwerkersovereenkomst (DPA) afsluiten met Tally**

---

## 📬 Overig

- **Gmail inbox info@brightpanda.nl opruimen via Cowork**
