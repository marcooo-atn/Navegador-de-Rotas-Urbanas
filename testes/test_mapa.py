import unittest

from dados.exemplo import criar_mapa_exemplo
from dominio.mapa import MapaUrbano
from tads.excecoes import (ChaveDuplicadaError, ElementoInexistenteError,
                           EstruturaCheiaError, EstruturaVaziaError,
                           PreCondicaoError)


class TestMapa(unittest.TestCase):
    def setUp(self):
        self.m = criar_mapa_exemplo()

    def id_de(self, nome):
        return self.m.buscar_por_nome(nome).id

    def test_nome_duplicado(self):
        with self.assertRaises(ChaveDuplicadaError):
            self.m.adicionar_local("praça central", "X", "Y", 3)

    def test_campos_invalidos_nao_deixam_lixo(self):
        antes = len(list(self.m.locais()))
        with self.assertRaises(PreCondicaoError):
            self.m.adicionar_local("Novo", "X", "Y", 9)
        self.assertEqual(len(list(self.m.locais())), antes)

    def test_rota_e_historico(self):
        rota = self.m.calcular_rota(self.id_de("Praça Central"), self.id_de("Café do Porto"))
        self.assertEqual(list(rota.paradas),
                         ["Praça Central", "Estádio Municipal", "Café do Porto"])
        self.assertAlmostEqual(rota.distancia, 3.3)
        self.assertEqual(len(self.m.historico), 1)

    def test_rota_inexistente(self):
        self.assertIsNone(self.m.calcular_rota(self.id_de("Praça Central"),
                                               self.id_de("Farol Distante")))

    def test_rota_evitando_bairro(self):
        rota = self.m.calcular_rota(self.id_de("Praça Central"),
                                    self.id_de("Parque das Águas"), evitar_bairro="Centro")
        self.assertIsNotNone(rota)   # origem no bairro evitado é permitida
        rota = self.m.calcular_rota(self.id_de("Praça Central"),
                                    self.id_de("Parque das Águas"), evitar_bairro="Jardim")
        self.assertIsNone(rota)      # destino está no bairro evitado

    def test_fila_de_solicitacoes(self):
        a, b, c = (self.id_de(n) for n in ("Praça Central", "Hospital Sul", "Terminal Norte"))
        self.m.solicitar_rota(a, b)
        self.m.solicitar_rota(a, c)
        self.assertEqual(list(self.m.atender_proxima_solicitacao().paradas)[-1], "Hospital Sul")
        self.assertEqual(list(self.m.atender_proxima_solicitacao().paradas)[-1], "Terminal Norte")
        with self.assertRaises(EstruturaVaziaError):
            self.m.atender_proxima_solicitacao()

    def test_historico_navegavel(self):
        a, b, c = (self.id_de(n) for n in ("Praça Central", "Hospital Sul", "Terminal Norte"))
        self.m.calcular_rota(a, b)
        self.m.calcular_rota(a, c)
        self.assertEqual(self.m.historico.atual().destino, "Terminal Norte")
        self.assertEqual(self.m.historico.anterior().destino, "Hospital Sul")
        self.assertEqual(self.m.historico.proxima().destino, "Terminal Norte")

    def test_remover_local_mantem_coerencia(self):
        pid = self.id_de("Parque das Águas")
        self.m.favoritar(pid)
        self.m.remover_local(pid)
        self.assertIsNone(self.m.buscar_por_nome("Parque das Águas"))
        self.assertEqual(len(self.m.favoritos), 0)
        self.assertEqual(len(self.m.autocompletar("parque")), 0)
        with self.assertRaises(ElementoInexistenteError):
            self.m.calcular_rota(pid, self.id_de("Praça Central"))

    def test_alterar_nome_atualiza_indice(self):
        pid = self.id_de("Praça Central")
        self.m.alterar_local(pid, nome="Praça da Aurora")
        self.assertIsNone(self.m.buscar_por_nome("Praça Central"))
        self.assertEqual(self.m.buscar_por_nome("praça da aurora").id, pid)
        with self.assertRaises(ChaveDuplicadaError):
            self.m.alterar_local(pid, nome="Mercado Municipal")

    def test_favoritos_capacidade_10(self):
        m = MapaUrbano(30)
        ids = [m.adicionar_local(f"Local {i:02d}", "B", "C", 4).id for i in range(11)]
        for i in ids[:10]:
            m.favoritar(i)
        with self.assertRaises(EstruturaCheiaError):
            m.favoritar(ids[10])
        with self.assertRaises(ChaveDuplicadaError):
            m.favoritar(ids[0])

    def test_autocompletar_e_isolados(self):
        nomes = [l.nome for l in self.m.autocompletar("PA")]
        self.assertEqual(nomes, ["Parque das Águas"])
        self.assertEqual([l.nome for l in self.m.isolados()], ["Farol Distante"])

    def test_pilha_voltar(self):
        n = self.m.navegacao
        n.entrar("menu"); n.entrar("busca")
        self.assertEqual(n.voltar(), "menu")
        with self.assertRaises(EstruturaVaziaError):
            n.voltar()


if __name__ == "__main__":
    unittest.main()


class TestMapaOrdenacao(unittest.TestCase):
    def setUp(self):
        self.m = criar_mapa_exemplo()

    def test_ordenar_nao_altera_cadastro_original(self):
        antes = [l.nome for l in self.m.locais()]
        self.m.locais_ordenados("nome", "quick")
        self.assertEqual([l.nome for l in self.m.locais()], antes)

    def test_criterios_e_algoritmos(self):
        for algoritmo in ("bubble", "selection", "insertion", "quick", "merge"):
            nomes = [l.nome for l in self.m.locais_ordenados("nome", algoritmo)]
            self.assertEqual(nomes[0], "Biblioteca Aurora")
            self.assertEqual(nomes[-1], "Universidade Nova")
            notas = [l.avaliacao for l in self.m.locais_ordenados("avaliacao", algoritmo)]
            self.assertEqual(notas, sorted(notas, reverse=True))

    def test_distancia(self):
        origem = self.m.buscar_por_nome("Praça Central").id
        ordenados = [l.nome for l in self.m.locais_ordenados("distancia", "merge", origem)]
        self.assertEqual(ordenados[0], "Praça Central")
        self.assertEqual(ordenados[-1], "Farol Distante")      # inalcançável por último

    def test_pre_condicoes(self):
        with self.assertRaises(PreCondicaoError):
            self.m.locais_ordenados("distancia")                # sem referência
        with self.assertRaises(PreCondicaoError):
            self.m.locais_ordenados("cor")
        with self.assertRaises(ValueError):
            self.m.locais_ordenados("nome", "heap")
