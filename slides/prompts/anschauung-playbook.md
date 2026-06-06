# Anschauung-Playbook

Handwerks-Anleitung für Anschauung-Bilder im Blueprint. **Nicht** ein Archetypen-Katalog — sondern eine Regel-Sammlung, wie man punktuell ein abstraktes Konzept mit einem vivid-Example-Bild bildlich einrasten lässt.

## Wann eine Anschauung einsetzen

- Selten: **1–3 pro Video-Deck**, nicht mehr.
- Wenn ein Konzept mit einem Satz nicht zündet, aber mit einem Bild sofort klar wird.
- Nie als Dekoration, immer als didaktisches Werkzeug.

Gute Kandidaten: abstrakte Mechaniken (Context Window, RAG, Embeddings, Loops), rollenbasierte Prozesse (Tool-Use, Delegation), Transformationen (Fine-Tuning, Distillation).

Schlechte Kandidaten: konkrete Fakten ("280k Stunden eingespart" — das ist ein Big-Stat), Definitionen ("Ein Agent ist..." — das ist Text), Ablauf-Diagramme ("Schritt 1 → 2 → 3" — das ist D2).

## Zielgruppe-Anker: Business-Professionals

Die Lernenden sind erwachsene Berufstätige. Analogien müssen aus ihrer Welt kommen, nicht aus Kindheit oder Fantasy.

**Mentale Modelle, aus denen sie bereits navigieren:**

- Projekte, Teams, Rollen, Delegation
- Meetings, Handouts, Protokolle, Agenden
- Operations, Prozesse, SOPs, Qualitätskontrolle
- Dashboards, Reporting, KPIs, Controlling
- Werkzeuge: Akten, Spreadsheets, Cockpits, Laboreinrichtung
- Räume: Meeting-Raum, Werkshalle, Rechenzentrum, Architektenbüro, Labor, Kontrollraum, Logistikzentrum
- Rollen: Bibliothekar:in, Architekt:in, Redakteur:in, Fluglotsin, Kurator:in, Produktionsleiter:in, Qualitätsmanager:in

**Was nicht in die Welt passt:**

- Märchen, Mythologie, Zauberei
- Cartoon-Tiere, antropomorphisierte Objekte
- Kindergarten-Beispiele (Bauklötze, Ampelmännchen, Legosteine)
- Superhelden, Videospiele
- Clipart, Duolingo-/Headspace-Stil, "cute" Illustrationen
- Surreale Größenrelationen ohne didaktischen Anker

## Ton und Anmutung

Editorial-Fotografie oder Illustration auf **Brand-Eins-Niveau** — erwachsen, gedeckt, ruhig. Farbpalette: gedämpfte Erdtöne mit einem ruhigen Akzent. Licht: natürlich, weich, leicht gerichtet. Keine Sättigung, keine Schockfarben, keine AI-Glow-Artefakte.

## Slide-Titel: indirekte Ansprache (wichtig)

Anschauung-Slide-Titel sind **beschreibend**, nicht anredend. Sie benennen die Szene oder das Motiv. Keine "du"/"Sie"/"man"-Formulierungen, keine Imperative.

| Vermeiden | Stattdessen |
|---|---|
| "Stell dir einen Bibliothekar vor" | "Die Bibliothekarin ohne Zutritt" |
| "Denk an einen Handwerker" | "Der Handwerker am Morgen" |
| "Stell dir vor, du bist Qualitätsprüfer" | "Qualitätsprüfung in der Fertigung" |
| "Man nehme eine Projektleiterin an" | "Projektleiterin am Whiteboard" |

Ebenso in den **Speaker-Notes**: statt "Stell dir einen Bibliothekar vor, der..." eine Indikativ-Einleitung wie "Eine Bibliothekarin, die... kann nur aus Erinnerung zitieren." Die Metapher wird beschrieben, nicht adressiert.

Grund: Die Zuschauerinnen und Zuschauer sind Business-Professionals. Eine direkte Anrede wirkt im Lehrvideo schnell belehrend oder vertraulich; eine beschreibende Szenensetzung dagegen lässt Raum für eigene Bildwerdung und passt zum editorialen Ton.

## Beispieltabelle

| Konzept | Gute Anschauung | Nicht geeignet |
|---|---|---|
| LLM ohne RAG | Bibliothekarin, die nur aus dem Gedächtnis zitieren darf — sie kann die Bibliothek nicht betreten | Zauberer mit leerem Zauberhut |
| Context Window | Schreibblock mit begrenzter Seitenzahl auf einem Arbeitsplatz | Rucksack, der überläuft |
| Tool Use | Projektleiterin, die am Whiteboard Spezialist:innen hinzuzieht | Roboter mit animiertem Werkzeugkasten |
| Agent Loop | Qualitätskontrolleurin in einer Fertigung mit Rückkopplungs-Schleife | Hamster im Rad |
| Fine-Tuning | Fachredakteurin, die einen Text mit roter Tinte auf Hausstil trimmt | Koch, der Gewürze mischt |
| Embedding | Bibliothekssystematik — Bücher thematisch nah beieinander auf Regalen | Blumenwiese mit Bienen |
| Prompt Injection | Kurierbrief, in dem jemand nachträglich eine falsche Anweisung eingefügt hat | Ninja, der Zettel stiehlt |
| Grounding | Lektorin, die Zitate in Originalquellen nachprüft | Anker im Meer |

## Prompt-Template für GPT-Image-2 oder Gemini

```
A [PROFESSIONAL ROLE] in [PROFESSIONAL SETTING], [DOING ONE SPECIFIC ACTION
THAT MAPS TO THE CONCEPT]. Editorial magazine photography aesthetic,
muted earth tones, dignified atmosphere, natural daylight.
```

**Beispiel — LLM ohne RAG:**

```
A librarian in a warm-lit reading room reaching for a specific book on a
high shelf, a small handwritten note in the other hand. Editorial magazine
photography aesthetic, muted earth tones, dignified atmosphere, natural
daylight.
```

Das Negative und die Composition-Regel kommen automatisch aus `profiles/anschauung.json` — nicht manuell in den Motiv-Prompt schreiben.

## Verbot: Was der Prompt nie enthalten darf

- "cartoon", "anime", "3D render", "stock photo"
- "cute", "playful", "whimsical", "magical"
- "isometric", "low-poly", "Pixar", "Disney"
- Explizite Marken oder reale Personen

Diese Token werden vom Profil `anschauung.json` bereits negativ gefiltert — aber im **User-Prompt** (Motiv) bitte auch nicht aktiv danach fragen.

## Qualitätskontrolle vor dem Einbau

Nach Bild-Generierung einmal prüfen:

1. Kann die Zielgruppe die Analogie ohne Erklärung lesen?
2. Wirkt das Bild erwachsen und editorial, oder verspielt/infantil?
3. Passt das Motiv zur Metapher, die in den Speaker-Notes ausgesprochen wird? (Andernfalls wird die Anschauung zu einer Verwirrung statt zu einem Anker.)
4. Hat es genug Negativraum für den Folien-Titel in der linken oberen Hälfte?

Wenn Punkt 1–3 nicht klar "ja" ist: **lieber kein Bild**. Ein gesprochener Satz schlägt ein halbgares Bild.
