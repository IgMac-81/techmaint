#!/usr/bin/env bash
# Cria o repositório TechMind-tech/techmaint, sobe este código, cria labels,
# milestones e as 50 issues, e liga tudo ao Project #1 da organização.
#
# Rode UMA vez, de dentro da pasta do projeto:
#     bash scripts/bootstrap_github.sh
#
# Pré-requisitos:
#   1. GitHub CLI instalado ......... https://cli.github.com
#   2. Autenticado com os escopos certos:
#          gh auth login
#          gh auth refresh -s project,read:project,repo,admin:org
#   3. Você precisa ser owner/admin da organização TechMind-tech.

set -euo pipefail

ORG="TechMind-tech"
REPO="techmaint"
PROJETO=1

echo "==> Conferindo o gh CLI"
command -v gh >/dev/null || { echo "ERRO: instale o GitHub CLI: https://cli.github.com"; exit 1; }
gh auth status >/dev/null || { echo "ERRO: rode 'gh auth login' primeiro."; exit 1; }

if ! gh auth status 2>&1 | grep -q "project"; then
  echo "AVISO: o token parece não ter escopo de Project."
  echo "       Rode: gh auth refresh -s project,read:project,repo"
  read -r -p "       Continuar mesmo assim? [s/N] " resposta
  [[ "$resposta" =~ ^[sS]$ ]] || exit 1
fi

echo "==> Criando o repositório $ORG/$REPO"
if gh repo view "$ORG/$REPO" >/dev/null 2>&1; then
  echo "    já existe, seguindo."
else
  gh repo create "$ORG/$REPO" \
    --private \
    --description "Sistema de Manutenção Predial e de Máquinas — Flask + PWA (UniAnchieta 2026/2)" \
    --disable-wiki
fi

echo "==> Subindo o código"
git init -q 2>/dev/null || true
git add -A
git commit -q -m "feat: estrutura inicial do TechMaint (Flask + PWA + docs + backlog)" 2>/dev/null || \
  echo "    nada novo para commitar"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$ORG/$REPO.git"
git push -u origin main

echo "==> Criando labels, milestones e issues (pode levar 2 a 3 minutos)"
python3 scripts/criar_issues.py

echo "==> Protegendo a branch main"
gh api "repos/$ORG/$REPO/branches/main/protection" --method PUT --input - <<'JSON' || \
  echo "    AVISO: proteção de branch exige repositório público ou plano pago. Configure em Settings > Branches."
{
  "required_status_checks": { "strict": true, "contexts": ["Testes e lint"] },
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 1 },
  "restrictions": null
}
JSON

echo ""
echo "Pronto."
echo "  Repositório: https://github.com/$ORG/$REPO"
echo "  Quadro:      https://github.com/orgs/$ORG/projects/$PROJETO"
echo ""
echo "Próximos passos:"
echo "  1. Convide os 7 integrantes em Settings > Collaborators and teams (permissão write)."
echo "  2. No quadro, renomeie as colunas para: Backlog / A fazer / Em andamento / Em revisão / Concluído."
echo "  3. Mande o link de docs/00-guia-do-calouro.md no grupo — é a primeira leitura de todos."
