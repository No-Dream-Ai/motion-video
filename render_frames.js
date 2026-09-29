// render_frames.js — rend les frames d'une ou plusieurs scènes du moteur anim.html via Chromium.
// Lit un job JSON : { htmlUrl, fps, scenes:[{scene, durMs, dir}] }
//
// Prérequis : `npm i puppeteer-core` dans ce dossier + un Chrome/Chromium installé.
// Chemin de l'exécutable configurable via la variable d'env CHROME_PATH, ou en dur ci-dessous.
// Exemples de chemins courants :
//   Windows : "C:/Program Files/Google/Chrome/Application/chrome.exe"
//   macOS   : "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
//   Linux   : "/usr/bin/google-chrome" ou "/usr/bin/chromium"
const puppeteer = require("puppeteer-core");
const fs = require("fs");
const EXE = process.env.CHROME_PATH || "C:/Program Files/Google/Chrome/Application/chrome.exe";

(async () => {
  const job = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const fps = job.fps || 30;
  const W = job.w || 1920, H = job.h || 1080;
  const b = await puppeteer.launch({ executablePath: EXE, headless: "new",
    args: ["--no-sandbox", "--disable-gpu", "--force-device-scale-factor=1", `--window-size=${W},${H}`] });
  const p = await b.newPage();
  await p.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  for (const s of job.scenes) {
    await p.goto(`${job.htmlUrl}?scene=${s.scene}&dur=${s.durMs}`, { waitUntil: "networkidle0" });
    await p.waitForFunction("window.__ready===true", { timeout: 8000 });
    const frames = Math.max(1, Math.round(s.durMs / 1000 * fps));
    for (let f = 0; f < frames; f++) {
      await p.evaluate(t => window.__seek(t), f / fps * 1000);
      await p.screenshot({ path: `${s.dir}/f${String(f).padStart(5, "0")}.jpg`, type: "jpeg", quality: 92 });
    }
    console.log("scene", s.scene, "->", frames, "frames");
  }
  await b.close();
})().catch(e => { console.error("ERR", e.message); process.exit(1); });
