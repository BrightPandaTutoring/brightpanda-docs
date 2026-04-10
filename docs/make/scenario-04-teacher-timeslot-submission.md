# Scenario 4 — Teacher Timeslot Submission

**Laatste update:** 10 april 2026
**Status:** ✅ Werkend — Aan

---

## Doel

Verwerkt het tijdslot dat een docent indient via **Tally Form 3**, nadat er een `Availability Conflict` was (geen overlappend tijdslot tussen docent en ouder). Slaat de definitieve datum op in Salesforce en stuurt bevestigings-WhatsApp naar ouder en docent.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Webhook URL | `https://hook.eu1.make.com/1aa2q2bnkvxodps6errjs6pxs3j4v4d9` |
| Afzender | Tally Form 3 |

---

## Module Volgorde (globaal)

```
[1]  Webhook → Custom Webhook (Tally Form 3)
        ↓
[2]  Salesforce → Search Records SOQL (matching ophalen)
        ↓
[3]  Salesforce → Get a Record (Student Account)
        ↓
[4]  Salesforce → Get a Record (Teacher Account)
        ↓
[5]  Salesforce → Update a Record (Trial_Lesson_Date__c + status)
        ↓
[6]  HTTP → 360dialog (WhatsApp bevestiging naar ouder)
        ↓
[7]  HTTP → 360dialog (WhatsApp bevestiging naar docent)
```

---

## Updates in Salesforce

| Veld | Waarde |
|------|--------|
| `Trial_Lesson_Date__c` | Tijdslot ingediend door docent |
| `Trial_Lesson_Status__c` | `Trial Lesson Scheduled` |

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 3](scenario-3b-ouder-tijdslot-verwerking.md) | Triggert Availability Conflict — docent krijgt instructie om ouder te bellen |
| [Scenario 5](scenario-05-availability-conflict-reminder.md) | Reminder aan docent zolang conflict open staat |
