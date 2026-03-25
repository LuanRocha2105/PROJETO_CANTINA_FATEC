from datetime import datetime
from Modelos.Pessoa import Pessoa
from Modelos.Pagamento import Pagamento
from Modelos.Produto import Produto

class Venda:
    def __init__(self, cliente: Pessoa, pagamento: Pagamento):
        self._cliente = cliente
        self._pagamento = pagamento
        self._data_venda = datetime.now()


    def adicionar_ao_carrinho(produto: Produto, quantidade: int):
        carrinho = {}
        carrinho[produto] = quantidade
        return carrinho
    
    def ver_carrinho(carrinho):
        print("Carrinho:")
        for produto, quantidade in carrinho.items():
            print(f"{produto.get_nome()} - Quantidade: {quantidade} - Preço Unitário: R${produto.get_preco_venda():.2f}")

    def calcular_total(carrinho):
        total = 0.0
        for produto, quantidade in carrinho.items():
            total += produto.get_preco_venda() * quantidade
        return total

    def finalizar_venda(carrinho):
        total = Venda.calcular_total(carrinho)
        print(f"Total da venda: R${total:.2f}")
        for produto, quantidade in carrinho.items():
            produto.set_quantidade(produto.get_quantidade() - quantidade)
        #adicionar pagamento ao relatorio de vendas
        
