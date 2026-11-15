# Gerüst für die Neufassung, Teil 2

Arbeitsdatei, wird nicht gerendert (die Site rendert nur `.qmd`).
Bewusst auf Deutsch und nur in Stichpunkten: Der englische Text der
Neufassung soll von Florian selbst kommen. Formeln, Figuren und
Reihenfolge stehen fest, Formulierungen nicht.

Teil 1 (klassisch und allgemein quantenmechanisch) liegt in
`posts/depolarizing-roots/`, sein Gerüst samt Prosa-Befund in
`posts/depolarizing-roots/REWRITE-OUTLINE.md`. Die Muster-Liste dort
gilt hier genauso. Ein eigener Prosa-Befund für Teil 2 folgt, wenn
Teil 1 steht.

## Stand nach der Trennung (2026-11-08)

- `draft: true`: wird gerendert und ist unter
  `/posts/clifford-roots/` erreichbar (die URL, die bisher den ganzen
  Post zeigte), steht aber nicht in der Liste.
- Die Kapitel sind umnummeriert: `_01-paulis` (früher 4),
  `_02-clifford-qubit` (5), `_03-clifford-higher-dimensions` (6),
  `_04-whats-next` (7).
- Verweise auf die Bloch-Kugel und die Qubit-Wurzel sind jetzt Links
  auf Teil 1 (`../depolarizing-roots/#fig-bloch`, `#fig-bloch-root`).
- Am Anfang jedes Kapitels steht ein `TODO(Florian)` mit den
  Rückverweisen auf Teil 1, die angepasst werden müssen ("the previous
  section", "the quantum section", "the hook", "the very start of
  this post").
- Neu nötig: Einleitung von Teil 2 (TODO in `index.qmd`), eigener
  Titel (bisher Arbeitstitel), Teaserbild, Datum.

## Ziel und Budget

| Teil | vorher | Ziel | Eingriff |
|:--|--:|--:|:--|
| Einleitung | 0 | 150 | neu: was Teil 1 geliefert hat, was jetzt kommt |
| 1 Qubit aus dem Bit | 2.070 | 1.300 | Kern bleibt, Einleitung kürzen |
| 2 Clifford am Qubit | 1.720 | 900 | nur Definition, Reduktion, Konstruktion |
| 3 Höhere Dimensionen | 2.730 | 900 | Aufbau zitieren statt herleiten |
| 4 Schluss | 540 | 300 | Tabelle, Historie, offene Frage |

## Einleitung (neu)

- Teil 2 von 2, Link auf Teil 1.
- Rückblick in zwei Sätzen: d − 1 klassisch, d² − 1 quantenmechanisch.
- Die Frage dieses Teils: was bleibt in einer starren Familie?

## 1 Das Qubit aus dem Bit (Kern bleibt)

Der Gedankengang, der bleiben soll: Bit, Gruppe, Darstellung,
zweite Darstellung, Phasenraum, Phase erzwungen.

- Tabelle mit offener dritter Spalte. Ein kurzer Absatz, warum
  Clifford. Der Rückblick "Two settings are closed" passt jetzt gut
  als Einstieg in Teil 2.
- Bit als ρ = ½(I + rZ) und der Kopierer T[Z] = (1 − 2a) Z stehen
  jetzt in Teil 1 (Kapitel 3). Hier nur ein Satz Rückverweis, dann
  direkt mit den Labels beginnen.
- Labels 0, 1. Z ist die Parität (−1)^x. b ↦ Z^b ist Darstellung
  von Z₂.
- Zweite Darstellung: Addition auf die Ergebnisse anwenden, das ist
  der Flip X. a ↦ X^a.
- Klassisch getrennt: Zustände in span{I, Z}, Kopierer in
  span{I, X}. Im Qubit beide als Operatoren: Z₂ × Z₂, Phasenraum.
- Zählargument: exakt und Basis zugleich geht nicht (Aside).
- XZ = −ZX, Y = iXZ, Pauli-Tafel, projektive Darstellung.
  Das Vorzeichen ist die symplektische Form.

## 2 Clifford am Qubit (auf die Konstruktion reduzieren)

- Definition: T[σ] = λ_σ h(σ), h Permutation von X, Y, Z.
- λ reell, |λ| ≤ 1. Vollständige Positivität bleibt zu prüfen.
- Reduktion in einer Formel: T²[X] = λ_X λ_{h(X)} h²(X).
  T^n = P genau dann, wenn jede Wanderung eine Null trifft.
- Drei Fälle für h in je einem Satz. Nur der Dreierzyklus gibt 3.
- Die Wurzel: T[X] = 0, T[Y] = ½X, T[Z] = ½Y. Figur 5 (Gitter).
- Das ist die Wurzel aus Figur 4 von Teil 1. Teil 1 zeigt sie ohne
  Nachweis, dass sie ein Kanal ist; der Nachweis steht hier.
- Legalität: ½ UρU† + ¼ (XU)ρ(XU)† + ¼ (YU)ρ(YU)† (Aside).
- Zwei Fäden für Kapitel 3: h linear; η = −η nur bei d = 2.

Streichkandidaten: die drei Exponate (Bitflip, Hadamard, P), die
Bouquet-Figur samt Unterschrift, der Rückblick auf Teil 1.

## 3 Höhere Dimensionen (zitieren statt herleiten)

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

## 4 Schluss

- Faktor zwei ist nur Clifford (Theorem 3.4, Proposition 3.5).
  Teile davon (allgemeine Konstruktion, Proposition 3.5, Speicher-
  Lesart) wandern eventuell in den Schluss von Teil 1; dann hier nur
  noch kurz darauf verweisen.
- Ein Satz Historie: Clifford kam zuerst.
- Ausgefüllte Tabelle.
- Offen: d nicht prim.
