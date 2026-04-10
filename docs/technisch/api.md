# API Documentatie

## Overzicht

De Bright Panda API is een RESTful API die alle functionaliteiten van het platform ontsluiten.

## Base URL

```
https://api.brightpanda.nl/v1
```

## Authenticatie

Alle API-verzoeken vereisen een Bearer token in de Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Gebruikers

| Methode | Endpoint | Beschrijving |
|---------|----------|-------------|
| GET | `/users/me` | Haal profiel van ingelogde gebruiker op |
| PUT | `/users/me` | Update profiel |
| GET | `/users/:id` | Haal gebruikersprofiel op (admin) |

### Docenten

| Methode | Endpoint | Beschrijving |
|---------|----------|-------------|
| GET | `/tutors` | Lijst van docenten (met filters) |
| GET | `/tutors/:id` | Docentprofiel ophalen |
| POST | `/tutors/apply` | Aanmelding als docent |
| PUT | `/tutors/:id/status` | Status wijzigen (admin) |

### Lessen

| Methode | Endpoint | Beschrijving |
|---------|----------|-------------|
| GET | `/lessons` | Lijst van lessen |
| POST | `/lessons` | Nieuwe les aanmaken |
| PUT | `/lessons/:id` | Les bijwerken |
| DELETE | `/lessons/:id` | Les annuleren |
| POST | `/lessons/:id/notes` | Lesnotities toevoegen |

### Betalingen

| Methode | Endpoint | Beschrijving |
|---------|----------|-------------|
| GET | `/payments` | Betalingsoverzicht |
| POST | `/payments/checkout` | Betaling initiëren |
| GET | `/payments/:id/status` | Betalingsstatus opvragen |

## Foutcodes

| Code | Betekenis |
|------|-----------|
| 400 | Ongeldig verzoek |
| 401 | Niet geautoriseerd |
| 403 | Geen toegang |
| 404 | Niet gevonden |
| 429 | Te veel verzoeken (rate limit) |
| 500 | Serverfout |

## Rate Limiting

- Maximaal 100 verzoeken per minuut per gebruiker
- Bij overschrijding ontvangt u een 429-respons
