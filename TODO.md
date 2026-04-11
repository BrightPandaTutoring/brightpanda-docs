# Bright Panda — To-Do Lijst
*Laatste update: 11 april 2026*

## 🔴 Hoge prioriteit
- [ ] End-to-end onboarding test: aanmelding → contract → Pending Onboarding → Tally → dagstart verwerking → onboarding emails
- [ ] Student Path guidance teksten instellen in Salesforce Path Settings voor alle lifecycle stages
- [ ] Scenarios 1 t/m 9 volledig documenteren in GitHub

## ⚙️ Make.com
- [ ] Scenario 10: WhatsApp module 6 fout (lege tekst parameter) fixen + heractiveren
- [ ] Scenario 11: Timezone fix — hardcoded +01:00 wintertijd vervangen door dynamische timezone
- [ ] Scenario 13: WhatsApp sturen na Interview Invited route
- [ ] Tally formulier automatisch sturen bij Pending Onboarding
- [ ] Onboarding emails bouwen in MailerLite met PDF bijlage (Docent Gids)
- [ ] Guidelines_Accepted__c veld aanmaken in Salesforce + checkbox in Tally formulier
- [ ] Tally formulier reminder bouwen voor Pending Onboarding (>3 dagen, leeg IBAN → WhatsApp)
- [ ] Bulk import scenario bouwen — alle On-boarded docenten naar MailerLite groep "On-boarded"
- [ ] Intern alert bouwen na proefles — reminder om ouder én docent te bellen
- [ ] Re-engagement flow bouwen voor No Show matchings (WhatsApp na 30 dagen + MailerLite)
- [ ] Salesforce status update toevoegen na versturen parent_timeslot_final
- [ ] TinyURL aanmaken voor alle lange Google Apps Script picker links
- [ ] Escalatie scenario checken — nog relevant na Scenario 5 en 6?
- [ ] AVG/GDPR data verwijdering bouwen (Offboarded 2 jaar, Not a Match 6 maanden)

## 📋 Salesforce
- [ ] Contract_Start_Date__c en Contract_End_Date__c toevoegen aan Business Account Layout
- [ ] Teaching_Location__c beschikbaar maken voor Teacher Record Type via klassieke URL
- [ ] Profile_Completed_Date__c toevoegen aan Teacher Path key fields (Pending Onboarding)
- [ ] ReferredToBPVia__c "Other" inschakelen voor Teacher én Student record type

## 📱 WhatsApp
- [ ] Template availability_conflict_teacher opnieuw indienen bij 360dialog met voorbeeldwaarden
- [ ] Template availability_conflict_teacher_reminder opnieuw indienen bij 360dialog
- [ ] Tekst schrijven voor 24u reminder naar docent (proefles tips)
- [ ] WhatsApp tekst schrijven voor handmatige availability check bij nieuwe matching

## 📧 MailerLite / Email
- [ ] Post-proefles flow inrichten (lijst "Bright Panda Ouders", segmentatie, Make.com koppeling)
- [ ] HTML design post-proefles email verwerken in MailerLite automation
- [ ] parent_timeslot_final template aanpassen (video vs afbeelding header)

## 📄 Docent Gids PDF
- [ ] Hoofdstuk toevoegen: waarom de proefles belangrijk is voor Bright Panda
- [ ] Hoofdstuk toevoegen: hoe het matching proces via WhatsApp werkt
- [ ] Geboortedatum toevoegen aan Tally formulier → Date_of_Birth__c
- [ ] Bsport uitleg verzamelen → verwerken in On-boarded welkomstmail

## 🔒 Compliance / GDPR
- [ ] GDPR compliance Tally formulier — DPA afsluiten met Tally
- [ ] Privacyverklaring brightpanda.nl controleren op verwerking docentgegevens

## 📊 Overig
- [ ] Gmail inbox info@brightpanda.nl opruimen via Cowork (labels + filters)
- [ ] Ashna Rajaram opvolgen: IBAN, studie, instelling, max niveau, max leerjaar, examentraining, basisschool
- [ ] Bsport uitleg verzamelen voor welkomstmail On-boarded docenten
