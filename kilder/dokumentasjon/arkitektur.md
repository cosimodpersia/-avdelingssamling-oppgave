# Arkitektur og observasjoner

## Forespørselsflyt

En saksbehandler sender et dokument til Dokumentflyt. Tjenesten kaller et internt
arkiv-API og venter på bekreftelse. Ved bekreftelse returnerer Dokumentflyt HTTP 200.
Når alle tillatte forsøk ender i tidsavbrudd, returnerer den HTTP 504.

En forespørsel har samme idempotensnøkkel i alle forsøk. Arkiv-API-et gjenkjenner
duplikater. Idempotens hindrer flere lagringer, men et nytt kall bruker fortsatt
kapasitet. Innsending på nytt fra bruker kan få ny nøkkel og er ikke dekket av
denne garantien.

## Tidsavbrudd og avbrutt venting

Klientens tidsavbrudd bestemmer hvor lenge Dokumentflyt venter per forsøk.
Det er ikke en grense for hvor lenge arkiv-API-et bruker på behandlingen.
Arkiv-API-et kan derfor fullføre og logge HTTP 200 etter at Dokumentflyt har gitt opp.
Det finnes ingen koblet kansellering i denne versjonen.

Ved tidsavbrudd venter Dokumentflyt den konfigurerte pausen og prøver igjen,
dersom flere forsøk er tillatt. Forsøkene fra Dokumentflyts perspektiv er sekvensielle,
men arbeidet i arkiv-API-et kan overlappe når ventingen er avbrutt.

## Loggfelter

- `applikasjon.jsonl`: ett sluttresultat per innkommende forespørsel.
  `elapsed_ms` inkluderer alle forsøk og pauser, men ikke brukerens nettverkstid.
- `arkivtjeneste.jsonl`: ett fullført kall per forsøk, med faktisk behandlingstid.
  `timestamp` er tidspunktet behandlingen ble fullført.
- Begge logger bruker UTC. Koble med `trace_id`; forsøk identifiseres med `attempt`.
- Utvalgene bruker de samme forespørselsnumrene før og etter utrulling.
  Versjonen er inkludert i sporingsidentifikatoren.
- Manglende bekreftelse hos klienten betyr ikke at dokumentet mangler i arkivet.

Utvalget før utrulling viser vellykket atferd. Hendelsesloggen inneholder også
varsler som ikke nødvendigvis forklarer feilen. Vurder tidslinje og mekanisme,
ikke bare hvilke linjer som har nivået WARN eller ERROR.
