import sqlite3
import time

class GerenciadorAtividades:
    def conectar(self):
        conexao = sqlite3.connect("estudos.db")
        return conexao
    def criar_tabela(self):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudos (
                id INTEGER PRIMARY KEY,
                materia TEXT NOT NULL,
                descricao TEXT,
                data_estudo TEXT
        )
    """)

        conexao.commit()
        conexao.close()


    def menu_gerenciador(self):
        print("\n--- Adicionar Nova Tarefa ---")
        time.sleep(0.5)
        tarefa = input("Informa a tarefa: ")
        time.sleep(0.3)
        prazo = input("Qual a descrição dessa tarefa? ")
        time.sleep(0.3)
        data = input("Insira a data desse registro: ")
        self.adicionar_estudo(tarefa, prazo, data)


    def adicionar_estudo(self, materia, descricao, data_estudo):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO estudos (materia, descricao, data_estudo)
            VALUES (?, ?, ?)
        """, (materia, descricao, data_estudo))
        conexao.commit()
        conexao.close()
        time.sleep(0.2)
        print("✅ Estudo adicionado com sucesso!")

    def listar_estudos(self):
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, materia,"
                       " descricao, data_estudo FROM estudos")
        registros = cursor.fetchall()
        conexao.close()

        print("\n📚 Lista de Estudos:")
        mapa_id_exibicao_para_bd = {}

        for i, (id_bd, materia, descricao, data) in enumerate (registros, 1):
            mapa_id_exibicao_para_bd[i] = id_bd
            print(f"{i} | {materia} | {descricao} | {data}")
        return registros, mapa_id_exibicao_para_bd

    def _listar_e_ignorar(self):
            self.listar_estudos()


    def excluir_estudo(self):

        print('\n --- Informe Qual Estudo Deve Ser Apagado ---')
        time.sleep(0.5)

        registros, mapa_ids = self.listar_estudos()

        if not registros:
            print("Não há estudos para excluir.")
            return

        try:
            numero_para_excluir = int(input("\n"
                                            "Digite o **NÚMERO DA LISTA** do estudo"
                                            " a ser EXCLUÍDO: "
                                            ))

            if numero_para_excluir not in mapa_ids:
                print("Aviso: Número da lista inválido.")
                return

            id_para_excluir = mapa_ids[numero_para_excluir]

            conexao = self.conectar()
            cursor = conexao.cursor()

            cursor.execute("DELETE FROM estudos WHERE id = ?",
                           (id_para_excluir,))

            if cursor.rowcount > 0:
                conexao.commit()
                print(f"✅ Estudo **{numero_para_excluir}**"
                      f" excluído com sucesso!")
            else:
                print(f" Aviso: "
                      f"Nenhum estudo encontrado com o ID {id_para_excluir}.")

            conexao.close()

        except ValueError:
            print("Erro: Por favor, digite um número"
                  " inteiro para o item da lista.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def atualizar_estudo(self):
        print('\n --- Atualizar Estudo Existente ---')
        time.sleep(0.5)

        try:
            registros, mapa_ids = self.listar_estudos()

            if not registros:
                print("Não há estudos para atualizar.")
                return

            numero_para_atualizar = int(input("\nDigite o **NÚMERO DA LISTA**"
                                              " do estudo a ser atualizado: "))

            if numero_para_atualizar not in mapa_ids:
                print(" Aviso: Número da lista inválido.")
                return

            id_para_atualizar = mapa_ids[numero_para_atualizar]
            print(f"\nEstudo selecionado. Digite os novos dados:")

        except Exception as e:
            print(f" Erro ao listar ou selecionar o ID: {e}")
            return

        time.sleep(0.3)
        nova_tarefa = input("Novo nome da tarefa/matéria: ")
        time.sleep(0.3)
        novo_prazo = input("Novo prazo para sua execução/descrição: ")
        time.sleep(0.3)
        nova_data = input("Nova data do registro: ")

        try:
            conexao = self.conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                UPDATE estudos
                SET materia = ?, descricao = ?, data_estudo = ?
                WHERE id = ?
            """, (nova_tarefa, novo_prazo, nova_data, id_para_atualizar))

            # 4. Confirma a alteração
            if cursor.rowcount > 0:
                conexao.commit()
                print(f"✅ Estudo atualizado com sucesso!")
            else:
                print(f"️ Aviso: Nenhum estudo encontrado ou alterado com o ID {id_para_atualizar}.")

            conexao.close()

        except Exception as e:
            print(f"Ocorreu um erro ao tentar atualizar: {e}")

if __name__ == "__main__":

    app = GerenciadorAtividades()

    app.criar_tabela()

    opcoes = {
        '1': app.menu_gerenciador,
        '2': app._listar_e_ignorar,
        '3': app.excluir_estudo,
        '4': app.atualizar_estudo,
    }

    pergunta_inicial = input(
        'Você deseja:\n'
        ' 1_Escrever algo;\n'
        ' 2_Ler arquivo;\n'
        ' 3_Concluir tarefa;\n'
        ' 4_Atualizar estudo;\n'
        ' 5_Sair;\n'
        ' Escolha uma opção: '
    )

    if pergunta_inicial in opcoes:
        opcoes[pergunta_inicial]()
    elif pergunta_inicial == '5':
        print('Ok, saindo...')
        time.sleep(1)
        exit()
    else:
        print("Opção inválida. Por favor, digite 1, 2, 3 ou 4.")
