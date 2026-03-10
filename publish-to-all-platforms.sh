#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/wells1137/meowload-downloader"
SKILL_DIR="./skills/meowload-downloader"

echo "============================================"
echo "  MeowLoad Downloader - Multi-Platform Publish"
echo "============================================"
echo ""
echo "GitHub Repo: $REPO_URL"
echo ""

# ── 1. Cursor Marketplace ──
echo "┌─ 1. Cursor Marketplace"
echo "│  Submit manually at:"
echo "│  https://cursor.com/marketplace/publish"
echo "│  Paste: $REPO_URL"
echo "└─"
echo ""

# ── 2. skills.sh (Vercel Labs) ──
echo "┌─ 2. skills.sh"
echo "│  Already discoverable! Users install with:"
echo "│  npx skills add wells1137/meowload-downloader"
echo "└─"
echo ""

# ── 3. agentskill.sh ──
echo "┌─ 3. agentskill.sh"
echo "│  Submit at: https://agentskill.sh/submit"
echo "│  Paste: $REPO_URL"
echo "└─"
echo ""

# ── 4. Sundial Hub ──
echo "┌─ 4. Sundial Hub (sundialhub.com)"
echo "│  Run these commands:"
echo "│    npx sundial-hub auth login"
echo "│    npx sundial-hub push ."
echo "│  Or submit at: https://sundialhub.com"
echo "└─"
echo ""

# ── 5. ClawHub / OpenClaw ──
echo "┌─ 5. ClawHub (clawhub.ai)"
echo "│  Sign up at: https://clawhub.ai"
echo "│  Then run:"
echo "│    npm i -g clawdhub"
echo "│    clawdhub login"
echo "│    clawdhub publish $SKILL_DIR --slug meowload-downloader --name 'MeowLoad Downloader' --version 1.0.0"
echo "└─"
echo ""

# ── 6. Playbooks.com ──
echo "┌─ 6. Playbooks.com"
echo "│  Already discoverable via GitHub!"
echo "│  Users install with:"
echo "│    npx playbooks add skill wells1137/meowload-downloader"
echo "└─"
echo ""

# ── 7. localskills.sh ──
echo "┌─ 7. localskills.sh"
echo "│  Run these commands:"
echo "│    npm i -g @localskills/cli"
echo "│    localskills login"
echo "│    localskills publish $SKILL_DIR --team wells1137 --name meowload-downloader --visibility public"
echo "└─"
echo ""

# ── 8. AgentSkillsRepo.com ──
echo "┌─ 8. AgentSkillsRepo.com"
echo "│  Auto-indexed from GitHub."
echo "│  Check listing at: https://agentskillsrepo.com"
echo "└─"
echo ""

echo "============================================"
echo "  Summary: Install commands for users"
echo "============================================"
echo ""
echo "  Cursor:       (install from Marketplace after approval)"
echo "  skills.sh:    npx skills add wells1137/meowload-downloader"
echo "  Sundial:      npx sundial-hub add meowload-downloader"
echo "  Playbooks:    npx playbooks add skill wells1137/meowload-downloader"
echo "  localskills:  localskills install wells1137/meowload-downloader"
echo ""
