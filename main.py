import json
import os
from typing import Dict, List, Optional
from datetime import datetime

# Modelos de dados

class Livro:
    def __init__(self, livro_id: int, titulo: str, autor: str, editora: str, ano: int):
        self.id = livro_id
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.disponivel = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "editora": self.editora,
            "ano": self.ano,
            "disponivel": self.disponivel
        }

# Empréstimos

class Emprestimo:
    def __init__(
        self,
        livro_id: int,
        nome: str,
        contato: str,
        data_emprestimo: str,
        data_devolucao: Optional[str] = None
    ):
        self.livro_id = livro_id
        self.nome = nome
        self.contato = contato
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao

    def to_dict(self) -> dict:
        return {
            "livro_id": self.livro_id,
            "nome": self.nome,
            "contato": self.contato,
            "data_emprestimo": self.data_emprestimo,
            "data_devolucao": self.data_devolucao
        }



# Sistema de Biblioteca

class Biblioteca:
    def __init__(self, arquivo="biblioteca.json"):
        self.arquivo = arquivo
        self.livros: Dict[int, Livro] = {}
        self.emprestimos: List[Emprestimo] = []
        self.proximo_id = 1
        self.carregar()

    def adicionar_livro(self, titulo, autor, editora, ano):
        livro = Livro(self.proximo_id, titulo, autor, editora, ano)
        self.livros[self.proximo_id] = livro
        print(f"\nLivro cadastrado com ID {self.proximo_id}")
        self.proximo_id += 1
        self.salvar()

    def registrar_emprestimo(self, livro_id, nome, contato) -> bool:
        livro = self.livros.get(livro_id)
        if not livro or not livro.disponivel:
            return False

        livro.disponivel = False
        self.emprestimos.append(
            Emprestimo(
                livro_id,
                nome,
                contato,
                datetime.now().strftime("%d/%m/%Y %H:%M")
            )
        )
        self.salvar()
        return True

    def devolver(self, livro_id) -> bool:
        livro = self.livros.get(livro_id)
        if not livro or livro.disponivel:
            return False

        for e in reversed(self.emprestimos):
            if e.livro_id == livro_id and e.data_devolucao is None:
                e.data_devolucao = datetime.now().strftime("%d/%m/%Y %H:%M")
                break

        livro.disponivel = True
        self.salvar()
        return True

    def listar_livros(self):
        return self.livros.values()

    def historico(self, livro_id: int):
        return [e for e in self.emprestimos if e.livro_id == livro_id]

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "proximo_id": self.proximo_id,
                    "livros": {k: v.to_dict() for k, v in self.livros.items()},
                    "emprestimos": [e.to_dict() for e in self.emprestimos]
                },
                f,
                ensure_ascii=False,
                indent=4
            )

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.proximo_id = dados["proximo_id"]

                for info in dados["livros"].values():
                    livro = Livro(
                        info["id"],
                        info["titulo"],
                        info["autor"],
                        info["editora"],
                        info["ano"]
                    )
                    livro.disponivel = info["disponivel"]
                    self.livros[livro.id] = livro

                for e in dados["emprestimos"]:
                    self.emprestimos.append(Emprestimo(**e))
        except Exception:
            print("Erro ao carregar dados. Arquivo ignorado.")


# Funções auxiliares e interface

def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    print("=" * 50)
    print(" SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ".center(50))
    print("=" * 50)
    print("1 - Cadastrar novo livro")
    print("2 - Registrar empréstimo")
    print("3 - Registrar devolução")
    print("4 - Listar livros")
    print("5 - Histórico de empréstimos")
    print("0 - Sair")
    return input("\nEscolha uma opção: ").strip()



def main():
    bib = Biblioteca()

    while True:
        limpar()
        op = menu()

        if op == "1":
            limpar()
            print("Cadastro de livro\n")
            bib.adicionar_livro(
                input("Título: "),
                input("Autor: "),
                input("Editora: "),
                int(input("Ano: "))
            )

        elif op == "2":
            limpar()
            print("Empréstimo de livro\n")
            livro_id = int(input("ID do livro: "))
            nome = input("Nome do leitor: ")
            contato = input("Contato: ")
            print("\nSucesso!" if bib.registrar_emprestimo(livro_id, nome, contato) else "\nErro no empréstimo.")

        elif op == "3":
            limpar()
            print("Devolução de livro\n")
            livro_id = int(input("ID do livro: "))
            print("\nDevolvido com sucesso!" if bib.devolver(livro_id) else "\nErro na devolução.")

        elif op == "4":
            limpar()
            print("Lista de livros\n")
            for l in bib.listar_livros():
                status = "Disponível" if l.disponivel else "Emprestado"
                print(f"[{l.id}] {l.titulo} - {l.autor} ({status})")

        elif op == "5":
            limpar()
            print("Histórico de empréstimos\n")
            livro_id = int(input("ID do livro: "))
            for e in bib.historico(livro_id):
                print(e.to_dict())

        elif op == "0":
            print("\nEncerrando sistema...")
            break

        else:
            print("\nOpção inválida.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()
