# Oppgave 5: En visuell arbeidsflate for agentverktøy

## Mål

Lag en visuell prototype som hjelper brukeren å lage, forstå eller teste
en skill eller et MCP-verktøy for hendelsesanalysen.
Brukeren skal kunne redigere noe meningsfullt og få konkret validering.

## Felles hendelse og rammer

Dokumenttjenesten «Dokumentflyt» får tidsavbrudd etter release 2026.11.0.
Alle grupper undersøker samme uforanderlige grunnlag under `kilder/`:
`feilrapport.md`, `logger/`, `dokumentasjon/`,
`konfigurasjon/runtime.json` og `replay.json`.
Ikke endre kildene eller anta at tidsmessig sammenfall beviser årsak.

Sett opp miljøet etter [README](../README.md), og kjør fra prosjektroten.
Simulatoren bruker bare Python-standardbiblioteket og fungerer uten nett.
Installer med `pip install -e .`, eller sett `PYTHONPATH=src` før kommandoene.
Opprett arbeids- og resultatmapper, og behold en egen baseline:

```sh
mkdir -p workspace artifacts
python -m incident_lab replay --config kilder/konfigurasjon/runtime.json --output artifacts/baseline.json
cp kilder/konfigurasjon/runtime.json workspace/runtime.json
python -m incident_lab replay --config workspace/runtime.json --output artifacts/candidate.json
python -m incident_lab verify --config workspace/runtime.json --output artifacts/verification.json
```

Kjør også `verify` mot den uendrede konfigurasjonen og lagre resultatet separat.
Baseline forventes å bryte SLO og gi exitkode 1 ved verifikasjon.
Endre bare arbeidskopien for kandidatforsøk. En vellykket verifikasjon skal
bygge på observerte resultater, ikke på at agenten sier at testen gikk bra.

## Arbeid og leveranse

- Velg én hovedbruker og én tydelig oppgave i analyseprosessen.
- Lag en redigerbar skill eller verktøydefinisjon med synlige inndata og utdata.
- Valider for eksempel påkrevde felt, kildeavgrensning eller rapportkrav.
- Vis hvor feilen er, hvorfor den betyr noe og hvordan brukeren retter den.
- Gjør koblingen mellom verktøyinnstillinger, kildebevis og resultat forståelig.
- Vis verktøyfeil og usikkerhet uten å presentere dem som vellykkede resultater.
- Lever kjørbar prototype, en kort brukerflyt og felles hendelsesrapport.
- Offline-mocker er tillatt, men merk tydelig hva som er simulert.

## Akseptansedemo

1. La en bruker åpne prototypen og endre en skill eller verktøydefinisjon.
2. Legg inn en konkret mangel og vis at valideringen oppdager den.
3. Rett mangelen og vis at endringen påvirker forhåndsvisning eller test.
4. Vis et eksempel på sporbarhet fra et kildefunn til rapporten.
5. Vis faktisk simulatorbaseline og kandidatverifikasjon som egne artefakter.
6. Forklar hvilke deler som er ekte integrasjon, og hvilke som er mocker.

En statisk skisse uten redigering og validering er ikke nok.
Mockede analyser må ikke brukes som bevis på at en retting består SLO.
Det er greit å kjøre den ekte simulatoren utenfor prototypen.

## Felles rapport og tidsplan

Bruk [rapportmalen](../examples/report-template.md) med engelske overskrifter.
Lever rapport, relevante artefakter og en kort instruksjon for å gjenta forsøket.
Oppgi kildebaner og linjenumre for påstander. Skill mellom observasjoner og
hypoteser, og beskriv foreslått retting, testresultater og gjenværende risiko.
Behold kode, kodevariabler, eksempler og eventuelle rapportfeltnavn på engelsk.

Dere har tre timer, kl. 13–16. Bruk omtrent 20 minutter på oppsett,
70 minutter på bygging, 50 minutter på forsøk og 10 minutter på rapport.
Kl. 15:30 starter frivillig deling frem til kl. 16.
Vis arbeidsmåten og dokumenterte resultater, også hvis løsningen ikke er ferdig.
