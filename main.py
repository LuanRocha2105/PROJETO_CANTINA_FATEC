from Estruturas.FilaEstoque import FilaEstoque
from Estruturas.PilhaPagamentos import PilhaPagamentos
from Modelos.Produto import Produto
from Modelos.Venda import Venda
from Modelos.Pessoa import Pessoa
from Relatorios import Relatorios
from Dados import salvar_dados, carregar_dados, gerar_produtos, gerar_vendas, listar_menu_produtos, PRODUTOS_PRECOS
from datetime import datetime

import os

estoque, pilha_pagamentos = carregar_dados()

if estoque is None:
    estoque = FilaEstoque()
    pilha_pagamentos = PilhaPagamentos()


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    limpar_tela()
    print("\n===== CANTINA FATEC =====")
    print("1. Adicionar produto ao estoque")
    print("2. Remover produto do estoque")
    print("3. Realizar venda")
    print("4. Relatórios")
    print("5. Popular Sistema (Faker)")
    print("6. Salvar dados")
    print("7. Limpar todos os dados")
    print("8. Sair")
    return input("Escolha uma opção: ")
   

def submenu_venda():
    limpar_tela()
    print("\n--- Carrinho de Compras ---")
    print("1. Adicionar produto ao carrinho")
    print("2. Ver carrinho")
    print("3. Finalizar compra")
    print("4. Voltar ao menu principal")
    return input("Escolha uma opção: ")


def submenu_relatorios():
    limpar_tela()
    print("\n--- Relatórios ---")
    print("1. Relatório de vendas")
    print("2. Relatório de consumo")
    print("3. Relatório de estoque")
    print("4. Voltar")
    return input("Escolha uma opção: ")

def submenu_popular():
    limpar_tela()
    print("\n--- Popular Sistema ---")
    print("1. Popular estoque")
    print("2. Gerar vendas")
    print("3. Voltar")
    return input("Escolha uma opção: ")


def adicionar_ao_estoque():
    print("\n--- Adicionar Produto ao Estoque ---")
    nome = listar_menu_produtos()
    if nome is None:
        return
    limpar_tela()
    print(f"Produto selecionado: {nome}\n")
    quantidade = int(input("Quantidade: "))
    data_vencimento = datetime.strptime(input("Data de vencimento (YYYY-MM-DD): "), "%Y-%m-%d")
    preco_compra, preco_venda = PRODUTOS_PRECOS[nome]
    produto = Produto(nome, quantidade, preco_compra, preco_venda, datetime.now(), data_vencimento)
    estoque.adicionar_produto(produto)
    print("Produto adicionado ao estoque.")


def realizar_venda():
    cliente = Pessoa.criar_com_menu()
    if cliente is None:
        return
    venda = Venda(cliente)
    while True:
        sub = submenu_venda()

        if sub == "1":
            limpar_tela()
            nomes = estoque.listar_nomes_disponiveis()
            if not nomes:
                print("Nenhum produto disponível no estoque.")
                input("\nPressione Enter para continuar...")
                continue
            print("\nProdutos disponíveisAAA:\n")
            for i, nome in enumerate(nomes, 1):
                print(f"{i}. {nome}")
            escolha = input("Escolha o número do produto: ")
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(nomes)):
                print("Opção inválida.")
                input("\nPressione Enter para continuar...")
                continue
            nome = nomes[int(escolha) - 1]
            quantidade = int(input("Quantidade: "))

            lotes = estoque.buscar_lotes_disponiveis(nome)
            total_disponivel = 0
            for lote in lotes:
                reservado = venda._itens.get(lote, 0)
                total_disponivel += lote.get_quantidade() - reservado

            if total_disponivel < quantidade:
                limpar_tela()
                print(f"Estoque insuficiente. Disponível: {total_disponivel}")
                input("\nPressione Enter para continuar...")
            else:
                restante = quantidade
                for lote in lotes:
                    if restante == 0:
                        break
                    reservado = venda._itens.get(lote, 0)
                    disponivel_lote = lote.get_quantidade() - reservado
                    if disponivel_lote <= 0:
                        continue
                    retirar = min(restante, disponivel_lote)
                    venda.adicionar_ao_carrinho(lote, retirar)
                    restante -= retirar
                limpar_tela()
                print("Produto adicionado ao carrinho.")
                input("\nPressione Enter para continuar...")

        elif sub == "2":
            limpar_tela()
            if not venda._itens:
                print("Carrinho vazio.")
                input("\nPressione Enter para continuar...")
            else:
                venda.ver_carrinho()
                print(f"Total: R${venda.calcular_total():.2f}")
                input("\nPressione Enter para continuar...")

        elif sub == "3":
            limpar_tela()
            if venda.realizar_venda(pilha_pagamentos):
                salvar_dados(estoque, pilha_pagamentos)
            input("\nPressione Enter para continuar...")
            break

        elif sub == "4":
            break


def limpar_dados():
    limpar_tela()
    confirmacao = input("Tem certeza que deseja limpar TODOS os dados? (s/n): ")
    if confirmacao.lower() == "s":
        estoque.limpar()
        pilha_pagamentos.limpar()
        salvar_dados(estoque, pilha_pagamentos)
        limpar_tela()
        print("Todos os dados foram limpos.")
    else:
        limpar_tela()
        print("Operação cancelada.")


def popular_sistema():
    while True:
        sub = submenu_popular()
        if sub == "1":
            limpar_tela()
            qtd = int(input("Quantos produtos gerar? "))
            gerar_produtos(estoque, qtd)
            limpar_tela()
            input("\nProdutos gerados com sucesso! Pressione Enter para continuar...")
        elif sub == "2":
            limpar_tela()
            qtd = int(input("Quantas vendas gerar? "))
            gerar_vendas(estoque, pilha_pagamentos, qtd)
            input("\nVendas geradas com sucesso! Pressione Enter para continuar...")
        elif sub == "3":
            break


def main():
    while True:
        escolha = menu()

        if escolha == "1":
            limpar_tela()
            adicionar_ao_estoque()
            input("\nPressione Enter para continuar...")

        elif escolha == "2":
            limpar_tela()
            vencidos = []
            atual = estoque._inicio
            while atual is not None:
                if atual.esta_vencido():
                    vencidos.append(atual)
                atual = atual.proximo

            if not vencidos:
                limpar_tela()
                print("Nenhum produto vencido no estoque.")
                input("\nPressione Enter para continuar...")
            else:
                print("\n--- Produtos Vencidos ---")
                for i, lote in enumerate(vencidos, 1):
                    validade = lote.get_validade().strftime("%d/%m/%Y")
                    print(f"{i}. {lote.get_nome()} - Qtd: {lote.get_quantidade()} - Venceu em: {validade}")
                escolha_rem = input("Escolha o número do produto a remover: ")
                if escolha_rem.isdigit() and 1 <= int(escolha_rem) <= len(vencidos):
                    lote = vencidos[int(escolha_rem) - 1]
                    estoque.remover_produto(lote.get_nome())
                    limpar_tela()
                    print("Produto removido com sucesso.")
                    input("\nPressione Enter para continuar...")
                else:
                    limpar_tela()
                    print("Opção inválida.")
                    input("\nPressione Enter para continuar...")


        elif escolha == "3":
            limpar_tela()   
            realizar_venda()

        elif escolha == "4":
            while True:
                sub = submenu_relatorios()
                if sub == "1":
                    limpar_tela()
                    Relatorios.relatorio_vendas(pilha_pagamentos)
                    input("\nPressione Enter para continuar...") 
                elif sub == "2":
                    limpar_tela()
                    Relatorios.relatorio_consumo(pilha_pagamentos)
                    input("\nPressione Enter para continuar...") 
                elif sub == "3":
                    limpar_tela()
                    Relatorios.relatorio_estoque(estoque)
                    input("\nPressione Enter para continuar...") 
                elif sub == "4":
                    break

        elif escolha == "5":
            popular_sistema()

        elif escolha == "6":
            limpar_tela()
            salvar_dados(estoque, pilha_pagamentos)
            input("\nDados salvos com sucesso! Pressione Enter para continuar...")

        elif escolha == "7":
            limpar_dados()
            input("\nPressione Enter para continuar...")

        elif escolha == "8":
            salvar_dados(estoque, pilha_pagamentos)
            limpar_tela()
            print("Até logo!\n\n")
            break

        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")


main()