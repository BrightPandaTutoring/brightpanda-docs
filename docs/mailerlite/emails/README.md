# Bright Panda — Email templates

MailerLite-ready, table-based HTML emails. Tweetalig (NL + EN). Alle afbeeldingen zijn gehost op de MailerLite-CDN (`storage.mlcdn.com`).

**Merge tags:** `{$name}`, `{$student_name}`, `{$teacher_name}`, `{$subjects}`, `{$trial_lesson_date}`, `{$unsubscribe}`.

## Templates

| # | Bestand | Statusbalk |
|---|---------|-----------|
| 1 | `1-welkomst.html` | Op zoek (stap 2) |
| 2 | `2-matching.html` | Op zoek (laad 2→3) |
| 3 | `3-docent-gevonden.html` | Docent gevonden (stap 3) |
| 4 | `4-proefles-bevestigd.html` | Proefles (stap 4) |
| 5 | `5-na-de-proefles.html` | Proefles → Bijles (laad 4→5) |
| 6 | `6-tips-voor-de-bijles.html` | Bijles van start (stap 5) |
| 7 | `7-geen-contact-1.html` | — |
| 8 | `8-geen-contact-2.html` | — |
| 9 | `9-geen-contact-3.html` | — |

## Gebruik in MailerLite
Plak de inhoud van een bestand in een **Custom HTML** blok. De merge tags worden automatisch ingevuld bij verzending.

## Mappenstructuur

```
emails/
├── 1-welkomst.html … 9-geen-contact-3.html   ← de 9 plak-klare emails
├── README.md
└── HOSTED-IMAGES.md                            ← welke CDN-URL hoort bij welke email
```

## Belangrijk over de afbeeldingen
De HTML's verwijzen naar **gehoste URLs** op MailerLite — die werken direct in elke emailclient. Mocht een CDN-URL ooit vervangen worden, upload het origineel opnieuw en pas de URL in de HTML aan. Zie `HOSTED-IMAGES.md` voor de koppeling.
