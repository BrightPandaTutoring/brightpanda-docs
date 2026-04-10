# Scenario 7 — Internal Alert Teacher No Response

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend

---

## Doel

Stuurt een intern WhatsApp alert naar Bright Panda wanneer een docent na 24 uur nog steeds niet heeft gereageerd op de uitnodiging om beschikbaarheid in te vullen.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 15 minuten |

---

## SOQL Query

```sql
SELECT Id, Teacher__c, Student__c, Name, Trial_Lesson_Status__c,
       Teacher_Invited_At__c, Teacher_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Teacher Invited'
AND Teacher_Invited_At__c < [24 uur geleden]
AND Teacher_Escalation_Sent__c = false
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
[4]  Salesforce → Get a Record (Student Account)
        ↓
[5]  HTTP → 360dialog (WhatsApp internal_alert_teacher_no_availability → 31613689666)
        ↓
[6]  Salesforce → Update a Record (Teacher_Escalation_Sent__c = true)
```

---

## WhatsApp Template

| Instelling | Waarde |
|-----------|--------|
| **Template** | `internal_alert_teacher_no_availability` |
| **Naar** | `31613689666` (intern Bright Panda nummer) |
| **Status template** | ✅ Goedgekeurd |

---

## Update

| Veld | Waarde |
|------|--------|
| `Teacher_Escalation_Sent__c` | `true` |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 6](scenario-06-teacher-availability-reminder.md) | Reminders aan docent voordat intern alert verstuurd wordt |
