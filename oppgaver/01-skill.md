# Oppgave 1: En repeterbar skill for feilanalyse

## Mål

Lag en skill som leder agenten fra feilrapport til en begrunnet anbefaling.
Skillen skal beskrive en gjenbrukbar arbeidsprosess, ikke en ferdig diagnose.
En ny agent skal kunne følge den uten å få gruppens konklusjon på forhånd.

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

- Velg et skill-format som støttes av verktøyet dere faktisk bruker.
- Beskriv når skillen skal brukes, nødvendige inndata og forventet resultat.
- La arbeidsflyten dekke innhenting, hypoteser, motbevis, forsøk og rapport.
- Krev sporbare kildehenvisninger og eksplisitt håndtering av usikkerhet.
- Definer når agenten skal stoppe eller be om hjelp ved manglende grunnlag.
- Lever selve skillen og rapporten fra minst én gjennomkjøring.
- Ikke bygg inn et bestemt konfigurasjonsvalg eller en antatt rotårsak.

## Akseptansedemo

1. Last skillen i en ny økt og gi agenten hendelsen uten en løsningsfasit.
2. Vis at skillen styrer rekkefølgen og kravene til bevis og rapport.
3. Vis baseline, et begrunnet kandidatforsøk og faktisk verifikasjonsresultat.
4. Gjenta starten i en ny økt og kontroller at de samme arbeidsstegene følges.
5. Forklar hva som er repeterbart, og hva som fortsatt avhenger av modellen.

Det er prosessen som skal kunne gjentas, ikke nødvendigvis identisk ordlyd.
En rapport alene er ikke en skill.

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
