# Oppgave 4: Et reelt isolert arbeidsmiljø

## Mål

La agenten undersøke hendelsen og teste en arbeidskopi i et isolert miljø.
Vis en faktisk håndhevet sikkerhetsgrense, ikke bare en instruks til modellen
eller en Python-liste over tillatte kommandoer.

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

- Velg en reell isolasjonsmekanisme, for eksempel en container eller en VM.
- Docker er valgfritt. Forklar hvilken grense den valgte mekanismen håndhever.
- Gjør kildene skrivebeskyttet og gi en isolert, skrivbar arbeidskopi.
- Gi bare nødvendige mapper tilgang. Ikke monter hjemmemappe eller vertssokler.
- Slå av nettverk for selve kjøringen, og gjør nødvendige avhengigheter klare først.
- Kjør helst uten privilegier og dokumenter rettigheter og gjenværende begrensninger.
- Plasser arbeidskopi og artefakter på skrivbare områder inne i isolasjonen.
- Lever miljødefinisjon, kjøreinstruksjon, sikkerhetsgrenser og rapport.

## Akseptansedemo

1. Start miljøet og vis at lesing av hendelseskildene er tillatt.
2. Endre en konfigurasjonskopi i arbeidsområdet og kjør simulatoren der.
3. Forsøk en ufarlig skriving under den skrivebeskyttede kilderoten.
4. Vis faktisk avvisning, og kontroller at kildene fortsatt er uendret.
5. Vis at nettverk er deaktivert gjennom miljøoppsett og en ufarlig lokal test.
6. Vis baseline som feiler SLO og en kandidat som består verifikasjonen.

Ikke let etter hemmeligheter på verten eller prøv å bryte ut av miljøet.
Bruk bare avtalte testbaner. En blokkert handling skal være blokkert av
isolasjonen, ikke av at agenten velger å la være.

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
