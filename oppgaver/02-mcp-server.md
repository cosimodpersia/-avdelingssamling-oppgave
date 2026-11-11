# Oppgave 2: Kontrollert lesetilgang gjennom MCP

## Mål

Lag en MCP-server som lar agenten finne relevante bevis i hendelsesgrunnlaget.
Serveren skal gi avgrenset lesetilgang, ikke vilkårlig fil- eller skalltilgang.
Demonstrer både nyttig informasjonsinnhenting og håndtering av verktøyfeil.

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

- Lag et lite sett verktøy for å finne og lese kildematerialet.
- Avgrens alle lesinger til den avtalte kilderoten.
- Kontroller oppløste baner, også absolutte baner, foreldresegmenter og symlenker.
- Returner kildebane og linjenumre slik at agenten kan sitere funnene.
- Gi forståelige verktøyfeil for avvist tilgang og filer som ikke finnes.
- Ikke eksponer skriving, generelt skall eller ubegrenset filsystemtilgang.
- Lever serverkode, oppstartsinstruksjon, klientoppsett og rapport.
- Kjør simulatoren separat fra leseverktøyene, og dokumenter skillet.

## Akseptansedemo

1. Koble en faktisk MCP-klient til serveren og hent bevis gjennom verktøyene.
2. Vis hvordan agenten bruker funnene i rapporten med sporbare henvisninger.
3. Prøv en ufarlig testbane utenfor roten og en symlenke til en testfil utenfor.
4. Vis at begge avvises, uten å lese ekte hemmeligheter eller private filer.
5. Be om en manglende fil og vis en forståelig feil som agenten kan håndtere.
6. Vis baseline og verifikasjon av et kandidatforsøk uten å endre kildene.

Bruk egne ufarlige testfiler. Ikke la en vellykket lesing alene telle som
bevis for at tilgangsgrensen virker.

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
