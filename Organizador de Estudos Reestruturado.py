import json
import os
import time


class GerenciadorAtividades:
    """
    Gerencia a leitura, escrita, exibição e exclusão de atividades
    armazenadas em um arquivo JSON.
    """
    def __init__(self, nome_arquivo='dados.json'):
        self.nome_arquivo = nome_arquivo

    def registrar_atividades(self):
        """
        Coleta dados do usuário sobre atividades, prazo e dificuldade,
        e salva no arquivo 'dados.json', ordenando-os.
        """
        dados_coletados = []

        try:
            numero_de_atividades = int(input(
                "Quantas atividades você deseja registrar? "
            ))
        except ValueError:
            print("Por favor, digite um número válido.")
            return

        for i in range(numero_de_atividades):
            print(f"\n--- Atividade {i + 1} ---")
            atividade = input("Qual a atividade? ")
            numeros_input = input(
                "Digite o prazo e a dificuldade, separados por espaço: "
            )

            try:
                prazo, dificuldade = map(int, numeros_input.split())
                dados_coletados.append([atividade, prazo, dificuldade])
            except ValueError:
                print(
                    "Entrada inválida. Por favor,"
                    " digite apenas dois números inteiros."
                )
                continue

        time.sleep(0.5)
        print("\nDados salvos com sucesso no arquivo 'dados.json':\n")
        time.sleep(0.3)
        try:
            with open('dados.json', 'r') as arquivo:
                dados_existentes = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            dados_existentes = []

        dados_existentes.extend(dados_coletados)
        dados_existentes.sort(key=lambda item: (item[1], -item[2]))

        with open('dados.json', 'w') as arquivo:
            json.dump(dados_existentes, arquivo, indent=4)

        for i, linha in enumerate(dados_existentes):
            print(f"{i+1}. Atividade: {linha[0]}, "
                  f"Prazo e dificuldade: {linha[1]}, {linha[2]}")


    def exibir_atividades(self):
        """
        Retoma os dados do usuário sobre atividades, prazo e dificuldade,
        ordenados.
        """

        dados_lidos = []

        try:
            with open('dados.json', 'r') as arquivo:
                dados_lidos = json.load(arquivo)
        except FileNotFoundError:
            print("Erro: O arquivo 'dados.json' não foi encontrado.")
            exit()
        except json.JSONDecodeError:
            print("Erro: O arquivo 'dados.json' está vazio ou corrompido.")
            exit()

        if not dados_lidos:
            print("O arquivo 'dados.json' foi lido, mas não contém dados.")

        else:
            dados_lidos.sort(key=lambda item: (item[1], item[2]))

            print("\n--- Conteúdo da lista ---")
            for i, item in enumerate(dados_lidos):
                print(
                    f"{i + 1}. Atividade: {item[0]}, "
                    f"Prazo e dificuldade: {item[1]}, {item[2]}"
                )


    def excluir_atividades(self):
        """
        Retoma os dados registrados do usuário, e exclue
        as atividades escolhidas.
        """

        def listar_e_remover_linha(nome_arquivo):
            if not os.path.exists(nome_arquivo):
                print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
                return

            try:
                with open(nome_arquivo, 'r') as arquivo:
                    dados = json.load(arquivo)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Erro ao ler o arquivo: {e}")
                return

            if not dados:
                print("O arquivo está vazio. Não há nada para remover.")
                return

            print("\nConteúdo atual do arquivo:")
            time.sleep(0.5)
            for i, item in enumerate(dados):
                print(f"{i + 1}: Atividade: {item[0]}, "
                      f"Prazo e dificuldade {item[1]}, {item[2]}"
                      )
            while True:
                try:
                    numero_para_remover = int(
                        input("\nDigite o número da linha que você"
                              " quer remover (ou 0 para cancelar): ")
                    )
                    if numero_para_remover == 0:
                        print("Operação cancelada.")
                        return
                    if 1 <= numero_para_remover <= len(dados):
                        break
                    else:
                        print(
                            f"Número inválido. Por favor,"
                            f" digite um número entre 1 e {len(dados)}."
                        )
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")

            del dados[numero_para_remover - 1]

            try:
                with open(nome_arquivo, 'w') as arquivo:
                    json.dump(dados, arquivo, indent=4)
                print(
                    f"\nA linha {numero_para_remover} "
                    f"foi removida com sucesso!"
                )
            except IOError as e:
                print(f"Erro ao escrever no arquivo: {e}")


        listar_e_remover_linha('dados.json')



class menu_principal:
    """Função que exibe o menu e controla o fluxo principal do programa."""


    gerenciador = GerenciadorAtividades()


    pergunta_inicial = input(
        'Você deseja:\n'
        ' 1_Escrever algo;\n'
        ' 2_Ler arquivo;\n'
        ' 3_Concluir tarefa;\n'
        ' 4_Sair;\n'
        ' Escolha uma opção: '
    )

    opcoes = {
        '1': gerenciador.registrar_atividades,
        '2': gerenciador.exibir_atividades,
        '3': gerenciador.excluir_atividades,
    }
    if pergunta_inicial in opcoes:
        opcoes[pergunta_inicial]()
    elif pergunta_inicial == '4':
        print('Ok, saindo...')
        time.sleep(1)
        exit()
    else:
        print("Opção inválida. Por favor, digite 1, 2, 3 ou 4.")


if __name__ == "__main__":
    menu_principal()