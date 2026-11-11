# Arrangørveiledning, inneholder fasit

Denne mappen er ikke en del av deltakernes bevisgrunnlag. Ikke bruk fasiten som
agentkontekst under gruppearbeidet. Instruksen i AGENTS.md er en arbeidsregel,
ikke tilgangskontroll. Hvis fasiten må holdes skjult, fjern denne mappen fra
deltakerutgaven før første publisering, og oppbevar den i et separat privat repo.
Å slette mappen i en senere commit fjerner den ikke fra Git-historikken.

## Forberedelser

- Avklar GitHub-organisasjon, synlighet og lisens med eier før publisering.
  Ingen fjernkobling eller lisens er valgt på vegne av organisasjonen.
- Ikke last opp den interne program-PDF-en uten tillatelse. Repoet har bare syntetiske data.
- Prøv README-kommandoene på deltakernes maskiner. Lokal replay trenger bare Python.
- Avklar godkjent modell, tilganger, kostnadsgrense og installerte agentverktøy.
  Ikke legg felles nøkler i repoet.
- Klargjør eventuelle MCP-avhengigheter og containerbilder på forhånd.
- Kontroller faktisk tilgang til både Pi og OpenCode for ekspertgruppen.
  Samme modell er ønskelig; eventuelle forskjeller skal oppgis, ikke skjules.
- Kjør enhetstester, kildekontroll og baseline. Baseline-verifikasjon skal gi kode 1.
- Ta vare på en urørt original, og la hver gruppe bruke egen kopi eller gren.

## Fasit: årsak og medvirkende forhold

Effektivt tidsavbrudd mot arkiv-API-et er 250 ms. Bare 4 av 40 behandlingstider
er innenfor denne grensen. De øvrige 36 forespørslene utløser tre like forsøk,
som alle avbryter ventingen før arkiv-API-et fullfører.

Arkiv-API-et fullfører med HTTP 200 selv om klienten har sluttet å vente.
Dermed kan dokumentet være arkivert samtidig som Dokumentflyt gir 504.
Flere forsøk gir kapasitetsbruk og mulig overlapp uten å rette denne feilen.
Dette er ikke bevis på et autentiseringsproblem eller at arkiv-API-et er nede.

Materialet underbygger for lavt effektivt tidsavbrudd som hovedårsak og gjentatte
forsøk som medvirkende forhold. Det viser ikke den eksakte kodeendringen eller
hvorfor konfigurasjonsmalen fikk denne verdien. Deltakerne skal ikke dikte opp
en enhetskonverteringsfeil eller andre detaljer som ikke finnes i kildene.

Den lukkede, inaktive tilkoblingen før utrulling og sertifikatvarselet er støy.
Et varsel om utløp om 30 dager forklarer ikke dagens feil når TLS-kontrollen består.
Den tidligere versjonen har 40 vellykkede forespørsler i det sammenlignbare utvalget.

## Forventede måltall

| Måltall | Uendret konfigurasjon | Eksempelkandidat |
| --- | --- | --- |
| Forespørsler | 40 | 40 |
| Andel vellykkede | 0,10 | 1,00 |
| p95 samlet svartid | 950 ms | 870 ms |
| Maksimal svartid | 950 ms | 920 ms |
| Antall arkivkall | 112 | 40 |
| Arkivkall per forespørsel | 2,80 | 1,00 |

En enkel kandidat er 1000 ms tidsavbrudd og ett totalt forsøk. Eksempelet er ikke
eneste akseptable løsning. Den bør begrunnes med målinger, kapasitet og gatewayens
tidsbudsjett, og trenger integrasjonstest før eventuell reell bruk.

Å bare øke tidsavbruddet kan bestå replay med tre forsøk fordi alle lykkes første
gang i datasettet. Det gir likevel et verste-fall-budsjett over 2500 ms ved treghet.
En god rapport oppdager dette og forklarer avveiningen mellom færre forsøk,
tilgjengelighet ved forbigående feil og tidsbudsjett.

Kjør eksempelrettingen bare som arrangør, fra repoets rot:

```sh
export PYTHONPATH="$PWD/src"
mkdir -p workspace artifacts
python - <<'PY'
import json
from pathlib import Path

config = json.loads(Path("kilder/konfigurasjon/runtime.json").read_text())
config["dependency"]["timeout_ms"] = 1000
config["dependency"]["max_attempts"] = 1
Path("workspace/facilitator.json").write_text(json.dumps(config, indent=2) + "\n")
PY
python -m incident_lab verify \
  --config workspace/facilitator.json \
  --output artifacts/facilitator-verification.json
```

Verifikasjonen skal gi avslutningskode 0 og måltallene i tabellen.
Ikke distribuer denne arbeidskopien som del av deltakernes startmateriale.

## Vurdering og deling

Bruk følgende spørsmål i stedet for bare å telle beståtte tester:

1. Underbygger rapporten årsaken med flere uavhengige kilder og konkrete henvisninger?
2. Skiller gruppen bekreftede funn, plausible forklaringer og ukjente forhold?
3. Er tiltaket lite, begrunnet og testet mot uendret datasett?
4. Vurderer gruppen verste fall, idempotens, last, utrulling og tilbakeføring?
5. Demonstrerer gruppen faktisk egenskapen i valgt oppgave?

For skill: se etter en gjentatt prosess, ikke bare én vellykket chat.
For MCP: se etter reell klientbruk og avvist tilgang, inkludert symlenker.
For subagenter: se etter selvstendig arbeid, uenighet og kritisk kontroll.
For sandbox: se etter håndhevet blokkering, ikke bare modellens lydighet.
For UX: se etter en fungerende brukerhandling som avdekker en feil eller mangel.
For harness-sammenligning: se etter sammenlignbare vilkår og ærlig omtale av forskjeller.

## Hva som ikke er inkludert

Ingen ferdig skill, MCP-server, subagentorkestrering, UX-prototype eller komplett
agentsandbox er levert. Dette er nettopp oppgavene gruppene skal løse.
Dockerfile er bare et minimalt startbilde. Agenttilgang og GitHub-publisering
må ordnes av arrangøren. Det er ikke kjørt en reell Pi/OpenCode-sammenligning.
