# Scenario 9 — Parent Timeslot Reminders & Escalatie

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend

---

## Doel

Stuurt automatisch herinneringen en escalaties naar ouders die niet reageren op de uitnodiging om een tijdslot te kiezen via de picker pagina (status `Parent Invited`). Na 72 uur zonder reactie wordt de status bijgewerkt naar `No Show`.

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
       Parent_Invited_At__c, Parent_Reminder_Sent__c, Parent_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c = 'Parent Invited'
```

---

## Router — 3 Routes

### Route 1 — Reminder na 24u
- **Conditie:** `Parent_Invited_At__c < 24u geleden` AND `Parent_Reminder_Sent__c = false`
- **Actie:** WhatsApp reminder naar ouder (picker link opnieuw sturen)
- **Update:** `Parent_Reminder_Sent__c = true`

### Route 2 — Escalatie na 48u
- **Conditie:** `Parent_Invited_At__c < 48u geleden` AND `Parent_Escalation_Sent__c = false`
- **Actie:** WhatsApp intern alert naar `31613689666`
- **Update:** `Parent_Escalation_Sent__c = true`

### Route 3 — Final na 72u → No Show
- **Conditie:** `Parent_Invited_At__c < 72u geleden`
- **Actie:** Update `Trial_Lesson_Status__c = No Show`

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 2](scenario-02-tally-webhook-ouder-planning.md) | Zet status op Parent Invited + vult Parent_Invited_At__c |
| [Scenario 3](scenario-3b-ouder-tijdslot-verwerking.md) | Verwerkt reactie ouder via picker |
