# Make.com Scenario Documentatie

Technisch naslagwerk per Make.com scenario voor Bright Panda.

> **Single source of truth voor scenario-statussen, ID's en activatie:** zie `/CLAUDE.md` in de repo root.
> Dit bestand bevat alleen de detail-documentatie per scenario. Status of activatie wijzigen? Werk CLAUDE.md bij.

---

## Scenario detail-bestanden

| # | Naam | Detail-bestand |
|---|------|----------------|
| 01 | Teacher Invitation | [scenario-01-docent-uitnodiging-whatsapp.md](scenario-01-docent-uitnodiging-whatsapp.md) |
| 02 | Parent Timeslot Invitation (Tally Webhook) | [scenario-02-tally-webhook-ouder-planning.md](scenario-02-tally-webhook-ouder-planning.md) |
| 03 | Trial Lesson Scheduled & Availability Conflict | [scenario-3b-ouder-tijdslot-verwerking.md](scenario-3b-ouder-tijdslot-verwerking.md) |
| 04 | Teacher Timeslot Submission | [scenario-04-teacher-timeslot-submission.md](scenario-04-teacher-timeslot-submission.md) |
| 05 | Availability Conflict Reminder | [scenario-05-availability-conflict-reminder.md](scenario-05-availability-conflict-reminder.md) |
| 06 | Teacher Availability Reminder | [scenario-06-teacher-availability-reminder.md](scenario-06-teacher-availability-reminder.md) |
| 07 | Internal Alert Teacher No Response | [scenario-07-internal-alert.md](scenario-07-internal-alert.md) |
| 08 | Lesson Date Reminder | [scenario-08-lesson-date-reminder.md](scenario-08-lesson-date-reminder.md) |
| 09 | Parent Timeslot Reminders & Escalatie | [scenario-09-parent-reminders.md](scenario-09-parent-reminders.md) |
| 10 | Salesforce → MailerLite New Registration | [scenario-10-salesforce-mailerlite.md](scenario-10-salesforce-mailerlite.md) |
| 11 | Post-proefles flow | [scenario-11-post-proefles-flow.md](scenario-11-post-proefles-flow.md) |
| 12 | Docent New Registration | [scenario-12-docent-new-registration.md](scenario-12-docent-new-registration.md) |
| 13 | Docent Lifecycle Automation | [scenario-13-docent-lifecycle.md](scenario-13-docent-lifecycle.md) |
| 14 | DocuSeal Contract Signed | [scenario-14-docuseal-webhook.md](scenario-14-docuseal-webhook.md) |
| 15 | Tally Reminder Pending Onboarding | (nog toe te voegen) |

---

## Gedeelde documentatie

- [gedeelde-configuratie.md](gedeelde-configuratie.md) — herbruikbare modules, error handling
- [whatsapp-templates.md](whatsapp-templates.md) — alle 360dialog template definities
- [google-apps-script.md](google-apps-script.md) — GAS Picker code en config
- [mailerlite.md](mailerlite.md) — MailerLite groepen, fields, automations
- [beslissingen.md](beslissingen.md) — log van architectuur-beslissingen

---

## Status Legenda (uit CLAUDE.md)

| Icoon | Betekenis |
|-------|-----------|
| ✅ | Actief en werkend in productie |
| 🔧 | Gebouwd, inactief, wacht op test |
| ⏳ | Wacht op externe actie (bijv. template goedkeuring) |
