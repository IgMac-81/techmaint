# Roadmap do TechMaint

Cronograma real, encaixado nas datas de entrega da disciplina. Hoje é **13/09/2026** — a
Entrega 1 é **amanhã**, então o Sprint 1 é curto e documental de propósito.

---

## Visão geral

| Sprint | Período | Entrega | Foco |
|---|---|---|---|
| **1** | até 14/09 | **Entrega 1** | Grupo, papéis, escopo, ambiente de todos rodando |
| **2** | 15/09 → 28/09 | **Entrega 2** | Arquitetura, banco, login e primeiros cadastros na tela |
| **3** | 29/09 → 12/10 | checkpoint interno | Estoque, notas fiscais e fluxo pedido → OS |
| **4** | 13/10 → 26/10 | **Entrega 3** | Relatórios, indicadores, PWA instalável, plano da apresentação |
| **5** | 27/10 → novembro | **Apresentação** | Congelamento, ensaios, slides, retrospectiva |

Capacidade considerada: **8 pessoas, ~6h/semana cada**, sendo 1 com experiência (Ronaldo) e 7
em formação. O roadmap assume que as tarefas de calouro levam **2 a 3 vezes** o tempo que
levariam para alguém experiente — e isso está embutido nas estimativas.

---

## Sprint 1 — até 14/09 · Entrega 1

**Entregável:** grupo, papéis e delimitação do sistema.

- Repositório criado, estruturado e com a `main` protegida
- Ambiente rodando na máquina dos 8 integrantes *(bloqueia todo o resto — faça hoje)*
- Escopo escrito: o que está dentro e o que está fora
- README com integrantes, papéis e combinados
- Quadro do Project organizado em 5 colunas

**Risco principal:** alguém não conseguir instalar o Python a tempo. Mitigação: a issue de
setup tem uma tabela de erros comuns, e quem terminar ajuda quem travou.

---

## Sprint 2 — 15/09 a 28/09 · Entrega 2

**Entregável:** arquitetura documentada e protótipo que já roda.

Ronaldo (crítico, bloqueia os outros — **fazer na primeira semana**):
- Arquitetura em camadas documentada
- Banco completo em SQLAlchemy + primeira migração
- Autenticação com hash de senha e CSRF
- Perfis e permissões
- CI no GitHub Actions

Equipe (só destrava depois do banco e do login):
- Tokens de design extraídos do Figma
- Layout base responsivo
- Tela de login e painel com os 4 cartões
- CRUD de Departamentos *(a tarefa que mais ensina — todo calouro deveria fazer uma dessas)*
- CRUD de Grupos e Subgrupos
- Busca, filtro e paginação em Equipamentos
- Primeiros testes com pytest
- Documento da Entrega 2

**Ordem importa:** modelagem do banco e login são pré-requisito de quase tudo. Ronaldo entrega
isso até **19/09** para a equipe ter 9 dias de trabalho desbloqueado.

---

## Sprint 3 — 29/09 a 12/10 · Checkpoint interno

**Entregável:** cadastros completos e o fluxo de manutenção funcionando.

- Peças, Fornecedores (com validação de CNPJ), Prestadores
- Nota fiscal com itens (formulário mestre-detalhe)
- Entrada de nota atualiza o estoque *(regra crítica — Ronaldo)*
- Estoque com alerta de mínimo e movimentação manual
- Pedido de manutenção: abrir, aprovar, rejeitar
- Conversão pedido → OS *(regra crítica 1:1 — Ronaldo)*
- OS: peças, horas, serviços, encerramento

**Este é o sprint mais pesado.** Se algo tiver que atrasar, que seja "Prestadores de Serviço" —
é o módulo menos essencial para a demonstração.

---

## Sprint 4 — 13/10 a 26/10 · Entrega 3

**Entregável:** versão funcional de ponta a ponta e plano da apresentação.

- Indicadores reais: tempo médio de atendimento, custo por máquina
- Gráficos gerados com Matplotlib (100% Python)
- Relatório com filtros + exportação Excel + exportação PDF
- **PWA instalável** no iPhone e no Android
- Deploy com HTTPS *(sem HTTPS o PWA não instala)*
- Checklist de responsividade em todas as telas
- Teste de ponta a ponta automatizado
- Manual do usuário
- Roteiro da apresentação com os 8 falando

---

## Sprint 5 — 27/10 a novembro · Apresentação

- Code freeze e tag `v1.0` *(só bug crítico entra depois disso)*
- Dois ensaios cronometrados
- Slides
- Checklist do dia
- Retrospectiva final

---

## Dentro do escopo

- Usuários, perfis e permissões (Administrador, Gestor, Técnico, Cliente)
- Cadastro de departamentos, grupos, subgrupos, equipamentos e peças
- Fornecedores, prestadores de serviço, notas fiscais e itens
- Estoque de peças com mínimo, alerta e histórico de movimentação
- Pedidos de manutenção e ordens de serviço com peças, serviços e apontamento de horas
- Dashboard com indicadores e gráficos
- Relatórios com filtros e exportação em Excel e PDF
- Aplicação web responsiva instalável como PWA no iPhone e no Android

## Fora do escopo (v1)

| Não vamos fazer | Por quê |
|---|---|
| Aplicativo nativo publicado na App Store / Play Store | Exige conta paga de desenvolvedor e revisão da loja; o PWA entrega o mesmo valor no prazo |
| Integração real com ERP | Não temos um ERP disponível; ficaria uma integração de mentira |
| Emissão fiscal de NF-e válida | Exige certificado digital e homologação na SEFAZ — outra disciplina inteira |
| Multiempresa | Dobra a complexidade do banco sem agregar à avaliação |
| Chat interno entre técnicos | Fora do problema que o sistema resolve |
| Notificações push | Depende de serviço externo; o alerta na tela já cumpre o requisito |
| Aplicativo offline com escrita e sincronização | Sincronizar dados offline é um problema difícil de verdade; o PWA faz cache de leitura, o que já demonstra o conceito |

---

## Riscos e planos

| Risco | Probabilidade | Plano |
|---|---|---|
| Alguém não consegue montar o ambiente | Alta | Issue de setup com tabela de erros; sessão de ajuda na primeira semana |
| Concentrar tudo na véspera da entrega | Alta | Quadro revisado toda semana; milestones com data no GitHub |
| Regra de estoque com bug silencioso | Média | Regras críticas ficam com o líder técnico + teste automatizado obrigatório |
| Internet falhar na apresentação | Média | Vídeo de plano B gravado + PWA instalado no celular |
| Sprint 3 estourar o prazo | Média | "Prestadores de Serviço" é o primeiro item a cortar |
