# Scenario 03 — Reminders & Escalatie

**Make naam:** Nog niet aangemaakt (werknaam: "Reminder & Escalation")
**Laatste update:** 10 april 2026
**Status:** 🔴 Nog te bouwen

> **Prioriteit:** Wordt opgepakt nadat Scenario 01 en 02 volledig werken.

---

## Doel

- Stuurt automatisch **reminders** naar docenten die niet binnen 24 uur reageren op een "Teacher Invited" status
- Stuurt een **escalatiemelding** naar Bright Panda intern als een docent niet reageert binnen 48 uur
- Doet hetzelfde voor **ouders** die niet reageren op een "Parent Invited" status

**Probleem dat het oplost:** Bright Panda moest handmatig bijhouden wie wel en niet gereageerd had.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule (tijdschema) |
| Frequentie | Elk uur |
| Reden | Balans tussen responsiviteit en Make.com operatiekosten |

---

## Modules / Stappen (gepland)

```
[1]  Salesforce → Search Records (docent reminder — 24u)
        ↓
[2]  HTTP → POST 360dialog → reminder naar docent
        ↓
[3]  Salesforce → Update Record (Teacher_Reminder_Sent__c = true)
        ↓
[4]  Salesforce → Search Records (docent escalatie — 48u)
        ↓
[5]  HTTP → POST 360dialog → escalatie naar Bright Panda intern
        ↓
[6]  Gmail / Email → escalatie email naar Bright Panda intern
        ↓
[7]  Salesforce → Update Record (Teacher_Escalation_Sent__c = true)
        ↓
[8-14] Herhaal stappen 1-7 voor ouder (Parent Invited flow)
```

---

## SOQL Queries

### Docent reminder (24u)
```sql
SELECT Id, Teacher__c, Trial_Lesson_Status__c, LastModifiedDate, Teacher_Reminder_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Teacher Invited'
AND Teacher_Reminder_Sent__c = false
AND LastModifiedDate < LAST_N_HOURS:24
```

### Docent escalatie (48u)
```sql
SELECT Id, Teacher__c, Trial_Lesson_Status__c, LastModifiedDate, Teacher_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Teacher Invited'
AND Teacher_Escalation_Sent__c = false
AND LastModifiedDate < LAST_N_HOURS:48
```

### Ouder reminder (24u)
```sql
SELECT Id, Student__c, Trial_Lesson_Status__c, LastModifiedDate, Parent_Reminder_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Parent Invited'
AND Parent_Reminder_Sent__c = false
AND LastModifiedDate < LAST_N_HOURS:24
```

### Ouder escalatie (48u)
```sql
SELECT Id, Student__c, Trial_Lesson_Status__c, LastModifiedDate, Parent_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Parent Invited'
AND Parent_Escalation_Sent__c = false
AND LastModifiedDate < LAST_N_HOURS:48
```

---

## Salesforce Velden (al aangemaakt)

| Veld | Type | Wanneer `true` |
|------|------|---------------|
| `Teacher_Reminder_Sent__c` | Checkbox | Na versturen 24u reminder aan docent |
| `Teacher_Escalation_Sent__c` | Checkbox | Na versturen 48u escalatie |
| `Parent_Reminder_Sent__c` | Checkbox | Na versturen 24u reminder aan ouder |
| `Parent_Escalation_Sent__c` | Checkbox | Na versturen 48u escalatie ouder |

> ✅ Alle 4 checkboxvelden zijn al aangemaakt in Salesforce en klaar voor gebruik.

---

## Filters / Condities

| Flow | Conditie |
|------|---------|
| Docent reminder | `status = Teacher Invited` AND `Teacher_Reminder_Sent__c = false` AND `LastModifiedDate < 24u geleden` |
| Docent escalatie | `status = Teacher Invited` AND `Teacher_Escalation_Sent__c = false` AND `LastModifiedDate < 48u geleden` |
| Ouder reminder | `status = Parent Invited` AND `Parent_Reminder_Sent__c = false` AND `LastModifiedDate < 24u geleden` |
| Ouder escalatie | `status = Parent Invited` AND `Parent_Escalation_Sent__c = false` AND `LastModifiedDate < 48u geleden` |

---

## Gekoppelde Apps & Services

| Service | Gebruik |
|---------|---------|
| **Salesforce** | SOQL queries + update checkboxvelden |
| **360dialog** | WhatsApp reminders naar docent/ouder + interne notificatie |
| **Gmail / Email** | Interne escalatie email naar Bright Panda |

---

## Escalatie Configuratie

- **Intern WhatsApp nummer:** `+31613689666`
- **Kanalen:** WhatsApp **én** email (bewuste keuze voor redundantie — escalaties mogen niet gemist worden)

---

## Speciale Opmerkingen

- 📋 WhatsApp template voor reminder nog **niet aangemaakt** — moet nog worden aangemaakt in 360dialog en ingediend bij Meta
- ✅ De 4 Salesforce checkboxvelden zijn al klaar
- 🚧 Bouwen na werkend Scenario 01 en 02

---

## Foutmeldingen & Oplossingen

*Nog geen fouten — scenario is nog niet gebouwd.*

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Zet status op Teacher Invited |
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Zet status op Parent Invited |
