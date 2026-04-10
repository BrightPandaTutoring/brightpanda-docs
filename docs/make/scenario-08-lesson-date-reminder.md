# Scenario 8 — Lesson Date Reminder

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend

---

## Doel

Stuurt automatische herinneringen aan docent en ouder voor een geplande proefles op 48 uur, 24 uur en 2 uur van tevoren.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule |
| Interval | Elke 15 minuten |

---

## SOQL Query

```sql
SELECT Id, Teacher__c, Student__c, Name, Trial_Lesson_Date__c,
       Trial_Class_Reminder_48h_Sent__c, Trial_Class_Reminder_24h_Sent__c,
       Trial_Class_Reminder_2h_Sent__c, Trial_Lesson_Status__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Trial Lesson Scheduled'
```

---

## Router — 4 Routes

| Route | Conditie | Template | Update veld |
|-------|----------|----------|-------------|
| 1 | 48u voor les + `Trial_Class_Reminder_48h_Sent__c = false` | reminder template docent | `Trial_Class_Reminder_48h_Sent__c = true` |
| 2 | 24u voor les + `Trial_Class_Reminder_24h_Sent__c = false` | reminder template ouder | `Trial_Class_Reminder_24h_Sent__c = true` |
| 3 | 2u voor les + `Trial_Class_Reminder_2h_Sent__c = false` | reminder template docent | `Trial_Class_Reminder_2h_Sent__c = true` |
| 4 | 2u voor les + `Trial_Class_Reminder_2h_Sent__c = false` | reminder template ouder | — (gecombineerd met route 3) |

---

## Salesforce Velden

| Veld | Type | Gebruik |
|------|------|---------|
| `Trial_Class_Reminder_48h_Sent__c` | Checkbox | Voorkomt dubbele 48u reminder |
| `Trial_Class_Reminder_24h_Sent__c` | Checkbox | Voorkomt dubbele 24u reminder |
| `Trial_Class_Reminder_2h_Sent__c` | Checkbox | Voorkomt dubbele 2u reminder |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 3](scenario-3b-ouder-tijdslot-verwerking.md) | Zet status op Trial Lesson Scheduled |
| [Scenario 4](scenario-04-teacher-timeslot-submission.md) | Alternatieve weg naar Trial Lesson Scheduled |
