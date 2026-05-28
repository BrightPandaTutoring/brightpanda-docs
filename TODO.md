# Bright Panda — TODO
Laatst bijgewerkt: 28 mei 2026

---

## ✅ Afgerond (recent)
- **✅ GEDAAN: WhatsApp templates goedgekeurd door Meta** (20 april 2026)
- **✅ GEDAAN: Docent Gids NL v1.0 + Teacher Guide EN v1.0 volledig afgerond**
- **✅ GEDAAN: Scenario 21 — Intake Flow gebouwd** (26 april 2026)
- **✅ GEDAAN: Scenario 22 — Daily Callbacks + Nieuwe aanmeldingen Slack 09:00 gebouwd** (26 april 2026)
- **✅ GEDAAN: MailerLite automations aangemaakt** (26 april 2026): Intake 1st/2nd/3rd Attempt No Answer, Intake Reached
- **✅ GEDAAN: Brand identity gedocumenteerd** (13 mei 2026) — Montserrat font, kleuren, tone of voice
- **✅ GEDAAN: 9 Salesforce KPI Reports aangemaakt** (14 mei 2026)
- **✅ GEDAAN: 3 Salesforce Dashboards gebouwd** (14 mei 2026): Student Funnel & Growth, Speed & Quality KPIs, Open Acties Team
- **✅ GEDAAN: Salesforce Home pagina ingericht** (14 mei 2026) — Bright Panda Home via Lightning App Builder met dashboards
- **✅ GEDAAN: TutorCruncher gekozen als Bsport-vervanger** (28 mei 2026) — beslissing genomen na grondige analyse en demo call. Nederlandse interface bevestigd mogelijk. Trial account actief.

---

## 🔴 Hoge prioriteit

- **Scenario 21 + 22 testen** — end-to-end test uitvoeren met testrecord

- **Scenario 1 aanpassen** — trigger wijzigen naar `Start_Process__c` veld (besluit sessie 14 mei). Veld nog aanmaken op Student_Teacher_Matching__c object. Nieuw scenario bouwen voor "Docent gevonden" email naar ouder met progress bar.

- **Student Path guidance teksten instellen in Salesforce**

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: juridisch laten beoordelen

---

## 🚀 TutorCruncher migratie (nieuw — hoge prioriteit)

Beslissing genomen op 28 mei 2026. TutorCruncher vervangt Bsport. Salesforce blijft het CRM.

### Fase 1 — Setup & inrichting
- **Nederlandse interface instellen** — uitvragen bij TutorCruncher hoe dit exact werkt (custom CSS of taalbestand)
- **Subjects/vakken aanmaken** in TutorCruncher — zelfde structuur als Salesforce `Subjects__c`
- **Tariefstructuur instellen** — charge rate (ouder) en tutor rate (docent) per vak/niveau
- **Ad Hoc Charge categorieën aanmaken** — registratiekosten, examentraining, extra vak, Pro service

### Fase 2 — Make.com integratie bouwen
- **Scenario A:** Salesforce lifecycle → "Trial Class" → automatisch Job aanmaken in TutorCruncher (docent + leerling + tarief)
- **Scenario B:** TutorCruncher webhook "Les voltooid" → Salesforce `Trial_Lesson_Status__c` bijwerken
- **Scenario C:** TutorCruncher webhook "Betaling ontvangen" → Salesforce record bijwerken
- **Scenario D:** Maandelijks einde maand → GET /payment-orders/ → alle docenten automatisch uitbetalen via API

### Fase 3 — Upsell bouwen
- **Lessenkaarten (Packages) activeren** — bijv. 10 lessen pakket met korting, zichtbaar in ouder-portal
- **Post-proefles upsell flow** — Make.com + MailerLite email na proefles met pakket-keuze
- **Ad Hoc Charge via API** — extra dienst toevoegen aan factuur vanuit Salesforce trigger

### Fase 4 — Migratie & go-live
- **Bestaande actieve leerlingen overzetten** naar TutorCruncher
- **Docenten uitnodigen** voor hun eigen TutorCruncher portal login
- **Bsport opzeggen** zodra TutorCruncher volledig draait
- **Geschatte doorlooptijd:** 3–4 weken parttime

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

- **`Start_Process__c` checkbox veld aanmaken** op Student_Teacher_Matching__c
- **Scenario 1 trigger aanpassen** → van `Trial_Lesson_Status__c` leeg naar `Start_Process__c = true`
- **Nieuw scenario bouwen** — "Docent gevonden" notificatie naar ouder (MailerLite email + progress bar stap 3)

---

## 💬 Slack

- **Escalatie alert bouwen** → #escalaties

---

## ⚙️ Make.com / Automations

- **MailerLite email "Intake - Reached" schrijven en automation aanmaken**
- **Scenario 21 polling vervangen door Salesforce webhook** (na Enterprise upgrade)
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
