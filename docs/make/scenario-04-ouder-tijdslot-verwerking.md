# Scenario 04 — Ouder Tijdslot Verwerking

**Make naam:** Nog niet aangemaakt
**Laatste update:** 10 april 2026
**Status:** 🔴 Nog te bouwen — logica ontworpen

---

## Doel

Verwerkt de tijdslot keuze die een ouder maakt via **Tally Form 2**. Zoekt het gekozen tijdslot op in `Available_Timeslots__c`, slaat de definitieve datum op in Salesforce, en stuurt een bevestiging naar zowel ouder als docent.

---

## Trigger

| Eigenschap | Waarde |
|-----------|--------|
| Type | Custom Webhook |
| Formulier | Tally Form 2 (`https://tally.so/r/WOozov`) |
| Webhook | Nog te koppelen in Tally Form 2 → Settings → Integrations → Webhooks |

---

## Geplande Module Volgorde

```
[1] Webhooks → Custom Webhook (Tally Form 2 submission)
        ↓
[2] Salesforce → Search Records (SOQL op matching_number)
        ↓
[3] Salesforce → Get a Record (haal Available_Timeslots__c op)
        ↓
[4] Tools → Parse tijdslot uit Available_Timeslots__c op basis van gekozen getal
        ↓
[5] IF: ouder koos "geen tijdslot past"
        ├── YES: HTTP → WhatsApp escalatie naar +31613689666
        └── NO:
                ↓
           [6] Salesforce → Update a Record
               - Trial_Lesson_Date__c = gevonden tijdslot
               - Trial_Lesson_Status__c = Trial Lesson Scheduled
                ↓
           [7] HTTP → WhatsApp bevestiging naar ouder (trial_lesson_confirmation)
                ↓
           [8] HTTP → WhatsApp bevestiging naar docent (trial_lesson_confirmation)
```

---

## Logica: Tijdslot Opzoeken

`Available_Timeslots__c` bevat de lijst in dit format (aangemaakt door Scenario 02):
```
1=12 maart 13:00-14:00|2=12 maart 14:00-15:00|3=25 maart 10:00-11:00
```

**Stappenplan:**
1. Ontvang gekozen getal van ouder via Form 2 (bijv. `2`)
2. Split `Available_Timeslots__c` op `|` → array van `"1=datum tijd"` strings
3. Zoek het item dat begint met `"2="` → `"2=12 maart 14:00-15:00"`
4. Strip het getal en `=` → `"12 maart 14:00-15:00"`
5. Sla op in `Trial_Lesson_Date__c`

---

## Form 2 Datastructuur (Tally Form 2)

**URL:** `https://tally.so/r/WOozov`

**Hidden fields (via URL parameters ingevuld door Scenario 02):**
- `matching_number` — bijv. `"0016"`
- `student_name` — bijv. `"Raouf"`

**Zichtbare velden:**
| Veld | Type | Verplicht | Beschrijving |
|------|------|-----------|-------------|
| Beschrijvingstekst | — | — | "Je hebt via WhatsApp een lijst met beschikbare tijdsloten ontvangen. Typ het nummer van het tijdslot dat het beste uitkomt." |
| Nummer van je keuze | NUMBER | Ja | Ouder typt het getal van het gewenste tijdslot |
| "Past geen tijdslot?" | CHECKBOXES | Nee | Optie: "Nee, geen van de tijdsloten past mij" |
| Datum 1 | INPUT_DATE | Nee | Alternatieve beschikbaarheid als geen tijdslot past |
| Tijdsloten datum 1 | CHECKBOXES | Nee | Alternatieve tijdsloten |
| Datum 2 | INPUT_DATE | Nee | — |
| Tijdsloten datum 2 | CHECKBOXES | Nee | — |
| Datum 3 | INPUT_DATE | Nee | — |
| Tijdsloten datum 3 | CHECKBOXES | Nee | — |

---

## Salesforce Veld Updates

| Veld | Waarde | Conditie |
|------|--------|---------|
| `Trial_Lesson_Date__c` | Gevonden tijdslot uit `Available_Timeslots__c` | Als ouder een getal koos |
| `Trial_Lesson_Status__c` | `Trial Lesson Scheduled` | Als tijdslot gevonden |

---

## WhatsApp Template

**Template:** `trial_lesson_confirmation`
**Status:** ✅ Goedgekeurd door Meta
**Ontvangers:** Zowel ouder als docent

> ⚠️ Disclaimer nog toe te voegen als **laatste stap na volledig testen**. Elke template wijziging vereist opnieuw Meta goedkeuring (wachttijd: 2-7 dagen).

---

## Speciale Opmerkingen

- 📱 Docent en ouder krijgen **elkaars telefoonnummer pas in de bevestiging** (privacy)
- ⚠️ Als checkbox "geen tijdslot past" aangevinkt → escalatie WhatsApp naar `+31613689666`
- 📋 Verzetten en annuleren van proeflessen gaat **handmatig** — contactgegevens staan in de WhatsApp disclaimer
- 💾 `Available_Timeslots__c` wordt aangemaakt in Scenario 02 (type: Text Area Long, 10.000 tekens)

---

## Gerelateerde Scenario's

| Scenario | Beschrijving |
|----------|-------------|
| [Scenario 02](scenario-02-tally-webhook-ouder-planning.md) | Vult `Available_Timeslots__c` en stuurt Form 2 link naar ouder |
| [Scenario 03](scenario-03-reminders-escalatie.md) | Reminders bij niet-reagerende ouder |
