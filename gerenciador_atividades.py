# =================================================================
# Conteúdo do arquivo: gerenciador_atividades.py
# =================================================================

import json
import os
import time
from typing import List, Dict, Any
# É crucial importar a classe Tarefa, que deve estar em 'tarefa.py'
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

    # ADICIONE OS NOVOS MÉTODOS PARA API AQUI (como sugerido anteriormente):
    def buscar_por_id(self, id_tarefa: int) -> Tarefa | None:
        """Retorna uma tarefa pelo ID ou None se não encontrar."""
        for tarefa in self.tarefas:
            if tarefa.id_tarefa == id_tarefa:
                return tarefa
        return None

    def atualizar_tarefa(self, id_tarefa: int, novos_dados: Dict[str, Any]) -> Tarefa | None:
        """Atualiza os dados de uma tarefa existente."""
        tarefa = self.buscar_por_id(id_tarefa)
        if tarefa:
            # Atualiza apenas os campos fornecidos, se existirem
            if 'descricao' in novos_dados:
                tarefa.descricao = novos_dados['descricao']
            if 'prazo' in novos_dados:
                tarefa.prazo = novos_dados['prazo']
            if 'dificuldade' in novos_dados:
                tarefa.dificuldade = novos_dados['dificuldade']

            self.salvar()
            return tarefa
        return None