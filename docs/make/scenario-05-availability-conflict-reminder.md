# Scenario 5 — Availability Conflict Reminder

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Stuurt automatisch een herinnerings-WhatsApp naar een docent elke 4 uur zolang de matching status `Availability Conflict` heeft en er nog geen definitieve datum (`Trial_Lesson_Date__c`) is ingepland. De docent wordt herinnerd om de ouder te bellen en een tijdslot in te plannen via Tally Form 3.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 4 uur |

---

## SOQL Query

```sql
SELECT Id, Teacher__c, Student__c, Name, Trial_Lesson_Status__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Availability Conflict'
AND Trial_Lesson_Date__c = NULL
```

---

## Module Volgorde

```
[1]  Schedule trigger
        ↓
[2]  Salesforce → Search Records SOQL
        ↓
[3]  Salesforce → Get a Record (Teacher Account)
        ↓
[4]  HTTP → 360dialog (WhatsApp availability_conflict_teacher_reminder)
        ↓
[5]  HTTP → TinyURL (Tally Form 3 URL verkorten)
        ↓
[6]  Salesforce → Update a Record (Teacher_Escalation_Sent__c = true)
```

---

## WhatsApp Template

| Instelling | Waarde |
|-----------|--------|
| **Template** | `availability_conflict_teacher_reminder` |
| **Status** | ✅ Goedgekeurd |

---

## TinyURL — Module 5

- **Doel:** Tally Form 3 URL verkorten voor WhatsApp bericht
- **API:** `https://api.tinyurl.com/create`
- **Branded domain:** `go.brightpanda.nl`

---

## Update

| Veld | Waarde |
|------|--------|
| `Teacher_Escalation_Sent__c` | `true` |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 3](scenario-3b-ouder-tijdslot-verwerking.md) | Zet status op Availability Conflict |
| [Scenario 4](scenario-04-teacher-timeslot-submission.md) | Verwerkt Tally Form 3 wanneer docent reageert |
