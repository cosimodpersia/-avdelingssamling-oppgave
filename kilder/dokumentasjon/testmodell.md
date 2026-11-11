# Lokal testmodell

`src/incident_lab/` er et kontrollverktøy, ikke en implementasjon gruppene skal
erstatte med sin løsning. Det bruker bare Python-standardbiblioteket, ingen
nettverkstilkobling, nøkler, modelltilgang eller faktisk venting.

## Hva modellen gjør

Den leser konfigurasjonen og de 40 behandlingstidene i `kilder/replay.json`.
Hver forespørsel behandles isolert. Et forsøk lykkes dersom behandlingstiden er
høyst det konfigurerte tidsavbruddet. Ellers bruker forsøket hele tidsavbruddet
og neste forsøk starter etter pausen. Alle forsøk for samme forespørsel bruker
samme behandlingstid. Samlet svartid inkluderer forsøk og pauser.

Resultatet inneholder sluttstatus, alle forsøk og samlede måltall.
Kommandoen `verify` kontrollerer i tillegg de fire faste kravene i driftsavtalen.

## Hva modellen ikke gjør

Den simulerer ikke kø, lastøkning, nettverksbrudd, autentisering, gatewayavbrudd,
kansellering, datatap eller reell duplikatbehandling. Den vet ikke om gruppens
årsaksforklaring er god. Den kan ikke bevise at en endring er trygg i produksjon.
Flere innstillinger kan bestå samme test. Begrunn valget og vurder også verste fall.

## Etterprøvbarhet

Resultatfiler lagrer SHA-256 for konfigurasjonsfil og datasett, inkludert deres
eksakte byteinnhold. Sammenlign før og etter mot samme, uendrede standarddatasett.
En alternativ `--dataset` kan brukes til tilleggstester, men erstatter ikke
felles regresjonstest. Oppgi tydelig når et annet datasett er brukt.

Avslutningskode 0 betyr at replay ble kjørt, eller at alle verifikasjonskrav bestod.
Kode 1 betyr at minst ett verifikasjonskrav feilet. Kode 2 betyr feil i inndata
eller filtilgang. Replay uten verifikasjon vurderer ikke om løsningen er god.
