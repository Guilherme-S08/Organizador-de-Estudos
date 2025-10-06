import time
import os

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

 dados_coletados.sort(key=lambda item: (item[1], -item[2]))


 print("\n--- Dados Ordenados ---")

 with open('dados.txt', 'a') as arquivo:
     for linha in dados_coletados:
         linha_formatada = f"Atividade: {linha[0]}, Prazo e dificuldade: {linha[1]}, {linha[2]}\n"

         print(linha_formatada.strip())  # .strip() remove a quebra de linha para a exibição na tela

         arquivo.write(linha_formatada)

 print("\nDados salvos com sucesso no arquivo 'dados.txt'.")

if inicio == '2':

    dados_lidos = []

    try:
        with open('dados.txt', 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()

                if not linha:
                    continue

                try:
                    partes = linha.split(', Prazo e dificuldade: ')
                    atividade = partes[0].replace('Atividade: ', '')

                    numeros_str = partes[1].split(', ')
                    n1, n2 = int(numeros_str[0]), int(numeros_str[1])

                    # Adiciona os dados na lista
                    dados_lidos.append([atividade, n1, n2])
                except (ValueError, IndexError):
                    print(f"Atenção: A linha '{linha}' não pôde ser lida e será ignorada.")

    except FileNotFoundError:
        print("Erro: O arquivo 'dados.txt' não foi encontrado.")
        exit()

    if not dados_lidos:
        print("O arquivo 'dados.txt' foi lido, mas não contém dados válidos para ordenar.")
    else:
        dados_lidos.sort(key=lambda item: (item[1], -item[2]))

        print("\n--- Conteúdo da lista ---")

        for i, item in enumerate(dados_lidos):
            print(f"{i + 1}. {item[0]}, Prazo: {item[1]}, dificuldade: {item[2]}")

if inicio == '3':

    def listar_e_remover_linha(nome_arquivo):
        if not os.path.exists(nome_arquivo):
            print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
            return

        try:
            with open(nome_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()
        except IOError as e:
            print(f"Erro ao ler o arquivo: {e}")
            return

        if not linhas:
            print("O arquivo está vazio. Não há nada para remover.")
            return

        print("\nConteúdo atual do arquivo:")
        time.sleep(0.5)
        for i, linha in enumerate(linhas):
            print(f"{i + 1}: {linha.strip()}")

        while True:
            try:
                numero_para_remover = int(
                    input("\nDigite o número da linha que você quer remover (ou 0 para cancelar): "))
                if numero_para_remover == 0:
                    print("Operação cancelada.")
                    return
                if 1 <= numero_para_remover <= len(linhas):
                    break
                else:
                    print(f"Número inválido. Por favor, digite um número entre 1 e {len(linhas)}.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

        del linhas[numero_para_remover - 1]

        try:
            with open(nome_arquivo, 'w') as arquivo:
                arquivo.writelines(linhas)
            print(f"A linha {numero_para_remover} foi removida com sucesso!")
        except IOError as e:
            print(f"Erro ao escrever no arquivo: {e}")


    listar_e_remover_linha('dados.txt')


if inicio == '4':
    print('Ok, saindo...')
    time.sleep(1)
    exit()
