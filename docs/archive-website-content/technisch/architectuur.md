# Architectuur

## Systeemoverzicht

Het Bright Panda platform bestaat uit de volgende componenten:

```
┌─────────────────────────────────────────────┐
│                  Frontend                    │
│            (Web App / Mobile)                │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│                 API Gateway                  │
└─────────────┬───────────────────────────────┘
              │
     ┌────────┼────────┬────────────┐
     ▼        ▼        ▼            ▼
┌────────┐┌────────┐┌────────┐┌──────────┐
│ Auth   ││ Users  ││Lessons ││ Payments │
│Service ││Service ││Service ││ Service  │
└────────┘└────────┘└────────┘└──────────┘
     │        │        │            │
     └────────┴────────┴────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│               Database Layer                 │
│          (PostgreSQL / Redis)                 │
└─────────────────────────────────────────────┘
```

## Componenten

| Component | Technologie | Beschrijving |
|-----------|------------|-------------|
| Frontend | React / Next.js | Web applicatie voor alle gebruikers |
| API Gateway | Node.js / Express | Centraal punt voor alle API-verzoeken |
| Auth Service | JWT / OAuth | Authenticatie en autorisatie |
| Users Service | Node.js | Beheer van gebruikersprofielen |
| Lessons Service | Node.js | Les-planning, notities, voortgang |
| Payments Service | Node.js + Mollie | Betalingsverwerking |
| Database | PostgreSQL | Primaire dataopslag |
| Cache | Redis | Sessies en caching |

## Hosting

- Cloud-gebaseerd (te specificeren)
- CI/CD pipeline voor automatische deployments
- Monitoring en logging
