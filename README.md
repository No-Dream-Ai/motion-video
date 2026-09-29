# motion-video

Produit des **vidéos pédagogiques en motion design** : texte et code animés, voix off française gratuite (edge-tts), rendu image par image via Chromium, assemblage `ffmpeg`. 100 % local, aucun service payant. Utilisable en pipeline autonome ou comme skill Claude Code.

*English summary: a data-driven motion-design video pipeline. You write scenes as JSON (title, code, terminal, tree, cards, diff, recap); an HTML/CSS engine renders them deterministically with headless Chromium (`puppeteer-core`), a French TTS voice-over is generated with `edge-tts`, and `ffmpeg` assembles shorts, a long video and a vertical teaser, with sound effects and metadata. Free, MIT. The bundled JSON episodes are demo content to replace.*

## Ce que fait l'outil

- Rend des scènes décrites en JSON (`motion/data/epNN.json`) avec le moteur `motion/ide.html` + `core.js`.
- Génère la voix off (edge-tts), le sound design (4 sons fournis), un teaser vertical 9:16, les métadonnées et le chapitrage.
- Reste déterministe : mêmes données, même vidéo.

## Ce que l'outil ne fait pas

- Aucune publication automatique (YouTube, réseaux) : vous gérez l'envoi.
- Ne rédige pas le contenu pédagogique : les épisodes fournis sont des **exemples à remplacer**.
- Pas de correction phonétique avancée avant la synthèse vocale (la fonction fournie est un passe-plat).
- Seule la voix edge-tts est câblée (remplaçable en éditant `_t()`).
- Rendu séquentiel : le temps croît avec le nombre de scènes.

## Prérequis

- Python 3.10+ et `pip install edge-tts`
- Node.js et `npm i puppeteer-core` (dans ce dossier)
- Chrome ou Chromium installé (chemin via la variable `CHROME_PATH`)
- `ffmpeg` et `ffprobe` dans le PATH

## Installation en 3 étapes

1. Cloner le dépôt : `git clone https://github.com/No-Dream-Ai/motion-video.git motion-video`, puis `npm i puppeteer-core` dans le dossier.
2. `pip install edge-tts`, puis vérifier `ffmpeg -version` et `node -v` (et définir `CHROME_PATH` si Chrome n'est pas au chemin par défaut).
3. Remplacer les exemples de `motion/data/epNN.json` par vos scènes (et les textes CTA de `make_course.py`).

## Exemple

```bash
python make_course.py     # rend et assemble shorts + longue
python add_sound.py       # sound design
python metadata.py        # titres, descriptions, chapitres
```

## Structure

```
SKILL.md, README.md, LICENSE
make_course.py  make_teaser.py  add_sound.py  metadata.py
render_frames.js  thumb.html  DIRECTIONS.json  package.json
assets_sfx/   vos sons ding, pop, thunk, whoosh (.wav) : non inclus, voir assets_sfx/LISEZ-MOI.md
motion/       core.js, ide.html, gabarits A/C/D/T, data/ep01-05.json (exemples)
```

## Licence

MIT, voir [LICENSE](LICENSE). Dépendances tierces (puppeteer-core, edge-tts, ffmpeg, Chromium) non incluses, licences propres.

## Plus d'outils No Dream

Cet outil est offert par la boutique No Dream : https://nodream-apercu-v73kq.netlify.app/prototype-5/
