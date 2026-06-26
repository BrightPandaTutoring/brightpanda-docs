# Bright Panda — TODO
Laatst bijgewerkt: 26 juni 2026

---

## ✅ Afgerond (recent)
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

- **Scenario 21 + 22 testen** — end-to-end test uitvoeren met testrecord

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: juridisch laten beoordelen

---

## 📊 Salesforce Dashboards

- **Formula velden aanmaken** voor tijdberekeningen:
  - `Days_in_Pending_Conversion__c` → `IF(ISBLANK(Pending_Conversion_Date__c), 0, TODAY() - Pending_Conversion_Date__c)`
  - `Days_Since_Registration__c` → `TODAY() - DATEVALUE(CreatedDate)`
- **Rejection_Reason__c gaan vullen** zodat Rejection Reason chart data toont
- **Dashboard 2 uitbreiden** zodra meer data beschikbaar is

---

## 🎨 Email Design (Progress Bar)

- **Progress bar verder uitwerken in claude.ai/design** — prototype klaar, nog uit te werken in High Fidelity
- **Progress bar als GIF exporteren** en in alle intake emails verwerken (via ScreenToGif of Canva)
- **MailerLite email "Intake - Reached" schrijven en automation aanmaken**
- **Pending Conversion emails schrijven** — dag 2, 5, 9 (automations aangemaakt, emails nog leeg)
- **Client welkomstmail schrijven** — automation aangemaakt (Scenario 25), email nog leeg

---

## 🔧 Matching Teacher flow

- ✅ **GEDAAN (9 juni 2026):** `Start_Trial_Class_Process__c` checkbox in gebruik, Scenario 1 trigger omgezet van "Trial_Lesson_Status leeg + polling" naar deze checkbox via Salesforce Flow (V10), en "Docent gevonden" notificatie naar ouder via MailerLite (module 13) live. Zie SESSION_LOG.md.
- **Progress bar stap 3 in de "Docent gevonden" ouder-email** — visueel nog afronden (valt samen met Email Design hierboven).

---

## 💬 Slack

- **Persoonlijk Slack account aanmaken voor Raouf** (eigen email, bv. raouf@brightpanda.nl) → joinen in Brightpanda workspace → User ID doorgeven zodat @mention in Make scenario 10 toegevoegd kan worden → dan krijgt Raouf ook badge notificaties bij nieuwe aanmeldingen
- **Escalatie alert bouwen** → #escalaties

---

## ⚙️ Make.com / Automations

- **MailerLite email "Intake - Reached" schrijven en automation aanmaken**
- **Scenario 21 polling vervangen door Salesforce webhook** (na Enterprise upgrade)
- **Scenario 17 (Auto On-boarded) omzetten naar event-driven webhook** — zelfde patroon als Scenario 1 en 11 (zie salesforce-flow-webhook-integratie.md)
- **Re-engagement flow bouwen voor No Show matchings**
- **AVG/GDPR data verwijdering automatiseren** (2 scenarios)

---

## 📧 MailerLite

- **Post-proefles email flow inrichten**
- **Pending Conversion emails schrijven** (dag 2, 5, 9)
- **Client welkomstmail schrijven**
- **MailerLite email "Intake - Reached" aanmaken**

---

## 👤 Docenten opvolging

- **Ashna Rajaram opvolgen**: studie, instelling, IBAN, naam op bankpas, max niveau, max leerjaar, examentraining voorkeur, basisschool voorkeur nog niet ingevuld.

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
- **Gmail logo aanpassen** — pulserende versie van het Bright Panda logo instellen als Gmail-profielfoto / verzendlogo (betere merkbeleving bij uitgaande mail)
