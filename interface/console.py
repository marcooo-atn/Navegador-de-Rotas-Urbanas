"""Interface de console (menu). Toda a regra de negócio fica em `dominio/`."""
from tads.excecoes import PreCondicaoError

MENU = """
=== Navegador de Rotas - Nova Aurora ===
 1) Listar locais            8) Solicitar rota (fila)
 2) Cadastrar local          9) Atender próxima solicitação
 3) Alterar local           10) Histórico de rotas (anterior/próxima)
 4) Excluir local           11) Favoritos
 5) Autocompletar nome      12) Alcançáveis (DFS) e isolados
 6) Conectar locais          v) Voltar (pilha de telas)
 7) Calcular rota (BFS)      0) Sair
"""


def _ler(msg: str) -> str:
    return input(msg).strip()


def _ler_numero(msg: str) -> float:
    while True:
        try:
            return float(_ler(msg).replace(",", "."))
        except ValueError:
            print("Valor inválido, tente de novo.")


def _pedir_local(mapa, msg: str):
    nome = _ler(msg)
    local = mapa.buscar_por_nome(nome)
    if local is None:
        print(f"Local {nome!r} não encontrado.")
    return local


def _mostrar_rota(rota) -> None:
    trajeto = " -> ".join(rota.paradas)
    print(f"Rota: {trajeto}")
    print(f"Paradas: {len(rota.paradas)} | Distância total: {rota.distancia:.1f} km")


def _listar(mapa) -> None:
    for local in mapa.locais():
        print(f"[{local.id}] {local.nome} | {local.bairro} | {local.categoria} | {local.avaliacao}")


def _cadastrar(mapa) -> None:
    local = mapa.adicionar_local(_ler("Nome: "), _ler("Bairro: "), _ler("Categoria: "),
                                 _ler_numero("Avaliação (0-5): "))
    print(f"Local cadastrado com id {local.id}.")


def _alterar(mapa) -> None:
    local = _pedir_local(mapa, "Nome do local a alterar: ")
    if local is None:
        return
    print("Deixe em branco para manter o valor atual.")
    nome = _ler(f"Novo nome [{local.nome}]: ") or None
    bairro = _ler(f"Novo bairro [{local.bairro}]: ") or None
    categoria = _ler(f"Nova categoria [{local.categoria}]: ") or None
    aval = _ler(f"Nova avaliação [{local.avaliacao}]: ")
    mapa.alterar_local(local.id, nome, bairro, categoria,
                       float(aval.replace(",", ".")) if aval else None)
    print("Local alterado.")


def _excluir(mapa) -> None:
    local = _pedir_local(mapa, "Nome do local a excluir: ")
    if local is not None:
        mapa.remover_local(local.id)
        print("Local excluído.")


def _autocompletar(mapa) -> None:
    achados = mapa.autocompletar(_ler("Prefixo: "))
    if len(achados) == 0:
        print("Nenhum local encontrado.")
    for local in achados:
        print(f"- {local.nome} ({local.bairro})")


def _conectar(mapa) -> None:
    a = _pedir_local(mapa, "Local A: ")
    b = _pedir_local(mapa, "Local B: ") if a is not None else None
    if a is not None and b is not None:
        mapa.conectar(a.id, b.id, _ler_numero("Distância (km): "))
        print("Locais conectados.")


def _rota(mapa) -> None:
    a = _pedir_local(mapa, "Origem: ")
    b = _pedir_local(mapa, "Destino: ") if a is not None else None
    if a is None or b is None:
        return
    evitar = _ler("Bairro a evitar (Enter = nenhum): ") or None
    rota = mapa.calcular_rota(a.id, b.id, evitar)
    if rota is None:
        print("Não existe rota entre esses locais com essas restrições.")
    else:
        _mostrar_rota(rota)


def _solicitar(mapa) -> None:
    a = _pedir_local(mapa, "Origem: ")
    b = _pedir_local(mapa, "Destino: ") if a is not None else None
    if a is not None and b is not None:
        mapa.solicitar_rota(a.id, b.id)
        print(f"Solicitação enfileirada. Pendentes: {mapa.navegacao.pendentes()}")


def _atender(mapa) -> None:
    rota = mapa.atender_proxima_solicitacao()
    if rota is None:
        print("Solicitação atendida: não há rota possível.")
    else:
        _mostrar_rota(rota)


def _historico(mapa) -> None:
    h = mapa.historico
    if len(h) == 0:
        print("Histórico vazio.")
        return
    _mostrar_rota(h.atual())
    while True:
        op = _ler("[a] anterior  [p] próxima  [Enter] sair: ").lower()
        if op == "a" and h.tem_anterior():
            _mostrar_rota(h.anterior())
        elif op == "p" and h.tem_proxima():
            _mostrar_rota(h.proxima())
        elif op == "":
            return
        else:
            print("Não há rota nessa direção.")


def _favoritos(mapa) -> None:
    for id_local in mapa.favoritos.listar():
        print(f"- {mapa.buscar_por_id(id_local).nome}")
    print(f"({len(mapa.favoritos)}/10 favoritos)")
    op = _ler("[a] adicionar  [r] remover  [Enter] sair: ").lower()
    if op in ("a", "r"):
        local = _pedir_local(mapa, "Nome do local: ")
        if local is None:
            return
        if op == "a":
            mapa.favoritar(local.id)
        else:
            mapa.favoritos.remover(local.id)
        print("Favoritos atualizados.")


def _alcance(mapa) -> None:
    origem = _pedir_local(mapa, "Alcançáveis a partir de: ")
    if origem is not None:
        print("Alcançáveis: " + ", ".join(l.nome for l in mapa.alcancaveis(origem.id)))
    isolados = ", ".join(l.nome for l in mapa.isolados()) or "nenhum"
    print(f"Locais isolados: {isolados}")


def _voltar(mapa) -> None:
    if mapa.navegacao.pode_voltar():
        print(f"Voltando para: {mapa.navegacao.voltar()}")
    else:
        print("Não há tela anterior.")


def executar(mapa) -> None:
    """Laço principal do menu. Erros de pré-condição viram mensagens."""
    mapa.navegacao.entrar("menu")
    acoes = (("1", _listar, "Locais"), ("2", _cadastrar, "Cadastro"),
             ("3", _alterar, "Alterar"), ("4", _excluir, "Excluir"),
             ("5", _autocompletar, "Busca"), ("6", _conectar, "Conexões"),
             ("7", _rota, "Rota"), ("8", _solicitar, "Solicitar rota"),
             ("9", _atender, "Atender rota"), ("10", _historico, "Histórico"),
             ("11", _favoritos, "Favoritos"), ("12", _alcance, "Alcance"))
    while True:
        print(MENU)
        try:
            op = _ler("Opção: ").lower()
        except EOFError:
            return
        if op == "0":
            print("Até logo!")
            return
        if op == "v":
            _voltar(mapa)
            continue
        for codigo, funcao, tela in acoes:
            if op == codigo:
                mapa.navegacao.entrar(tela)
                try:
                    funcao(mapa)
                except PreCondicaoError as erro:
                    print(f"Operação não permitida: {erro}")
                except EOFError:
                    return
                break
        else:
            print("Opção inválida.")
