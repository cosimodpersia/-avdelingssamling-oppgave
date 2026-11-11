# Avdelingssamlingen 2026: Fra feilrapport til begrunnet løsning

Alle gruppene skal automatisere den samme prosessen: undersøke en teknisk
feilrapport og foreslå en etterprøvbar løsning. Gruppene bruker samme kildemateriale,
men velger én av seks tekniske tilnærminger fra programmet for samlingen.

**Start her:** Les [feilrapporten](kilder/feilrapport.md), velg en oppgave nedenfor,
og kjør oppsettet. Ikke les `arrangor/` under gruppearbeidet, der ligger fasiten.

Kildemateriale og oppgavetekster er på norsk. Kode, kodeeksempler og eksempelmaler
er på engelsk. Hendelsen er fiktiv, og alle data er syntetiske.
Det interne programdokumentet er ikke inkludert.

## Velg én oppgave

| Oppgave | Dere lager | Det dere skal vise |
| --- | --- | --- |
| [1. Skill](oppgaver/01-skill.md) | En gjenbrukbar arbeidsbeskrivelse for agenten | Strukturert og repeterbar feilanalyse |
| [2. MCP-server](oppgaver/02-mcp-server.md) | Avgrensede verktøy for å lese bevis | Relevant informasjonsinnhenting og kontrollert tilgang |
| [3. Subagenter](oppgaver/03-subagenter.md) | Samarbeid mellom tydelige roller | Selvstendige funn, kritisk kontroll og syntese |
| [4. Sandboxing](oppgaver/04-sandboxing.md) | Et faktisk isolert arbeidsmiljø | Tillatt handling, blokkert handling og vellykket test |
| [5. UX for agentverktøy](oppgaver/05-ux-for-agentverktoy.md) | En visuell prototype | Konfigurasjon eller visualisering som avdekker feil |
| [6. Pi og OpenCode, ekspert](oppgaver/06-harness-sammenligning.md) | Et sammenlignbart forsøk i begge verktøy | Dokumentert sammenligning og begrunnet anbefaling |

Repoet gir felles data, rapportmal og testverktøy, ikke ferdige løsninger på
gruppeoppgavene. Gruppen velger selv språk og rammeverk for sitt bidrag.

## Kom i gang

Kjør alle kommandoer fra roten av dette repoet. Lokal replay krever Python 3.10
eller nyere og har ingen eksterne Python-avhengigheter. Conda-miljøet `p` kan
brukes dersom det allerede finnes. Docker er valgfritt.

```sh
python --version
export PYTHONPATH="$PWD/src"
python -m unittest discover -s tests -v
mkdir -p workspace artifacts
cp kilder/konfigurasjon/runtime.json workspace/runtime.json
python -m incident_lab replay \
  --config kilder/konfigurasjon/runtime.json \
  --output artifacts/baseline.json
```

Dette oppsettet krever verken installasjon eller nettverk. I PowerShell kan
miljøvariabelen settes med `$env:PYTHONPATH = "$PWD/src"`.

Et valgfritt alternativ er å installere pakken i et eget miljø. Da trenger dere
ikke sette `PYTHONPATH`:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install --no-build-isolation --no-deps -e .
```

Dette alternativet krever at `pip` og `setuptools>=61` finnes i miljøet.
Bruk oppsettet uten installasjon hvis de ikke finnes eller nettverk er sperret.

## Undersøk, endre en kopi og test

1. Les [kildeoversikten](kilder/README.md) og dokumentasjonen.
2. Lagre baseline. Den uendrede konfigurasjonen skal gjenskape feilen.
3. Bygg løsningen for valgt gruppeoppgave.
4. Endre bare `workspace/runtime.json`, ikke de delte kildene eller simulatoren.
5. Sammenlign kandidat og baseline, og begrunn årsak, tiltak og risiko.

```sh
python -m incident_lab verify \
  --config kilder/konfigurasjon/runtime.json \
  --output artifacts/baseline-verification.json
```

**Forventet avslutningskode her er 1.** Hendelsen er fortsatt uløst.
En vellykket kjøring av `replay` gir kode 0 selv om hendelsen ikke er løst.
Enhetstestene skal også bestå før dere retter noe, de tester selve testverktøyet.

Etter deres egen endring i arbeidskopien:

```sh
python -m incident_lab replay \
  --config workspace/runtime.json \
  --output artifacts/candidate.json
python -m incident_lab verify \
  --config workspace/runtime.json \
  --output artifacts/verification.json
```

Verifikasjon krever minst 99 prosent vellykkede forespørsler, p95 høyst 1200 ms,
maksimal svartid høyst 2500 ms og høyst 1,10 arkivkall per forespørsel i gjennomsnitt.
Alle krav må bestå, mot det samme standarddatasettet. Resultatet inneholder
input-hasher. Les [modellens begrensninger](kilder/dokumentasjon/testmodell.md):
en bestått simulering er ikke en produksjonsgodkjenning eller en årsaksforklaring.

Kontroller at kildene er uendret før levering, på systemer med `sha256sum`:

```sh
sha256sum --check kilder/SHA256SUMS
git diff -- kilder src tests
```

Sjekksummen er en praktisk kontroll mot utilsiktede endringer, ikke en sikkerhetsgrense.

## Leveranse

Legg gruppens kode og kjøreinstruksjon i for eksempel `solution/`.
Lever en kort rapport basert på [den engelske rapportmalen](examples/report-template.md),
baseline og kandidatmålinger, konfigurasjonsdiff og en demonstrasjon av valgt oppgave.
Rapportteksten kan være norsk, men behold malens engelske felter og overskrifter.

Påstander skal ha kildebaner og linjenumre. Skill observasjoner fra hypoteser.
Oppgi nøyaktige kommandoer, avslutningskoder, modell, verktøyversjoner og rettigheter.
Bruk gjerne [sesjonsmalen](examples/session-record.json). Ikke lagre API-nøkler,
tilgangstokener eller ukritisk eksport av agenthistorikk.

`workspace/` og `artifacts/` er utelatt fra Git. Del relevante resultater bevisst,
for eksempel som vedlegg eller gjennomgåtte kopier under gruppens leveransemappe.
Ikke bruk `git add -f` på en hel mappe som kan inneholde hemmeligheter.

## Tidsplan mandag

- 13:00 til 13:20: Velg oppgave, les grunnlaget og få baseline til å kjøre.
- 13:20 til 14:30: Bygg første versjon av arbeidsmåten.
- 14:30 til 15:20: Undersøk hendelsen, prøv endring og kontroller resultatet.
- 15:20 til 15:30: Ferdigstill rapport og kort demonstrasjon.
- 15:30 til 16:00: Frivillig deling. Vis også mislykkede forsøk og begrensninger.

## Modeller, nettverk og isolasjon

Agenttilgang avtales med arrangøren. Bruk godkjent modell og klient, og avklar kostnad
og databehandling før bruk. Replay fungerer uten modell, men erstatter ikke en
agentdemonstrasjon. MCP- og andre rammeverk kan kreve separat installasjon.
Klargjør slike avhengigheter før samlingen.

En minimal [Dockerfile](Dockerfile) er tilgjengelig som startpunkt for oppgave 4:

```sh
docker build -t incident-lab:local .
docker run --rm --network none incident-lab:local python -m incident_lab --help
```

Byggingen kan trenge nettverk for basisbildet. Dockerfile alene er ikke en ferdig
sandbox. Gruppen må selv etablere og demonstrere lesegrenser, skrivbare arbeidsområder
og øvrige begrensninger. Ikke monter hjemmemappen, Docker-sokkelen eller ekte
hemmeligheter. Ikke test tilgang mot faktiske interne tjenester.

## For arrangøren

Les [arrangørveiledningen](arrangor/README.md) før publisering og samlingen.
Git-repoet er initialisert lokalt, men ikke publisert til GitHub.
