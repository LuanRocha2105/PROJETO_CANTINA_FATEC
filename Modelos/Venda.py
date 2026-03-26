from datetime import datetime
from Modelos.Pessoa import Pessoa
from Modelos.Produto import Produto

class Venda:
    def __init__(self, cliente: Pessoa):
        self._cliente = cliente
        self._data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._itens = {}

    def adicionar_ao_carrinho(self, produto: Produto, quantidade: int) -> None:
        if produto in self._itens:
            self._itens[produto] += quantidade
        else:
            self._itens[produto] = quantidade

    def remover_do_carrinho(self, produto: Produto):
        if produto in self._itens:
            del self._itens[produto]

    def ver_carrinho(self):
        print("\n--- Carrinho ---\n")
        for produto, quantidade in self._itens.items():
            print(f"{produto.get_nome()} - Quantidade: {quantidade} - Preço Unitário: R${produto.get_preco_venda():.2f}")

    def calcular_total(self):
        total = 0.0
        for produto, quantidade in self._itens.items():
            total += produto.get_preco_venda() * quantidade
        return total

    def realizar_venda(self, pilha_pagamentos):
        if not self._itens:
            print("\nCarrinho vazio. Adicione produtos antes de finalizar.\n")
            return False

        total = self.calcular_total()

        for produto, quantidade in self._itens.items():
            produto.set_quantidade(produto.get_quantidade() - quantidade)

       
        from Estruturas.PilhaPagamentos import Pagamento
        itens_dict = {produto.get_nome(): qtd for produto, qtd in self._itens.items()}
        nome, categoria, curso = self._cliente.get_info()
        pagamento = Pagamento(nome, categoria, curso, total, itens_dict)
        pilha_pagamentos.empilhar(pagamento)

        print(f"\nVenda realizada para {nome} no valor de R${total:.2f} em {self._data_venda}\n")
        return True
        
        
