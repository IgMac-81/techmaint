#!/usr/bin/env python3
"""Cria o repositório, sobe o código, cria labels/milestones/issues e liga ao Project.

Usa só a biblioteca padrão do Python + git. Não precisa do gh CLI.

    export GH_PAT=ghp_xxxxx
    python3 scripts/subir_github.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from scripts.backlog import LABELS, MILESTONES, TAREFAS  # noqa: E402

ORG = "TechMind-tech"
REPO = "techmaint"
PROJETO = 1
TOKEN = os.environ.get("GH_PAT", "").strip()

if not TOKEN:
    sys.exit("ERRO: defina GH_PAT com o seu token do GitHub.")


def api(caminho: str, metodo: str = "GET", dados: dict | None = None, base: str = "https://api.github.com"):
    url = caminho if caminho.startswith("http") else f"{base}/{caminho.lstrip('/')}"
    corpo = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(url, data=corpo, method=metodo)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "techmaint-bootstrap")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            texto = r.read().decode()
            return json.loads(texto) if texto else {}
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode()
        return {"_erro": e.code, "_detalhe": detalhe}


def graphql(query: str, variaveis: dict):
    return api("https://api.github.com/graphql", "POST", {"query": query, "variables": variaveis})


def sh(*args: str, cwd: Path = RAIZ, secreto: bool = False):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        msg = (r.stderr or r.stdout).strip()
        if secreto:
            msg = msg.replace(TOKEN, "***")
        print(f"    aviso git: {msg[:300]}")
    return r.returncode == 0


# ---------------------------------------------------------------- 1. repositório
print(f"==> 1/6 Repositório {ORG}/{REPO}")
existente = api(f"/repos/{ORG}/{REPO}")
if "_erro" not in existente:
    print("    já existe, seguindo.")
else:
    criado = api(
        f"/orgs/{ORG}/repos",
        "POST",
        {
            "name": REPO,
            "description": "Sistema de Manutenção Predial e de Máquinas — Flask + PWA (UniAnchieta 2026/2)",
            "private": True,
            "has_wiki": False,
            "has_projects": True,
        },
    )
    if "_erro" in criado:
        sys.exit(f"    FALHOU ao criar o repositório: {criado['_detalhe'][:400]}")
    print("    criado.")

# ---------------------------------------------------------------- 2. push
print("==> 2/6 Subindo o código")
if not (RAIZ / ".git").exists():
    sh("git", "init", "-q")
sh("git", "config", "user.name", "Ronaldo Bueno")
sh("git", "config", "user.email", "ronaldo.bueno@iagentics.com.br")
sh("git", "config", "commit.gpgsign", "false")
sh("git", "add", "-A")
sh("git", "commit", "-q", "-m", "feat: estrutura inicial do TechMaint (Flask + PWA + docs + backlog)")
sh("git", "branch", "-M", "main")
sh("git", "remote", "remove", "origin")
sh("git", "remote", "add", "origin", f"https://x-access-token:{TOKEN}@github.com/{ORG}/{REPO}.git", secreto=True)
if sh("git", "push", "-u", "origin", "main", secreto=True):
    print("    código no ar.")
sh("git", "remote", "set-url", "origin", f"https://github.com/{ORG}/{REPO}.git")

# ---------------------------------------------------------------- 3. labels
print(f"==> 3/6 Labels ({len(LABELS)})")
for nome, cor, descricao in LABELS:
    r = api(f"/repos/{ORG}/{REPO}/labels", "POST", {"name": nome, "color": cor, "description": descricao})
    if "_erro" in r and r["_erro"] != 422:
        print(f"    falhou {nome}: {r['_detalhe'][:120]}")
print("    ok.")

# ---------------------------------------------------------------- 4. milestones
print(f"==> 4/6 Milestones ({len(MILESTONES)})")
numeros: dict[str, int] = {}
atuais = api(f"/repos/{ORG}/{REPO}/milestones?state=all&per_page=100")
if isinstance(atuais, list):
    numeros = {m["title"]: m["number"] for m in atuais}
for m in MILESTONES:
    if m["titulo"] in numeros:
        continue
    r = api(
        f"/repos/{ORG}/{REPO}/milestones",
        "POST",
        {"title": m["titulo"], "description": m["descricao"], "due_on": f"{m['vence_em']}T23:59:59Z"},
    )
    if "_erro" in r:
        print(f"    falhou {m['titulo']}: {r['_detalhe'][:120]}")
    else:
        numeros[m["titulo"]] = r["number"]
print(f"    {len(numeros)} milestones.")

# ---------------------------------------------------------------- 5. issues
print(f"==> 5/6 Issues ({len(TAREFAS)}) — leva ~2 minutos")
node_ids: list[str] = []
criadas = 0
for i, tarefa in enumerate(TAREFAS, 1):
    d = tarefa.dict()
    payload = {"title": d["titulo"], "body": d["corpo"], "labels": d["labels"]}
    if d["milestone"] in numeros:
        payload["milestone"] = numeros[d["milestone"]]
    r = api(f"/repos/{ORG}/{REPO}/issues", "POST", payload)
    if "_erro" in r:
        print(f"    [{i}] FALHOU: {r['_detalhe'][:160]}")
    else:
        criadas += 1
        node_ids.append(r["node_id"])
        print(f"    [{i:02d}/{len(TAREFAS)}] #{r['number']} {d['titulo'][:60]}")
    time.sleep(1.2)  # respeita o limite de criação de conteúdo do GitHub
print(f"    {criadas} issues criadas.")

# ---------------------------------------------------------------- 6. project
print(f"==> 6/6 Ligando ao Project #{PROJETO}")
consulta = graphql(
    "query($org:String!,$n:Int!){organization(login:$org){projectV2(number:$n){id title}}}",
    {"org": ORG, "n": PROJETO},
)
projeto_id = (
    consulta.get("data", {}).get("organization", {}).get("projectV2", {}) or {}
).get("id")

if not projeto_id:
    print("    AVISO: não consegui acessar o Project.")
    print("    O token precisa do escopo 'project'. Detalhe:", json.dumps(consulta)[:300])
    print("    As issues já estão criadas — dá para adicioná-las pelo quadro depois.")
else:
    adicionadas = 0
    for node_id in node_ids:
        r = graphql(
            "mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}",
            {"p": projeto_id, "c": node_id},
        )
        if r.get("data", {}).get("addProjectV2ItemById"):
            adicionadas += 1
        time.sleep(0.4)
    print(f"    {adicionadas} de {len(node_ids)} issues no quadro.")

print("\nPronto.")
print(f"  Repositório: https://github.com/{ORG}/{REPO}")
print(f"  Quadro:      https://github.com/orgs/{ORG}/projects/{PROJETO}")
