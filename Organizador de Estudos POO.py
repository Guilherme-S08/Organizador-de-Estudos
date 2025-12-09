from typing import Dict, Any


class Tarefa:
    """
    Representa uma única tarefa com descrição, prazo e dificuldade.
    Funciona como o Modelo (Entity) de dados do projeto.
    """

    def __init__(self, descricao: str, prazo: str, dificuldade: str, id_tarefa: int = None):
        self.id_tarefa = id_tarefa
        self.descricao = descricao
        self.prazo = prazo
        self.dificuldade = dificuldade

    def __str__(self):
        """Retorna uma representação legível da tarefa."""
        status = " (ID não definido)"
        if self.id_tarefa is not None:
            status = f" (ID: {self.id_tarefa})"

        return (f"Descrição: {self.descricao}\n"
                f"  Prazo: {self.prazo}\n"
                f"  Dificuldade: {self.dificuldade}" + status)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a tarefa para um dicionário, pronta para ser salva em JSON."""
        return {
            "id_tarefa": self.id_tarefa,
            "descricao": self.descricao,
            "prazo": self.prazo,
            "dificuldade": self.dificuldade
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> 'Tarefa':
        """Cria um objeto Tarefa a partir de um dicionário (lido do JSON)."""
        return Tarefa(
            descricao=d['descricao'],
            prazo=d['prazo'],
            dificuldade=d['dificuldade'],
            id_tarefa=d.get('id_tarefa')
        )


import json
import os
import time
from typing import List, Dict, Any
from tarefa import Tarefa


class GerenciadorAtividades:
    """
    Gerencia a lista de tarefas, lidando com a persistência de dados (JSON)
    e a manipulação da lista (CRUD, ordenação).
    """

    def __init__(self, arquivo='data.json'):
        self.arquivo = arquivo
        self._proximo_id = 1
        self.tarefas: List[Tarefa] = self.carregar()

    def carregar(self) -> List[Tarefa]:
        """
        Lê o JSON, converte o conteúdo para objetos Tarefa e retorna a lista.
        Também atualiza o _proximo_id.
        """
        tarefas_carregadas = []
        maior_id = 0

        if os.path.exists(self.arquivo) and os.path.getsize(self.arquivo) > 0:
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for item_dict in dados:
                        tarefa = Tarefa.from_dict(item_dict)
                        tarefas_carregadas.append(tarefa)
                        if tarefa.id_tarefa and tarefa.id_tarefa > maior_id:
                            maior_id = tarefa.id_tarefa
            except json.JSONDecodeError:
                print("Aviso: Arquivo JSON inválido. Iniciando com lista vazia.")
                return []

        self._proximo_id = maior_id + 1
        return tarefas_carregadas

    def salvar(self):
        """Salva a lista atual de objetos Tarefa no JSON, convertendo-os para dicionário."""
        lista_dicts = [tarefa.to_dict() for tarefa in self.tarefas]
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(lista_dicts, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")

    def adicionar_tarefa(self, tarefa: Tarefa):
        """Adiciona uma nova tarefa à lista e atribui um ID único."""
        tarefa.id_tarefa = self._proximo_id
        self._proximo_id += 1
        self.tarefas.append(tarefa)
        self.salvar()

    def listar(self) -> List[Tarefa]:
        """
        Retorna a lista de tarefas ordenada pelo atributo 'prazo'.
        """
        self.tarefas.sort(key=lambda t: t.prazo)
        return self.tarefas

    def remover(self, id_tarefa: int) -> bool:
        """
        Remove uma tarefa com base no seu ID de Tarefa.
        Retorna True se removeu, False caso contrário.
        """
        tarefa_encontrada = None
        for tarefa in self.tarefas:
            if tarefa.id_tarefa == id_tarefa:
                tarefa_encontrada = tarefa
                break

        if tarefa_encontrada:
            self.tarefas.remove(tarefa_encontrada)
            self.salvar()
            return True
        return False


class Menu:
    """
    Lida com a interface do usuário (exibir opções, receber entradas).
    Não contém lógica de negócio, apenas chama métodos do GerenciadorAtividades.
    """

    def __init__(self):
        self.gerenciador = GerenciadorAtividades()

    def _exibir_opcoes(self):
        """Exibe o menu principal."""
        print("\n--- Gerenciador de Atividades (POO) ---")
        print("1. Adicionar Nova Tarefa")
        print("2. Listar Todas as Tarefas (Ordenado por Prazo)")
        print("3. Remover Tarefa (Concluir)")
        print("4. Sair")
        print("-" * 37)

    def executar(self):
        """Loop principal do menu."""
        while True:
            self._exibir_opcoes()
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self._adicionar_menu()
            elif escolha == '2':
                self._listar_menu()
            elif escolha == '3':
                self._remover_menu()
            elif escolha == '4':
                print("Saindo do Gerenciador. Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")

            time.sleep(0.5)

    def _obter_dados_tarefa(self) -> Tarefa:
        """Coleta dados do usuário para criar um objeto Tarefa."""
        print("\n--- Adicionar Nova Tarefa ---")
        descricao = input("Descrição da Tarefa: ")
        prazo = input("Prazo (formato: DD-MM-YYYY): ")
        dificuldade = input("Dificuldade (ex: Baixa, Média, Alta): ")

        return Tarefa(descricao=descricao, prazo=prazo, dificuldade=dificuldade)

    def _adicionar_menu(self):
        """Chama a lógica para adicionar uma tarefa."""
        nova_tarefa = self._obter_dados_tarefa()
        self.gerenciador.adicionar_tarefa(nova_tarefa)
        print("✅ Tarefa adicionada com sucesso!")

    def _listar_menu(self):
        """Chama a lógica para listar e exibe os resultados."""
        tarefas = self.gerenciador.listar()

        if not tarefas:
            print("\nNenhuma tarefa registrada.")
            return

        print("\n📚 Lista de Tarefas (Ordenadas por Prazo):")
        for tarefa in tarefas:
            print("-" * 30)
            print(f"ID: {tarefa.id_tarefa}")
            print(f"Descrição: {tarefa.descricao}")
            print(f"Prazo: {tarefa.prazo}")
            print(f"Dificuldade: {tarefa.dificuldade}")
        print("-" * 30)

    def _remover_menu(self):
        """Chama a lógica para remover uma tarefa."""
        self._listar_menu()

        if not self.gerenciador.tarefas:
            return

        try:
            id_para_remover = int(input("\nDigite o ID da tarefa a ser REMOVIDA (Concluída): "))

            if self.gerenciador.remover(id_para_remover):
                print(f"✅ Tarefa com ID {id_para_remover} removida/concluída com sucesso!")
            else:
                print(f"❌ Erro: Nenhuma tarefa encontrada com o ID {id_para_remover}.")

        except ValueError:
            print("❌ Erro: Por favor, insira um ID numérico válido.")


if __name__ == "__main__":
    """
    Roda a aplicação principal, instanciando o Menu e iniciando a execução.
    """
    app = Menu()
    app.executar()