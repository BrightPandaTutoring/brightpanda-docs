# Bright Panda — TODO
Laatst bijgewerkt: 23 april 2026

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

---

## 🔴 Hoge prioriteit

- **Student Path guidance teksten instellen in Salesforce** — IN UITVOERING 20 april 2026.

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: juridisch laten beoordelen
  en verwerken in contracttekst.

---

## ⚙️ Make.com / Automations

- **Scenario 21 bouwen — Tally "Aanvullende Profielinfo" → Salesforce automatisering**:
  Trigger: Tally webhook voor formulier `tally.so/r/NpY9RW`. Gebruik volledige veldmapping
  in CLAUDE.md. Let op: Tally stuurt vaknamen in het Nederlands, Salesforce verwacht Engels
  → vertaaltabel nodig (zie TODO hieronder).

- **Tally vaknamen NL → EN vertaling oplossen voor Scenario 21**: Tally stuurt bijv.
  "Wiskunde B" maar Salesforce verwacht "Mathematics B". Oplossing: ofwel vaknamen in
  Tally omzetten naar Engels, ofwel vertaaltabel bouwen in Make.com via Data Store.

- **Scenario 1 polling vervangen door Salesforce webhook**.

- **Intern alert bouwen na proefles**.

- **Salesforce status updaten na versturen `parent_timeslot_final`**.

- **Re-engagement flow bouwen voor No Show matchings**.

- **TinyURL short links aanmaken** voor picker links (Scenario 2, 5, 6, escalatie).

- **Escalatie scenario controleren**.

- **AVG/GDPR data verwijdering automatiseren** (2 scenarios).

---

## 📧 MailerLite

- **Update email sturen naar alle On-boarded docenten**: over waar Bright Panda mee
  bezig is en naartoe wil werken, inclusief de Docent Gids. Versturen via MailerLite
  campagne naar groep "On-boarded". HTML blokken klaar (23 april 2026).

- **Post-proefles email flow inrichten**.

- **HTML design verwerken in post-proefles automation**.

---

## 📱 WhatsApp / 360dialog

- **WhatsApp tekst schrijven voor handmatige availability check**.

- **`parent_timeslot_final` template aanpassen**: video → afbeelding in header.

---

## 👤 Docenten opvolging

- **Ashna Rajaram opvolgen**: studie, instelling, IBAN, naam op bankpas, max niveau,
  max leerjaar, examentraining voorkeur, basisschool voorkeur nog niet ingevuld.

---

## 🔒 GDPR / Compliance

- **Verwerkersovereenkomst (DPA) afsluiten met Tally**.

---

## 📬 Overig

- **Gmail inbox info@brightpanda.nl opruimen via Cowork**.
