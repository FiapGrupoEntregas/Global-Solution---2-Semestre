"""Menu para rodar o projeto escolhendo uma opção (sem digitar os comandos). Execute: python iniciar.py"""
import subprocess
import sys

OPCOES = {
    "1": ("Gerar base sintética", ["gerar_dados.py"]),
    "2": ("Treinar modelos e ver métricas", ["treinar_modelo.py"]),
    "3": ("Criar banco SQL e ver consultas", ["banco.py"]),
    "4": ("Rodar os testes", ["-m", "pytest", "-q", "tests"]),
    "5": ("Abrir o painel (Streamlit)", ["-m", "streamlit", "run", "app.py"]),
    "6": ("Rodar tudo (1 a 4)", None),
}


def rodar(args):
    return subprocess.run([sys.executable, *args]).returncode


def main():
    while True:
        print("\n=== TriaSUS (POC, dados sintéticos) ===")
        for k, (nome, _) in OPCOES.items():
            print(f"  {k}) {nome}")
        print("  0) Sair")
        op = input("Escolha uma opção: ").strip()
        if op == "0":
            break
        if op not in OPCOES:
            print("Opção inválida.")
            continue
        if op == "6":
            for k in "1234":
                print(f"\n>>> {OPCOES[k][0]}")
                if rodar(OPCOES[k][1]) != 0:
                    print("Etapa falhou; interrompendo.")
                    break
        else:
            rodar(OPCOES[op][1])


if __name__ == "__main__":
    main()
