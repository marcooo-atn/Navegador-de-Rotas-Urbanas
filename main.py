"""Ponto de entrada: apenas orquestra a execução."""
from dados.exemplo import criar_mapa_exemplo
from interface.console import executar


def main() -> None:
    executar(criar_mapa_exemplo())


if __name__ == "__main__":
    main()
