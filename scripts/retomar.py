#!/usr/bin/env python3
"""Retoma o bootstrap: cria só as issues que faltam e liga tudo ao Project."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from scripts.backlog import MILESTONES, TAREFAS  # noqa: E402

ORG, REPO, PROJETO = "TechMind-tech", "techmaint", 1
TOKEN = os.environ.get("GH_PAT", "").strip()
LIMITE = float(os.environ.get("LIMITE_SEGUNDOS", "140"))
INICIO = time.time()


def api(caminho, metodo="GET", dados=None):
    url = caminho if caminho.startswith("http") else f"https://api.github.com/{caminho.lstrip('/')}"
    corpo = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(url, data=corpo, method=metodo)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "techmaint")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            t = r.read().decode()
            return json.loads(t) if t else {}
    except urllib.error.HTTPError as e:
        return {"_erro": e.code, "_detalhe": e.read().decode()}


def graphql(query, variaveis):
    return api("https://api.github.com/graphql", "POST", {"query": query, "variables": variaveis})


# --- o que já existe
existentes: dict[str, str] = {}
pagina = 1
while True:
    lote = api(f"/repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={pagina}")
    if not isinstance(lote, list) or not lote:
        break
    for i in lote:
        if "pull_request" not in i:
            existentes[i["title"]] = i["node_id"]
    pagina += 1

milestones = {m["title"]: m["number"] for m in api(f"/repos/{ORG}/{REPO}/milestones?state=all&per_page=100")}
print(f"já existem {len(existentes)} issues; {len(MILESTONES)} milestones")

# --- cria as que faltam
faltando = [t for t in TAREFAS if t.titulo not in existentes]
print(f"faltam {len(faltando)}")
for t in faltando:
    if time.time() - INICIO > LIMITE:
        print("PARCIAL: tempo esgotado, rode de novo para continuar.")
        break
    d = t.dict()
    payload = {"title": d["titulo"], "body": d["corpo"], "labels": d["labels"]}
    if d["milestone"] in milestones:
        payload["milestone"] = milestones[d["milestone"]]
    r = api(f"/repos/{ORG}/{REPO}/issues", "POST", payload)
    if "_erro" in r:
        print(f"  FALHOU {d['titulo'][:45]}: {r['_detalhe'][:120]}")
        time.sleep(3)
    else:
        existentes[d["titulo"]] = r["node_id"]
        print(f"  #{r['number']} {d['titulo'][:58]}")
    time.sleep(1.0)

# --- Project
if len(existentes) >= len(TAREFAS):
    c = graphql("query($o:String!,$n:Int!){organization(login:$o){projectV2(number:$n){id}}}", {"o": ORG, "n": PROJETO})
    pid = ((c.get("data") or {}).get("organization") or {}).get("projectV2", {})
    pid = pid.get("id") if pid else None
    if not pid:
        print("PROJECT: sem acesso —", json.dumps(c)[:200])
    else:
        ja = set()
        cur = None
        while True:
            q = ("query($p:ID!,$a:String){node(id:$p){... on ProjectV2{items(first:100,after:$a)"
                 "{pageInfo{hasNextPage endCursor}nodes{content{... on Issue{id}}}}}}}")
            r = graphql(q, {"p": pid, "a": cur})
            it = (((r.get("data") or {}).get("node") or {}).get("items") or {})
            for n in it.get("nodes", []):
                if n.get("content", {}).get("id"):
                    ja.add(n["content"]["id"])
            if not it.get("pageInfo", {}).get("hasNextPage"):
                break
            cur = it["pageInfo"]["endCursor"]
        pendentes = [n for n in existentes.values() if n not in ja]
        print(f"PROJECT: {len(ja)} já no quadro, adicionando {len(pendentes)}")
        add = 0
        for n in pendentes:
            if time.time() - INICIO > LIMITE + 25:
                print("PROJECT PARCIAL: rode de novo.")
                break
            r = graphql("mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}",
                        {"p": pid, "c": n})
            if (r.get("data") or {}).get("addProjectV2ItemById"):
                add += 1
            time.sleep(0.25)
        print(f"PROJECT: +{add}")

print(f"TOTAL issues: {len(existentes)}/{len(TAREFAS)}")
