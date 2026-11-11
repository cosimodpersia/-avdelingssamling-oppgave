# Konfigurasjon

`konfigurasjon/runtime.json` er eksportert effektiv konfigurasjon for Dokumentflyt
etter utrullingen. Verdiene i eksporten er dem tjenesten faktisk brukte.
Det er derfor ikke nødvendig å gjette på miljøvariabler eller skjulte standardverdier.

| Felt | Betydning | Tillatt i testmodellen |
| --- | --- | --- |
| `service` | Tjenesteidentifikator | `document-flow` |
| `release` | Versjonsmerke, bare metadata | Tekst |
| `dependency.timeout_ms` | Hvor lenge hvert kall kan vente på arkiv-API-et | Heltall 1 til 2000 |
| `dependency.max_attempts` | Totalt antall forsøk, inkludert første kall | Heltall 1 til 5 |
| `dependency.retry_backoff_ms` | Pause mellom forsøk, ikke etter siste forsøk | Heltall 0 til 1000 |

Tidsverdier er millisekunder, ikke sekunder. En bekreftelse som mottas akkurat på
tidsgrensen, regnes som vellykket. Nye forsøk gjøres bare ved tidsavbrudd i modellen.

## Endringsnotat for 2026.11.0

Utrullingen oppdaterte basisbildet og innførte en ny konfigurasjonsmal.
Arkiv-API, dokumentformat og autentisering var uendret.
Konfigurasjon fra forrige utrulling er ikke eksportert i dette materialet.
Undersøk den effektive konfigurasjonen og målte resultater fremfor å anta
at standardverdiene er de samme som før.

Arkiv-API-et har ikke noe eget krav om at alle kall må være ferdige innen en
bestemt klientgrense. Avklar en passende grense ut fra observasjoner og det
samlede tidsbudsjettet. Gruppen må begrunne sitt valg.
