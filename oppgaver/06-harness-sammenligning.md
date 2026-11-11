# Oppgave 6: Sammenlign Pi og OpenCode på like vilkår

## Mål

Dette er ekspertoppgaven. Løs samme hendelsesanalyse i Pi og OpenCode,
og sammenlign brukeropplevelse, styring, verktøybruk og resultat.
Anbefal et harness for et konkret behov, med grunnlag i observerte forsøk.

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

- Kontroller først hva som faktisk er installert og tilgjengelig på maskinen.
- Registrer eksakte harness-versjoner, modell-ID, leverandør og kjøretidspunkt.
- Bruk samme modell, modellinnstillinger, oppgaveprompt og kildegrunnlag.
- Gi samme verktøytilgang, tillatelser og budsjett for tid, kall og tokenbruk.
- Beskriv ulikheter som ikke kan utjevnes, fremfor å skjule dem.
- Start ferske økter og separate arbeidskopier uten resultater fra det andre forsøket.
- Arkiver startprompt, relevante innstillinger, øktlogger og egne testartefakter.
- Lever sammenligningstabell, rapport fra hvert forsøk og en begrunnet anbefaling.

## Akseptansedemo

1. Vis versjonsinformasjon og at begge bruker den avtalte modellen.
2. Vis identiske startbetingelser og hvordan budsjettet ble målt eller avgrenset.
3. Vis et representativt verktøykall og en styringssituasjon fra hvert harness.
4. Sammenlign kildebruk, usikkerhet, testresultater og behov for menneskelig hjelp.
5. Vis baseline og kandidatverifikasjon fra de separate arbeidskopiene.
6. Skill observerte forskjeller fra preferanser og tilfeldige modellvariasjoner.

Ikke påstå tilgjengelighet, funksjoner, kostnader eller målinger dere ikke har
kontrollert. Hvis samme modell eller et harness mangler, dokumenter hindringen
og merk sammenligningen som ufullstendig. Ikke erstatt manglende forsøk med
oppdiktede resultater. Én kjøring per harness gir begrenset generaliserbarhet.

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
