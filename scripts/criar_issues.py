#!/usr/bin/env python3
"""Cria labels, milestones e issues no GitHub e adiciona tudo ao Project.

Pré-requisitos:
    1. GitHub CLI instalado:  https://cli.github.com
    2. Autenticado com escopo de projeto:
           gh auth login
           gh auth refresh -s project,read:project,repo

Uso:
    python scripts/criar_issues.py --dry-run     # mostra o que seria criado
    python scripts/criar_issues.py               # cria de verdade

As issues são criadas SEM responsável (o time ainda não tem os usuários do
GitHub). Depois é só abrir o quadro e atribuir.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.backlog import LABELS, MILESTONES, TAREFAS  # noqa: E402

REPO = "TechMind-tech/techmaint"
ORG = "TechMind-tech"
PROJECT_NUMERO = 1


def rodar(args: list[str], entrada: str | None = None) -> str:
    resultado = subprocess.run(
        args, input=entrada, capture_output=True, text=True, encoding="utf-8"
    )
    if resultado.returncode != 0:
        erro = (resultado.stderr or "").strip()
        # "already exists" não é falha para nós — seguimos em frente.
        if "already exists" in erro.lower() or "already_exists" in erro.lower():
            return ""
        raise RuntimeError(f"Falhou: {' '.join(args[:4])}...\n{erro}")
    return resultado.stdout.strip()


def criar_labels(seco: bool) -> None:
    print(f"\n== Labels ({len(LABELS)}) ==")
    for nome, cor, descricao in LABELS:
        print(f"  • {nome}")
        if seco:
            continue
        rodar(
            [
                "gh", "label", "create", nome,
                "--repo", REPO,
                "--color", cor,
                "--description", descricao,
                "--force",
            ]
        )


def criar_milestones(seco: bool) -> dict[str, int]:
    print(f"\n== Milestones ({len(MILESTONES)}) ==")
    numeros: dict[str, int] = {}
    for m in MILESTONES:
        print(f"  • {m['titulo']}  (vence {m['vence_em']})")
        if seco:
            continue
        corpo = json.dumps(
            {
                "title": m["titulo"],
                "description": m["descricao"],
                "due_on": f"{m['vence_em']}T23:59:59Z",
                "state": "open",
            }
        )
        saida = rodar(
            ["gh", "api", f"repos/{REPO}/milestones", "--method", "POST", "--input", "-"],
            entrada=corpo,
        )
        if saida:
            numeros[m["titulo"]] = json.loads(saida)["number"]
    return numeros


def criar_issues(seco: bool) -> list[str]:
    print(f"\n== Issues ({len(TAREFAS)}) ==")
    urls: list[str] = []
    for tarefa in TAREFAS:
        dados = tarefa.dict()
        print(f"  • [{dados['milestone'].split('—')[0].strip()}] {dados['titulo']}")
        if seco:
            continue
        args = [
            "gh", "issue", "create",
            "--repo", REPO,
            "--title", dados["titulo"],
            "--body", dados["corpo"],
            "--milestone", dados["milestone"],
        ]
        for label in dados["labels"]:
            args += ["--label", label]
        url = rodar(args)
        if url:
            urls.append(url.splitlines()[-1])
    return urls


def adicionar_ao_projeto(urls: list[str], seco: bool) -> None:
    print(f"\n== Adicionando {len(urls)} issues ao Project #{PROJECT_NUMERO} ==")
    if seco:
        return
    for url in urls:
        rodar(
            ["gh", "project", "item-add", str(PROJECT_NUMERO), "--owner", ORG, "--url", url]
        )
        print(f"  ✓ {url}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="só mostra, não cria nada")
    parser.add_argument("--pular-labels", action="store_true")
    parser.add_argument("--pular-milestones", action="store_true")
    args = parser.parse_args()

    if not args.pular_labels:
        criar_labels(args.dry_run)
    if not args.pular_milestones:
        criar_milestones(args.dry_run)

    urls = criar_issues(args.dry_run)
    adicionar_ao_projeto(urls, args.dry_run)

    print(
        f"\nPronto. {len(TAREFAS)} tarefas"
        + (" (simulação, nada foi criado)." if args.dry_run else f" criadas em {REPO}.")
    )


if __name__ == "__main__":
    main()
