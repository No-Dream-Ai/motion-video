# -*- coding: utf-8 -*-
"""make_teaser.py — SHORT teaser vertical 9:16 (1080x1920) pour TikTok/IG/FB/YT Shorts.

[SCRIPT À FOURNIR] no-op de repli pour la normalisation TTS (voir make_course.py).
Personnalisation : VO ci-dessous est un EXEMPLE — remplacez par votre propre texte de teaser."""
import sys, json, subprocess, asyncio, shutil
from pathlib import Path
import edge_tts

def normalize(text: str, domains=None) -> str:
    """Passe-plat. Remplacez par votre propre normalisation phonétique si besoin."""
    return text

HERE=Path(__file__).resolve().parent; MOTION=HERE/"motion"
VOICE,RATE,FPS,TAIL,W,H="fr-FR-HenriNeural","+3%",30,0.5,1080,1920
# EXEMPLE — remplacez ces 4 phrases par le teaser de votre propre cours.
VO=[
 "Et si tu pouvais apprendre ça en 4 minutes ?",
 "Pas un cours magistral. Une démo, pas à pas.",
 "Tu vois, tu comprends, tu appliques.",
 "La vidéo complète est sur la chaîne. Abonne-toi !",
]
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip() or 0)
async def _t(t,o): await edge_tts.Communicate(normalize(t,domains=["tech"]),VOICE,rate=RATE).save(str(o))
def main():
  work=HERE/"_teaser_build"
  if work.exists(): shutil.rmtree(work)
  work.mkdir(); auds=[]; scenes=[]
  for i,t in enumerate(VO):
    mp3=work/f"a{i}.mp3"; asyncio.run(_t(t,mp3)); d=dur(mp3); auds.append((mp3,d))
    fd=work/f"f{i}"; fd.mkdir(); scenes.append({"scene":i+1,"durMs":int(round((d+TAIL)*1000)),"dir":fd.resolve().as_posix()})
    print(f"  voix {i+1}: {d:.1f}s")
  (work/"job.json").write_text(json.dumps({"htmlUrl":(MOTION/"T-teaser.html").resolve().as_uri(),"fps":FPS,"w":W,"h":H,"scenes":scenes}),encoding="utf-8")
  print("  rendu frames 9:16…"); subprocess.run(["node",str(HERE/"render_frames.js"),str(work/"job.json")],check=True)
  clips=[]
  for i,(mp3,d) in enumerate(auds):
    c=work/f"c{i}.mp4"
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),"-i",str(work/f"f{i}"/"f%05d.jpg"),
      "-i",str(mp3),"-c:v","libx264","-crf","20","-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-b:a","192k",str(c)],check=True)
    clips.append(c)
  lst=work/"l.txt"; lst.write_text("".join(f"file '{c.resolve().as_posix()}'\n" for c in clips),encoding="utf-8")
  out=HERE/"ep01-B-TEASER-9x16.mp4"
  subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(lst),
    "-c:v","libx264","-crf","20","-pix_fmt","yuv420p","-r",str(FPS),"-c:a","aac","-b:a","192k",str(out)],check=True)
  print(f"[OK] {out.name} — {dur(out):.1f}s ({W}x{H})")
if __name__=="__main__":
  if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8",errors="replace")
  main()
