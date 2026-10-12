# Gerüst für die Neufassung

Arbeitsdatei, wird nicht gerendert (die Site rendert nur `.qmd`).
Bewusst auf Deutsch und nur in Stichpunkten: Der englische Text der
Neufassung soll von Florian selbst kommen. Formeln, Figuren und
Reihenfolge stehen fest, Formulierungen nicht.

## Ziel und Budget

Fließtext heute rund 12.000 Wörter, dazu 4.200 in Asides. Ziel: rund
6.500 Wörter Fließtext, Asides etwa halbiert.

| Teil | heute | Ziel | Eingriff |
|:--|--:|--:|:--|
| Vorwort | 260 | 150 | neu schreiben, LLM-Satz ehrlich fassen |
| 1 Hook | 710 | 500 | neu schreiben, Speicher-Bild kürzen |
| 2 Klassisch | 2.130 | 1.500 | Struktur bleibt, Pointen und Rückverweise raus |
| 3 Quanten | 1.800 | 1.300 | Struktur bleibt |
| 4 Qubit aus dem Bit | 2.070 | 1.300 | Kern bleibt, Einleitung kürzen |
| 5 Clifford am Qubit | 1.720 | 900 | nur Definition, Reduktion, Konstruktion |
| 6 Höhere Dimensionen | 2.730 | 900 | Aufbau zitieren statt herleiten |
| 7 Schluss | 540 | 300 | Tabelle, Historie, offene Frage |

## Vorwort

- Diplomarbeit Hannover 2010, Speicherkanäle, daraus die Teilfrage.
- Wer hat was gemacht: Mathematik und Text von Florian, Grammatik
  maschinell geprüft, Figuren mit LLM-Hilfe gebaut.
- Route in einem Satz.

## 1 Hook

- Kopie der Kopie, Information geht in Schritten verloren.
- Zwei Extreme: ein Schritt; erst im Grenzwert (Fußnote Burgarth et
  al., Sanz et al., Wolf). Nicht das Thema.
- Die Frage: genau k gleiche Schritte bis zur totalen Löschung, wie
  groß kann k sein?
- Ein Satz zur Speicher-Lesart (Kretschmann und Werner).
- Vorschau: d − 1, d² − 1, (d² − 1)/2.

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
- d² − 1 Parameter gegen d − 1.
- Kanal: linear, spurerhaltend, vollständig positiv; unital.
- Gleiches Skelett, k ≤ d² − 1, erreicht (Aside: Choi-Matrix,
  ε ≤ 1/(d(d² − 2)), Theorem 3.4 im Paper). Figur 4.
- Überleitung: was bleibt in einer starren Familie?

## 4 Das Qubit aus dem Bit (Kern bleibt)

Der Gedankengang, der bleiben soll: Bit, Gruppe, Darstellung,
zweite Darstellung, Phasenraum, Phase erzwungen.

- Tabelle mit offener dritter Spalte. Ein kurzer Absatz, warum
  Clifford.
- Bit als ρ = ½(I + rZ). Labels 0, 1. Z ist die Parität (−1)^x.
  b ↦ Z^b ist Darstellung von Z₂.
- Kopierer in dieser Sprache: T[Z] = (1 − 2a) Z.
- Zweite Darstellung: Addition auf die Ergebnisse anwenden, das ist
  der Flip X. a ↦ X^a.
- Klassisch getrennt: Zustände in span{I, Z}, Kopierer in
  span{I, X}. Im Qubit beide als Operatoren: Z₂ × Z₂, Phasenraum.
- Zählargument: exakt und Basis zugleich geht nicht (Aside).
- XZ = −ZX, Y = iXZ, Pauli-Tafel, projektive Darstellung.
  Das Vorzeichen ist die symplektische Form.

## 5 Clifford am Qubit (auf die Konstruktion reduzieren)

- Definition: T[σ] = λ_σ h(σ), h Permutation von X, Y, Z.
- λ reell, |λ| ≤ 1. Vollständige Positivität bleibt zu prüfen.
- Reduktion in einer Formel: T²[X] = λ_X λ_{h(X)} h²(X).
  T^n = P genau dann, wenn jede Wanderung eine Null trifft.
- Drei Fälle für h in je einem Satz. Nur der Dreierzyklus gibt 3.
- Die Wurzel: T[X] = 0, T[Y] = ½X, T[Z] = ½Y. Figur 5 (Gitter).
- Legalität: ½ UρU† + ¼ (XU)ρ(XU)† + ¼ (YU)ρ(YU)† (Aside).
- Zwei Fäden für Kapitel 6: h linear; η = −η nur bei d = 2.

Streichkandidaten: die drei Exponate (Bitflip, Hadamard, P), die
Bouquet-Figur samt Unterschrift, der Rückblick auf Kapitel 3.

## 6 Höhere Dimensionen (zitieren statt herleiten)

Was im Text bleibt:

- Shift X und Uhr Z, ZX = ωXZ, w(a, b) = τ^{ab} X^a Z^b,
  w(η)† = w(−η). Als Fakten mit Literaturverweis, ohne Aside.
- d prim, Labelebene F_d².
- Familie: T[w(η)] = λ(η) w(hη), h ∈ GL(2, F_d),
  λ(−η) = conj λ(η).
- Wanderungsformel, Zyklen von h, Nullen setzen.
- Der lange Zyklus: Satz und kurzer Beweis im Haupttext (siehe
  unten). Beispiel d = 3 mit dem Achterring. Figur 6.
- −1 = g^{(d²−1)/2}, also liegt das Nullenpaar gegenüber:
  k = (d² − 1)/2.
- Kanal: Nullen auf einem Spiegelpaar, sonst ε ≤ 1/(d² − 3).
- Obere Schranke in zwei Sätzen (Zyklus spiegelsymmetrisch oder
  zwei disjunkte Zyklen).

Was durch Zitate ersetzt wird:

- Basis-Eigenschaft und Spiegelregel der Weyl-Operatoren.
- Kriterium für vollständige Positivität: Thesis Lemma 5.1.
- Aufbau endlicher Körper: Lidl und Niederreiter, Kapitel 2.
- Elemente maximaler Ordnung in GL(2, F_d) heißen in der Literatur
  Singer-Zyklen. Das Stichwort lohnt als Verweis.

Mögliche Quellen für den diskreten Phasenraum, vor dem Zitieren
selbst prüfen: Wootters 1987 (Wigner-Funktion für endliche
Systeme), Appleby 2005 (erweiterte Clifford-Gruppe), Gross 2006
(Hudson-Theorem für endliche Systeme).

### Der lange Zyklus, eingedampft

Aussage: Für jede Primzahl d gibt es h ∈ GL(2, F_d), das alle
d² − 1 Labels ungleich null in einem Zyklus durchläuft.

Beweisskizze in vier Schritten:

1. Es gibt einen Körper K mit d² Elementen, der F_d enthält
   (für ungerades d: x² − s mit einem Nichtquadrat s; Zitat).
2. Für jeden Teiler e von n = d² − 1 hat x^e = 1 höchstens e
   Lösungen in K. Hat ein Element a die Ordnung e, dann sind
   seine Potenzen bereits alle Lösungen, und genau φ(e) davon
   haben Ordnung e. Also gibt es höchstens φ(e) Elemente der
   Ordnung e.
3. Jedes der n Elemente hat eine Ordnung, die n teilt, und
   Σ_{e | n} φ(e) = n. Also wird jede Schranke ausgeschöpft,
   insbesondere bei e = n: Es gibt g der Ordnung n.
4. K ist eine Ebene über F_d, und η ↦ g·η ist F_d-linear. Das ist
   h. Seine Potenzen sind die Potenzen von g.

Zwei Fakten werden zitiert statt bewiesen: Existenz von K und
Σ φ(e) = n (Gauß).

## 7 Schluss

- Faktor zwei ist nur Clifford (Theorem 3.4, Proposition 3.5).
- Ein Satz Historie: Clifford kam zuerst.
- Ausgefüllte Tabelle.
- Offen: d nicht prim.
