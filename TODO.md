# Bright Panda — TODO
Laatst bijgewerkt: 21 april 2026

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

---

## 🔴 Hoge prioriteit

- **Student Path guidance teksten instellen in Salesforce** — IN UITVOERING 20 april 2026:
  stel voor elke klant lifecycle stage de key fields en guidance tekst in via
  Salesforce Path Settings. Stages: New, Enrollment, Matching Teacher, Trial Class,
  Client, Stopped - Never Converted, Stopped - Existing Client, Wrong Match, Churned.

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: de Docent Gids stelt dat
  bij het organiseren van lessen buiten Bright Panda om het contract per direct wordt
  ontbonden en dat aanvullende sancties opgelegd kunnen worden, waaronder het vorderen
  van een schadevergoeding. Dit moet juridisch verankerd worden in het freelance
  contract dat docenten ondertekenen via DocuSeal. Laten beoordelen door een jurist
  en vervolgens verwerken in de contracttekst.

---

## 🗄️ Salesforce — Nieuwe velden aanmaken

- **Nieuw veld: `Graduated__c`** (of "Currently Studying") — aanmaken op Account (Teacher).
  Picklist met waarden: "Studeer momenteel" / "Afgestudeerd". Mappen vanuit Tally vraag
  "Studeer je momenteel of ben je al afgestudeerd?".

- **Nieuw veld: `Exam_Training_Details__c`** — textarea op Account (Teacher).
  Mappen vanuit Tally vraag "In welke vakken kun je examentraining geven en op welk niveau?".

- **Nieuw veld: `Profile_Comments__c`** — textarea op Account (Teacher).
  Aparte sectie voor opmerkingen uit het aanvullend profielformulier (Tally), los van
  `Comments_FromWebForm__c` die voor de initiële aanmelding is.

---

## ⚙️ Make.com / Automations

- **Scenario 20 bouwen — Tally "Aanvullende Profielinfo" → Salesforce automatisering**:
  Vervang de handmatige dagstart-verwerking van deze Tally submissions door een Make.com
  scenario. Gebruik de volledige veldmapping in CLAUDE.md. Trigger: Tally webhook voor
  formulier `tally.so/r/NpY9RW`. Zet `Profile_Completed_Date__c` pas als alle verplichte
  velden zijn gevuld.

- **Scenario 1 polling vervangen door Salesforce webhook**: het huidige polling
  interval vervangen door een directe Salesforce webhook trigger zodat de invitation
  meteen wordt verstuurd bij een nieuwe matching.

- **Intern alert bouwen na proefles**: een Make.com scenario dat Raouf en Yasin een
  herinnering stuurt om de ouder én docent te bellen na afloop van de proefles.

- **Salesforce status updaten na versturen `parent_timeslot_final`**: na het versturen
  van dit WhatsApp template moet `Trial_Lesson_Status__c` automatisch bijgewerkt worden.

- **Re-engagement flow bouwen voor No Show matchings**: als een matching de status
  "No Show" krijgt, automatisch na 30 dagen een WhatsApp sturen + MailerLite campagne.

- **TinyURL short links aanmaken** voor alle lange Google Apps Script picker links die
  via WhatsApp worden verstuurd (Scenario 2, 5, 6, escalatie).

- **Escalatie scenario controleren**: nakijken wat dit scenario precies doet en of het
  nog relevant is nu Scenario 5 en 6 actief zijn.

- **AVG/GDPR data verwijdering automatiseren**: twee maandelijkse Make.com scenarios
  bouwen: (1) Offboarded > 2 jaar → persoonsgegevens wissen; (2) Not a Match / Not
  Interested > 6 maanden → persoonsgegevens wissen.

---

## 📧 MailerLite

- **Post-proefles email flow inrichten**: lijst "Bright Panda Ouders" aanmaken met
  custom velden en segmenten. Koppelen aan Make.com.

- **HTML design verwerken in post-proefles automation**: het gebouwde HTML email
  design (4 stappen + quote blok) verwerken als email automation in MailerLite.

---

## 🗄️ Salesforce — Overig

- **Contract_Start_Date__c en Contract_End_Date__c toevoegen aan Business Account Layout**.

- **Teaching_Location__c beschikbaar maken voor Teacher Record Type** via klassieke URL:
  `brightpanda.my.salesforce.com/setup/ui/recordtypefields.jsp?id=012KB000000ojZLYAY&type=Account&setupid=AccountRecordTypes`

- **Profile_Completed_Date__c toevoegen aan Teacher Path key fields**.

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
