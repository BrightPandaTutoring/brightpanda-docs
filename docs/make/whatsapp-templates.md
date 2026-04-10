# WhatsApp Templates — Overzicht

Alle templates zijn ingediend bij 360dialog en door Meta goedgekeurd.

**360dialog endpoint:** `https://waba-v2.360dialog.io/messages`
**WhatsApp nummer:** `+1 555-759-0811` (API formaat: `15557590811`)

---

## Overzicht

| Template naam | Status | Params | Naar | Gebruikt in |
|--------------|--------|--------|------|------------|
| `teacher_invitation` | ✅ APPROVED | 6 | Docent | Scenario 1 |
| `parent_timeslot_invitation` | ✅ APPROVED | 4 | Ouder | Scenario 2 |
| `trial_lesson_confirmation_parent` | ✅ APPROVED | 6 | Ouder | Scenario 3b Route 1 + Scenario 4 |
| `trial_lesson_confirmed_teacher` | ✅ APPROVED | 6 | Docent | Scenario 3b Route 1 + Scenario 4 |
| `availability_conflict_teacher` | ✅ APPROVED | 5 | Docent | Scenario 3b Pad B |
| `availability_conflict_teacher_reminder` | ✅ APPROVED | 5 | Docent | Scenario 5 |
| `teacher_availability_reminder` | ✅ APPROVED | 3 | Docent | Scenario 6 Route 1 |
| `teacher_availability_reminder_repeat` | ✅ APPROVED | 3 | Docent | Scenario 6 Route 2 |
| `parent_timeslot_reminder` | ✅ APPROVED | 4 | Ouder | Reminders & Escalatie Route 1 |
| `parent_timeslot_escalation` | ✅ APPROVED | 4 | Ouder | Reminders & Escalatie Route 2 |
| `parent_timeslot_final` | ✅ APPROVED | 3 | Ouder | Reminders & Escalatie Route 3 (+ video header) |
| `internal_alert_teacher_no_availability` | ✅ APPROVED | 5 | Intern | Scenario 7 |
| `internal_alert_teacher_no_conflict_resolution` | ✅ APPROVED | 5 | Intern | Scenario 5 (escalatie) |
| `internal_alert_parent_no_timeslot` | ✅ APPROVED | 6 | Intern | Reminders & Escalatie Route 2 |
| `lesson_reminder_48h_teacher` | ✅ APPROVED | 4 | Docent | Scenario 8 Route 1 |
| `lesson_reminder_24h_parent` | ✅ APPROVED | 5 | Ouder | Scenario 8 Route 2 |
| `lesson_reminder_2h_teacher` | ✅ APPROVED | 6 | Docent | Scenario 8 Route 3 |
| `lesson_reminder_2h_parent` | ✅ APPROVED | 5 | Ouder | Scenario 8 Route 4 |

> ⚠️ Elke template aanpassing vereist opnieuw Meta goedkeuring (wachttijd: 2-7 werkdagen). Pas templates alleen aan na volledig testen. Dien altijd in als **Utility** categorie zonder emoji's in de tekst.

---

## Volledige Template Teksten

---

### `teacher_invitation`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=vak NL, `{{4}}`=ouder naam, `{{5}}`=ouder telefoon, `{{6}}`=Tally Form 1 link

```
Hoi {{1}},

Je bent gematcht met een nieuwe leerling via Bright Panda Bijles.

Leerling: *{{2}}*
Vak: *{{3}}*

Contactgegevens ouder:
Naam: *{{4}}*
Telefoon: *{{5}}*

Vul zo snel mogelijk je beschikbaarheid in via deze link:

{{6}}

Neem daarna contact op met de ouder via WhatsApp of telefoon om jezelf voor te stellen.
Dit maakt een goede eerste indruk en biedt de kans om alvast belangrijke details te bespreken.

Hoe sneller jij reageert, hoe groter de kans dat wij deze leerling aan jou kunnen koppelen!

Dit nummer is alleen voor het inplannen van proeflessen en wordt niet gebruikt voor communicatie.
Voor andere vragen kun je ons bereiken via WhatsApp of telefoon: +31613689666.

Bedankt!
```

---

### `parent_timeslot_invitation`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=docent naam, `{{4}}`=picker link (TinyURL)

```
Hoi {{1}},

Leerling {{2}} is gematcht met een docent via Bright Panda Bijles!

Docent: {{3}}

Kies een tijdslot voor de proefles via de link hieronder.
Hoe sneller je kiest, hoe eerder de proefles ingepland kan worden!

{{4}}

Dit nummer is alleen voor het inplannen van proeflessen en wordt niet gebruikt voor communicatie.
Voor andere vragen kun je ons bereiken via WhatsApp: +31613689666 of telefoon: 071-3031901.

Bedankt!
```

---

### `trial_lesson_confirmation_parent`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=datum, `{{4}}`=tijd, `{{5}}`=docent naam, `{{6}}`=docent telefoon

```
Hoi {{1}},

De proefles is bevestigd!

Leerling: {{2}}
Datum: {{3}}
Tijd: {{4}}

Contactgegevens docent:
Naam: {{5}}
Telefoon: {{6}}

Tot dan!
```

---

### `trial_lesson_confirmed_teacher`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=datum, `{{4}}`=tijd, `{{5}}`=ouder naam, `{{6}}`=ouder telefoon

```
Hoi {{1}},

De proefles is bevestigd.

Leerling: {{2}}
Datum: {{3}}
Tijd: {{4}}

Contactgegevens ouder:
Naam: {{5}}
Telefoon: {{6}}

Tot dan!
```

---

### `availability_conflict_teacher`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=ouder naam, `{{4}}`=ouder telefoon, `{{5}}`=Tally Form 3 link

```
⚠️ *Actie vereist!*

Hoi {{1}}, de ouder van leerling {{2}} kon geen geschikt tijdslot vinden in de planner.

*Neem direct contact op met de ouder om een tijdslot af te spreken voor de proefles.*

Ouder: {{3}}
Telefoon: {{4}}

✅ Heb je een tijdslot afgesproken? Vul dit dan direct in via onderstaande link — anders blijf je iedere 4 uur een herinnering ontvangen:
{{5}}

Heb je vragen? Stuur een WhatsApp naar +31613689666 of bel 071-3031901.
```

---

### `availability_conflict_teacher_reminder`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=ouder naam, `{{4}}`=ouder telefoon, `{{5}}`=Tally Form 3 link

```
⚠️ *Reminder!*

Hoi {{1}}, ons systeem heeft nog geen bevestiging ontvangen van een geplande proefles voor leerling {{2}}.

*Neem direct contact op met de ouder en spreek een tijdslot af.*

Ouder: {{3}}
Telefoon: {{4}}

✅ Heb je een tijdslot afgesproken? Vul dit dan direct in via onderstaande link — anders blijf je iedere 4 uur een herinnering ontvangen:
{{5}}

Heb je vragen? Stuur een WhatsApp naar +31613689666 of bel 071-3031901.
```

---

### `teacher_availability_reminder`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=Tally Form 1 link

```
⚠️ *Reminder!*

Hoi {{1}}, 12 uur geleden ben je gematcht met leerling {{2}}, maar we hebben nog geen beschikbaarheid ontvangen.

Ouders melden hun kind aan met veel vertrouwen en wachten gespannen op nieuws. Elke uur telt, een snelle reactie is het verschil tussen een enthousiaste ouder en een afhakende ouder!

*Klik op de link en vul je beschikbaarheid in. Zolang dit niet is gedaan, blijf je iedere 2 uur een herinnering ontvangen.*

{{3}}

Heb je vragen? Stuur een WhatsApp naar +31613689666 of bel 071-3031901.
```

---

### `teacher_availability_reminder_repeat`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=Tally Form 1 link

```
⚠️ *Reminder!*

Hoi {{1}}, we hebben nog steeds geen beschikbaarheid ontvangen voor leerling {{2}}.

Ouders melden hun kind aan met veel vertrouwen en wachten gespannen op nieuws. Elke uur telt, een snelle reactie is het verschil tussen een enthousiaste ouder en een afhakende ouder!

*Klik op de link en vul je beschikbaarheid in. Zolang dit niet is gedaan, blijf je iedere 2 uur een herinnering ontvangen.*

{{3}}

Heb je vragen? Stuur een WhatsApp naar +31613689666 of bel 071-3031901.
```

---

### `parent_timeslot_reminder`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=docent naam, `{{4}}`=picker link (TinyURL)

```
⚠️ *Reminder!*

Hoi {{1}}, je hebt nog geen tijdslot gekozen voor de proefles van {{2}} met docent {{3}}.

*Klik op de link en kies een tijdslot, het duurt maar 1 minuut en hoe eerder je kiest, hoe sneller de proefles ingepland is!*

{{4}}

Heb je vragen? Stuur een WhatsApp naar +31613689666 of bel 071-3031901.
```

---

### `parent_timeslot_escalation`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=docent naam, `{{4}}`=picker link (TinyURL)

```
⚠️ *Heb je de proefles opgegeven?* ⚠️

Hoi {{1}},

Docent {{3}} staat klaar om de proefles aan {{2}} te geven. Het enige wat nog gedaan moet worden is een datum plannen! Er is helaas nog geen datum gepland, dit is een laatste reminder om dit alsnog te doen.

Dit kost minder dan een minuut en kan via deze link:
{{4}}

We kunnen de docent niet onbeperkt gereserveerd houden. Bij uitblijven van een keuze vervalt de beschikbaarheid en de proefles.

Heb je vragen? Stuur een WhatsApp naar +31613689666 of bel 071-3031901.
```

---

### `parent_timeslot_final`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=docent naam
**Header:** Video — `https://media.tenor.com/AHr4JyE49zMAAAPo/x4ndrr-jake-gyllenhaal.mp4`

> ⚠️ Video speelt niet automatisch af in WhatsApp — overweging: vervangen door afbeelding

```
⚠️ *Proces inplannen proefles gestopt* ⚠️

Hoi {{1}},

Docent {{3}} was gekoppeld om de proefles aan {{2}} te geven. Helaas is er geen datum ingepland en sluiten we daarom deze file.

Is dit een fout of wil je alsnog de proefles inplannen? Neem dan contact met ons op via WhatsApp +31613689666 of bel 071-3031901.
```

---

### `internal_alert_teacher_no_availability`
**Params:** `{{1}}`=docent voornaam, `{{2}}`=docent achternaam, `{{3}}`=leerling naam, `{{4}}`=docent telefoon, `{{5}}`=matching number
**Naar:** `31613689666`

```
⚠️ *Actie vereist — Bright Panda intern!*

Docent {{1}} {{2}} heeft na 24 uur nog geen beschikbaarheid ingevuld voor leerling {{3}}.

*Neem direct contact op met de docent.*

Docent telefoon: {{4}}
Matching: {{5}}

Bel nu!
```

---

### `internal_alert_teacher_no_conflict_resolution`
**Params:** `{{1}}`=docent voornaam, `{{2}}`=docent achternaam, `{{3}}`=leerling naam, `{{4}}`=docent telefoon, `{{5}}`=matching number
**Naar:** `31613689666`

```
⚠️ *Actie vereist — Bright Panda intern!*

De ouder van leerling {{3}} heeft aangegeven dat geen van de aangeboden tijdsloten past. Docent {{1}} {{2}} heeft na 24 uur nog geen nieuw tijdslot afgesproken met de ouder.

*Neem direct contact op met de docent.*

Docent telefoon: {{4}}
Matching: {{5}}

Bel nu!
```

---

### `internal_alert_parent_no_timeslot`
**Params:** `{{1}}`=leerling naam, `{{2}}`=docent voornaam, `{{3}}`=docent achternaam, `{{4}}`=ouder naam, `{{5}}`=ouder telefoon, `{{6}}`=matching number
**Naar:** `31613689666`

```
⚠️ *Actie vereist — Bright Panda intern!*

De ouder van leerling {{1}} heeft na 48 uur nog geen tijdslot gekozen voor de proefles met docent {{2}} {{3}}.

*Neem direct contact op met de ouder.*

Ouder: {{4}}
Telefoon: {{5}}
Matching: {{6}}

Bel nu!
```

---

### `lesson_reminder_48h_teacher`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=datum (DD-MM-YYYY), `{{4}}`=tijd (HH:mm)

```
🔔 *Herinnering proefles!*

Hoi {{1}},

Op {{3}} om {{4}} geef je proefles aan leerling {{2}}.

💡 *Tips voor een succesvolle proefles:*

📚 *Voorbereiding:*
- Vraag welke stof behandeld wordt en vraag foto's via WhatsApp
- Wees op tijd, bij voorkeur 5 minuten eerder

👋 *Eerste indruk:*
- Stel jezelf voor en vraag naar de leerdoelen
- Zorg voor een verzorgde uitstraling, je krijgt maar één kans op een goede eerste indruk!

✏️ *Tijdens de les:*
- Breek het ijs, vertel iets over jezelf
- Wees assertief, jij bent de docent
- Ritme: uitleg, voorbeeld, zelfstandig oefenen
- Vraag door, niet elke leerling geeft aan als hij/zij iets niet snapt

🏁 *Afsluiting:*
- Geef aan wat er in een volgende les behandeld kan worden
- Bright Panda neemt na de proefles contact op met de ouder

💻 *Online les?*
- Stuur vandaag nog een Google Meet link. Nog geen Workspace account? Neem contact op
- Zorg voor een rustige locatie, goede internetverbinding en zet je camera aan

Veel succes! 🌟
```

---

### `lesson_reminder_24h_parent`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=docent naam, `{{4}}`=datum, `{{5}}`=tijd

```
🔔 *Herinnering proefles morgen!*

Hoi {{1}}, morgen is de proefles van {{2}} met docent {{3}}.

📅 Datum: {{4}}
⏰ Tijd: {{5}}

Neem bij vragen contact op via WhatsApp +31613689666 of bel 071-3031901.
```

---

### `lesson_reminder_2h_teacher`
**Params:** `{{1}}`=docent naam, `{{2}}`=leerling naam, `{{3}}`=datum, `{{4}}`=tijd, `{{5}}`=ouder naam, `{{6}}`=ouder telefoon

```
🔔 *Proefles over 2 uur!*

Hoi {{1}}, over 2 uur geef je proefles aan leerling {{2}}.

📅 Datum: {{3}}
⏰ Tijd: {{4}}

Ouder: {{5}}
Telefoon: {{6}}

Veel succes! 🌟
```

---

### `lesson_reminder_2h_parent`
**Params:** `{{1}}`=ouder naam, `{{2}}`=leerling naam, `{{3}}`=docent naam, `{{4}}`=datum, `{{5}}`=tijd

```
🔔 *Veel succes met de proefles!*

Hoi {{1}}, over 2 uur begint de proefles van {{2}} met docent {{3}}. Bij Bright Panda is de leerling in goede handen, we hebben er alle vertrouwen in!

📅 Datum: {{4}}
⏰ Tijd: {{5}}

Na de proefles nemen we contact met je op om te horen hoe het ging.

Neem bij vragen contact op via WhatsApp +31613689666 of bel 071-3031901.
```
