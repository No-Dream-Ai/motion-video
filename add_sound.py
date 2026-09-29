# -*- coding: utf-8 -*-
"""add_sound.py — pose le sound design (whoosh transitions + tic révélation) sur les vidéos
du cours motion (shorts + longue), à partir des segments de _course_build. Voix = maître.
Réécrit les .mp4 finaux en place (via temp)."""
import json, subprocess, shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent; OUT=HERE.parent; WORK=HERE/"_course_build"; DATA=HERE/"motion"/"data"; SFX=HERE/"assets_sfx"
VOL={"whoosh":0.20,"pop":0.28}
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip() or 0)
def clip(pfx,i): return WORK/f"{pfx}_{i:02d}.mp4"
def ep_clips(N,noout=False):
    d=json.loads((DATA/f"ep{N:02d}.json").read_text(encoding="utf-8"))
    return [clip(f"e{N}",i) for i in range(len(d)) if not (noout and d[i].get("isOutro"))]
C={"111":clip("cta",0),"113":clip("cta",1),"101":clip("cta",2),"103":clip("cta",3),"m0":clip("cta",4),"m1":clip("cta",5)}

def sequences():
    seqs={}
    for N in [1,2,3,4,5]:
        seqs[f"ep{N:02d}-SHORT"]=[C["111"]]+ep_clips(N,False)+[C["113"]]
    L=[C["101"]]+ep_clips(1,True)+ep_clips(2,True)+[C["m0"]]+ep_clips(3,True)+ep_clips(4,True)+[C["m1"]]+ep_clips(5,True)+[C["103"]]
    seqs["course-LONGUE"]=L
    return seqs

def sound_one(name, clips):
    src=OUT/f"{name}.mp4"
    if not src.exists(): print("absent:",name); return
    # cues
    cues=[]; t=0.0
    for i,c in enumerate(clips):
        d=dur(c)
        if i>0: cues.append((t,"whoosh"))
        cues.append((t+0.45,"pop"))
        t+=d
    N=len(cues)
    bed=WORK/f"_bed_{name}.wav"
    args=["ffmpeg","-y","-hide_banner","-loglevel","error"]
    for _,ty in cues: args+=["-i",str(SFX/f"{ty}.wav")]
    parts=[];labs=[]
    for k,(tm,ty) in enumerate(cues):
        ms=int(round(tm*1000)); v=round(VOL[ty]*N,2)
        parts.append(f"[{k}]aresample=48000,adelay={ms},volume={v}[a{k}]"); labs.append(f"[a{k}]")
    fc=";".join(parts)+";"+"".join(labs)+f"amix=inputs={N}:duration=longest[bed]"
    subprocess.run(args+["-filter_complex",fc,"-ac","1","-map","[bed]",str(bed)],check=True)
    tmp=OUT/f"_tmp_{name}.mp4"
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(src),"-i",str(bed),
        "-filter_complex","[0:a]aresample=48000,volume=2[v];[1:a]aresample=48000,volume=2[s];[v][s]amix=inputs=2:duration=first[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",str(tmp)],check=True)
    shutil.move(str(tmp),str(src)); bed.unlink(missing_ok=True)
    print(f"[SON] {name} — {N} cues")

def main():
    for name,clips in sequences().items():
        sound_one(name,clips)
    print("[DONE] son posé sur toutes les vidéos")

if __name__=="__main__":
    import sys
    if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8",errors="replace")
    main()
