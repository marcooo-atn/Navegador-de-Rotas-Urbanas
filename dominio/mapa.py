"""Serviço de domínio: integra cadastro, índice, grafo, favoritos e histórico.

Camada de aplicação: contém as regras do tema e usa os TADs; não guarda
estado global (tudo vive na instância).
"""
from dominio.cadastro import Cadastro
from dominio.favoritos import Favoritos
from dominio.historico import Historico
from dominio.local import Local, Rota
from dominio.navegacao import Navegacao
from tads.arvore_bst import ArvoreBST
from tads.excecoes import (ChaveDuplicadaError, ElementoInexistenteError,
                           PreCondicaoError)
from tads.grafo import Grafo
from tads.lista_encadeada import ListaEncadeada


def _chave(nome: str) -> str:
    return nome.strip().lower()


class MapaUrbano:
    def __init__(self, capacidade_locais: int = 100):
        self._grafo = Grafo(capacidade_locais)
        self._cadastro = Cadastro(capacidade_locais)
        self._indice = ArvoreBST()        # chave: nome em minúsculas; valor: id
        self.favoritos = Favoritos()
        self.historico = Historico()
        self.navegacao = Navegacao()

    # --- cadastro ---------------------------------------------------------
    def adicionar_local(self, nome, bairro, categoria, avaliacao) -> Local:
        """Pré: nome não vazio e inédito; 0 <= avaliacao <= 5; há capacidade."""
        self._validar_campos(nome, avaliacao)
        if self._indice.buscar(_chave(nome)) is not None:
            raise ChaveDuplicadaError(f"já existe um local chamado {nome!r}")
        id_local = self._grafo.adicionar_vertice()
        local = Local(id_local, nome.strip(), bairro, categoria, avaliacao)
        self._cadastro.incluir(local)
        self._indice.inserir(_chave(nome), id_local)
        return local

    def alterar_local(self, id_local, nome=None, bairro=None,
                      categoria=None, avaliacao=None) -> None:
        """Pré: local existe; novo nome (se houver) é inédito e válido."""
        local = self._exigir_local(id_local)
        if avaliacao is not None:
            self._validar_campos(local.nome, avaliacao)
        if nome is not None:
            self._validar_campos(nome, local.avaliacao)
            if _chave(nome) != _chave(local.nome):
                if self._indice.buscar(_chave(nome)) is not None:
                    raise ChaveDuplicadaError(f"já existe um local chamado {nome!r}")
                self._indice.remover(_chave(local.nome))
                self._indice.inserir(_chave(nome), id_local)
            nome = nome.strip()
        self._cadastro.alterar(id_local, nome, bairro, categoria, avaliacao)

    def remover_local(self, id_local: int) -> None:
        """Pré: local existe. Mantém cadastro, índice, grafo e favoritos coerentes."""
        local = self._exigir_local(id_local)
        self._cadastro.excluir(id_local)
        self._indice.remover(_chave(local.nome))
        self._grafo.remover_vertice(id_local)
        self.favoritos.remover_se_existir(id_local)

    def locais(self):
        return self._cadastro.listar()

    def buscar_por_nome(self, nome: str):
        """Devolve o Local ou None (busca na BST, O(log n) em média)."""
        no = self._indice.buscar(_chave(nome))
        return None if no is None else self._cadastro.buscar_por_id(no.valor)

    def buscar_por_id(self, id_local: int):
        return self._cadastro.buscar_por_id(id_local)

    def autocompletar(self, prefixo: str) -> ListaEncadeada:
        """Locais cujo nome começa com `prefixo`, em ordem alfabética."""
        res = ListaEncadeada()
        for chave in self._indice.autocompletar(_chave(prefixo)):
            res.inserir_fim(self._cadastro.buscar_por_id(self._indice.buscar(chave).valor))
        return res

    # --- conexões ---------------------------------------------------------
    def conectar(self, id_a: int, id_b: int, distancia: float) -> None:
        """Pré: locais existem, distância > 0, ids diferentes."""
        self._exigir_local(id_a)
        self._exigir_local(id_b)
        self._grafo.adicionar_aresta(id_a, id_b, distancia)

    def desconectar(self, id_a: int, id_b: int) -> None:
        self._grafo.remover_aresta(id_a, id_b)

    def favoritar(self, id_local: int) -> None:
        self._exigir_local(id_local)
        self.favoritos.adicionar(id_local)

    # --- rotas e análises -------------------------------------------------
    def calcular_rota(self, id_origem: int, id_destino: int, evitar_bairro=None):
        """Rota com menos paradas (BFS). Devolve `Rota` ou None se não existe.

        Complementar: `evitar_bairro` impede passar por locais daquele bairro.
        Registra a rota no histórico quando encontrada.
        """
        self._exigir_local(id_origem)
        self._exigir_local(id_destino)
        bloqueado = None
        if evitar_bairro is not None:
            alvo = evitar_bairro.strip().lower()

            def bloqueado(v):
                return self._cadastro.buscar_por_id(v).bairro.strip().lower() == alvo

        ids = self._grafo.menor_caminho_paradas(id_origem, id_destino, bloqueado)
        if ids is None:
            return None
        nomes = ListaEncadeada()
        for v in ids:
            nomes.inserir_fim(self._cadastro.buscar_por_id(v).nome)
        rota = Rota(self._cadastro.buscar_por_id(id_origem).nome,
                    self._cadastro.buscar_por_id(id_destino).nome,
                    nomes, self._grafo.custo_caminho(ids))
        self.historico.registrar(rota)
        return rota

    def solicitar_rota(self, id_origem: int, id_destino: int) -> None:
        """Enfileira uma solicitação. Pré: ambos os locais existem."""
        self._exigir_local(id_origem)
        self._exigir_local(id_destino)
        self.navegacao.solicitar_rota(id_origem, id_destino)

    def atender_proxima_solicitacao(self):
        """Atende a solicitação mais antiga. Pré: fila não vazia."""
        id_origem, id_destino = self.navegacao.proxima_solicitacao()
        return self.calcular_rota(id_origem, id_destino)

    def alcancaveis(self, id_origem: int) -> ListaEncadeada:
        """Locais alcançáveis a partir da origem (DFS), como lista de Local."""
        self._exigir_local(id_origem)
        return self._para_locais(self._grafo.alcancaveis(id_origem))

    def isolados(self) -> ListaEncadeada:
        """Locais sem nenhuma conexão."""
        return self._para_locais(self._grafo.isolados())

    # --- internos ---------------------------------------------------------
    def _para_locais(self, ids) -> ListaEncadeada:
        res = ListaEncadeada()
        for v in ids:
            res.inserir_fim(self._cadastro.buscar_por_id(v))
        return res

    def _exigir_local(self, id_local: int) -> Local:
        local = self._cadastro.buscar_por_id(id_local)
        if local is None:
            raise ElementoInexistenteError(f"local {id_local} não existe")
        return local

    @staticmethod
    def _validar_campos(nome, avaliacao) -> None:
        if not isinstance(nome, str) or nome.strip() == "":
            raise PreCondicaoError("nome não pode ser vazio")
        if not 0 <= avaliacao <= 5:
            raise PreCondicaoError("avaliação deve estar entre 0 e 5")
