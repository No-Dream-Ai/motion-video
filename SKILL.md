---
name: motion-video
description: >
  Produit des cours/vidéos pédagogiques FR en MOTION DESIGN (HTML/CSS animé → rendu image par
  image via Chromium → ffmpeg + voix off edge-tts), à partir de DONNÉES de scènes. Moteur
  data-driven `ide.html` (style IDE code-native) + types de scène paramétrés. Produit, par
  cours : N épisodes-SHORTS + 1 version LONGUE assemblée, + sound design + miniatures +
  métadonnées. 100% local, 0 € (edge-tts + Chromium + ffmpeg). Triggers — "fais une vidéo/un
  cours motion design", "rends ce script en vidéo animée", "épisode en style IDE", "version
  longue + shorts", "miniatures + métadonnées de la vidéo".
metadata:
  type: tooling
---

# motion-video

Vidéos motion design **sans mouvement de fond** (règle dure : ça vibre). Chaque élément entre
une fois puis FIGE ; rendu **déterministe image par image** (Web Animations API + `__seek(ms)` →
screenshot Chromium), donc fluide et net.

## Prérequis

- **Node.js** + `npm i puppeteer-core` dans ce dossier (`render_frames.js` en dépend)
- **Chrome ou Chromium** installé — chemin configurable via la variable d'env `CHROME_PATH`
  (sinon éditer la constante `EXE` en tête de `render_frames.js`)
- **ffmpeg + ffprobe** dans le PATH
- **Python 3.10+**, `pip install edge-tts`

## DÉCOUPAGE (architecture)
Un cours = plusieurs **épisodes** (étapes). Pour chaque cours on produit DEUX choses :
- **SHORTS = les épisodes** (un mp4 par épisode, 16:9). CTA abonnement **début + fin** seulement.
- **LONGUE = les épisodes ASSEMBLÉS** en une vidéo. Dedans : intro (abonne/like/partage),
  **rappels d'abonnement ENTRE les épisodes** (2-3), outro abo. **AUCUN carton
  « épisode suivant »** dans la longue (coupé : les scènes `isOutro` sont retirées) — sinon redondant.

## PIPELINE (ordre) — lancer depuis le dossier de travail d'un cours (OUT = dossier parent du dossier de travail)
1. **Données** : `motion/data/epNN.json` = liste de scènes `{type, vo, ...contenu, isOutro?}`.
   Écrivez le contenu de VOS épisodes ici (les fichiers fournis en `motion/data/` sont un EXEMPLE
   de démo sur le thème "présentation d'un outil de code IA" — remplacez-les entièrement).
2. **Rendu + assemblage** : `python make_course.py` → rend chaque scène (ide.html piloté par data),
   construit les **shorts** (CTA début/fin) + la **longue** (assemblée, rappels entre épisodes,
   sans isOutro). Sortie dans le dossier parent : `epNN-SHORT.mp4` + `course-LONGUE.mp4`.
   Éditez en tête du script `EPS`, `CTA_VO`, `MID_VO` avec vos propres textes avant de lancer.
3. **Sound design** : `python add_sound.py` → whoosh aux transitions + tic à la révélation, mixés
   SOUS la voix, sur toutes les vidéos produites (réécrit en place).
4. **Métadonnées** : `python metadata.py` → `epNN-SHORT.json` (titre/desc/tags) + `course-LONGUE.json`
   (avec **chapitres** calculés sur les segments). Déposez optionnellement un `epNN-META.json`
   par épisode (titre/description/tags) dans ce dossier pour override les valeurs par défaut.
5. **Miniatures** : rendre `thumb.html?i=N` en 1280×720 (Chromium `--screenshot`) → `epNN-SHORT.png` +
   `course-LONGUE.png` (style IDE, badge épisode, gros mot-clé, étincelle).
6. **Teaser vertical** (optionnel) : `python make_teaser.py` → short 9:16 pour TikTok/IG/Shorts.
   Éditez la liste `VO` en tête du script.
7. **Publication** : ce skill NE fournit PAS de script de publication automatique (upload YouTube,
   posts réseaux) — cette étape dépend fortement de vos propres identifiants API et de votre
   pipeline de publication. Uploadez manuellement ou branchez votre propre outil.

## MOTEUR (`motion/`)
- `core.js` — mécanique : anims (rise/pop/slam/draw/type/wipe/scan/spin), `__seek` déterministe,
  typo cinétique (`kinetic`), `spark`, échelle `STAGE_W/STAGE_H` (déf 1280×720 ; vertical = 1080×1920).
  **core.js + le html + `episode-data.js` doivent être dans le MÊME dossier** (src relatifs).
- `ide.html` — **moteur de production** data-driven : lit `window.EPISODE` (depuis `episode-data.js`,
  écrit par make_course), `?scene=i` rend `EPISODE[i-1]`, ids 101/102/103/111/113 = scènes CTA.
  Types : title, statement, verb, code, terminal, tree, cards, diff, recap.
- `A-editorial.html`, `C-kinetic.html`, `D-premium.html`, `T-teaser.html` — **références de style**
  (échantillons 3 scènes / vertical), pas data-driven. ide.html (style B/IDE) = la direction retenue
  dans les exemples fournis (voir `DIRECTIONS.json` pour le raisonnement de choix de style).
- `render_frames.js` — Chromium (puppeteer-core) → frames. Lit `w`/`h` du job (vertical OK).
- `data/epNN.json` — les données de scènes par épisode (contenu d'EXEMPLE fourni, à remplacer).

## Format des données de scène (pour ide.html)
`{ "type": "...", "vo": "voix off verbatim", "isOutro": false, ...champs du type }`
- title{title,subtitle} · statement{keyword,lead} · verb{verb,body} · code{lines[],highlight?,caption}
- terminal{term:[{text,kind:cmd|out|ok}],caption} · tree{items:[{label,hot?}],caption} ·
  cards{cards:[{label,sub}],caption} · diff{minus[],plus[],caption} · recap{chips[],punch}
`isOutro:true` = scène « dans le prochain épisode… » → gardée dans le short, COUPÉE dans la longue.

## GARDE-FOUS QUALITÉ
Zéro mouvement de fond · UN seul orange actif par frame · pas de curseur clignotant en boucle ·
pas de glow/dégradé (ombres plates) · code à l'écran plausible SANS faute · typing par rafale ·
sauge = accepté/réversible, suppression = barré terracotta (jamais rouge seul) · valider en
planche-contact (1 frame/scène) AVANT le rendu complet. Détail du raisonnement de style dans
`DIRECTIONS.json` (issu d'un panel de critique adversarial sur 4 directions artistiques).

## PIÈGES TECHNIQUES (à ne pas refaire)
- **puppeteer-core doit être installé DANS le dossier** qui lance `render_frames.js` (`npm i puppeteer-core`).
- **Chemin Chrome** configurable via `CHROME_PATH` (variable d'env) ou en dur en tête de `render_frames.js`.
- **URL fichier** : utiliser `pathToFileURL` (Node) / `Path(...).as_uri()` (Python). Attention aux
  regex avec `\\` dans un heredoc bash (souvent mangées par l'interpréteur).
- **AUDIO = MONO de bout en bout.** La voix edge-tts est MONO ; un `aformat=...stereo` applique un
  **−3 dB** (compensation de puissance) → voix plus basse partout. Tout garder mono.
- **ffmpeg `amix normalize=0` NON respecté** (build 8.1 testé) : il divise par le nb d'entrées. Compenser
  ×N (bed SFX) et ×2 (mix final voix+bed). **`amerge` de deux mono** échoue (ambiguïté de canaux) → utiliser amix mono + compensation.
- Scripts `make_*`/`metadata`/`add_sound` supposent que le dossier de sortie (`OUTDIR`) est le
  parent du dossier où vivent ces scripts. Organisez votre arborescence en conséquence (un
  sous-dossier de travail par cours, ce skill à côté ou dedans).

## Ce qui N'EST PAS fourni

- **Publication automatique** (upload YouTube/réseaux) : dépend de vos identifiants API et de
  votre pipeline. `publish_motion.py` n'est pas inclus (il dépendait de modules privés
  non réutilisables). Uploadez manuellement, ou écrivez votre propre script d'upload
  (l'API YouTube Data v3 + `google-api-python-client` est la voie standard).
- **Normalisation phonétique TTS** : les scripts contiennent un no-op de repli
  (`normalize()` qui renvoie le texte tel quel). Si votre contenu a des anglicismes/sigles mal
  prononcés par la voix FR, écrivez votre propre pré-traitement texte.
