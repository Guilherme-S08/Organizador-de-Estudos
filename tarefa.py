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