# Navegador de Rotas Urbanas - Estrutura de Dados

Trabalho Final de Estrutura de Dados (UNI-CET). Aplicativo em Python 3 para uma
cidade **fictícia** (Nova Aurora): cadastro de locais, busca por nome com
autocompletar, rotas com menos paradas, histórico, favoritos e análise de
alcance. As estruturas centrais são **implementadas pelo grupo** (sem
`append`, `pop`, `insert`, `deque`, `queue`, `heapq`, `set`, `dict`, `sorted`
ou `sort`).

## Como executar
```bash
git clone <URL-DO-REPOSITORIO>
cd navegador-rotas
python3 main.py                                   # menu em console
python3 -m unittest discover -s testes -t .       # testes automatizados
```
Requer Python 3.9+. O `matplotlib` (`pip install -r requirements.txt`) só será
necessário para o benchmark (Etapa 2).

## Benchmark de ordenação
```bash
python3 -m benchmark.benchmark                          # completo: 5 algoritmos x 1.000/10.000/50.000 x 3 cenários
python3 -m benchmark.benchmark --max-quadratico 10000   # pula O(n²) em 50.000 (rápido)
python3 -m benchmark.benchmark --so-grafico             # refaz tabela e gráfico a partir do CSV
```
Gera `benchmark/resultados/ordenacao.csv`, `tabela.md` (tempos e razão de crescimento
medida × teórica) e `ordenacao.png`. O CSV é gravado a cada medição e a execução pode ser
retomada. **Os arquivos de resultados incluídos foram medidos em outra máquina:** antes da
entrega, apague `benchmark/resultados/ordenacao.csv` e rode o benchmark completo no
computador do grupo (o O(n²) em 50.000 leva em torno de 15 a 25 minutos), para que a
análise do relatório use medições do grupo.

## Estrutura
```
main.py          só orquestra
dominio/         regras do tema (camada de aplicação)
tads/            estruturas de dados (TADs)
algoritmos/      ordenacao.py, busca.py          (Etapas 2 e 3)
benchmark/       benchmark.py                    (Etapa 2)
interface/       menu de console
dados/           dados fictícios de exemplo
testes/          test_*.py
```

## Status
| Etapa | Conteúdo | Situação |
|---|---|---|
| 1 | Cadastro, lista estática, listas simples/dupla, pilha, fila, BST, grafo (BFS/DFS), testes | **Pronta** |
| 2 | Bubble, Selection, Insertion, Quick, Merge + `benchmark.py` | **Pronta** |
| 3 | Busca sequencial/binária, tabela hash, Conjunto, demo de balanceamento da BST, ranking (IA/CD), estudo de caso | Pendente |
| Final | Funcionalidade complementar (feita: rota que evita um bairro), relatório PDF, defesa | Complementar pronta; relatório pendente |

## Mapeamento da ementa (parcial)
| Item | Módulo / função |
|---|---|
| 1.1 TADs, pré/pós | `tads/*` (docstrings; exceções em `tads/excecoes.py`); lógica em `dominio/` |
| 1.2 Matriz e referências | `tads/grafo.py` (matriz de adjacência); `No`, `NoDuplo`, `NoBST` |
| 1.3 Modularização | `dominio/`, `interface/`, `dados/`; sem estado global |
| 1.4 Vetor de registros | `dominio/cadastro.py` (`Cadastro`: incluir, listar, alterar, excluir) |
| 1.5 Lista estática | `tads/lista_estatica.py`; `dominio/favoritos.py` (capacidade 10) |
| 2.1/2.2 Lista encadeada | `tads/lista_encadeada.py` (trajeto da rota) |
| 2.3 Lista dupla | `tads/lista_dupla.py`; `dominio/historico.py` |
| 2.4 Pilha e fila | `tads/pilha.py` (voltar), `tads/fila.py` (solicitações); `dominio/navegacao.py` |
| 2.5 BST | `tads/arvore_bst.py` (`inserir`, `buscar`, `remover`, `em_ordem`, `pre_ordem`, `pos_ordem`, `autocompletar`) |
| 2.5 Grafo, BFS, DFS | `tads/grafo.py` (`menor_caminho_paradas`, `alcancaveis`, `isolados`) |
| 3.1 Ordenação simples | `algoritmos/ordenacao.py` (`bubblesort`, `selectionsort`, `insertionsort`); usada em `MapaUrbano.locais_ordenados` por nome, avaliação e distância |
| 3.2 Ordenação eficiente | `algoritmos/ordenacao.py` (`quicksort`, `mergesort`); `benchmark/benchmark.py` |
| 3.3 a 3.5 | pendentes |
| Testes | `testes/` (75 testes) |

## Fluxo de Git do grupo
```bash
git config user.name  "Seu Nome"
git config user.email "email-da-sua-conta-github"
git checkout main && git pull
git checkout -b feature/nome-da-tarefa
git add <arquivos> && git commit -m "Mensagem clara em português"
git push -u origin feature/nome-da-tarefa     # depois abra um Pull Request
```
Regras: cada integrante commita o que escreveu; Pull Request revisado por outro
integrante; merge com "Create a merge commit"; sem `push --force` na `main`.

## Declaração de uso de IA
Uso de IA como apoio (a detalhar no relatório): geração do esqueleto inicial do
projeto, dos TADs da Etapa 1, do menu e dos testes. Todo o código foi revisado
e deve ser explicado por qualquer integrante na defesa.
