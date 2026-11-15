# Gerüst für die Neufassung, Teil 1

Arbeitsdatei, wird nicht gerendert (die Site rendert nur `.qmd`).
Bewusst auf Deutsch und nur in Stichpunkten: Der englische Text der
Neufassung soll von Florian selbst kommen. Formeln, Figuren und
Reihenfolge stehen fest, Formulierungen nicht.

## Gerüst-Modus (2026-11-08)

Die Kapitel von Teil 1 bestehen jetzt aus Stichpunkt-Kästen
(`::: {.skeleton}`, in der Vorschau gelb gestrichelt) zwischen den
festen Teilen: Formeln, Figuren, Asides, Fußnoten. Jeden Kasten
ersetzt du durch deinen eigenen Text; wenn der letzte weg ist, auch
den `.skeleton`-Block am Ende von `styles.css` löschen.

Der alte LLM-Text liegt unverändert in `_llm-text/` (wird nicht
gerendert). Die Zeilennummern im Prosa-Befund unten beziehen sich auf
diese Dateien. Das Gerüst wurde mit einem Skript gebaut, das Formeln,
Asides, Figuren und Fußnoten wörtlich aus `_llm-text/` übernimmt.

## Stand nach der Trennung (2026-11-08)

Der Post ist in zwei Einträge geteilt.

- **Teil 1**, `posts/depolarizing-roots/`: Vorwort, Hook, klassisch
  ($d - 1$), quantenmechanisch ($d^2 - 1$), neuer Schluss. Startpost
  der Serie, steht in der Liste.
- **Teil 2**, `posts/clifford-roots/` (`draft: true`): Pauli-Matrizen,
  Clifford-Kanäle am Qubit, höhere Dimensionen, Schluss. Wird
  gerendert, ist unter der alten URL erreichbar, steht aber nicht in
  der Liste. Eigenes Gerüst: `posts/clifford-roots/REWRITE-OUTLINE.md`.

Alle Stellen, die durch die Trennung kaputt sind, tragen im Quelltext
einen Kommentar `TODO(Florian)`. Finden mit:

```bash
grep -rn "TODO(Florian)" posts/
```

Die Kommentare stehen nach dem Rendern im HTML-Quelltext der Seite
(nicht sichtbar auf der Seite selbst). Vor dem Pushen also abarbeiten
oder in Kauf nehmen.

## Ziel und Budget

Fließtext heute rund 4.800 Wörter, dazu knapp 1.000 in Asides
(Formeln nicht mitgezählt).

| Teil | heute | Ziel | Eingriff |
|:--|--:|--:|:--|
| Vorwort | 280 | 150 | neu schreiben, LLM-Satz ehrlich fassen, Route ohne Clifford |
| 1 Hook | 710 | 500 | neu schreiben, Speicher-Bild kürzen, Clifford-Vorschau raus |
| 2 Klassisch | 2.050 | 1.500 | Struktur bleibt, Pointen und Rückverweise raus |
| 3 Quanten | 1.770 | 1.300 | Struktur bleibt, Schlussabsatz neu |
| 4 Schluss | 0 | 300 | neu, `_04-close.qmd` |

## Vorwort

- Diplomarbeit Hannover 2010, Speicherkanäle, daraus die Teilfrage.
- Wer hat was gemacht: Mathematik und Text von Florian, Grammatik
  maschinell geprüft, Figuren mit LLM-Hilfe gebaut. Der Satz muss am
  Ende stimmen (siehe unten, Abschnitt "Grundsatz").
- Route in einem Satz: Speicher, klassisch, Quanten. Teil 2 als
  Ausblick.
- Hinweis "Teil 1 von 2".

## 1 Hook

- Kopie der Kopie, Information geht in Schritten verloren.
- Zwei Extreme: ein Schritt; erst im Grenzwert (Fußnote Burgarth et
  al., Sanz et al., Wolf). Nicht das Thema.
- Die Frage: genau k gleiche Schritte bis zur totalen Löschung, wie
  groß kann k sein?
- Ein Satz zur Speicher-Lesart (Kretschmann und Werner).
- Vorschau: d − 1 und d² − 1 in diesem Teil. Die Clifford-Zahl
  (d² − 1)/2 höchstens als Ausblick auf Teil 2.

## 2 Klassisch (bleibt im Aufbau)

- Zustand als Wahrscheinlichkeitsvektor, Simplex. Figur 1.
- Linear, also Matrix; stochastisch; Mitte fest, also bistochastisch.
- P und die Definition: S^k = P, S^j ≠ P für j < k.
- Jede stochastische Wurzel fixiert die Mitte (SP = PS).
- Ein Bit: S v = (1 − 2a) v, also k = 1.
- S = P + N, PN = NP = 0, S^k = P + N^k. Wurzel heißt N nilpotent.
- Beispiel d = 3 mit u = (1, −1, 0), v = (1, 1, −2). Figur 2.
- Schranke k ≤ d − 1, erreicht (Aside: Jordan-Block, ε ≤ 1/d).

## 3 Quanten (bleibt im Aufbau)

- Bloch-Kugel, Länge und Richtung. Figur 3.
- ρ ausgeschrieben, Eigenwerte ½(1 ± ℓ).
- Neu (aus Teil 2 geholt): x = y = 0 gibt ρ = diag(p, 1 − p) =
  ½(I + rZ). Das klassische Bit ist die z-Achse der Kugel, die Kugel
  wächst um die Strecke herum. Nur Z, kein X und Y.
- d² − 1 Parameter gegen d − 1.
- Kanal: linear, spurerhaltend, vollständig positiv; unital.
- Gleiches Skelett, k ≤ d² − 1, erreicht (Aside: Choi-Matrix,
  ε ≤ 1/(d(d² − 2)), Theorem 3.4 im Paper). Figur 4.
- Neu: d = 2 als Mechanismus. Das Bit kann Z nur skalieren,
  S(Z) = (1 − 2a) Z, also k = 1. Die Qubit-Wurzel schiebt
  z → y → x → 0, (r₁, r₂, r₃) ↦ (r₂/2, r₃/2, 0): zwei zusätzliche
  Richtungen zum Zwischenparken. Genau die Animation in Figur 4.
- Neu: Übergang in den Schluss statt in die Clifford-Kapitel.
- Offene Frage durch die Trennung: Die Qubit-Wurzel in Figur 4 hat
  die Faktoren ½. Das Aside garantiert für d = 2 nur ε ≤ ¼. Dass die
  Figur wirklich einen Kanal zeigt, beweist erst Teil 2 (Legalitäts-
  Aside dort). Entscheiden: ein Satz Verweis auf Teil 2, oder das
  Aside hierher holen.

## 4 Schluss (neu)

- Zwischenstand: k ≤ d − 1 und k ≤ d² − 1, beide erreicht.
- Speicher-Lesart schließen: ein Qubit-Speicher überlebt höchstens
  drei Benutzungen, allgemein d² − 1.
- Maximale Wurzeln müssen nicht nahe bei P liegen (Proposition 3.5).
- Historie, falls sie hierher gehört: die allgemeine Konstruktion kam
  zuletzt, die Clifford-Kanäle zuerst.
- Ausblick auf Teil 2: starre Familie, Faktor zwei.
- Fußnote zur Diplomarbeit.

Steinbruch: `posts/clifford-roots/_04-whats-next.qmd`, Absätze 1
bis 3 und die Fußnoten.

---

# Prosa-Befund Teil 1: was du selbst neu schreiben musst

## Grundsatz

Ehrlich vorweg: Praktisch jeder englische Satz in Teil 1 ist von
einem LLM formuliert, die Commit-Historie zeigt das. Die Einteilung
unten sortiert nach zwei Fragen: Wo merkt ein aufmerksamer Leser es
am ehesten, und wo sitzt die meiste Stimme? Kategorie A und B sind
Pflicht. C solltest du machen. D kann bleiben, **aber nur, wenn das
Vorwort offen sagt, dass Teile mit LLM-Hilfe formuliert sind.** Soll
das Vorwort sagen "Text von mir", dann gehört auch D durch deine
Hände.

Arbeitstipp: Schreib jede Stelle aus den Stichpunkten oben und den
Formeln neu, nicht durch Umformulieren des englischen Texts. Wer
LLM-Text nur umbaut, behält dessen Rhythmus, und den hört man.

## A. Muss neu: durch die Trennung kaputt

Alle mit `TODO(Florian)` markiert.

| Datei, Zeile | Stelle | Problem |
|:--|:--|:--|
| `index.qmd`, Front Matter | `description` | fehlt; die alte war auf Clifford zugeschnitten und steht jetzt in Teil 2 |
| `index.qmd`, Z. 46 | "The route, roughly ..." | nennt Clifford-Kanäle und Faktor zwei |
| `_01-hook.qmd`, Z. 40 | "If you build things for a living ..." | verspricht "finite groups and finite fields" (das ist Teil 2) |
| `_01-hook.qmd`, Z. 90 und 98 | "That largest $k$ ..." und "It almost doesn't." | ganze Clifford-Vorschau |
| `_03-quantum-upgrade.qmd`, Z. 95 | letzter Satz: "file one promise away ..." | verspricht die Pauli-Matrizen "in the next section" |
| `_03-quantum-upgrade.qmd`, Fußnote `[^arw]` | "... the Clifford story below ..." | verweist auf Teil 2 |
| `_03-quantum-upgrade.qmd`, Z. 345 | "The unrestricted answer is therefore ..." | leitet in die Clifford-Kapitel über |
| `_04-close.qmd` | ganzer Schluss | fehlt, Stichpunkte stehen in der Datei |

## B. Muss neu: klingt stark nach KI, und zwar an sichtbaren Stellen

Das sind Anfang, Übergänge und die zentrale Definition, also die
Stellen, an denen ein Leser über deine Stimme entscheidet.

| Datei, Zeile | Stelle | Was es verrät |
|:--|:--|:--|
| `index.qmd`, Z. 37 | "The original was written for examiners ..." | "not for curious readers", "the advent of LLMs finally removed my last excuse", Dreierliste "pictures, worked examples, and a slower pace". Persönliche Aussage, muss von dir kommen und stimmen. |
| `_01-hook.qmd`, Z. 8 | "This is a familiar form of loss." | Dreierliste Hitze, Farbe, Regen; "Everywhere you look"; Chiasmus "processes that destroy information are processes that destroy it in *steps*" |
| `_01-hook.qmd`, Z. 15 | "Erasure in one step. Done." | Ein-Wort-Pointe |
| `_01-hook.qmd`, Z. 40 | "... one question wearing opposite uniforms" | dichtester KI-Absatz im ganzen Teil: "the eraser's patience and the survivor's endurance are the same number", "for the beauty of where the chase leads", "stay to the end and you will watch" (auch A) |
| `_01-hook.qmd`, Z. 63 und 74 | Speicher-Bild | "Not small, gone.", "To ask X is to ask Y". Laut Plan reicht ohnehin ein Satz. |
| `_02-classical-setup.qmd`, Z. 187 | Definition der Wurzel | "stops being a story about photocopiers and becomes one line of mathematics", "the whole post in miniature", "(and the beauty)", "the hunt". Dazu Z. 190, ein nachträglich eingeflickter Satz ("Here $k$ is a positive integer, the number of passes."), erkennbar an der überlangen Zeile. |
| `_02-classical-setup.qmd`, Z. 205 | "And here the restriction we imposed by hand grants itself." | Personifikation; "is not a fence we built around the hunt. It is a property ..."; "names the terrain honestly" |
| `_02-classical-setup.qmd`, Z. 218 | "Before hunting, notice where the teeth of the problem are." | "teeth" zweimal, "wearing a different name each time", Vorausdeutung "will grow into the main obstacle of the whole story" |
| `_02-classical-setup.qmd`, Z. 393 | "And that is the classical story." | Abschlusspointe "A clean bound, a clean construction, and not much more to say about it." |
| `_03-quantum-upgrade.qmd`, Z. 3 | "Everything so far was a rehearsal." | Meta-Größe: "the count turns out to be the whole plot of this section" |
| `_03-quantum-upgrade.qmd`, Z. 26 | "This is not a mathematical fiction." | Nicht-X-sondern-Y-Einstieg |
| `_03-quantum-upgrade.qmd`, Z. 177 | "So the quantum state space ..." | "every result in this post is a shadow of that one fact" |
| `_03-quantum-upgrade.qmd`, Z. 221 | "The classical bonus survives the upgrade word for word." | "not a restriction on the hunt but a property every candidate brings along", wiederholt die Figur aus `_02` Z. 205 |
| `_03-quantum-upgrade.qmd`, Z. 229 | "Here is where that quadratic shows up where it counts." | Wegweiser; dazu Flickstelle "a rank-one map, rank one as a linear map" (Z. 232) |
| `_03-quantum-upgrade.qmd`, Z. 302 | "Set $d = 2$." | "The room to subdivide erasure grew, and it grew quadratically." |

## C. Sollte neu: Erklärprosa mit typischen Ticks

Inhaltlich meist gut, aber mit den Mustern aus der Liste unten.

- `_01-hook.qmd`, Z. 1 bis 6: der Einstieg. Nicht schlimm, aber der
  erste Absatz, den jemand von HN liest. In deinen Worten.
- `_01-hook.qmd`, Z. 22: "This is a genuinely interesting region of
  design space."
- `_01-hook.qmd`, Z. 29 bis 34: die Frage selbst. Schlicht, aber der
  Kernsatz des Posts. In deinen Worten.
- `_02-classical-setup.qmd`, Z. 6 und 13: "the honest description",
  "nothing else counts".
- `_02-classical-setup.qmd`, Z. 21: Simplex-Absatz. Lange
  Apposition-Ketten, Rückverweis "the grey noise from the start of
  this post", "the whole job of an erasing copier".
- `_02-classical-setup.qmd`, Z. 50 bis 58: "it is worth asking what
  we want to insist on", "a contradiction in terms".
- `_02-classical-setup.qmd`, Z. 92: "It is worth seeing ...",
  "nothing but".
- `_02-classical-setup.qmd`, Z. 114 und 121: "in retrospect it is the
  most interesting one", rhetorisches "Why?", Vorausdeutung "in a
  moment it will reveal itself as no restriction at all".
- `_02-classical-setup.qmd`, Z. 159: "One small fact worth pinning
  down".
- `_02-classical-setup.qmd`, Z. 244: "pay off", "The question has
  collapsed."
- `_02-classical-setup.qmd`, Z. 264: "That is the whole recipe."
  Inhaltlich: "it can have rank at most one" gilt so nur für d = 3.
  Das Aside sagt es richtig (2 rank N ≤ d), der Haupttext nicht.
- `_02-classical-setup.qmd`, Z. 296 und 318: "an honest copier",
  "funnelling", "hands us the general bound for free", "runs out of
  room".
- `_03-quantum-upgrade.qmd`, Z. 8 und 15: "One number, one dimension
  of freedom.", "one of the genuine surprises", "the geometry of
  states, not the algebra of amplitudes".
- `_03-quantum-upgrade.qmd`, Z. 35: "that, and not fuzziness, is what
  the surface is encoding".
- `_03-quantum-upgrade.qmd`, Z. 50: "watch the ball fall out of it".
- `_03-quantum-upgrade.qmd`, Z. 70: rhetorisches "Where does three
  come from?", "are not a metaphor. They are the room this matrix
  has."
- `_03-quantum-upgrade.qmd`, Z. 95: "The matrix even knows the ball
  is *round*."
- `_03-quantum-upgrade.qmd`, Z. 136 und 140: "the pattern worth
  chasing", "its rules are not arbitrary. They are ...", "That last
  clause is the point", "that is where the quantum content lives".
- `_03-quantum-upgrade.qmd`, Z. 182: "The rest of the cast",
  "genuinely new", zweimal "simply", "we will not pry them open".
- `_03-quantum-upgrade.qmd`, Z. 206: "the name matters less than the
  picture".
- Bildunterschrift Figur 4 (`_03`, Z. 312): "the blue $z$-pole is the
  hero".
- Fußnote `[^qcvc]` (`_03`, Z. 54): persönliche Empfehlung ("the
  gentlest on-ramp I know"), sollte in deinen Worten sein.

## D. Kann bleiben, leicht glätten genügt

- Sachliche Absätze, die eine Formel tragen: `_02` Z. 88, 102, 135,
  166, 179, 229; `_03` Z. 158, 215.
- Alle sieben Asides. Es sind Herleitungen und lesen sich neutral.
  Einzelne Ticks: "These two descriptions had better agree" (`_02`
  Z. 77). Im Jordan-Aside (`_02` Z. 350) "That matrix is a
  representation of $N$": In Teil 2 heißt "representation" etwas
  anderes (Gruppendarstellung). Besser "the matrix of $N$ in a
  suitable basis".
- Bildunterschriften der Figuren 1 bis 3. Nur "an even wash" kommt
  doppelt vor (Text und Unterschrift).
- Literatur-Fußnoten (`[^mixing-ref]`, `[^memory-channels]`,
  `[^channels]`, `[^arw]` bis auf den letzten Satz).
- Vorwort, Absatz 1 und 4 (`index.qmd` Z. 30 und 52).

## Muster zum Selbstprüfen

Wenn du beim Schreiben eines davon bemerkst, kurz innehalten. Die
Zahlen sind die Häufigkeit im heutigen Text von Teil 1.

1. **"exactly"**: 27-mal (15 davon in `_02`). Das auffälligste
   Einzelwort. Dazu "whole" 12, "room" 9, "worth" 7, "genuine(ly)" 6,
   "simply" 6, "hunt" 5, "lawful" 5, "honest(ly)" 3, "nothing but" 3.
2. **Nicht X. Sondern Y.** "is not a fence ... It is", "not a
   mathematical fiction", "not a metaphor. They are", "not a
   restriction on the hunt but".
3. **Pointen-Fragmente am Absatzende.** "Done.", "Not small, gone.",
   "That is the whole recipe.", "The question has collapsed."
4. **Meta-Größe.** "the whole plot of this section", "the whole post
   in miniature", "a shadow of that one fact", "the most instructive
   part of the whole story".
5. **Vorausdeutungen.** "in a moment it will reveal itself", "file
   one promise away", "it will grow into the main obstacle".
6. **Durchgezogene Metaphern.** teeth, hunt, lawful, room,
   rehearsal, "wearing opposite uniforms", "wearing a different
   name", hero.
7. **Personifikation.** "the matrix even knows", "the restriction
   grants itself".
8. **Wegweiser.** "it is worth asking", "worth pinning down",
   "Notice", "Here is where".
9. **Dreierlisten.** Hitze, Farbe, Regen; "pictures, worked examples,
   and a slower pace".
10. **Rhetorische Frage mit sofortiger Antwort.** "Why? The uniform
    distribution ...", "Where does three come from?"
11. **Rückverweis-Ketten.** "from a moment ago", "from the start of
    this post", "the grey centre of the triangle from a moment ago".
