#!/usr/bin/env bash
# Collega questo progetto al repository GitHub e pubblica il ramo main.
#
# Uso:  bash COLLEGA-GITHUB.sh TUO-UTENTE-GITHUB
#
# Cosa fa, in ordine: verifica di essere in un repo git pulito o con modifiche
# committabili, imposta il remote origin se manca, allinea il ramo a main,
# committa l'eventuale residuo e pusha. Non tocca niente altro.

set -euo pipefail

UTENTE="${1:-}"
if [ -z "$UTENTE" ]; then
  echo "Uso: bash COLLEGA-GITHUB.sh TUO-UTENTE-GITHUB"
  exit 1
fi

REPO="${2:-tino}"
REMOTE_URL="https://github.com/${UTENTE}/${REPO}.git"

# In un worktree .git è un file, non una cartella: si chiede a git, non al filesystem.
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "ERRORE: qui non c'è un repository git. Lancia lo script dalla cartella del progetto."
  exit 1
fi

# 1. Identità git: se manca, la imposta a livello di repository (non globale).
if ! git config user.email >/dev/null 2>&1; then
  git config user.name "Tino"
  git config user.email "tino@users.noreply.github.com"
  echo "· identità git impostata per questo repository"
fi

# 2. Eventuale residuo non committato.
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "Stato corrente del progetto"
  echo "· commit del residuo non tracciato"
fi

# 3. Remote.
if git remote get-url origin >/dev/null 2>&1; then
  ATTUALE="$(git remote get-url origin)"
  if [ "$ATTUALE" != "$REMOTE_URL" ]; then
    echo "ERRORE: origin punta già a $ATTUALE"
    echo "Se è sbagliato: git remote set-url origin $REMOTE_URL"
    exit 1
  fi
else
  git remote add origin "$REMOTE_URL"
  echo "· remote origin → $REMOTE_URL"
fi

# 4. Ramo main.
RAME="$(git rev-parse --abbrev-ref HEAD)"
if [ "$RAME" != "main" ]; then
  git branch -M main
  echo "· ramo rinominato in main"
fi

# 5. Push. Se il repo remoto ha già commit (es. README creato sul sito), serve --force-with-lease
#    o un merge: qui proviamo il push semplice e spieghiamo l'errore.
if git push -u origin main; then
  echo
  echo "Fatto: https://github.com/${UTENTE}/${REPO}"
  echo "Prossimo passo: Settings → Secrets → Actions → ANTHROPIC_API_KEY (opzionale),"
  echo "poi Actions → tino → Run workflow per il primo run verde."
else
  echo
  echo "Il push non è andato. Cause tipiche:"
  echo "  · repo remoto non creato (apri https://github.com/new?name=${REPO}&visibility=public)"
  echo "  · password invece di token (serve un token con scope Contents: write)"
  echo "  · il repo remoto ha già commit: git pull --rebase origin main  poi rilancia"
fi
