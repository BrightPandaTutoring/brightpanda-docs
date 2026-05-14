# Bright Panda — TODO
Laatst bijgewerkt: 14 mei 2026

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

---

## 🔴 Hoge prioriteit

- **Scenario 21 + 22 testen** — end-to-end test uitvoeren met testrecord

- **Scenario 1 aanpassen** — trigger wijzigen naar `Start_Process__c` veld (besluit sessie 14 mei). Veld nog aanmaken op Student_Teacher_Matching__c object. Nieuw scenario bouwen voor "Docent gevonden" email naar ouder met progress bar.

- **Student Path guidance teksten instellen in Salesforce**

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

## 🔒 GDPR / Compliance

- **Verwerkersovereenkomst (DPA) afsluiten met Tally**

---

## 📬 Overig

- **Gmail inbox info@brightpanda.nl opruimen via Cowork**
