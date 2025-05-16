import os
import subprocess
import sys
from typing import Callable


def clear_screen():
    """Limpa o console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(options: list[tuple[str, Callable]], header: str = None):
    """Função menu"""
    while True:
        clear_screen()
        if header:
            print(f"\n{header}\n{'=' * len(header)}\n")

        for i, (label, _) in enumerate(options, 1):
            print(f"{i}. {label}")

        print("\n0. Sair")

        try:
            choice = int(input("\nEscolha uma opção: "))
            if choice == 0:
                print("\nOperação cancelada. Até logo!")
                sys.exit()

            _, action = options[choice - 1]
            action()
            input("\nPressione Enter para continuar...")

        except (ValueError, IndexError):
            input("\nOpção inválida! Tente novamente...")


def run_script(script_name: str):
    """Executa um script via Poetry"""
    script_path = os.path.join(os.path.dirname(__file__), f"{script_name}.py")
    try:
        subprocess.run(["poetry", "run", "python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nErro ao executar {script_name}: {e}")
        input("Pressione Enter para continuar...")


def main_menu():
    """Programa principal"""
    menu_options = [
        ("Criar tabelas no banco de dados", lambda: run_script("pi2_cria_tabelas")),
        ("Popular dados fictícios", lambda: run_script("pi2_cria_dados")),
        ("Remover todas as tabelas", lambda: run_script("pi2_remove_tabelas")),
        ("Sobre o projeto", about_info),
    ]

    display_menu(
        options=menu_options,
        header="Sistema Hospitalar - PI2 Gestão de Dados"
    )


def about_info():
    """Dados do projeto"""
    clear_screen()
    print("""
    Projeto Integrador 2 - Senac EAD

    Funcionalidades:
    - Criação de estrutura de banco de dados
    - Geração de dados fictícios para testes
    - Gestão de recursos hospitalares

    Tecnologias:
    - Python 3.10+
    - DuckDB
    - Pandas
    - Poetry
    """)
    input("\nPressione Enter para voltar...")


if __name__ == "__main__":
    main_menu()