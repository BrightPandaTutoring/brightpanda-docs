# Bright Panda — To-Do Lijst
*Laatste update: 11 april 2026*

## ✅ Afgerond vandaag (11 april 2026)
- [x] Scenario 12 gefixt — variabelen hersteld, actief op 1 uur
- [x] Scenario 10 WhatsApp module 6 fout — al opgelost
- [x] Scenario 11 timezone fix — al opgelost
- [x] Scenario 8 timezone fix — SOQL query bijgewerkt met dynamische timezone
- [x] Twee testrecords (Raouf Angudi Teacher + Raouf test 2) op On-boarded gezet
- [x] WhatsApp template interview_invitation_confirmation ingediend en goedgekeurd door Meta
- [x] HTTP module toegevoegd aan Scenario 13 Interview Invited route voor WhatsApp
- [x] Is_Pro_Teacher__c checkbox veld aangemaakt in Salesforce + toegevoegd aan Business Account Layout
- [x] Pro Teacher criteria toegevoegd aan Pending Onboarding guidance text in Salesforce Path
- [x] Interview stage guidance text bijgewerkt met Pro Teacher criteria
- [x] Contracting stage guidance text bijgewerkt
- [x] Contract_Sent__c checkbox veld aangemaakt in Salesforce + toegevoegd aan Business Account Layout + Contracting Path key fields
- [x] Scenario 13 Contracting route gesplitst in Contracting + Renew — beide met Contract_Sent__c check
- [x] DocuSeal email templates ingesteld (signature request, reminder, document copy, completed notification)
- [x] DocuSeal velden op readonly gezet zodat docent alleen kan tekenen
- [x] MailerLite Pending Onboarding automation geactiveerd
- [x] Tally link fix in MailerLite — URL correct opgebouwd met {$email} merge tag
- [x] DNS records toegevoegd in Squarespace voor MailerLite (A + TXT groen, MX pending)
- [x] Scenario 14 end-to-end getest — contract → ondertekening → Pending Onboarding → Tally email
- [x] Scenarios 1 t/m 9 gedocumenteerd in GitHub (gisteren)

## 🔴 Hoge prioriteit
- [ ] End-to-end onboarding volledig valideren met echte docent (niet testrecord)
- [ ] Student Path guidance teksten instellen in Salesforce voor alle lifecycle stages
- [ ] MX record controleren in MailerLite zodra DNS is gepropageerd (binnen 24 uur)

## ⚙️ Make.com
- [ ] Scenario 13 dubbele trigger monitoren
- [ ] Tally reminder bouwen — dagelijks scenario voor docenten >3 dagen in Pending Onboarding met lege Profile_Completed_Date__c → reminder email via MailerLite
- [ ] Onboarding emails bouwen in MailerLite met PDF bijlage (Docent Gids)
- [ ] Guidelines_Accepted__c veld aanmaken in Salesforce + checkbox in Tally
- [ ] Bulk import scenario bouwen — On-boarded docenten → MailerLite
- [ ] Intern alert bouwen na proefles — reminder om ouder én docent te bellen
- [ ] Re-engagement flow bouwen voor No Show matchings
- [ ] TinyURL aanmaken voor alle lange Google Apps Script picker links
- [ ] Escalatie scenario checken — nog relevant na Scenario 5 en 6?
- [ ] AVG/GDPR data verwijdering bouwen

## 📋 Salesforce
- [ ] Contract_Start/End_Date__c toevoegen aan Business Account Layout
- [ ] Teaching_Location__c beschikbaar maken via klassieke URL
- [ ] Profile_Completed_Date__c toevoegen aan Teacher Path key fields
- [ ] ReferredToBPVia__c "Other" inschakelen voor Teacher én Student

## 📱 WhatsApp
- [ ] Templates availability_conflict_teacher + reminder opnieuw indienen bij 360dialog
- [ ] 24u reminder tekst schrijven voor docent (proefles tips)

## 📧 MailerLite / Email
- [ ] Post-proefles flow inrichten
- [ ] HTML design post-proefles email verwerken
- [ ] parent_timeslot_final template aanpassen
- [ ] Welkomstmail bouwen voor On-boarded docenten met Docent Gids PDF

## 📄 Docent Gids PDF
- [ ] Hoofdstuk toevoegen: proefles belang voor Bright Panda
- [ ] Hoofdstuk toevoegen: matching proces WhatsApp
- [ ] Geboortedatum toevoegen aan Tally → Date_of_Birth__c
- [ ] Bsport uitleg verzamelen

## 🔒 Compliance / GDPR
- [ ] DPA afsluiten met Tally
- [ ] Privacyverklaring controleren op verwerking docentgegevens

## 📊 Overig
- [ ] Gmail inbox opruimen (labels + filters)
- [ ] Ashna Rajaram opvolgen: IBAN, studie, instelling, max niveau, max leerjaar, examentraining, basisschool
- [ ] Bsport uitleg verzamelen voor welkomstmail On-boarded docenten
- [ ] Testrecord emailadres terugzetten naar info@brightpanda.nl na afronding tests
