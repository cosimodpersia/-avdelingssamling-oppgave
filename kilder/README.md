# Felles kildemateriale

Alt her er syntetisk og skal behandles som skrivebeskyttet bevismateriale.
Bruk en kopi i `workspace/` når dere vil endre konfigurasjon.

| Fil | Innhold |
| --- | --- |
| `feilrapport.md` | Meldt hendelse og oppdrag |
| `logger/applikasjon.jsonl` | 40 forespørsler før og 40 etter utrulling |
| `logger/arkivtjeneste.jsonl` | Fullførte kall, også etter at klienten har sluttet å vente |
| `logger/hendelser.jsonl` | Utrulling, varsler og driftsobservasjoner |
| `konfigurasjon/runtime.json` | Effektiv konfigurasjon etter utrulling |
| `dokumentasjon/arkitektur.md` | Forespørselsflyt og loggsemantikk |
| `dokumentasjon/driftsavtale.md` | Krav, tidsbudsjetter og sikker endring |
| `dokumentasjon/konfigurasjon.md` | Parametre og endringsinformasjon |
| `dokumentasjon/testmodell.md` | Forutsetninger og begrensninger ved lokal replay |
| `replay.json` | Faste behandlingstider for 40 testforespørsler |

JSON-feltnavn er på engelsk for å kunne brukes direkte i kode. Beskrivelser og
meldinger er på norsk. Linjenumre telles fra 1, også i JSONL-filer.
Feltene `trace_id` og `attempt` brukes til å koble logger. `request_id` alene er
ikke unikt på tvers av de to utvalgene.

Ved publisering av et faktisk internt dokument må arrangøren avklare deling.
Den interne program-PDF-en er ikke kopiert inn i dette repoet.
