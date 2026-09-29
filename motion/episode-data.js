window.EPISODE=[
 {
  "type": "title",
  "vo": "Imagine un collègue qui connaît ton projet par cœur, qui peut lire tes fichiers, éditer du code, et lancer des commandes dans le terminal. Eh bien, ça existe. C'est Claude Code.",
  "title": "Claude Code",
  "subtitle": "Ton collègue qui lit, édite et lance ton code"
 },
 {
  "type": "statement",
  "vo": "Claude Code, c'est pas un chatbot qui te recrache juste du texte. Non, c'est un AGENT. Il lit ton code, il l'édite, il teste, il agit vraiment.",
  "keyword": "AGENT",
  "lead": "Pas un chatbot. Un agent qui agit vraiment."
 },
 {
  "type": "verb",
  "vo": "Première chose : Claude Code lit ton code. Tu lui dis « j'ai un bug dans mon authentification », et hop, il fouille tes fichiers, comprend comment ça marche, trouve le souci.",
  "verb": "LIT",
  "body": "Il fouille tes fichiers, comprend le code et trouve le bug."
 },
 {
  "type": "diff",
  "vo": "Deuxième chose : il édite tes fichiers à la bonne place. Il modifie le code, ajoute ce qu'il faut, supprime ce qui traîne. Et chaque modif, tu peux la voir, l'accepter ou la refuser. C'est toi qui décides.",
  "minus": [
   "if (user.password === input) {",
   "  return true",
   "}"
  ],
  "plus": [
   "if (await verifyHash(input, user.hash)) {",
   "  return createSession(user)",
   "}"
  ],
  "caption": "Chaque modif : tu vois, tu acceptes ou tu refuses."
 },
 {
  "type": "terminal",
  "vo": "Troisième chose, et c'est crucial : Claude Code peut lancer des commandes. Il exécute tes tests, compile, pousse sur git, tout ce que tu ferais en ligne de commande.",
  "term": [
   {
    "text": "npm test",
    "kind": "cmd"
   },
   {
    "text": "Tests:  24 passed, 24 total",
    "kind": "out"
   },
   {
    "text": "git push origin main",
    "kind": "cmd"
   },
   {
    "text": "main -> main (poussé)",
    "kind": "ok"
   }
  ],
  "caption": "Il lance tes commandes, comme toi dans le terminal."
 },
 {
  "type": "cards",
  "vo": "Donc pendant que toi tu peux te détendre, Claude Code travaille. Il lit, il modifie, il teste, il corrige. C'est un AGENT qui agit, pas juste un bot qui parle.",
  "cards": [
   {
    "label": "Lit",
    "sub": "comprend le projet"
   },
   {
    "label": "Modifie",
    "sub": "édite les fichiers"
   },
   {
    "label": "Teste",
    "sub": "vérifie le résultat"
   },
   {
    "label": "Corrige",
    "sub": "boucle jusqu'au vert"
   }
  ],
  "caption": "Un agent qui agit, pas un bot qui parle."
 },
 {
  "type": "statement",
  "vo": "Pourquoi c'est ouf ? Parce que c'est vraiment automatisé. Pas de copier-coller manuel, pas de « il me donne du code et je colle ». Non, tout se fait directement dans tes fichiers.",
  "keyword": "DIRECT",
  "lead": "Zéro copier-coller. Tout se fait dans tes fichiers."
 },
 {
  "type": "tree",
  "vo": "Et ça marche partout. Dans le terminal, VS Code, ton IDE JetBrains, sur le web, sur le desktop app. C'est le même Claude Code peu importe où tu l'utilises.",
  "items": [
   {
    "label": "Terminal",
    "hot": true
   },
   {
    "label": "VS Code"
   },
   {
    "label": "JetBrains"
   },
   {
    "label": "Web"
   },
   {
    "label": "Desktop app"
   }
  ],
  "caption": "Le même Claude Code, partout où tu travailles."
 },
 {
  "type": "terminal",
  "vo": "Tu peux aussi demander à Claude Code de créer des commits. Tu lui dis « commite tes changements », et il stage les fichiers, écrit un bon message, crée la branche. Prêt à merger.",
  "term": [
   {
    "text": "git add .",
    "kind": "cmd"
   },
   {
    "text": "git commit -m \"fix: corrige l'authentification\"",
    "kind": "cmd"
   },
   {
    "text": "[fix-auth a1b2c3d] 3 fichiers modifiés",
    "kind": "out"
   },
   {
    "text": "branche prête à merger",
    "kind": "ok"
   }
  ],
  "caption": "Il stage, écrit un bon message et crée la branche."
 },
 {
  "type": "cards",
  "vo": "Et tu peux le customiser à fond. Ajouter tes propres instructions dans CLAUDE.md, créer des skills réutilisables, brancher tes outils externes avec MCP. Pas de boîte noire.",
  "cards": [
   {
    "label": "CLAUDE.md",
    "sub": "tes instructions"
   },
   {
    "label": "Skills",
    "sub": "réutilisables"
   },
   {
    "label": "MCP",
    "sub": "tes outils externes"
   }
  ],
  "caption": "Personnalisable à fond. Pas de boîte noire."
 },
 {
  "type": "terminal",
  "vo": "Si tu changes d'avis ? Aucun problème. Chaque modif est sauvegardée, tu peux annuler, revenir en arrière, recommencer. C'est totalement sécurisé.",
  "term": [
   {
    "text": "git checkout -- src/auth.js",
    "kind": "cmd"
   },
   {
    "text": "fichier restauré (version précédente)",
    "kind": "out"
   },
   {
    "text": "rien de cassé, tout est sauvegardé",
    "kind": "ok"
   }
  ],
  "caption": "Annule, reviens en arrière, recommence. Sécurisé."
 },
 {
  "type": "recap",
  "vo": "Récap simple : Claude Code lit ton code, le comprend, l'édite, teste, crée des commits. C'est autonome MAIS tu contrôles tout. Tu dis oui ou non, toujours.",
  "chips": [
   "Lit",
   "Comprend",
   "Édite",
   "Teste",
   "Commit"
  ],
  "punch": "Autonome, mais c'est toi qui contrôles tout."
 },
 {
  "type": "title",
  "vo": "Dans la vidéo suivante, on te montre comment l'installer et faire ton premier truc avec. Allez, on se lance !",
  "title": "Épisode 2",
  "subtitle": "Installation et premier pas. On se lance !",
  "isOutro": true
 }
];