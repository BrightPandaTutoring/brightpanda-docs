# Bright Panda — TODO
Laatst bijgewerkt: 17 april 2026

---

## ⏳ Wacht op externe actie (geen actie vereist, alleen opvolgen)
- Template `pending_onboarding_tally_reminder` is ingediend bij 360dialog/Meta en wacht
  op goedkeuring. Zodra goedgekeurd is Scenario 15 volledig operationeel.
- Template `availability_conflict_teacher` opnieuw indienen bij 360dialog met
  voorbeeldwaarden (eerder ingediend zonder voorbeelden, werd afgewezen).
- Template `availability_conflict_teacher_reminder` opnieuw indienen bij 360dialog
  met voorbeeldwaarden (zelfde probleem als hierboven).
- Templates `teacher_invitation` (aangepast) en `teacher_intro_message_parent` (nieuw)
  ingediend bij 360dialog/Meta — wachten op goedkeuring voordat Scenario 1 getest
  kan worden.

---

## 🔴 Hoge prioriteit

- **End-to-end onboarding test uitvoeren**: doorloop de volledige flow van aanmelding
  → contract tekenen → Pending Onboarding → Tally invullen → dagstart verwerking →
  onboarding emails. Controleer of alle stappen correct doorlopen en Salesforce velden
  correct gevuld worden.

- **Student Path guidance teksten instellen in Salesforce**: stel voor elke klant
  lifecycle stage de key fields en guidance tekst in via Salesforce Path Settings.
  Stages: New, Enrollment, Matching Teacher, Trial Class, Client, Stopped - Never
  Converted, Stopped - Existing Client, Wrong Match, Churned.

- **Sanctie toevoegen aan freelance contract (DocuSeal)**: de Docent Gids stelt dat
  bij het organiseren van lessen buiten Bright Panda om het contract per direct wordt
  ontbonden en dat aanvullende sancties opgelegd kunnen worden, waaronder het vorderen
  van een schadevergoeding. Dit moet juridisch verankerd worden in het freelance
  contract dat docenten ondertekenen via DocuSeal. Laten beoordelen door een jurist
  en vervolgens verwerken in de contracttekst.

---

## 🧪 Testen

- **Scenario 13 — Interview Invited WhatsApp testen**: de module is gebouwd maar nog
  niet getest. Test door de lifecycle stage van een bestaande docent handmatig naar
  "Interview Invited" te zetten en te controleren of de WhatsApp correct binnenkomt.

- **Scenario 1 testen**: zodra templates `teacher_invitation` en
  `teacher_intro_message_parent` zijn goedgekeurd door Meta. Controleer of beide
  WhatsApps binnenkomen met 180s tussenpoos en of de variabelen kloppen
  ({{1}}=ParentSPhone__c, {{2}}=ParentSName__c, {{3}}=docent FirstName,
  {{4}}=student FirstName).

---

## 📄 Docent Gids & Onboarding

- **Bijenkorf boekje analyseren voor aanvullingen Gedragscode (H2)**: doorlopen
  en relevante punten verwerken in de bestaande paragrafen van Hoofdstuk 2.

- **✅ GEDAAN: Tally akkoord-formulier gebouwd** (tally.so/r/aQDq1B) — docent bevestigt
  Docent Gids gelezen te hebben. MailerLite automation verstuurt de email via groep
  "Teacher Guide To Be Read" (Scenario 16 trigger). Make.com vult
  `Documentation_Agreed__c` in Salesforce na submit.

- **Geboortedatum toevoegen aan Tally aanvullend profiel formulier** (tally.so/r/NpY9RW)
  en mappen naar `Date_of_Birth__c` in Salesforce via Make.com.

---

## ⚙️ Make.com / Automations

- **Getekend contract opslaan in Salesforce**: Scenario 14 webhook uitbreiden zodat
  de ondertekende PDF van DocuSeal wordt opgeslagen als bijlage (Attachment/File) op
  het docent record in Salesforce. PDF URL uit de webhook payload halen, downloaden
  via HTTP module, en uploaden naar Salesforce.

- **Scenario 1 polling vervangen door Salesforce webhook**: het huidige polling
  interval vervangen door een directe Salesforce webhook trigger zodat de invitation
  meteen wordt verstuurd bij een nieuwe matching i.p.v. afhankelijk te zijn van
  de polling cyclus.

- **✅ GEDAAN: Scenario 17 — Auto On-boarded gebouwd**: dagelijks scenario dat docenten
  in Pending Onboarding checkt of alle drie velden gevuld zijn
  (Profile_Completed_Date__c, Bsport_Account_Created__c, Documentation_Agreed__c) →
  LifecycleStage__c automatisch naar On-boarded. Schedule: dagelijks 08:00.

- **Scenario 10 fout oplossen**: WhatsApp module 6 geeft een fout door een lege
  tekst parameter. Module 6 inspecteren, de lege variabele identificeren en fixen.

- **Bulk import scenario bouwen (eenmalig)**: een Make.com scenario dat alle
  bestaande On-boarded docenten met een emailadres importeert in de MailerLite groep
  "On-boarded". Gebruik Salesforce Search Records + MailerLite Create/Update Subscriber.
  Na uitvoering direct deactiveren.

- **Intern alert bouwen na proefles**: een Make.com scenario dat Raouf en Yasin een
  herinnering stuurt om de ouder én docent te bellen na afloop van de proefles om te
  horen hoe het ging.

- **Salesforce status updaten na versturen `parent_timeslot_final`**: na het versturen
  van dit WhatsApp template moet `Trial_Lesson_Status__c` automatisch bijgewerkt worden
  naar de juiste waarde.

- **Re-engagement flow bouwen voor No Show matchings**: als een matching de status
  "No Show" krijgt, automatisch na 30 dagen een WhatsApp sturen ("Ben je nog steeds
  op zoek naar bijles?") + een MailerLite email campagne starten voor ouders die niet
  reageren op WhatsApp.

- **TinyURL short links aanmaken** voor alle lange Google Apps Script picker links die
  via WhatsApp worden verstuurd (Scenario 2, Scenario 5, Scenario 6, escalatie scenario).
  Gebruik de TinyURL API via HTTP GET naar `https://tinyurl.com/api-create.php?url=`.

- **Escalatie scenario controleren**: nakijken wat dit scenario precies doet en of het
  nog relevant is nu Scenario 5 en 6 actief zijn.

- **AVG/GDPR data verwijdering automatiseren**: twee maandelijkse Make.com scenarios
  bouwen: (1) docenten met status Offboarded waarbij `Offboarded_Date__c` meer dan 2
  jaar geleden is → persoonsgegevens wissen uit Salesforce; (2) docenten met status
  Not a Match of Not Interested waarbij `LastModifiedDate` meer dan 6 maanden geleden
  is → persoonsgegevens wissen.

---

## 📧 MailerLite

- **Post-proefles email flow inrichten**: één lijst aanmaken "Bright Panda Ouders" met
  custom velden (Trial_Lesson_Date, Teacher_Name, Student_Name, Status) en segmenten
  (Proefles gehad, Actieve klant, No Show). Koppelen aan Make.com zodat ouders
  automatisch worden toegevoegd na een proefles.

- **HTML design verwerken in post-proefles automation**: het gebouwde HTML email
  design (4 stappen + quote blok) verwerken als email automation in MailerLite.

---

## 🗄️ Salesforce

- **Contract_Start_Date__c en Contract_End_Date__c toevoegen aan Business Account
  Layout**: zodat deze datums zichtbaar zijn op het docent record zonder naar de
  details tab te gaan.

- **Teaching_Location__c beschikbaar maken voor Teacher Record Type**: via de klassieke
  Salesforce URL de picklist waarden activeren voor het Teacher record type. URL:
  `brightpanda.my.salesforce.com/setup/ui/recordtypefields.jsp?id=012KB000000ojZLYAY&type=Account&setupid=AccountRecordTypes`

- **Profile_Completed_Date__c toevoegen aan Teacher Path key fields**: dit veld
  toevoegen aan de Pending Onboarding stage in de Salesforce Path Settings, en
  beschikbaar maken via dezelfde klassieke URL hierboven.

---

## 📱 WhatsApp / 360dialog

- **WhatsApp tekst schrijven voor handmatige availability check**: een kant-en-klare
  tekst schrijven die Raouf of Yasin kan sturen wanneer een docent handmatig benaderd
  wordt bij een nieuwe matching. Inclusief docent naam, vak, niveau, locatie en
  beschikbaarheidsvraag.

- **`parent_timeslot_final` template aanpassen**: beslissen of de header een video of
  afbeelding wordt. Video speelt niet automatisch af in WhatsApp, dus voorkeur gaat
  naar een afbeelding. Template aanpassen in 360dialog.

---

## 👤 Docenten opvolging

- **Ashna Rajaram opvolgen**: heeft gereageerd op het profiel update verzoek maar
  heeft de volgende velden nog niet ingevuld: studie, instelling/universiteit, IBAN,
  naam op bankpas, max niveau, max leerjaar, examentraining voorkeur, basisschool
  voorkeur. Later opnieuw opvragen.

---

## 🔒 GDPR / Compliance

- **Verwerkersovereenkomst (DPA) afsluiten met Tally**: Tally verwerkt
  persoonsgegevens van docenten (IBAN, geboortedatum etc.). Een DPA is verplicht
  onder de AVG. Transparantietekst toevoegen aan het formulier en controleren of
  de privacyverklaring op brightpanda.nl de verwerking van docentgegevens beschrijft.

---

## 📬 Overig

- **Gmail inbox info@brightpanda.nl opruimen via Cowork**: labels aanmaken en
  filters instellen zodat inkomende emails automatisch gesorteerd worden per
  categorie (docenten, ouders, intern, sollicitaties etc.).

- **Dagstart routine**: elke ochtend "dagstart" typen in Claude. Claude haalt dan
  automatisch op: (1) Google Calendar van vandaag, (2) Salesforce overzicht van
  docenten per lifecycle stage, (3) nieuwe Tally form submissions verwerken via
  Gmail, (4) ongelezen emails met profielreacties en sollicitaties.
