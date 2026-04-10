# Scenario 03 — Reminders & Escalatie

**Make naam:** Bright Panda - Reminders & Escalatie
**Laatste update:** 10 april 2026
**Status:** ✅ Gebouwd — draait elke 15 minuten

---

## Doel

- Stuurt automatisch **reminders** naar docenten die niet binnen 24 uur reageren op een "Teacher Invited" status
- Stuurt **escalatiemeldingen** naar Bright Panda intern als een docent niet reageert binnen 48 uur
- Doet hetzelfde voor **ouders** die niet reageren op een "Parent Invited" status

**Probleem dat het oplost:** Bright Panda moest handmatig bijhouden wie wel en niet gereageerd had.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Schedule (tijdschema) |
| Interval | Elke 15 minuten (Make.com Free plan limiet) |

---

## Module Volgorde

```
[1] Salesforce → Search Records (SOQL — alle Teacher/Parent Invited)
        ↓
    ROUTER (4 routes)
        ├── Route 1: Teacher Reminder (24u)
        │       ↓ HTTP → WhatsApp naar docent
        │       ↓ Salesforce → Update (Teacher_Reminder_Sent__c = true)
        │
        ├── Route 2: Teacher Escalatie (48u)
        │       ↓ HTTP → WhatsApp naar intern +31613689666
        │       ↓ Salesforce → Update (Teacher_Escalation_Sent__c = true)
        │
        ├── Route 3: Parent Reminder (24u)
        │       ↓ HTTP → WhatsApp naar ouder
        │       ↓ Salesforce → Update (Parent_Reminder_Sent__c = true)
        │
        └── Route 4: Parent Escalatie (48u)
                ↓ HTTP → WhatsApp naar intern +31613689666
                ↓ Salesforce → Update (Parent_Escalation_Sent__c = true)
```

---

## SOQL Query (Module 1)

```sql
SELECT Id, Name, Teacher__c, Student__c, Trial_Lesson_Status__c, LastModifiedDate,
       Teacher_Reminder_Sent__c, Teacher_Escalation_Sent__c,
       Parent_Reminder_Sent__c, Parent_Escalation_Sent__c
FROM Student_Teacher_Matching__c
WHERE Trial_Lesson_Status__c IN ('Teacher Invited', 'Parent Invited')
```

---

## Router Condities

### Route 1 — Teacher Reminder (24u)
| Veld | Conditie |
|------|---------|
| `Trial_Lesson_Status__c` | = `Teacher Invited` |
| `Teacher_Reminder_Sent__c` | = `false` |
| `LastModifiedDate` | > 24 uur geleden |

- **Actie:** WhatsApp via `teacher_invitation` template (zelfde parameters als Scenario 01)
- **Update:** `Teacher_Reminder_Sent__c` = `true`

### Route 2 — Teacher Escalatie (48u)
| Veld | Conditie |
|------|---------|
| `Trial_Lesson_Status__c` | = `Teacher Invited` |
| `Teacher_Escalation_Sent__c` | = `false` |
| `LastModifiedDate` | > 48 uur geleden |

- **Actie:** WhatsApp vrije tekst → intern nummer `31613689666`
- **Update:** `Teacher_Escalation_Sent__c` = `true`

### Route 3 — Parent Reminder (24u)
| Veld | Conditie |
|------|---------|
| `Trial_Lesson_Status__c` | = `Parent Invited` |
| `Parent_Reminder_Sent__c` | = `false` |
| `LastModifiedDate` | > 24 uur geleden |

- **Actie:** WhatsApp via `parent_timeslot_invitation` template
- **Update:** `Parent_Reminder_Sent__c` = `true`

### Route 4 — Parent Escalatie (48u)
| Veld | Conditie |
|------|---------|
| `Trial_Lesson_Status__c` | = `Parent Invited` |
| `Parent_Escalation_Sent__c` | = `false` |
| `LastModifiedDate` | > 48 uur geleden |

- **Actie:** WhatsApp vrije tekst → intern nummer `31613689666`
- **Update:** `Parent_Escalation_Sent__c` = `true`

---

## Salesforce Checkboxvelden

> ✅ Alle 4 velden zijn al aangemaakt in Salesforce en klaar voor gebruik.

| Veld | Type | Wanneer `true` |
|------|------|---------------|
| `Teacher_Reminder_Sent__c` | Checkbox | Na versturen 24u reminder aan docent |
| `Teacher_Escalation_Sent__c` | Checkbox | Na versturen 48u escalatie |
| `Parent_Reminder_Sent__c` | Checkbox | Na versturen 24u reminder aan ouder |
| `Parent_Escalation_Sent__c` | Checkbox | Na versturen 48u escalatie ouder |

---

## Gekoppelde Apps & Services

| Service | Gebruik |
|---------|---------|
| **Salesforce** | SOQL query + update checkboxvelden |
| **360dialog** | WhatsApp reminders + interne notificaties |

---

## Speciale Opmerkingen

- 📢 Escalaties gaan via WhatsApp naar `+31613689666` (intern Bright Panda nummer)
- 📋 WhatsApp reminder templates: `teacher_invitation` (al goedgekeurd) en `parent_timeslot_invitation` (al goedgekeurd)
- ⏱️ Draait elke 15 minuten vanwege Make.com Free plan limiet (ideaal zou elk uur zijn)

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 01](scenario-01-docent-uitnodiging-whatsapp.md) | Zet status op Teacher Invited |
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Zet status op Parent Invited |
