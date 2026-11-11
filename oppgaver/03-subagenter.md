# Oppgave 3: Uavhengige subagenter og kritisk syntese

## Mål

Fordel feilanalysen mellom subagenter med tydelige roller.
Undersøk om uavhengig evidensinnhenting og kritikk forbedrer anbefalingen.
Flere navn i én samtale er ikke tilstrekkelig som demonstrasjon av subagenter.

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

- Bruk minst to separate agentkontekster og en tydelig ansvarlig for syntesen.
- Gi for eksempel én agent logger og én dokumentasjon og konfigurasjon.
- La dem først hente bevis selvstendig, uten å se hverandres konklusjon.
- Avtal et kort svarformat med kilder, usikkerhet og alternative forklaringer.
- La en kontrollør utfordre antakelser og lete etter motbevis.
- Samle funnene uten å skjule uenighet eller telle flertall som sannhet.
- La syntesen velge begrunnede forsøk og sammenholde dem med testresultater.
- Lever rollebeskrivelser, delegeringsinstrukser, agentutdrag og felles rapport.

## Akseptansedemo

1. Vis at agentene faktisk har separate kontekster og avgrensede oppdrag.
2. Vis minst to uavhengige funn med kildebaner og linjenumre.
3. Vis en konkret innvending fra kontrolløren og hvordan den ble behandlet.
4. Spor én beslutning fra agentfunn gjennom syntese til et kandidatforsøk.
5. Vis baseline og verifikasjon, også hvis forsøket avkrefter forslaget.
6. Forklar hva samarbeidet bidro med, og hvilken ekstra kostnad det ga.

Ikke konstruer uenighet i etterkant. Hvis agentene er enige, skal kontrolløren
fortsatt prøve å falsifisere begrunnelsen og dokumentere utfallet.

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
