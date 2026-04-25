# Bright Panda — TODO
Laatst bijgewerkt: 25 april 2026

---

## ✅ Afgerond (recent)
- **✅ GEDAAN: WhatsApp templates goedgekeurd door Meta** (20 april 2026)
- **✅ GEDAAN: Docent Gids NL v1.0 + Teacher Guide EN v1.0 volledig afgerond**
- **✅ GEDAAN: Bijenkorf boekje verwerkt in H2 Gedragscode**
- **✅ GEDAAN: Tally akkoord-formulier gebouwd** (tally.so/r/aQDq1B)
- **✅ GEDAAN: Scenario 17 — Auto On-boarded gebouwd**
- **✅ GEDAAN: Geboortedatum toegevoegd aan Tally profielformulier** (21 april 2026) → `Date_of_Birth__c`
- **✅ GEDAAN: Bulk import On-boarded docenten naar MailerLite** (21 april 2026) — 104 docenten geïmporteerd
- **✅ GEDAAN: MailerLite Scenario 13 — Name + Last name velden toegevoegd** (21 april 2026)
- **✅ GEDAAN: Salesforce velden aangemaakt** (21 april 2026): `Graduated__c`, `Exam_Training_Details__c`, `Profile_Comments__c`
- **✅ GEDAAN: Contract datums op layout** — staat al in Details tab, voldoende
- **✅ GEDAAN: Teaching_Location__c geactiveerd voor Teacher Record Type** (23 april 2026)
- **✅ GEDAAN: Profile_Completed_Date__c toegevoegd aan Teacher Path** (23 april 2026)
- **✅ GEDAAN: Email campagne "Docenten Update — April 2026" HTML klaar** (25 april 2026) — NL + EN blokken klaar voor MailerLite
- **✅ GEDAAN: Slack workspace aangemaakt** (25 april 2026) — Bright Panda workspace
- **✅ GEDAAN: Slack verbonden in Make.com** (25 april 2026) — "Bright Panda Slack" connectie
- **✅ GEDAAN: Scenario 10 uitgebreid met Slack module** (25 april 2026) → #nieuwe-aanmeldingen

---

## 🔴 Hoge prioriteit

- **Email campagne "Docenten Update — April 2026" versturen**: HTML klaar, link Docent Gids nog invoegen → versturen via MailerLite naar groep "On-boarded".

- **Student Lifecycle stages toevoegen in Salesforce** (handmatig via Setup):
  - Intake (vervangt Enrollment)
  - Pending Conversion
  - Unreachable
  - Churned - Finished
  - Churned - Temporary
  - Enrollment deactiveren

- **Contact_Status__c waarden toevoegen + kleuren instellen** (handmatig via Setup):
  - Not Contacted (grijs)
  - Called - 1st Attempt, No Answer (geel)
  - Called - 2nd Attempt, No Answer (oranje)
  - Called - 3rd Attempt, No Answer (rood)
  - Reached - Need to Call Back (blauw)
  - Reached (groen)

- **Student Path guidance teksten instellen in Salesforce** — IN UITVOERING 20 april 2026.

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: juridisch laten beoordelen en verwerken in contracttekst.

---

## 🏢 Salesforce Enterprise upgrade

- **Salesforce gesprek opvolgen**: bevestiging Enterprise upgrade + 50% korting voor 2-3 jaar contract
- **Vragen bevestigen**: Change Data Capture beschikbaar? ContentVersion API toegang? Picklist via Metadata API?

---

## 💬 Slack

- **Resterende kanalen aanmaken** in Bright Panda workspace:
  - #callbacks
  - #proeflessen
  - #pending-conversie
  - #escalaties
- **Intake flow Slack berichten** bouwen in Make.com (dagelijks 09:00 overzicht #callbacks)
- **Proefles voltooid alert** bouwen → #proeflessen
- **Escalatie alerts** bouwen → #escalaties
- **Pending conversie alerts** bouwen → #pending-conversie

---

## ⚙️ Make.com / Automations

- **Intake flow bouwen (nieuw scenario)**:
  - Trigger: Contact_Status__c wijziging op Student record
  - Poging 1 → WhatsApp + email ouder + Slack delay 09:00 (#callbacks)
  - Poging 2 → WhatsApp + email ouder (urgenter) + Slack delay 09:00 (#callbacks)
  - Poging 3 → WhatsApp + email ouder (laatste) + LifecycleStage → Unreachable
  - Reached - Need to Call Back → Salesforce Task + Slack delay 09:00

- **Scenario 21 bouwen — Tally "Aanvullende Profielinfo" → Salesforce automatisering**:
  Trigger: Tally webhook voor formulier `tally.so/r/NpY9RW`. Let op: vaknamen NL → EN vertaaltabel nodig.

- **Tally vaknamen NL → EN vertaling oplossen voor Scenario 21**.

- **Scenario 1 polling vervangen door Salesforce webhook**.

- **Intern alert bouwen na proefles**.

- **Salesforce status updaten na versturen `parent_timeslot_final`**.

- **Re-engagement flow bouwen voor No Show matchings**.

- **TinyURL short links aanmaken** voor picker links (Scenario 2, 5, 6, escalatie).

- **Escalatie scenario controleren**.

- **AVG/GDPR data verwijdering automatiseren** (2 scenarios).

---

## 📧 MailerLite

- **Post-proefles email flow inrichten**.

- **HTML design verwerken in post-proefles automation**.

---

## 📱 WhatsApp / 360dialog

- **WhatsApp tekst schrijven voor handmatige availability check**.

- **`parent_timeslot_final` template aanpassen**: video → afbeelding in header.

---

## 👤 Docenten opvolging

- **Ashna Rajaram opvolgen**: studie, instelling, IBAN, naam op bankpas, max niveau, max leerjaar, examentraining voorkeur, basisschool voorkeur nog niet ingevuld.

---

## 🔒 GDPR / Compliance

- **Verwerkersovereenkomst (DPA) afsluiten met Tally**.

---

## 📬 Overig

- **Gmail inbox info@brightpanda.nl opruimen via Cowork**.
