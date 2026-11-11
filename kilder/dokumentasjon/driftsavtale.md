# Driftsavtale for øvelsen

## Mål for Dokumentflyt

Ved normal drift skal minst 99 prosent av forespørslene lykkes. Den lokale
regresjonstesten anvender samme grense på det faste utvalget med 40 forespørsler.
Det betyr at alle 40 må lykkes for at akkurat dette utvalget skal bestå.

- 95-persentilen for samlet svartid skal være høyst 1200 millisekunder.
- Ingen forespørsel skal overskride 2500 millisekunder i lokal test.
- Antall kall til arkiv-API-et per innkommende forespørsel skal i gjennomsnitt
  være høyst 1,10. Dette beskytter kapasiteten ved feil og gjentatte forsøk.
- Alle fire krav må oppfylles samtidig. Raskt returnerte feil er ikke en løsning.

Disse grensene er faste i testmodellen, ikke innstillinger gruppen kan senke.
Bruk nærmeste rang ved beregning av persentiler: sorter verdiene og velg
observasjon nummer avrundet opp av 0,95 multiplisert med antall observasjoner.

## Tidsbudsjett og endringer

Inngående gateway har et samlet tidsbudsjett på 2500 millisekunder.
Et enkelt oppsett for verste fall er antall forsøk multiplisert med
tidsavbrudd per forsøk, pluss pauser mellom forsøkene. Modellen måler det faktiske
forløpet i utvalget, ikke alle mulige fremtidige feil. Vurder begge deler.

En foreslått endring skal være minst mulig og bevare dokumenter, sporbarhet og
idempotens. Ikke løs oppgaven ved å deaktivere arkivering, slette logger,
endre målegrunnlaget eller returnere en falsk bekreftelse.

Beskriv stegvis utrulling, målinger og et konkret kriterium for tilbakeføring.
Tilbakeføring av applikasjonen må også gjenopprette riktig effektiv konfigurasjon.
En lokal simulering erstatter ikke lasttest, integrasjonstest eller godkjenning.
