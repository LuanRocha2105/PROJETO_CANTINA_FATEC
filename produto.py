from datetime import datetime

class Produto:
    def __init__(self, nome, quantidade, preco_compra, preco_venda, data_compra, data_vencimento):
        self._nome = nome
        self._quantidade = quantidade
        self._preco_compra = preco_compra
        self._preco_venda = preco_venda
        self._data_compra = data_compra
        self._data_vencimento = data_vencimento
        self.proximo = None


    #def atualizar_quantidade():
    

    def esta_vencido(self):
        if datetime.now() > self._data_vencimento:
            return True
        return False

