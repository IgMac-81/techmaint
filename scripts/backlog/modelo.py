"""Monta o corpo em Markdown de cada issue a partir de campos estruturados.

Todo mundo do grupo lê a issue no mesmo formato: o que entregar, por que,
passo a passo, exemplo de código, como testar e o que estudar antes.
"""

from dataclasses import dataclass, field


@dataclass
class Tarefa:
    titulo: str
    milestone: str
    labels: list[str]
    estimativa: str
    objetivo: str
    porque: str
    passos: list[str]
    aceite: list[str]
    testar: list[str] = field(default_factory=list)
    exemplo: str = ""
    estudar: list[str] = field(default_factory=list)
    arquivos: list[str] = field(default_factory=list)
    depende_de: list[str] = field(default_factory=list)
    extra: str = ""

    def corpo(self) -> str:
        p = []
        p.append("## 🎯 O que você vai entregar\n\n" + self.objetivo)
        p.append("## 🧠 Por que isso importa\n\n" + self.porque)

        if self.arquivos:
            p.append(
                "## 📁 Arquivos que você vai mexer\n\n"
                + "\n".join(f"- `{a}`" for a in self.arquivos)
            )

        if self.depende_de:
            p.append(
                "## ⛔ Antes de começar, estas tarefas precisam estar prontas\n\n"
                + "\n".join(f"- {d}" for d in self.depende_de)
            )

        p.append(
            "## 📋 Passo a passo\n\n"
            + "\n".join(f"{i}. {passo}" for i, passo in enumerate(self.passos, 1))
        )

        if self.exemplo:
            p.append("## 💻 Exemplo para se guiar\n\n" + self.exemplo.strip())

        p.append(
            "## ✅ Critérios de aceite (o revisor vai conferir isto)\n\n"
            + "\n".join(f"- [ ] {a}" for a in self.aceite)
        )

        if self.testar:
            p.append(
                "## 🧪 Como testar antes de abrir o Pull Request\n\n"
                + "\n".join(f"{i}. {t}" for i, t in enumerate(self.testar, 1))
            )

        if self.estudar:
            p.append(
                "## 📚 Leia antes (15 a 30 minutos, vale a pena)\n\n"
                + "\n".join(f"- {e}" for e in self.estudar)
            )

        if self.extra:
            p.append("## ⭐ Quer ir além? (opcional, não bloqueia a entrega)\n\n" + self.extra)

        p.append(f"## ⏱ Estimativa\n\n{self.estimativa}")

        p.append(
            "## 🆘 Se travar\n\n"
            "Travou por mais de **40 minutos**? Pare e peça ajuda no grupo — isso não é "
            "fracasso, é o combinado do time. Escreva: (1) o que você tentou, (2) a "
            "mensagem de erro **inteira**, (3) o link do seu branch. Marque o líder técnico "
            "(@Buehno) na própria issue."
        )

        return "\n\n".join(p)

    def dict(self) -> dict:
        return {
            "titulo": self.titulo,
            "corpo": self.corpo(),
            "labels": self.labels,
            "milestone": self.milestone,
        }


M1 = "Entrega 1 — Grupo, papéis e delimitação"
M2 = "Entrega 2 — Arquitetura e protótipo que roda"
M3 = "Sprint 3 — Módulos do núcleo"
M4 = "Entrega 3 — Versão funcional ponta a ponta"
M5 = "Apresentação final"

RONALDO = "dono: ronaldo"
EQUIPE = "dono: equipe"
INICIANTE = "nível: iniciante"
INTERMEDIARIO = "nível: intermediário"
AVANCADO = "nível: avançado"
DESAFIO = "desafio ⭐"
BLOQUEIA = "bloqueia outros"
