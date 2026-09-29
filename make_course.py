# -*- coding: utf-8 -*-
"""make_course.py — produit un COURS complet en motion design (moteur data-driven ide.html) :
- N SHORTS (un par épisode) : CTA abonnement début + fin.
- 1 LONGUE : épisodes assemblés, SANS les cartons « épisode suivant » (isOutro coupés),
  rappels d'abonnement ENTRE les épisodes + intro/outro.
100% local. Sortie : ep0N-SHORT.mp4 (xN) + course-LONGUE.mp4

Prérequis :
  - Node.js + `npm i puppeteer-core` dans CE dossier (render_frames.js en dépend)
  - ffmpeg + ffprobe dans le PATH
  - `pip install edge-tts`

[SCRIPT À FOURNIR] Ce script appelait à l'origine une bibliothèque maison de normalisation
de prononciation TTS (correction phonétique du texte avant synthèse, utile pour les
anglicismes/sigles mal prononcés par la voix FR). Non embarquée ici : `normalize()`
ci-dessous est un no-op de repli (texte passé tel quel à edge-tts). Écrivez votre propre
pré-traitement texte si nécessaire et branchez-le à la place.

Personnalisation : CTA_VO / MID_VO / EPS sont des EXEMPLES — remplacez-les par vos propres
textes de CTA et le nombre d'épisodes de votre cours avant de lancer.
"""
import sys, json, subprocess, asyncio, shutil
from pathlib import Path
import edge_tts

HERE = Path(__file__).resolve().parent; MOTION = HERE/"motion"; DATA = MOTION/"data"
OUTDIR = HERE.parent   # dossier du cours (parent du dossier de travail)
VOICE, RATE, FPS, TAIL = "fr-FR-HenriNeural", "+3%", 30, 0.5
EPS = [1,2,3,4,5]

# --- [SCRIPT À FOURNIR] no-op de repli pour la normalisation TTS ---
def normalize(text: str, domains=None) -> str:
    """Passe-plat. Remplacez par votre propre normalisation phonétique si besoin."""
    return text

# EXEMPLE de textes de CTA — à remplacer par les vôtres.
CTA_VO = {
 101: "Avant de commencer : abonne-toi, like et partage, ça aide énormément la chaîne. Et petit secret : cette vidéo a coûté presque zéro euro, réalisée de façon automatique.",
 103: "Voilà ! Si c'était utile, abonne-toi pour ne rien rater de la suite du cours. À très vite.",
 111: "Avant de commencer, pense à t'abonner : c'est gratuit et ça aide la chaîne.",
 113: "Si ça t'a aidé, abonne-toi pour la suite du cours.",
}
MID_VO = ["Si ça t'aide, pense à t'abonner, c'est gratuit.",
          "Toujours là ? Un petit abonnement, ça aide vraiment la chaîne.",
          "Tu apprends des trucs ? Abonne-toi pour la suite."]
work = HERE/"_course_build"

def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],
                                capture_output=True, text=True).stdout.strip() or 0)
async def _t(t,o): await edge_tts.Communicate(normalize(t,domains=["tech"]),VOICE,rate=RATE).save(str(o))

def set_episode(epData):
    (MOTION/"episode-data.js").write_text("window.EPISODE="+json.dumps(epData if epData is not None else [],ensure_ascii=False)+";",encoding="utf-8")

def render_unit(epData, specs, prefix):
    """specs = list of (sceneId, vo). Retourne liste de clips mp4."""
    set_episode(epData)
    scenes, auds = [], []
    for i,(sid,vo) in enumerate(specs):
        mp3 = work/f"{prefix}_{i:02d}.mp3"; asyncio.run(_t(vo,mp3)); d=dur(mp3)
        fd = work/f"{prefix}_{i:02d}"; fd.mkdir(parents=True,exist_ok=True)
        scenes.append({"scene":sid,"durMs":int(round((d+TAIL)*1000)),"dir":fd.resolve().as_posix()}); auds.append((mp3,d))
    job = work/f"{prefix}_job.json"
    job.write_text(json.dumps({"htmlUrl":(MOTION/"ide.html").resolve().as_uri(),"fps":FPS,"scenes":scenes}),encoding="utf-8")
    subprocess.run(["node",str(HERE/"render_frames.js"),str(job)],check=True)
    clips=[]
    for i,(mp3,d) in enumerate(auds):
        c=work/f"{prefix}_{i:02d}.mp4"
        subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),
            "-i",str(work/f"{prefix}_{i:02d}"/"f%05d.jpg"),"-i",str(mp3),"-c:v","libx264","-crf","20",
            "-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-b:a","192k",str(c)],check=True)
        clips.append(c)
    return clips

def concat(clips, out):
    lst=work/("_l_"+out.stem+".txt"); lst.write_text("".join(f"file '{c.resolve().as_posix()}'\n" for c in clips),encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(lst),
        "-c:v","libx264","-crf","20","-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-b:a","192k",str(out)],check=True)
    print(f"[OK] {out.name} — {dur(out):.1f}s, {len(clips)} segments")

def main():
    if work.exists(): shutil.rmtree(work)
    work.mkdir()
    # 1) CTA (episode-data vide)
    cta_specs=[(111,CTA_VO[111]),(113,CTA_VO[113]),(101,CTA_VO[101]),(103,CTA_VO[103]),
               (102,MID_VO[0]),(102,MID_VO[1]),(102,MID_VO[2])]
    cta=render_unit(None, cta_specs, "cta")
    C={"111":cta[0],"113":cta[1],"101":cta[2],"103":cta[3],"mid":[cta[4],cta[5],cta[6]]}
    # 2) épisodes
    ep_clips={}   # N -> list of (clip, isOutro)
    for N in EPS:
        data=json.loads((DATA/f"ep{N:02d}.json").read_text(encoding="utf-8"))
        specs=[(i+1, s["vo"]) for i,s in enumerate(data)]
        clips=render_unit(data, specs, f"e{N}")
        ep_clips[N]=[(clips[i], bool(data[i].get("isOutro"))) for i in range(len(clips))]
        # SHORT N = CTA intro + contenu (tout) + CTA outro
        short=[C["111"]] + [c for c,_ in ep_clips[N]] + [C["113"]]
        concat(short, OUTDIR/f"ep{N:02d}-SHORT.mp4")
    # 3) LONGUE = intro + episodes (sans isOutro) + rappels entre + outro
    seq=[C["101"]]
    gap_after={2:C["mid"][0], 4:C["mid"][1]}  # 2 rappels d'abo bien espacés (ex. après ep2 et ep4)
    for idx,N in enumerate(EPS):
        seq += [c for c,o in ep_clips[N] if not o]   # contenu sans cartons "épisode suivant"
        if N in gap_after and N!=EPS[-1]:
            seq.append(gap_after[N])
    seq.append(C["103"])
    concat(seq, OUTDIR/"course-LONGUE.mp4")
    print(f"[COURSE DONE] {len(EPS)} shorts + 1 longue")

if __name__=="__main__":
    if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8",errors="replace")
    main()
