# Scenario 6 — Teacher Availability Reminder

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Stuurt automatisch een herinnerings-WhatsApp naar een docent die niet reageert op de uitnodiging om beschikbaarheid in te vullen (status `Teacher Invited`). Twee routes: eerste reminder na 12 uur, herhaalde reminder daarna.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 2 uur |

---

## SOQL Query

```sql
SELECT Id, Teacher__c, Student__c, Name, Trial_Lesson_Status__c,
       Teacher_Invited_At__c, Teacher_Reminder_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Teacher Invited'
AND Teacher_Invited_At__c < [12 uur geleden]
AND Teacher_Reminder_Sent__c = false
```

---

## Router — 2 Routes

### Route 1 — Eerste reminder
- **Filter:** `Teacher_Reminder_Sent__c = false`
- **Template:** `teacher_availability_reminder`
- **Update:** `Teacher_Reminder_Sent__c = true`

### Route 2 — Herhaalde reminder
- **Filter:** `Teacher_Reminder_Sent__c = true`
- **Template:** `teacher_availability_reminder_repeat`

---

## WhatsApp Templates

| Template | Status | Gebruik |
|----------|--------|---------|
| `teacher_availability_reminder` | ✅ Goedgekeurd | Eerste reminder na 12u |
| `teacher_availability_reminder_repeat` | ✅ Goedgekeurd | Herhaalde reminder |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 1](scenario-01-docent-uitnodiging-whatsapp.md) | Zet status op Teacher Invited + vult Teacher_Invited_At__c |
| [Scenario 7](scenario-07-internal-alert.md) | Intern alert na 24u geen reactie |
