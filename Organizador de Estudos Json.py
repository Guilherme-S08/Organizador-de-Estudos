import time
import os
import json



inicio = input('Você deseja: 1_Escrever algo;  2_Ler arquivo; 3_Concluir tarefa; 4_Sair.: ')

if inicio == '1':

    dados_coletados = []

    try:
     numero_de_atividades = int(input("Quantas atividades você deseja registrar? "))
    except ValueError:
     print("Por favor, digite um número válido.")
     exit()

    for i in range(numero_de_atividades):
     print(f"\n--- Atividade {i + 1} ---")

     atividade = input("Qual a atividade? ")

     numeros_input = input("Digite o prazo e a dificuldade, separados por espaço: ")
     try:
         n1, n2 = map(int, numeros_input.split())

         dados_coletados.append([atividade, n1, n2])
     except ValueError:
         print("Entrada inválida. Por favor, digite apenas dois números inteiros.")
         continue

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
        print(f"{i+1}. Atividade: {linha[0]}, Prazo e dificuldade: {linha[1]}, {linha[2]}")


    print("\nDados salvos com sucesso no arquivo 'dados.json'.")

if inicio == '2':

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
            print(f"{i + 1}. Atividade: {item[0]}, Prazo e dificuldade: {item[1]}, {item[2]}")


if inicio == '3':

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
            print(f"{i + 1}: Atividade: {item[0]}, Prazo e dificuldade {item[1]}, {item[2]}")

        while True:
            try:
                numero_para_remover = int(
                    input("\nDigite o número da linha que você quer remover (ou 0 para cancelar): "))
                if numero_para_remover == 0:
                    print("Operação cancelada.")
                    return
                if 1 <= numero_para_remover <= len(dados):
                    break
                else:
                    print(f"Número inválido. Por favor, digite um número entre 1 e {len(dados)}.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

        del dados[numero_para_remover - 1]

        try:
            with open(nome_arquivo, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)
            print(f"A linha {numero_para_remover} foi removida com sucesso!")
        except IOError as e:
            print(f"Erro ao escrever no arquivo: {e}")


    listar_e_remover_linha('dados.json')


if inicio == '4':
    print('Ok, saindo...')
    time.sleep(1)
    exit()
