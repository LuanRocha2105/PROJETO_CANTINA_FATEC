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
    nome = listar_menu_produtos()
    if nome is None:
        return
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
            print("\n--- Produtos disponíveis ---")
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
            total_disponivel = sum(l.get_quantidade() for l in lotes)

            if total_disponivel < quantidade:
                print(f"Estoque insuficiente. Disponível: {total_disponivel}")
            else:
                restante = quantidade
                for lote in lotes:
                    if restante == 0:
                        break
                    retirar = min(restante, lote.get_quantidade())
                    venda.adicionar_ao_carrinho(lote, retirar)
                    restante -= retirar
                print("Produto adicionado ao carrinho.")

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
    confirmacao = input("Tem certeza que deseja limpar TODOS os dados? (s/n): ")
    if confirmacao.lower() == "s":
        estoque.limpar()
        pilha_pagamentos.limpar()
        salvar_dados(estoque, pilha_pagamentos)
        print("Todos os dados foram limpos.")
    else:
        print("Operação cancelada.")


def popular_sistema():
    while True:
        sub = submenu_popular()
        if sub == "1":
            qtd = int(input("Quantos produtos gerar? "))
            gerar_produtos(estoque, qtd)
        elif sub == "2":
            qtd = int(input("Quantas vendas gerar? "))
            gerar_vendas(estoque, pilha_pagamentos, qtd)
        elif sub == "3":
            break


def main():
    while True:
        escolha = menu()

        if escolha == "1":
            adicionar_ao_estoque()

        elif escolha == "2":
            nome = listar_menu_produtos()
            if nome and not estoque.remover_produto(nome):
                print("Produto não encontrado.")
            elif nome:
                print("Produto removido com sucesso.")

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
            salvar_dados(estoque, pilha_pagamentos)

        elif escolha == "7":
            limpar_dados()

        elif escolha == "8":
            salvar_dados(estoque, pilha_pagamentos)
            print("Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")


main()