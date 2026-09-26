"""
database.py
-----------
Tudo que fala com o banco de dados (SQLite) mora aqui.

Por que separar em um arquivo só?
- app.py cuida das telas (rotas)
- database.py cuida dos dados (SQL)
Assim, quando você criar uma nova entidade, copia este arquivo e troca o SQL.

SQLite é um banco de dados que vive em um arquivo unico (techmaint.db).
Nao precisa instalar servidor nenhum: ja vem junto com o Python.
"""

import sqlite3

# Nome do arquivo do banco. Ele e criado sozinho na primeira execucao.
NOME_DO_BANCO = "techmaint.db"

DEPARTAMENTOS = [
    (1, "DIRETORIA"),
    (2, "ADMINISTRATIVO"),
    (3, "RECURSOS HUMANOS (RH)"),
    (4, "FINANCEIRO"),
    (5, "CONTABILIDADE"),
    (6, "COMPRAS / SUPRIMENTOS"),
    (7, "JURÍDICO"),
    (8, "MARKETING E COMUNICAÇÃO"),
    (9, "COMERCIAL / VENDAS"),
    (10, "ATENDIMENTO AO CLIENTE / SUPORTE"),
    (11, "PESQUISA & DESENVOLVIMENTO (P&D)"),
    (12, "PRODUÇÃO / OPERAÇÕES"),
    (13, "LOGÍSTICA"),
    (14, "FROTA"),
    (15, "INFRAESTRUTURA / PREDIAL"),
    (16, "FERRAMENTARIA"),
    (17, "TECNOLOGIA DA INFORMAÇÃO (TI)"),
    (18, "AUTOMAÇÃO INDUSTRIAL"),
    (19, "UTILIDADES INDUSTRIAIS"),
    (20, "METROLOGIA"),
    (21, "QUALIDADE"),
    (22, "SEGURANÇA PATRIMONIAL"),
    (23, "MEIO AMBIENTE / SUSTENTABILIDADE"),
    (24, "SERVIÇOS E BENFEITORIAS"),
    (25, "MÓVEIS E UTENSÍLIOS"),
    (26, "SEGURANÇA DO TRABALHO"),
]


def conectar():
    """Abre uma conexao com o banco e devolve ela.

    O `row_factory = sqlite3.Row` faz cada linha do resultado virar algo
    parecido com um dicionario. Sem ele, voce acessaria por posicao
    (`linha[0]`, `linha[1]`). Com ele, acessa por nome (`linha["nome"]`),
    que e muito mais facil de ler no HTML.
    """
    conexao = sqlite3.connect(NOME_DO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    """Cria a tabela caso ela ainda nao exista.

    Roda toda vez que o app sobe. O `IF NOT EXISTS` garante que nada
    seja apagado se a tabela ja estiver la.
    """
    conexao = conectar()
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS Grupos (
            IdGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
            Grupo   VARCHAR(100) NOT NULL
        )
        """
    )
    conexao.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_grupos_nome
        ON Grupos (Grupo)
        """
    )
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS SubGrupos (
            IdSubGrupo INTEGER PRIMARY KEY AUTOINCREMENT,
            Subgrupo   VARCHAR(200) NOT NULL,
            IdGrupo    INTEGER NOT NULL,
            FOREIGN KEY (IdGrupo) REFERENCES Grupos (IdGrupo)
        )
        """
    )
    conexao.execute("DROP INDEX IF EXISTS idx_subgrupos_nome_grupo")
    conexao.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_subgrupos_nome
        ON SubGrupos (Subgrupo)
        """
    )
    colunas_existentes = [
        coluna[1]
        for coluna in conexao.execute("PRAGMA table_info(equipamentos)")
    ]
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS equipamentos (
            IdEquipamento INTEGER PRIMARY KEY AUTOINCREMENT,
            Codigo        VARCHAR(50) NOT NULL,
            Descricao     VARCHAR(200) NOT NULL,
            IdGrupo       INTEGER NOT NULL,
            Grupo         VARCHAR(100) NOT NULL,
            IdSubGrupo    INTEGER NOT NULL,
            Subgrupo      VARCHAR(200) NOT NULL,
            IdDepartamento INTEGER,
            Departamento   VARCHAR(100),
            FOREIGN KEY (IdGrupo) REFERENCES grupos (IdGrupo),
            FOREIGN KEY (IdSubGrupo) REFERENCES subgrupos (IdSubGrupo)
        )
        """
    )
    if colunas_existentes and "IdDepartamento" not in colunas_existentes:
        conexao.execute(
            """
            ALTER TABLE equipamentos
            ADD COLUMN IdDepartamento INTEGER
            """
        )
    if colunas_existentes and "Departamento" not in colunas_existentes:
        conexao.execute(
            """
            ALTER TABLE equipamentos
            ADD COLUMN Departamento VARCHAR(100)
            """
        )
    informacoes_colunas = {
        coluna[1]: coluna
        for coluna in conexao.execute("PRAGMA table_info(equipamentos)")
    }
    if (
        informacoes_colunas["IdDepartamento"][3]
        or informacoes_colunas["Departamento"][3]
    ):
        conexao.execute("PRAGMA foreign_keys = OFF")
        conexao.execute("DROP TABLE IF EXISTS equipamentos_novo")
        conexao.execute(
            """
            CREATE TABLE equipamentos_novo (
                IdEquipamento INTEGER PRIMARY KEY AUTOINCREMENT,
                Codigo        VARCHAR(50) NOT NULL,
                Descricao     VARCHAR(200) NOT NULL,
                IdGrupo       INTEGER NOT NULL,
                Grupo         VARCHAR(100) NOT NULL,
                IdSubGrupo    INTEGER NOT NULL,
                Subgrupo      VARCHAR(200) NOT NULL,
                IdDepartamento INTEGER,
                Departamento   VARCHAR(100),
                FOREIGN KEY (IdGrupo) REFERENCES grupos (IdGrupo),
                FOREIGN KEY (IdSubGrupo) REFERENCES subgrupos (IdSubGrupo)
            )
            """
        )
        conexao.execute(
            """
            INSERT INTO equipamentos_novo (
                IdEquipamento, Codigo, Descricao, IdGrupo, Grupo,
                IdSubGrupo, Subgrupo, IdDepartamento, Departamento
            )
            SELECT
                IdEquipamento, Codigo, Descricao, IdGrupo, Grupo,
                IdSubGrupo, Subgrupo, NULL, NULL
            FROM equipamentos
            """
        )
        conexao.execute("DROP TABLE equipamentos")
        conexao.execute("ALTER TABLE equipamentos_novo RENAME TO equipamentos")
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS Departamentos (
            IdDepartamento INTEGER PRIMARY KEY AUTOINCREMENT,
            NomeDepartamento VARCHAR(100) NOT NULL,
            Responsavel VARCHAR(100)
        )
        """
    )
    conexao.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_departamentos_nome
        ON Departamentos (NomeDepartamento)
        """
    )
    for id_departamento, nome_departamento in DEPARTAMENTOS:
        conexao.execute(
            """
            INSERT INTO Departamentos (IdDepartamento, NomeDepartamento)
            VALUES (?, ?)
            ON CONFLICT(IdDepartamento) DO UPDATE SET
                NomeDepartamento = excluded.NomeDepartamento
            """,
            (id_departamento, nome_departamento),
        )
    conexao.commit()
    conexao.close()


def listar_grupos(busca=""):
    """READ: devolve os grupos disponiveis para os formularios."""
    conexao = conectar()
    if busca:
        grupos = conexao.execute(
            """
            SELECT IdGrupo, Grupo FROM Grupos
            WHERE Grupo LIKE ?
            ORDER BY IdGrupo ASC
            """,
            (f"%{busca}%",),
        ).fetchall()
    else:
        grupos = conexao.execute(
            "SELECT IdGrupo, Grupo FROM Grupos ORDER BY IdGrupo ASC"
        ).fetchall()
    conexao.close()
    return grupos


def listar_subgrupos(busca=""):
    """READ: devolve subgrupos com o grupo ao qual pertencem."""
    conexao = conectar()
    if busca:
        subgrupos = conexao.execute(
            """
            SELECT IdSubGrupo, Subgrupo, IdGrupo
            FROM SubGrupos
            WHERE Subgrupo LIKE ?
            ORDER BY IdSubGrupo ASC
            """,
            (f"%{busca}%",),
        ).fetchall()
    else:
        subgrupos = conexao.execute(
            """
            SELECT IdSubGrupo, Subgrupo, IdGrupo
            FROM SubGrupos
            ORDER BY IdSubGrupo ASC
            """
        ).fetchall()
    conexao.close()
    return subgrupos


def criar_subgrupo(nome_subgrupo, id_grupo):
    """CREATE: insere um subgrupo dentro de um grupo."""
    conexao = conectar()
    try:
        conexao.execute(
            "INSERT INTO SubGrupos (Subgrupo, IdGrupo) VALUES (?, ?)",
            (nome_subgrupo, id_grupo),
        )
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def atualizar_subgrupo(id_subgrupo, nome_subgrupo, id_grupo):
    """UPDATE: altera o nome e o grupo de um subgrupo."""
    conexao = conectar()
    try:
        conexao.execute(
            """
            UPDATE SubGrupos
            SET Subgrupo = ?, IdGrupo = ?
            WHERE IdSubGrupo = ?
            """,
            (nome_subgrupo, id_grupo, id_subgrupo),
        )
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def apagar_subgrupo(id_subgrupo):
    """DELETE: remove um subgrupo sem equipamentos vinculados."""
    conexao = conectar()
    try:
        dependencias = conexao.execute(
            "SELECT COUNT(*) FROM equipamentos WHERE IdSubGrupo = ?",
            (id_subgrupo,),
        ).fetchone()[0]
        if dependencias:
            raise ValueError(
                "O subgrupo possui equipamentos vinculados."
            )
        conexao.execute(
            "DELETE FROM SubGrupos WHERE IdSubGrupo = ?", (id_subgrupo,)
        )
        conexao.commit()
    finally:
        conexao.close()


def listar_departamentos(busca=""):
    """READ: devolve os departamentos disponiveis para os formularios."""
    conexao = conectar()
    if busca:
        departamentos = conexao.execute(
            """
            SELECT IdDepartamento, NomeDepartamento, Responsavel
            FROM Departamentos
            WHERE NomeDepartamento LIKE ? OR Responsavel LIKE ?
            ORDER BY IdDepartamento ASC
            """,
            (f"%{busca}%", f"%{busca}%"),
        ).fetchall()
    else:
        departamentos = conexao.execute(
            """
            SELECT IdDepartamento, NomeDepartamento, Responsavel
            FROM Departamentos
            ORDER BY IdDepartamento ASC
            """
        ).fetchall()
    conexao.close()
    return departamentos


def criar_departamento(nome_departamento, responsavel):
    """CREATE: insere um departamento."""
    conexao = conectar()
    try:
        conexao.execute(
            """
            INSERT INTO Departamentos (NomeDepartamento, Responsavel)
            VALUES (?, ?)
            """,
            (nome_departamento, responsavel),
        )
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def atualizar_departamento(id_departamento, nome_departamento, responsavel):
    """UPDATE: altera um departamento."""
    conexao = conectar()
    try:
        conexao.execute(
            """
            UPDATE Departamentos
            SET NomeDepartamento = ?, Responsavel = ?
            WHERE IdDepartamento = ?
            """,
            (nome_departamento, responsavel, id_departamento),
        )
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def apagar_departamento(id_departamento):
    """DELETE: remove um departamento sem equipamentos vinculados."""
    conexao = conectar()
    try:
        dependencias = conexao.execute(
            "SELECT COUNT(*) FROM equipamentos WHERE IdDepartamento = ?",
            (id_departamento,),
        ).fetchone()[0]
        if dependencias:
            raise ValueError(
                "O departamento possui equipamentos vinculados."
            )
        conexao.execute(
            "DELETE FROM Departamentos WHERE IdDepartamento = ?",
            (id_departamento,),
        )
        conexao.commit()
    finally:
        conexao.close()


def buscar_grupo(id_grupo):
    """READ: devolve um grupo pelo identificador."""
    conexao = conectar()
    grupo = conexao.execute(
        "SELECT IdGrupo, Grupo FROM Grupos WHERE IdGrupo = ?", (id_grupo,)
    ).fetchone()
    conexao.close()
    return grupo


def criar_grupo(nome_grupo):
    """CREATE: insere um grupo e informa se ele ja existia."""
    conexao = conectar()
    try:
        conexao.execute("INSERT INTO Grupos (Grupo) VALUES (?)", (nome_grupo,))
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def atualizar_grupo(id_grupo, nome_grupo):
    """UPDATE: altera o nome de um grupo."""
    conexao = conectar()
    try:
        conexao.execute(
            "UPDATE Grupos SET Grupo = ? WHERE IdGrupo = ?",
            (nome_grupo, id_grupo),
        )
        conexao.commit()
        return True
    except sqlite3.IntegrityError:
        conexao.rollback()
        return False
    finally:
        conexao.close()


def apagar_grupo(id_grupo):
    """DELETE: remove um grupo que nao possua dependencias."""
    conexao = conectar()
    try:
        dependencias = conexao.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM SubGrupos WHERE IdGrupo = ?)
                + (SELECT COUNT(*) FROM equipamentos WHERE IdGrupo = ?)
            """,
            (id_grupo, id_grupo),
        ).fetchone()[0]
        if dependencias:
            raise ValueError("O grupo possui subgrupos ou equipamentos vinculados.")
        conexao.execute("DELETE FROM Grupos WHERE IdGrupo = ?", (id_grupo,))
        conexao.commit()
    finally:
        conexao.close()


def buscar_subgrupo(id_subgrupo):
    """READ: devolve um subgrupo pelo identificador."""
    conexao = conectar()
    subgrupo = conexao.execute(
        "SELECT IdSubGrupo, Subgrupo, IdGrupo FROM SubGrupos WHERE IdSubGrupo = ?",
        (id_subgrupo,),
    ).fetchone()
    conexao.close()
    return subgrupo


def buscar_departamento(id_departamento):
    """READ: devolve um departamento pelo identificador."""
    conexao = conectar()
    departamento = conexao.execute(
        """
        SELECT IdDepartamento, NomeDepartamento, Responsavel
        FROM Departamentos
        WHERE IdDepartamento = ?
        """,
        (id_departamento,),
    ).fetchone()
    conexao.close()
    return departamento


# ---------------------------------------------------------------------------
# As quatro operacoes do CRUD
#
#   C = Create  (criar)   -> criar_equipamento()
#   R = Read    (ler)     -> listar_equipamentos() e buscar_equipamento()
#   U = Update  (alterar) -> atualizar_equipamento()
#   D = Delete  (apagar)  -> apagar_equipamento()
#
# Repare que TODA consulta usa `?` no lugar dos valores. Isso se chama
# "query parametrizada" e protege contra SQL Injection. Nunca monte SQL
# com f-string ou com `+`.
# ---------------------------------------------------------------------------


def listar_equipamentos(busca=""):
    """READ: devolve equipamentos filtrados por codigo ou descricao."""
    conexao = conectar()
    if busca:
        # O `%` do LIKE significa "qualquer coisa antes ou depois".
        linhas = conexao.execute(
            """
            SELECT * FROM equipamentos
            WHERE Codigo LIKE ? OR Descricao LIKE ?
            ORDER BY IdEquipamento ASC
            """,
            (f"%{busca}%", f"%{busca}%"),
        ).fetchall()
    else:
        linhas = conexao.execute(
            "SELECT * FROM equipamentos ORDER BY IdEquipamento ASC"
        ).fetchall()
    conexao.close()
    return linhas


def buscar_equipamento(id_do_equipamento):
    """READ: devolve UM equipamento pelo id (ou None se nao existir).

    Usado na tela de edicao, para preencher o formulario.
    """
    conexao = conectar()
    linha = conexao.execute(
        "SELECT * FROM equipamentos WHERE IdEquipamento = ?",
        (id_do_equipamento,),
    ).fetchone()
    conexao.close()
    return linha


def criar_equipamento(
    codigo,
    descricao,
    id_departamento,
    departamento,
    id_grupo,
    grupo,
    id_subgrupo,
    subgrupo,
):
    """CREATE: insere um novo equipamento."""
    conexao = conectar()
    conexao.execute(
        """
        INSERT INTO equipamentos
            (Codigo, Descricao, IdDepartamento, Departamento, IdGrupo, Grupo,
             IdSubGrupo, Subgrupo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            codigo,
            descricao,
            id_departamento,
            departamento,
            id_grupo,
            grupo,
            id_subgrupo,
            subgrupo,
        ),
    )
    # `commit` = confirma a gravacao. Sem ele, nada e salvo de verdade.
    conexao.commit()
    conexao.close()


def atualizar_equipamento(
    id_do_equipamento,
    codigo,
    descricao,
    id_departamento,
    departamento,
    id_grupo,
    grupo,
    id_subgrupo,
    subgrupo,
):
    """UPDATE: altera um equipamento existente.

    Cuidado: UPDATE sem WHERE altera a tabela inteira. O WHERE e obrigatorio.
    """
    conexao = conectar()
    conexao.execute(
        """
        UPDATE equipamentos
        SET Codigo = ?, Descricao = ?, IdDepartamento = ?, Departamento = ?,
            IdGrupo = ?, Grupo = ?, IdSubGrupo = ?, Subgrupo = ?
        WHERE IdEquipamento = ?
        """,
        (
            codigo,
            descricao,
            id_departamento,
            departamento,
            id_grupo,
            grupo,
            id_subgrupo,
            subgrupo,
            id_do_equipamento,
        ),
    )
    conexao.commit()
    conexao.close()


def apagar_equipamento(id_do_equipamento):
    """DELETE: remove um equipamento pelo id."""
    conexao = conectar()
    conexao.execute(
        "DELETE FROM equipamentos WHERE IdEquipamento = ?", (id_do_equipamento,)
    )
    conexao.commit()
    conexao.close()
