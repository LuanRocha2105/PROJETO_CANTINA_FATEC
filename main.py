from Estruturas.FilaEstoque import FilaEstoque
from Modelos.Produto import Produto
from Modelos.Venda import Venda

estoque = FilaEstoque()

estoque.adicionar_produto(Produto("Coca-Cola", 10, 1.0, 1.5, "2024-01-01", "2024-12-31"))
estoque.adicionar_produto(Produto("Pepsi", 20, 0.8, 1.2, "2024-02-01", "2024-11-30"))
estoque.adicionar_produto(Produto("Coca-Cola", 10, 1.0, 1.5, "2025-01-01", "2025-12-31"))
estoque.adicionar_produto(Produto("Fanta", 15, 0.9, 1.3, "2024-03-01", "2024-10-31"))
estoque.adicionar_produto(Produto("Coca-Cola", 5, 1.0, 1.5, "2024-01-01", "2024-12-31"))
estoque.adicionar_produto(Produto("Pepsi", 10, 0.8, 1.2, "2024-02-01", "2024-11-30"))
estoque.adicionar_produto(Produto("Fanta", 5, 0.9, 1.3, "2024-03-01", "2025-10-31"))



def menu():
    print("1. Adicionar produto")
    print("2. Remover produto")
    print("3. Listar produtos")
    print("4. Realizar venda")
    print("5. Sair")
    escolha = input("Escolha uma opção: ")
    return escolha

def main():
    while True:
        escolha = menu()
        if escolha == "1":
            nome = input("Nome do produto: ")
            quantidade = int(input("Quantidade: "))
            preco_compra = float(input("Preço de compra: "))
            preco_venda = float(input("Preço de venda: "))
            data_compra = input("Data de compra (YYYY-MM-DD): ")
            data_vencimento = input("Data de vencimento (YYYY-MM-DD): ")
            produto = Produto(nome, quantidade, preco_compra, preco_venda, data_compra, data_vencimento)
            estoque.adicionar_produto(produto)
        elif escolha == "2":
            nome = input("Nome do produto a remover: ")
            if estoque.remover_produto(nome):
                print("Produto removido com sucesso.")
            else:
                print("Produto não encontrado.")
        elif escolha == "3":
            estoque.listar_produtos()
        elif escolha == "4":
            # Implementar lógica de venda
            print("Funcionalidade de venda ainda não implementada.")
            
        elif escolha == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")



main()