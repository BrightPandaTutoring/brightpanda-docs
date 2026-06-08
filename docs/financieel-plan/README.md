# 🐼💶 Bright Panda — Financieel Plan

> **Doel van dit document:** het vaste financiële sturingsdocument van Bright Panda. Hier kijken Raouf en Yasin **wekelijks** en **maandelijks** naar. Het vertaalt onze winst- en revenue-doelen naar concrete hefbomen, KPI's en acties.
>
> **Laatst bijgewerkt:** 8 juni 2026 (eerste versie, strategiesessie)
>
> **Bestanden in deze map:**
> - `README.md` — dit document: strategie, KPI's, meetfundament, hefbomen
> - `maand-review.md` — maandelijkse review (template + log)
> - `week-check.md` — wekelijkse check (template + log)

---

## 0. De kerngedachte

We hebben **4 hefbomen** om meer winst over te houden:

1. **Kosten omlaag**
2. **Prijs omhoog**
3. **Verkoop aan méér mensen**
4. **Verkoop méér aan dezelfde mensen**

De centrale rekensom die alles verbindt:

```
LTV  = wat een klant gemiddeld waard is over zijn hele levensduur
CAC  = wat het kost om één klant te werven
LTV : CAC = de gezondheidsmaatstaf (vuistregel: gezond > 3:1)
```

Zolang **CAC < LTV**, mogen we gas geven op acquisitie. Hoe hoger de LTV (hefboom 2 & 4) en hoe lager de CAC (hefboom 1 & 3), hoe meer winst.

---

## 1. ⚠️ PRIORITEIT #1 — Het meetfundament (loopt PARALLEL met quick wins)

**Zonder meting kunnen we de verbetering niet zien.** Bijna elk idee in dit plan verbetert onze KPI's, maar we kunnen het effect niet sturen zolang we niet meten. Dit is daarom de fundering onder alles — en het is **één samenhangende ingreep**, geen tien losse.

**Wat we in Salesforce betrouwbaar moeten vastleggen per klant:**
- **Datum van elke statuswijziging** in de lifecycle (New → Enrollment → Matching → Trial → Client → Stopped/Churned). Vergelijk met hoe we `Offboarded_Date__c` voor docenten al doen.
- **Werfkanaal** — `ReferredToBPVia__c` (dit veld bestaat al; consequent invullen).
- **Instroommaand** — om seizoenseffect te kunnen meten.

**Wat dit fundament ontsluit (nu nog blinde vlekken):**
- Lead → Client conversie (per stap én per kanaal)
- Het churnpunt (in welke maand haakt het grootste % af)
- Seizoens-LTV (september-instromer vs. mei-instromer)
- Betrouwbare CAC per kanaal en per maand

> **Actie:** Salesforce inrichten op statusdatums + kanaal + conversietracking. Onderzoeken of veldhistorie volstaat of dat we datumvelden moeten toevoegen.

---

## 2. KPI-dashboard — baseline juni 2026

| KPI | Nu | Status | Hefboom die het verbetert |
|---|---|---|---|
| **LTV** | ~€800 | ✅ bekend | 2 (prijs) + 4 (upsell/retentie) |
| **CAC** | ~€99 | ⚠️ onbetrouwbaar (alleen laatste maand) | 1 + 3 |
| **LTV : CAC** | ~8:1 | ⚠️ fragiel (CAC onzeker) | hoofdmaatstaf — houden > 3:1 |
| **Brutomarge** | 33–55% | ⚠️ te breed (22 ppt spread) | 1 (tariefkaart) + 2 (prijs) |
| **Lead → Client conversie** | onbekend | ❌ blinde vlek — eerst meten | 3 (funnel-lekken) |
| **Klant-LTV per instroommaand** | onbekend | ❌ blinde vlek — eerst meten | 3 (zomerproducten) + CAC-timing |
| **Churnpunt (maand)** | onbekend | ❌ blinde vlek — eerst meten | 4 (retentie-interventie) |

### Wat de baseline ons nu al vertelt
- **8:1 betekent: ons probleem is waarschijnlijk niet dat acquisitie te duur is, maar dat we te wéinig acquireren.** We laten geld liggen door niet méér uit te geven aan kanalen die werken. → Nadruk verschuift naar hefboom 3.
- **Sanity check die nog moet kloppen:** €1.600/mnd advertenties ÷ €99 CAC ≈ 16 klanten/mnd uit advertenties. Klopt dat? Zo niet, dan is de echte CAC hoger en de 8:1 te rooskleurig.
- **Marge-spread 33–55%** komt vrijwel zeker door ongelijke docenttarieven (geen tariefkaart). De onderkant omhoog duwen = directe winst.

---

## 3. De vier hefbomen — strategie & ideeën

### Hefboom 1 — Kosten omlaag

**Verbindende KPI: regionale balans.** Per regio bijhouden: aantal actieve docenten, vraag (studenten), match-rate, gemiddelde HourlyRate. Eén overzicht stuurt tegelijk tariefbeleid én advertentiebudget (verzadigde regio → lager tarief + Indeed uit; schaarse regio → meer bieden + actief adverteren).

- **Tariefkaart docenten (grootste margehefboom).** Vaste matrix op objectieve variabelen → automatisch tarief/smalle band, zodat Yasin hetzelfde biedt als Raouf. Variabelen uit Salesforce: `HBO_WO__c`, `Is_Pro_Teacher__c`, `Date_of_Birth__c`, `Can_Give_Exam_Training__c`, `Teaching_Location__c` + regionale balans. *KPI: gem. HourlyRate, marge/les, spreiding geboden tarieven per interviewer.*
- **Indeed.** Meet **kost per gekoppelde (geactiveerde) docent**, niet per geworven docent. Per maand per regio: genoeg actief aanbod → Indeed uit voor die regio. *KPI: Indeed-uitgave per gekoppelde docent, activatie-ratio, aanbod-overschot per regio.*
- **Marktplaats + Google Ads.** CAC per kanaal via `ReferredToBPVia__c`. Budget mag omhoog zolang CAC < LTV. *KPI: CAC per kanaal, nieuwe klanten per kanaal, conversie per kanaal.*
- **Studieverenigingen / universiteiten.** Goedkoopste docentkanaal (bijna €0/docent, hogere kwaliteit, regiogericht). Bestaande samenwerking: **studievereniging Leiden**. *KPI: docenten via partnerships + kost/docent vs. Indeed.*
- **Operationele kosten** — zie sectie 4.
- **Bring-a-friend / referral** (docenten én klanten). Laagste CAC die bestaat. *KPI: % aanmeldingen via referral, CAC referral vs. andere kanalen.*

> **Kanttekening:** "kosten omlaag" mag de motor niet uitzetten. Snij **verspilling** (niet-gekoppelde Indeed-docenten, verzadigde regio's, ongebruikte abonnementen), niet de kanalen die groei leveren.

### Hefboom 2 — Prijs omhoog  ⏳ NOG TE BEHANDELEN

Deze hefboom is in de sessie van 8 juni **overgeslagen** (we gingen 1 → 3 → 4). Voor een volgende sessie. Eerste aanknopingspunten die elders al opkwamen:
- VOG-screening rechtvaardigt mede een hogere prijs (vertrouwen).
- Letselschade-tarief (~€60/u) is mogelijk te laag → all-in tarief €70–85 testen.
- Decoy pricing & abo-naming (zie hefboom 4A) raken prijsstrategie.

### Hefboom 3 — Verkoop aan méér mensen

Twee verschillende bewegingen, bewust gescheiden (ander risico, andere KPI's):

**Bucket A — zelfde service (bijles) aan meer mensen** (veiligste groei, unit economics bekend)
- **SEO / hogere ranking.** Op termijn goedkoopste betaalde kanaal (CAC daalt bij meer verkeer). Sluit aan op de €1.542/mnd SEO-post → moet zich bewijzen in klanten. Werkt het sterkst lokaal (per stad), sluit aan op regionale balans. *KPI leidend: organisch verkeer, rankende zoekwoorden op kerntermen, CTR naar aanmeldpagina. KPI resultaat: nieuwe Clients via organisch + CAC (€1.542 ÷ #SEO-klanten).*
- **Cold calls B2B.** Geen B2C-kanaal (we bellen geen ouders koud) — richt op scholen/bedrijven. Hoge waarde per deal, lange salescyclus. *KPI: gesprekken → afspraken → deals, gem. contractwaarde.*
- **Social media content.** Acquisitiekanaal voor bestaand product. *KPI: leads → conversie → CAC.*

**Bucket B — services uitbreiden (nieuwe producten)** (hogere groei, hoger risico)
Zes lijnen — scoren op **omzetpotentieel × inspanning-om-te-lanceren**, dan 1–2 per kwartaal uitrollen (focusrisico met 2 oprichters!):
- Examentrainingen B2C — *quick win* (docenten al bekend via `Can_Give_Exam_Training__c`)
- Boswell-examens internationale leerlingen (zomer) — *quick win* (vult rustige periode, bestaande docenten)
- B2B proctoring / surveilleren op scholen — hoog potentieel, hoog effort
- Examentraining áán scholen — hoog potentieel, hoog effort
- Spaanse groepscursus (8 wk) — apart product, validatie nodig (prioriteit 4)
- Nederlands voor expats (B2C + B2B) — apart product (prioriteit 5)

*KPI per nieuw product (uniform, zodat vergelijkbaar): betalende validatie-aanmeldingen vóór investering → break-even (# deelnemers) → marge per product.*

### Hefboom 4 — Verkoop méér aan dezelfde klanten (rijkste hefboom — acquisitie al betaald)

**A. Upsellen van lessen (pricing & retentie)**
- **Decoy pricing** — los pakket bewust duurder dan abo. Abo-naming strategischer ("aanbevolen" i.p.v. "small"). *Let op: blijf eerlijk, gebruik "aanbevolen" niet "vereist" → anders refunds/reputatie.*
- **Follow-up / reminders ("lessen bijna op").** ⭐ QUICK WIN — infrastructuur staat al (Make.com + MailerLite + 360dialog). Automatiseert herhaal-aankoop die we nu laten liggen.
- **Jaarabonnementen** tegen lagere prijs — ruil marge voor zekerheid/cashflow. *Vereist: gem. klantlevensduur kennen. Korting alleen winst als levensduur < 12 mnd.*
- **Churnpunt-korting.** Vlak vóór het churnpunt een retentie-moment. *Richt op gedragssignalen (lessen lopen af, langere gaten), niet puur kalendermaand — anders train je kortingsgedrag. Korting is niet de enige knop: check-in ("tevreden?") kost geen marge.* Operationeel via Make.com-scenario zodra churnpunt bekend.
- **Cadeau-pad bij continuïteit (gamification).** Mijlpalen (wk 4, 6, …) met oplopende beloningen. Koppel duurste beloningen aan punten ná de churnpiek. Overweeg ervaring boven spullen (bonusles, opgavenboekje, certificaat) — goedkoper én houdt klant binnen product. *KPI: voltooiing per mijlpaal, retentie mét vs. zónder pad, kosten per behouden klant-maand.*
- **Small wins zichtbaar maken (herhaalde mini-toets).** ⭐ Sterkste retentie-idee. Nulmeting op proefles, herhaling 4 lessen later → vooruitgang zichtbaar lang vóór het rapport. Verkoopt *bewijs van resultaat*. Voedt voortgangsrapportage-add-on, cijfergarantie én marketing. *Vereist docent-discipline → vastleggen in Docent Gids + Salesforce-veld (beginscore/herhaalscore).*
- **Schooljaar-overgang (juli→sept).** ⭐ Scherpste vorm van seizoensverlies — we verliezen al-gekoppelde, tevreden klanten op het breukvlak. Oplossing: bewuste **her-inschrijf-beweging** vóór de zomer (jaarabo over de zomer heen, zomerproducten als brug: Boswell/cursussen, "we zien je in september"-traject met vroegboekvoordeel). *KPI: % klanten dat schooljaar-overgang overleeft.*

**B. Upsellen van extra services (margeproducten)**
- **Voorrang bij koppelen (€20)** bij proefles-aanmelding als leerling snel docent nodig heeft. Verkoopt snelheid. *Let op: wachttijd gratis klanten acceptabel houden.*
- **Maandelijkse voortgangsrapportage (€10/mnd).** Hoge marge — laat AI (Anthropic API, al beschikbaar) genereren o.b.v. docent-input. Recurring over honderden klanten.
- **Opgavenboekjes** — 3 routes oplopend in effort: (1) externe uitgever met marge [start hier, valideer vraag] → (2) eigen database via AI/freelancer → (3) opgave-/uitlegvideo's.
- **Cijfergarantie (NIET "verzekering" noemen).** Upsell + volumedriver + lead magnet (Google Ads). Voorwaarden: min. 2u/wk, 8–12 wk, geen gemiste lessen, huiswerk af, Magister-inzage, intensieve 3u toetssessie per vak. ⚠️ **Juridisch:** "verzekering/garantie" tegen premie kan onder AFM/Wft + consumentenrecht vallen → noem het *resultaatbelofte*, laat constructie door jurist toetsen vóór lancering. ⚠️ **Risicomodel:** reken als verzekeraar — premie × alle klanten moet verwachte uitkeringen + marge dekken. Magister-inzage = sterkste troef (meet instapniveau; 5→6 ≠ 3→7). *KPI: attach-rate per add-on, marge per add-on, uitkeringsratio vs. premie-inkomsten (vanaf dag 1).*

**C. Meer focus op B2B (grootste contracten)**
- **Letselschadebedrijven (~€60/u).** Niet prijsgevoelig zoals ouders; vergoeden vanuit dossier, willen betrouwbaarheid + facturatie. All-in tarief €70–85 testen.
- **Scholen** — examentraining, bijles op school, surveilleren, onderwijsassistenten, invalkracht bij uitval. Inval-/extra-handjes raakt acute pijn (lerarentekort) → er is budget.
- **Gemeentesubsidies** — mogelijk goedkoopste groei (overheid betaalt acquisitie). Bijles + digitale geletterdheid/AI-vaardigheid voor leerlingen (NPO-gelden, onderwijsachterstandsmiddelen). Inspanning = aanvraag/verantwoording, niet sales. *Eigen uitzoekwerk.*
- **Nederlands voor anderstaligen / expats** — inburgering/B1-B2 (paspoort) = urgente behoefte + betalingsbereidheid. Via werkgever = B2B (grotere contracten). Klaslokaal-model: 1 docent × meerdere betalende deelnemers = veel hogere marge/lesuur. Troef: docenten via studievereniging Leiden.

*KPI C: aantal B2B-deals per type, gem. contractwaarde, omzet per B2B-klant vs. B2C-klant, subsidies aangevraagd vs. toegekend vs. besteed.*

**Dwars door de funnel: VOG-screening docenten**
- **Filtering vóór aannamegesprek** — kleine drempel filtert impulsieve aanmelders (raakt Indeed-activatieprobleem).
- **Vertrouwen bij klanten** — "alle docenten VOG-gescreend" rechtvaardigt hogere prijs (hefboom 2) + vaak vereist voor scholen/letselschade (opent B2B).
- **Veiligheid/risico** — we werken met minderjarigen; beperkt aansprakelijkheid.
- *Keuze: wie betaalt & wanneer in funnel? Aanrader: VOG ná positief gesprek, als voorwaarde voor eerste koppeling, door BP vergoed of verrekend → toegangsbewijs i.p.v. drempel.*
- ⚠️ **AVG:** registreer **dát** de VOG is gezien + datum; bewaar het document niet langer dan nodig. Sluit aan op bestaand AVG-beleid + velden zoals `Documentation_Agreed__c`. Mogelijk nieuw veld: `VOG_Verified__c` / `VOG_Received_Date__c`, meenemen in scenario 17 (Auto On-boarded).
- *KPI: koppel-ratio mét vs. zónder VOG-stap, doorlooptijd VOG, effect op klantconversie/prijs.*

---

## 4. Operationele kosten (baseline juni 2026)

**Totaal: €4.622,34/mnd — €55.468/jaar.** 81% zit in 2 categorieën: mensen/freelancers (45%) + marketing (36%). Software = 15%. → Winst zit in freelancers + advertentie-efficiëntie, niet in abonnementen uitpluizen.

| Post | €/mnd | Advies |
|---|---|---|
| SEO specialist | 1.542,00 | ⚠️ **Grootste post (33%!).** Hoeveel klanten kwamen via SEO? Moet maandelijks met cijfers rapporteren. |
| Indeed | 700,00 | Meten: kost per gekoppelde docent; per regio uit-zetten |
| Marktplaats advertenties | 600,00 | CAC meten — groeimotor, niet blind snijden |
| Taryn (website) | 400,00 | Mogelijke overlap met SEO + agency → consolideren |
| Google Ads | 300,00 | CAC meten — mag omhoog zolang < LTV |
| Bsport | 200,00 | ⚠️ Wordt het volledig gebruikt? Wat doet het dat Salesforce niet doet? |
| Salesforce Enterprise | 175,00 | Vast t/m apr 2029 — laten |
| Digitale marketing agency | 160,00 | Overlap met SEO/Taryn? → consolideren |
| KPN | 102,00 | ⚠️ Hoog — downgraden/overstappen kan €30–50 schelen |
| Claude (Anthropic) | 90,00 | Kerninfra — laten |
| ABN schadeverzekering | 87,64 | Laten (aansprakelijkheid) |
| Channable | 72,00 | Hoort bij advertentie-prioriteit |
| 360dialog WhatsApp | 49,00 | Kerninfra — laten |
| Marktplaats Pro | 49,00 | Bij advertentiestrategie |
| MoneyMonk | 35,70 | Overlap met accountant? Goedkoper pakket? |
| Make.com | 20,00 | Kerninfra — laten |
| DocuSeal | 20,00 | Kerninfra — laten |
| MailerLite | 10,00 | Kerninfra — laten |
| Tally + TinyURL | 10,00 | Kerninfra — laten |

**Realistisch "veilig" besparingspotentieel zonder de motor te raken:** ~€300–500/mnd (KPN, mogelijk Bsport/MoneyMonk, freelancer-consolidatie). De échte hefboom (€1.542 SEO + €1.600 advertenties) pas beoordelen als CAC/ROI bekend is.

> *Geen financieel/juridisch advies — contract- en verzekeringskeuzes horen bij Raouf/Yasin + accountant/jurist.*

---

## 5. Quick wins (PARALLEL met meetfundament)

1. **"Lessen-bijna-op" reminder** — Make.com + MailerLite/360dialog. Lage inspanning, directe omzet.
2. **Tariefkaart docenten** — trekt marge-spread dicht, zorgt voor consistentie Yasin/Raouf.

---

## 6. Openstaande getallen die we moeten ophalen

- [ ] Gemiddelde klantlevensduur (maanden, Client → Churned) → scharnierpunt voor jaarabo + churnpunt + LTV-verfijning
- [ ] Lead → Client conversie (per stap, per kanaal)
- [ ] Klanten via SEO/organisch afgelopen 3–6 mnd (rechtvaardigt €18.500/jr?)
- [ ] Werkelijke CAC per kanaal over meerdere maanden (sanity check 16 klanten/mnd?)
- [ ] LTV per instroommaand (seizoenseffect)
- [ ] Churnpunt (welke maand piek-uitval)
