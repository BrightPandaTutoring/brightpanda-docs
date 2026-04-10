# MailerLite Inrichting — Bright Panda Bijles

**URL:** app.mailerlite.com
**Account:** Bright Panda Bijles
**Plan:** Growing Business
**Connectienaam in Make.com:** MailerLite Bright Panda
**API Token:** opgeslagen door gebruiker (niet in docs om veiligheidsredenen)

---

## Groepen

| Naam | Doel |
|------|------|
| Nieuwe Proefles Aanmelding | Automatisch bij aanmelding → triggert welkomstmail automation |
| Proefles Ingepland | Na bevestiging proefles |
| Actieve Klanten | Na succesvolle proefles |
| Wrong Match | Status-gebaseerde opvolging |
| Stopped - Never Converted | Uitgestroomde niet-klanten |
| Stopped - Existing Client | Gestopte klanten |

---

## Custom Fields

| Naam | Type | MailerLite Tag |
|------|------|----------------|
| `student_name` | TEXT | `{$student_name}` |
| `has_trial_lesson` | TEXT | `{$has_trial_lesson}` |
| `is_active_client` | TEXT | `{$is_active_client}` |
| `trial_lesson_outcome` | TEXT | `{$trial_lesson_outcome}` |
| `registration_date` | DATE | `{$registration_date}` |
| `total_matchings` | NUMBER | `{$total_matchings}` |
| `education_level` | TEXT | `{$education_level}` |
| `school_year` | NUMBER | `{$school_year}` |
| `subjects` | TEXT | `{$subjects}` |
| `is_pro` | TEXT | `{$is_pro}` |
| `referred_by` | TEXT | `{$referred_by}` |
| `gender_preference` | TEXT | `{$gender_preference}` |
| `comments` | TEXT | `{$comments}` |

> **Beginswaarden bij aanmelding:** `has_trial_lesson = false`, `is_active_client = false`, `total_matchings = 0`. Deze worden later bijgewerkt via Make.com wanneer de status in Salesforce verandert.

---

## Automation — Welkomstmail Proefles Aanmelding

| Instelling | Waarde |
|-----------|--------|
| **Naam** | Welkomstmail Proefles Aanmelding |
| **Trigger** | Subscriber joins group → Nieuwe Proefles Aanmelding |
| **Stap** | Send email → Welkomstmail Proefles Aanmelding |
| **Status** | ✅ ACTIEF |

---

## Email — Welkomstmail Proefles Aanmelding

| Instelling | Waarde |
|-----------|--------|
| **Onderwerp NL** | 🐼 Welkom bij Bright Panda! |
| **Onderwerp EN** | 🐼 Welcome to Bright Panda! |
| **Preheader NL** | We gaan voor je aan de slag! |
| **Sender naam** | Bright Panda Bijles |
| **Sender email** | info@brightpanda.nl |
| **Font** | Verdana |

### Email Structuur

```
Header PNG (logo/banner)
        ↓
Titel (tweetalig)
        ↓
Intro tekst (NL + EN)
        ↓
HTML Stappen blok NL (table layout)
        ↓
HTML Stappen blok EN (table layout)
        ↓
Button (link naar tarieven pagina)
        ↓
Footer
```

> **Tweetalig:** Nederlands eerst, dan Engels.
> **HTML stappen blok:** Gebouwd als `<table>` layout (niet flexbox) voor Gmail compatibiliteit. `line-height: 36px` voor verticale centrering van nummering bolletjes.
> **Button URL:** `https://www.brightpanda.nl/tarieven`

---

## Beslissingen

| Beslissing | Reden |
|------------|-------|
| MailerLite is geen CRM | Salesforce blijft bron van waarheid — MailerLite alleen voor emails |
| Docent-info niet opslaan in MailerLite | Wordt per email meegegeven via Make.com op het moment van versturen |
| `has_trial_lesson` en `is_active_client` starten op `false` | Worden later bijgewerkt via Make.com bij statuswijziging |
| Geen double opt-in | Ouder meldt zich aan via Salesforce web-to-lead, niet via MailerLite form |
| Growing Business plan is voldoende | Geen upgrade naar Advanced nodig voor huidige functionaliteit |
| HTML stappen blok via drag & drop content block | Custom HTML editor niet beschikbaar op Growing Business plan |
| Vakken vertaald naar NL vóór opslaan | Betere leesbaarheid in emails; `subjects` custom field bevat Nederlandse namen |
| Email tweetalig | Bright Panda bedient zowel NL- als EN-sprekende ouders |

---

## Gebruik van Custom Fields in Emails

| Tag | Gebruik |
|-----|---------|
| `{$student_name}` | Naam leerling personalisatie |
| `{$subjects}` | Vak(ken) in het bericht |
| `{$education_level}` | Niveau voor gerichte communicatie |
| `{$registration_date}` | Aanmeldingsdatum |

---

## Post-Proefles Flow (nog te bouwen)

Toekomstige updates van subscriber data via Make.com:
- Na proefles ingepland: `has_trial_lesson = true` + group → Proefles Ingepland
- Na actieve klant: `is_active_client = true` + group → Actieve Klanten
- Bij uitstroom: group → Wrong Match / Stopped

---

## Gerelateerde Documenten

| Document | Inhoud |
|----------|--------|
| [Scenario 10](scenario-10-salesforce-mailerlite.md) | Make.com scenario dat subscriber aanmaakt |
| [Google Apps Script](google-apps-script.md) | Script 1 — vakvertaling voor `subjects` field |
