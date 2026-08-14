# PRE — Production Reference Environment

Prywatne środowisko produkcji filmowej AI, automatyzujące workflow
wypracowany w projektach Higgsfield (HELL GRIND, CULLY HILL BOYS, ONEIRIC).

Cel docelowy: **scenariusz → wybrana scena → nakręcona i zmontowana scena**,
obsługiwane przez rozmowę po polsku.

## Dokumentacja

| Plik | Zawartość |
|---|---|
| `CLAUDE.md` | zasady projektu, nienaruszalne reguły |
| `docs/PRE_PROJECT_CONTEXT.md` | pełny kontekst i workflow docelowy |
| `docs/DECISIONS.md` | podjęte decyzje (D-001…D-010) |
| `docs/DECISION_GATES.md` | gdzie system działa sam, a gdzie staje i pyta |
| `docs/ARCHITECTURE_AUDIT.md` | audyt specyfikacji, sprzeczności i otwarte kwestie |
| `docs/modules/01_global_script_analyzer.md` | specyfikacja Modułu 01 |
| `docs/references/` | cztery briefy produkcyjne Higgsfield |
| `docs/skills/` | sześć skilli produkcyjnych |

## Stan: Moduł 01 — Global Script Analyzer

Zaimplementowana jest **warstwa deterministyczna** — ta, którą zgodnie ze
specyfikacją (§35) musi obsługiwać kod, a nie model językowy.

**Gotowe:**

- utworzenie projektu (`Film.pre/` z `project.db` i katalogami produkcyjnymi),
- blokada projektu i bezpieczne zamknięcie bazy (istotne w iCloud/Dropbox — D-010),
- import scenariusza z zachowaniem oryginalnego pliku bez zmian,
- adaptery formatów: Fountain, Final Draft (.fdx), Celtx, Word (.docx),
  PDF i TXT,
- parsowanie scen — nagłówki polskie (WN./PL./ZEW.) i angielskie (INT./EXT.),
  pory dnia, sublokacje, numery scen, kolejność scenariuszowa,
- rozdzielenie dialogu od didaskaliów, rozpoznanie `(O.S.)`, `(V.O.)`,
  `(POZA KADREM)`, `(Z OFF)`,
- wykrycie postaci (z didaskaliów i cue'ów) oraz lokacji (z nagłówków),
- wystąpienia postaci w scenach z rozróżnieniem `FACT` / `INFERENCE`,
- aliasy zachowujące oryginalny zapis ze scenariusza,
- wykrycie jawnych znaczników chronologii (RETROSPEKCJA, SEN, FLASHBACK),
- wymagania głosowe i aktorskie dla postaci mówiących i powracających,
- zgłoszenia do decyzji (`ReviewFlag`) przy podobnych nazwach — **bez
  automatycznego scalania**,
- ślad źródłowy (`source_evidence`) — „skąd PRE to wie",
- podsumowanie po polsku z poprawną odmianą liczebników,
- 80 testów.

**Jeszcze nie zaimplementowane (warstwa semantyczna, Moduł 01 część 2):**

- wykrywanie zdarzeń zmieniających stan (przemoczenie, rana, zmiana kostiumu),
- budowa osi stanów i zależności continuity,
- rozpoznawanie istotnych rekwizytów,
- rozstrzyganie aliasów wymagających rozumienia treści,
- wnioskowanie chronologii bez jawnego znacznika,
- plan wymagań assetowych (`AssetRequirement`).

To jest praca dla modelu, nie dla kodu — z walidacją i zapisem przez warstwę
deterministyczną, zgodnie z §35–36 specyfikacji.

## Obsługiwane formaty scenariusza

| Format | Skąd czytana jest struktura |
|---|---|
| `.fountain`, `.spmd` | konwencja zapisu Fountain |
| `.fdx` (Final Draft) | typy akapitów zapisane w pliku |
| `.celtx` | klasy akapitów w dokumencie HTML wewnątrz kontenera |
| `.docx` (Word) | style akapitów, a gdy ich brak — konwencja zapisu |
| `.pdf` | warstwa tekstowa + wcięcia (wymaga `pypdf`) |
| `.txt` | konwencja zapisu |

Formaty strukturalne (FDX, Celtx, Word ze stylami) nie zgadują, co jest
nagłówkiem, a co postacią — czytają to wprost z pliku.

Przy PDF-ach usuwane są numery stron oraz znaczniki `CONTINUED` i `(MORE)`,
a puste linie rozdzielające bloki są odtwarzane na podstawie wcięć — bez
tego kwestia dialogowa wchłonęłaby didaskalia, które po niej następują.
PDF bez warstwy tekstowej (skan) jest odrzucany z informacją, że potrzebny
jest OCR.

## Uruchomienie

Wymagany Python 3.11+. Do importu PDF dodatkowo:

```bash
pip install pypdf
```

```bash
python3 -m pre.cli nowy ~/Filmy/Moj_film --nazwa "Mój film"
python3 -m pre.cli import ~/Filmy/Moj_film.pre scenariusz.fountain
python3 -m pre.cli sceny ~/Filmy/Moj_film.pre
python3 -m pre.cli postac ~/Filmy/Moj_film.pre "ANNA"
python3 -m pre.cli niejasnosci ~/Filmy/Moj_film.pre
```

Konsola istnieje po to, żeby sprawdzić analizę na prawdziwym scenariuszu.
Docelowym interfejsem jest czat (D-003).

## Testy

```bash
python3 -m pytest
```

Scenariusz testowy (`fixtures/synthetic_pl.fountain`) jest w pełni
syntetyczny i celowo zawiera: powracające postacie i lokację, zmianę
kostiumu, przemoczenie, ranę i opatrunek, rekwizyt niesiony przez sceny i
zmieniający stan, wariant dnia i nocy tej samej lokacji, retrospekcję oraz
dwa przypadki celowej niejednoznaczności.
