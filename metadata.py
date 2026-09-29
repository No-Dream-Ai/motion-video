# -*- coding: utf-8 -*-
"""metadata.py — génère les .json (titre/description/tags) pour les N shorts motion + la longue,
avec chapitrage de la longue calculé sur les segments rendus (_course_build).

Personnalisation : EPTITLE_DEFAULT / la description-modèle en bas de fichier sont des EXEMPLES.
Si vous avez déjà un titre/description/tags par épisode (venant d'un autre outil de votre pipeline),
déposez-les dans `ep{N:02d}-META.json` (même dossier que ce script, un fichier par épisode,
clés `title`/`description`/`tags`) — le script les reprendra automatiquement à la place des
valeurs par défaut."""
import json, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; OUT=HERE.parent; WORK=HERE/"_course_build"; DATA=HERE/"motion"/"data"
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip() or 0)
def ts(s): m,sec=divmod(int(round(s)),60); h,m=divmod(m,60); return (f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}")

# 1) SHORTS : reprendre un fichier `ep{N:02d}-META.json` si présent, sinon défaut générique
EPTITLE={}
for N in range(1,6):
    src=HERE/f"ep{N:02d}-META.json"
    meta=json.loads(src.read_text(encoding="utf-8")) if src.exists() else {"title":f"Épisode {N}","description":"","tags":[]}
    EPTITLE[N]=meta["title"].split("—")[0].split("(")[0].strip()
    out={"title":meta["title"][:100],"description":meta.get("description",""),"tags":meta.get("tags",[]),"lang":"fr"}
    (OUT/f"ep{N:02d}-SHORT.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"ep{N:02d}-SHORT.json : {out['title'][:60]}")

# 2) LONGUE : reconstruire la séquence (cf. make_course) + durées des clips -> chapitres
def clip(prefix,i): return WORK/f"{prefix}_{i:02d}.mp4"
def ep_noout(N):
    data=json.loads((DATA/f"ep{N:02d}.json").read_text(encoding="utf-8"))
    return [clip(f"e{N}",i) for i in range(len(data)) if not data[i].get("isOutro")]
# cta clips : ordre = [111,113,101,103,102a,102b,102c]
C101,C103,M0,M1=clip("cta",2),clip("cta",3),clip("cta",4),clip("cta",5)
seq=[("intro",[C101])]
seq+=[(f"ep{N}",ep_noout(N)) for N in [1,2]]
seq+=[("mid",[M0])]
seq+=[(f"ep{N}",ep_noout(N)) for N in [3,4]]
seq+=[("mid",[M1])]
seq+=[("ep5",ep_noout(5))]
seq+=[("outro",[C103])]
chapters=[]; t=0.0
for tag,clips in seq:
    if tag.startswith("ep"):
        N=int(tag[2]); chapters.append((t, EPTITLE[N]))
    elif tag=="intro":
        chapters.append((t,"Bienvenue"))
    for c in clips: t+= dur(c) if c.exists() else 0
total=t
chap_txt="\n".join(f"{ts(s)} {ti}" for s,ti in chapters)
# EXEMPLE de titre/description — remplacez COURSE_TITLE / COURSE_DESC_INTRO par les vôtres.
COURSE_TITLE = "Mon cours — le cours complet en français (FR)"
COURSE_DESC_INTRO = (
    "Sujet expliqué simplement, en français — le cours complet, tous les épisodes réunis.\n\n"
    "Du b.a.-ba jusqu'aux notions avancées : comprends et applique, pas à pas.\n\n"
)
desc=(COURSE_DESC_INTRO +
      "Chapitres :\n"+chap_txt+"\n\n"
      "Vidéo pédagogique animée, réalisée de façon automatisée. Abonne-toi pour la suite des cours.")
tags=[]
for N in range(1,6):
    for tg in json.loads((OUT/f"ep{N:02d}-SHORT.json").read_text(encoding="utf-8")).get("tags",[]):
        if tg not in tags: tags.append(tg)
longmeta={"title":COURSE_TITLE[:100],"description":desc,"tags":tags[:30],"lang":"fr"}
(OUT/"course-LONGUE.json").write_text(json.dumps(longmeta,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"\ncourse-LONGUE.json — {ts(total)} total, {len(chapters)} chapitres")
print(chap_txt)
