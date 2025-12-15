from typing import TypedDict, List
from flask import Flask, jsonify, abort  # Incluindo 'abort' para lidar com erros
from doctor import api

from tarefa import Tarefa
from gerenciador_atividades import GerenciadorAtividades

# 1. INICIALIZAÇÃO E INSTÂNCIA ÚNICA (Corrigido)
app = Flask(__name__)
API = api.API(app)

# Instância única do Gerenciador de Atividades
gerenciador = GerenciadorAtividades()


# 2. DEFINIÇÃO DOS SCHEMAS (TypedDict) para o doctor

# Esquema de Entrada (Input) para POST e PUT
class TarefaInput(TypedDict):
    descricao: str
    prazo: str
    dificuldade: str


# Esquema de Saída (Output) para GETs e POST
class TarefaOutput(TypedDict):
    id_tarefa: int
    descricao: str
    prazo: str
    dificuldade: str


# 3. IMPLEMENTAÇÃO DOS ENDPOINTS (Rotas)

# A. POST /tarefas (Criação)
@API.route('/tarefas', methods=['POST'])
@api.params(TarefaInput)  # Valida se a entrada JSON tem os campos e tipos corretos
@api.returns(TarefaOutput)  # Valida se a saída está no formato correto
def criar_tarefa(dados_tarefa: TarefaInput) -> TarefaOutput:
    """Cria uma nova tarefa e retorna o objeto criado com ID."""

    # Cria o objeto Tarefa a partir dos dados validados
    nova_tarefa = Tarefa.from_dict(dados_tarefa)

    # Adiciona a tarefa (atribui ID e salva no JSON)
    gerenciador.adicionar_tarefa(nova_tarefa)

    # Retorna o dicionário (que será convertido em JSON pelo Flask)
    return nova_tarefa.to_dict()


# B. GET /tarefas (Listagem de Todas)
@API.route('/tarefas', methods=['GET'])
@api.returns(List[TarefaOutput])  # Retorna uma lista de objetos TarefaOutput
def listar_tarefas() -> List[TarefaOutput]:
    """Lista todas as tarefas existentes, ordenadas por prazo."""

    tarefas = gerenciador.listar()

    # Converte a lista de objetos Tarefa para uma lista de dicionários
    return [t.to_dict() for t in tarefas]


# C. GET /tarefas/{id} (Consulta por ID)
@API.route('/tarefas/<int:id_tarefa>', methods=['GET'])
@api.returns(TarefaOutput)
def obter_tarefa(id_tarefa: int) -> TarefaOutput:
    """Consulta uma única tarefa pelo seu ID."""

    tarefa = gerenciador.buscar_por_id(id_tarefa)

    if tarefa is None:
        # Aborta a requisição com código 404 Not Found
        # (O Flask cuida do JSON de erro)
        abort(404, description=f"Tarefa com ID {id_tarefa} não encontrada.")

    return tarefa.to_dict()


# 4. EXECUÇÃO DA APLICAÇÃO
if __name__ == '__main__':
    # O servidor web Flask é iniciado
    app.run(debug=True)