# Bright Panda Bijles — Technische Documentatie
> Laatst bijgewerkt: 10 april 2026

---

## 1. SYSTEMEN & CREDENTIALS

### Salesforce
- URL: brightpanda.my.salesforce.com
- Username: info@brightpanda.nl
- Security Token: RJ8TRqHatJ94cQymv9KwfZeC
- Make.com Connection ID: 5705141
- Connection naam: Bright Panda Salesforce (brightpanda.my.salesforce.com - Raouf Angudi)

### 360dialog (WhatsApp)
- API Key: xl6Aj3Gs66I40LQl7C6GbjlxAK (let op: lowercase L, niet hoofdletter I)
- Endpoint: https://waba-v2.360dialog.io/messages
- Intern WhatsApp nummer: +31613689666
- Raouf: +31630892143
- Yasin: +31623325599

### MailerLite
- Make.com Connection ID: 6136292
- Connection naam: MailerLite Bright Panda
- Groep "Nieuwe Docent Aanmelding" ID: 183306606217266363

### Anthropic API
- Key naam: Bright Panda Make.com
- Endpoint: https://api.anthropic.com/v1/messages
- Model: claude-opus-4-6

### DocuSeal
- EU endpoint: https://api.docuseal.eu/submissions
- Template ID: 485548
- API Key: kF6DXM8V8AEJcRhXshwE1RxdvarDx9NHwuYjd9FnZz3
- Template velden (altijd lowercase): name, street, city, start_date, hourly_rate, signing_date, signature
- Document naam dynamisch via: OfficialName__c

### TinyURL
- API Token: azYv7XXfVtOTugtEc5Yep12MaN24vz0fRObVwYMHjfcxNKcT1VHDEAqCPnji
- Branded domain: go.brightpanda.nl
- CNAME target: hrj2vlx.customer.tinyurl.com
- API endpoint: https://tinyurl.com/api-create.php?url=[LANGE_URL]
- Output path in Make.com: MODULE_NUMBER.data.data.tiny_url

### Make.com
- Team ID: 1179486
- Organization ID: 6817575
- EU regio: eu1.make.com
- Make MCP URL: https://eu1.make.com/mcp/server/79146aa0-dea6-44e8-90be-0c3dd9d06110/t/scq2NktCps_SG2juuHm4ynBgm3YzS8Vh41Yyi6C3pU/stateless

### Tally Forms
- Form 1 (Ouder tijdslot): https://tally.so/r/2Ekaq9
- Form 3 (Docent tijdslot na conflict): https://tally.so/r/q4PDV9
- Form Aanvullende Profielinfo Docent: https://tally.so/r/NpY9RW
- Notificatie afzender: notifications@tally.so
- Notificatie subject: "New Tally Form Submission for Docent — Aanvullende Profielinfo / Additional Profile"

### Google Apps Script (Subject Picker)
- URL: https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec
- Input: matching_number, student_name, status (chosen/no_match)
- Output: JSON met gekozen tijdslot of no_match → webhook naar Scenario 3

### Google Calendar
- Docent inplanningslink: https://calendar.app.google/ArBhdKvAnLR924Xa6

---

## 2. SALESFORCE OBJECTEN & VELDEN

### Record Types
- Teacher Record Type ID: 012KB000000ojZLYAY
- Student Record Type ID: 012KB000000ojZGYAY

### Klassieke URL voor picklist waarden per record type
```
brightpanda.my.salesforce.com/setup/ui/recordtypefields.jsp?id=012KB000000ojZLYAY&type=Account&setupid=AccountRecordTypes
```
**Belangrijk:** Nieuwe picklist waarden voor Person Account record types zijn NIET automatisch beschikbaar — altijd handmatig inschakelen via bovenstaande klassieke URL.

### Teacher Lifecycle Stages (LifecycleStage__c)
New → Interview Invited → Interview → Contracting → Pending Onboarding → On-boarded → Contract Expiring Soon → Renew → Offboarded → Not a Match → Not Interested

### Student Lifecycle Stages (LifecycleStage__c)
New → Enrollment → Matching Teacher → Trial Class → Client → Stopped - Never Converted → Stopped - Existing Client → Wrong Match → Churned

### Trial_Lesson_Status__c waarden
New → Teacher Invited → Availability Conflict → Trial Lesson Scheduled → Trial Lesson Completed → No Show

### Custom velden — Account object

| API naam | Label | Type |
|---|---|---|
| LifecycleStage__c | Lifecycle Stage | Picklist |
| IBAN__c | IBAN | Text(255) |
| NameOnBankCard__c | Name On Bank Card | Text(255) |
| OfficialName__c | Official Name | Text(255) |
| HourlyRate__c | Hourly Rate | Currency |
| Contract_Start_Date__c | Contract Start Date | Date |
| Contract_End_Date__c | Contract End Date | Date |
| Offboarded_Date__c | Offboarded Date | Date |
| Profile_Completed_Date__c | Profile Completed Date | Date |
| Date_of_Birth__c | Date of Birth | Date |
| Claude_Recommendation__c | Claude Recommendation | Textarea |
| Teaching_Level_Details__c | Teaching Level Details | Textarea |
| Teaching_Location__c | Teaching Location | Picklist |
| Can_Give_Exam_Training__c | Can Give Exam Training | Checkbox |
| CanTeachElementarySchool__c | Can Teach Elementary School | Checkbox |
| Can_Teach_Until_Education_Level__c | Can Teach Until Education Level | Picklist |
| Can_Teach_Until_School_Year__c | Can Teach Until School Year | Picklist |
| Subjects__c | Subject(s) | Multi-picklist |
| Study__c | Study | Text(255) |
| University__c | University | Text(255) |
| University_HBO__c | University (HBO) | Picklist |
| University_WO__c | University (WO) | Picklist |
| HBO_WO__c | HBO / WO | Picklist |
| HBO_Bachelor__c | HBO (Bachelor) | Picklist |
| WO_Bachelor__c | WO Bachelor | Picklist |
| WO_Master__c | WO Master | Picklist |
| Comments_FromWebForm__c | Comments (From Web Form) | Textarea |
| ReferredToBPVia__c | Referred to BP Via | Picklist |
| Previous_Lifecycle_Stage__c | Previous Lifecycle Stage | Text(255) |
| Contact_Status__c | Contact Status | Picklist |
| Pro_Student_sign_up__c | Pro Student sign up | Checkbox |
| Trial_Lesson_Status__c | Trial Lesson Status | Picklist |
| Trial_Lesson_Date__c | Trial Lesson Date | Datetime |
| Teacher_Invited_At__c | Teacher Invited At | Datetime |
| Teacher_Reminder_Sent__c | Teacher Reminder Sent | Checkbox |
| Teacher_Escalation_Sent__c | Teacher Escalation Sent | Checkbox |
| Available_Timeslots__c | Available Timeslots | Textarea |
| ParentSName__c | Parent's Name | Text |
| ParentSEmail__c | Parent's Email | Email |
| ParentSPhone__c | Parent's Phone | Phone |

### SOQL timezone patroon (Amsterdam)
```
formatDate(addMinutes(now; -60); "YYYY-MM-DDTHH:mm:ss"; "Europe/Amsterdam")+01:00
```
**Let op:** Dit is wintertijd hardcoded. Dynamische versie nodig: YYYY-MM-DDTHH:mm:ssZ

---

## 3. MAKE.COM SCENARIOS

### Scenario 1 — Teacher Invitation
- **Status:** Werkend, Actief
- **Trigger:** Watch Records elke 15 min
- **Filter:** Status = Trial Class + Trial_Lesson_Status__c leeg
- **Actie:** WhatsApp template `teacher_invitation` naar docent
- **Update:** Teacher_Invited_At__c, Trial_Lesson_Status__c = Teacher Invited

### Scenario 2 — Parent Timeslot Invitation
- **Status:** Werkend, Actief
- **Trigger:** Webhook van Tally Form 1 (Immediately)
- **Module 35:** TinyURL van Google Apps Script picker link
- **Actie:** WhatsApp template `parent_timeslot_invitation`
- **Update:** Available_Timeslots__c, Trial_Lesson_Status__c = Parent Invited, Parent_Invited_At__c
- **Test URL:** https://tally.so/r/2Ekaq9?matching_number=Matching%20Number%200016&student_name=Raouf

### Scenario 3 — Trial Lesson Scheduled and Availability Conflict
- **Status:** Werkend, Actief
- **Trigger:** Webhook van Google Apps Script picker
- **Webhook URL:** https://hook.eu1.make.com/jgrnq4k8yob8txh5x0jn2ojxx94awnwr
- **Route 1 (chosen):** Bevestigt proefles, update Trial_Lesson_Date__c, status = Trial Lesson Scheduled
- **Route 2 (no_match):** Module 30 TinyURL Tally Form 3 → WhatsApp `availability_conflict_teacher` → status = Availability Conflict

### Scenario 4 — Teacher Timeslot Submission
- **Status:** Werkend, Actief
- **Trigger:** Webhook van Tally Form 3
- **Actie:** Verwerkt tijdslot na conflict, bevestiging naar ouder en docent
- **Update:** Trial_Lesson_Date__c, Trial_Lesson_Status__c = Trial Lesson Scheduled

### Scenario 5 — Availability Conflict Reminder
- **Status:** Werkend, Actief
- **Trigger:** Elke 4 uur
- **SOQL filter:** Trial_Lesson_Status__c = Availability Conflict AND Trial_Lesson_Date__c = NULL
- **Module 5:** TinyURL Tally Form 3 link
- **Actie:** WhatsApp template `availability_conflict_teacher_reminder`
- **Update:** Teacher_Escalation_Sent__c = True
- **Let op:** Ignore error handler op module 2

### Scenario 6 — Teacher Availability Reminder
- **Status:** Werkend, Actief
- **Trigger:** Elke 2 uur
- **SOQL:** Trial_Lesson_Status__c = Teacher Invited AND Teacher_Invited_At__c < 12u geleden AND Teacher_Reminder_Sent__c = false
- **Route 1 (First Reminder):** Module 8 TinyURL → template `teacher_availability_reminder`
- **Route 2 (Repeat):** Module 9 TinyURL → template `teacher_availability_reminder_repeat`
- **Update:** Teacher_Reminder_Sent__c = True
- **Let op:** Ignore error handler op module 2

### Scenario 7 — Internal Alert Teacher No Response
- **Status:** Werkend, Actief
- **Trigger:** Elke 15 minuten
- **SOQL:** Trial_Lesson_Status__c = Teacher Invited AND Teacher_Invited_At__c < 24u geleden AND Teacher_Escalation_Sent__c = false
- **Actie:** WhatsApp template `internal_alert_teacher_no_availability` naar intern nummer (+31613689666)
- **Update:** Teacher_Escalation_Sent__c = True

### Scenario 8 — Lesson Date Reminder
- **Status:** Werkend, Actief
- **Trigger:** Elke 15 minuten
- **SOQL:** Trial_Lesson_Status__c = Trial Lesson Scheduled
- **Router 4 routes:** 48h teacher, 24h parent, 2h teacher, 2h parent

### Scenario 9 — Parent Timeslot Reminders en Escalatie
- **Status:** Werkend, Actief
- **Trigger:** Elke 15 minuten

### Scenario 10 — Salesforce → MailerLite New Registration
- **Status:** Deels werkend
- **Fix toegepast:** Filter toegevoegd om records met lege Subjects__c te skippen
- **Openstaand probleem:** WhatsApp module 6 error — lege tekst parameter

### Scenario 11 — Post-trial lesson flow
- **Status:** Werkend maar timezone probleem
- **Probleem:** SOQL gebruikt hardcoded +01:00 (wintertijd)
- **Fix nodig:** Dynamische timezone YYYY-MM-DDTHH:mm:ssZ

### Scenario 12 — Docent New Registration
- **Status:** Actief, werkend
- **Scenario ID:** 5223712
- **Schedule:** Elke 15 minuten (interval: 900)
- **Modules:**
  1. Salesforce Watch Records — nieuwe Account (create), limit 10
  2. Salesforce Get a Record — filter: RecordTypeId = 012KB000000ojZLYAY AND LifecycleStage__c = New
  3. MailerLite Create/Update Subscriber — groep 183306606217266363
- **Claude AI module:** bewust verwijderd (JSON escaping problemen in Make.com JSON string mode)
- **Reden verwijdering:** Make.com's JSON string mode ondersteunt char() niet → "Function 'char' not found"

### Scenario 13 — Docent Lifecycle Automation
- **Status:** Werkend, Actief
- **Trigger:** Salesforce Watch Records op LifecycleStage__c wijziging
- **Route 1 — Interview Invited:**
  - MailerLite groep toevoegen + automation starten
  - WhatsApp sturen: "Hoi {FirstName}, we hebben je zojuist een uitnodiging voor een gesprek gestuurd via email. Check ook je spambox. Tot snel! 🐼 Team Bright Panda"
  - Telefoonnummer via: replace(1.Phone; "+"; "")
- **Route 2 — Contracting:**
  - Contract_End_Date__c berekenen: Contract_Start_Date__c + 365 dagen
  - Contract versturen via DocuSeal met velden: name, street, city, start_date, hourly_rate, signing_date
  - Document naam via OfficialName__c
- **Route 3 — On-boarded:**
  - MailerLite groep updaten
- **Route 4 — Not a Match / Not Interested / Offboarded:**
  - Verwijderen uit MailerLite
  - Offboarded_Date__c invullen bij Offboarded

### Scenario 14 — DocuSeal Contract Signed Webhook
- **Status:** Werkend, Actief
- **Trigger:** DocuSeal webhook (contract getekend)
- **Actie:** SOQL lookup op email → update lifecycle naar Pending Onboarding → MailerLite groep toevoegen

---

## 4. WHATSAPP TEMPLATES

| Template naam | Status | Omschrijving |
|---|---|---|
| teacher_invitation | Approved | Uitnodiging docent voor proefles |
| parent_timeslot_invitation | Approved | Tijdslot selectie voor ouder |
| parent_timeslot_final | Approved | Bevestiging proefles naar ouder |
| availability_conflict_teacher | Pending/Probleem | Conflict melding naar docent — opnieuw indienen met voorbeeldwaarden |
| availability_conflict_teacher_reminder | Pending/Probleem | Reminder bij conflict — opnieuw indienen |
| teacher_availability_reminder | Approved | Eerste reminder beschikbaarheid |
| teacher_availability_reminder_repeat | Approved | Herhaalde reminder beschikbaarheid |
| internal_alert_teacher_no_availability | Approved | Intern alert bij geen reactie docent |
| lesson_reminder_48h_teacher | Approved | 48u herinnering aan docent |

**Let op:** parent_timeslot_final — video header speelt niet automatisch af in WhatsApp → overweeg afbeelding

---

## 5. TALLY FORMULIEREN

### Form 1 — Ouder tijdslot (tally.so/r/2Ekaq9)
- Hidden fields: matching_number, student_name
- Output: gekozen tijdslot → Google Apps Script picker → Scenario 3 webhook

### Form 3 — Docent tijdslot na conflict (tally.so/r/q4PDV9)
- Trigger: Beschikbaarheidsconflict
- Output: nieuw tijdslot → Scenario 4

### Form Aanvullende Profielinfo Docent (tally.so/r/NpY9RW)
- Verstuurd bij: Pending Onboarding
- Notificatie naar: info@brightpanda.nl
- Subject: "New Tally Form Submission for Docent — Aanvullende Profielinfo / Additional Profile"
- **Velden die gemapt worden naar Salesforce:**

| Tally veld | Salesforce veld |
|---|---|
| IBAN | IBAN__c |
| Naam op bankpas | NameOnBankCard__c |
| Straat + huisnummer | BillingStreet |
| Postcode | BillingPostalCode |
| Stad | BillingCity |
| Vakken | Subjects__c |
| Max niveau | Can_Teach_Until_Education_Level__c |
| Max leerjaar | Can_Teach_Until_School_Year__c |
| Examentraining | Can_Give_Exam_Training__c |
| Basisschool | CanTeachElementarySchool__c |
| Geboortedatum | Date_of_Birth__c |
| Ingevuld op | Profile_Completed_Date__c (= vandaag) |

---

## 6. GOOGLE APPS SCRIPT

### Subject Picker
- **URL:** https://script.google.com/macros/s/AKfycbyrP2jVtMak_H2r5glM57KPvmjzBgBQ-GiObv6Iel1A5f0Y9Fu6X2GV7DmBkOX4kDRISA/exec
- **Input parameters:** matching_number, student_name
- **Wat het doet:** Toont een picker interface voor ouder/docent om tijdslot te kiezen
- **Output:** POST naar Scenario 3 webhook met JSON: `{"matching_number": "...", "student_name": "...", "status": "chosen" | "no_match"}`
- **TinyURL short link:** Aanmaken via go.brightpanda.nl voor WhatsApp gebruik

---

## 7. OPGELOSTE PROBLEMEN

### Probleem: JSON crash in Scenario 12 HTTP module
- **Foutmelding:** "Bad control character in string literal in JSON at position 1942"
- **Oorzaak:** Comments_FromWebForm__c bevatte newlines die de JSON body braken
- **Oplossing geprobeerd:** char(10), char(13), char(34) functies → werkt niet in JSON string mode
- **Uiteindelijke oplossing:** Claude AI module volledig verwijderd uit Scenario 12

### Probleem: char() functie werkt niet in Make.com JSON string mode
- **Foutmelding:** "Function 'char' not found"
- **Alternatief:** `newline` keyword gebruiken: `{{replace(2.Comments_FromWebForm__c; newline; " ")}}`

### Probleem: Scenario 12 per ongeluk verwijderd
- **Oorzaak:** Claude heeft het scenario verwijderd i.p.v. alleen de module
- **Oplossing:** Nieuw aangemaakt via API met ID 5223712
- **Afspraak:** Claude vraagt voortaan ALTIJD bevestiging voordat een scenario wordt verwijderd

### Probleem: Variabelen zwart in Make.com na API update
- **Oorzaak:** Interface metadata gaat verloren bij blueprint updates via API
- **Les:** Modules aanpassen via API werkt voor scheduling/activeren, maar complexe module inhoud handmatig doen in Make.com UI

### Probleem: Picklist waarde "Other" niet zichtbaar voor Teacher/Student
- **Oorzaak:** Nieuwe picklist waarden worden niet automatisch aan Person Account record types gekoppeld
- **Oplossing:** Handmatig inschakelen via klassieke Salesforce URL per record type

### Probleem: ReferredToBPVia__c "Other" waarde niet beschikbaar
- **Oplossing:** Via klassieke URL inschakelen voor beide record types:
  - Teacher: `brightpanda.my.salesforce.com/setup/ui/recordtypefields.jsp?id=012KB000000ojZLYAY`
  - Student: `brightpanda.my.salesforce.com/setup/ui/recordtypefields.jsp?id=012KB000000ojZGYAY`

### Probleem: Make.com checkbox velden in router filters
- **Oplossing:** Gebruik Text operators met string waarden "true" / "false", NIET Boolean operators

### Probleem: MailerLite merge tags formaat
- **Fout:** `{field_name}`
- **Correct:** `{$field_name}`

---

## 8. OPENSTAANDE PROBLEMEN

### Scenario 10 — WhatsApp module 6 fout
- **Foutmelding:** Lege tekst parameter in WhatsApp module
- **Status:** Nog niet opgelost
- **Volgende stap:** Module 6 inspecteren en lege variabele identificeren

### Scenario 11 — Timezone hardcoded wintertijd
- **Probleem:** SOQL gebruikt +01:00 hardcoded, nu zomertijd (+02:00)
- **Fix:** Dynamische timezone met formatDate + Z formaat

### WhatsApp templates opnieuw indienen
- `availability_conflict_teacher` — opnieuw indienen met voorbeeldwaarden
- `availability_conflict_teacher_reminder` — opnieuw indienen met voorbeeldwaarden

---

## 9. BESLISSINGEN & AFSPRAKEN

### Make.com via API
- Scenarios activeren/deactiveren/schedule aanpassen: ✅ via API
- Eenvoudige blueprint aanpassingen: ✅ via API
- Complexe module inhoud met variabelen: ❌ handmatig in UI (interface metadata gaat verloren)
- Scenario verwijderen: ⚠️ ALTIJD bevestiging vragen aan Raouf

### Salesforce Offboarded_Date__c
- Wordt automatisch gevuld via Scenario 13 Route 4
- Geen aparte Salesforce Flow nodig

### Contract verlenging
- Bewuste keuze: NIET automatisch verlengen
- Werkwijze: 30 dagen voor verlopen → intern alert → handmatige beoordeling → dan nieuw contract via DocuSeal

### Dagstart routine
Bij "dagstart" voert Claude uit:
1. Google Calendar vandaag ophalen
2. Salesforce docenten per lifecycle stage
3. Gmail Tally submissions verwerken (from:notifications@tally.so) → parse → update Salesforce → Profile_Completed_Date__c = vandaag
4. Gmail unread: nieuwe profielreacties + sollicitaties

### Telefoonformat
- Altijd internationaal met landcode: +31XXXXXXXXX
- Voor 360dialog API: replace(Phone; "+"; "") → verwijdert de +

### Documentnaam DocuSeal
- Dynamisch via OfficialName__c veld
- Alle template velden in lowercase

### MailerLite custom fields

| Veld | Merge tag |
|---|---|
| trial_lesson_outcome | {$trial_lesson_outcome} |
| total_matchings | {$total_matchings} |
| teacher_name | {$teacher_name} |
| subjects | {$subjects} |
| student_name | {$student_name} |
| school_year | {$school_year} |
| registration_date | {$registration_date} |
| referred_by | {$referred_by} |
| is_pro | {$is_pro} |
| is_active_client | {$is_active_client} |
| has_trial_lesson | {$has_trial_lesson} |
| name (standaard) | {$name} |
| last_name (standaard) | {$last_name} |
| phone (standaard) | {$phone} |

---

> Documentatie gegenereerd via Claude Code — Bright Panda Tutoring
