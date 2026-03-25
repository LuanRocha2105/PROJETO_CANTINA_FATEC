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


    def set_quantidade(self, quantidade):
        self._quantidade = quantidade
    

    def esta_vencido(self):
        if datetime.now() > self._data_vencimento:
            return True
        return False

    def get_nome(self):
        return self._nome
    
    def get_validade(self):
        return self._data_vencimento
    
    def get_preco_venda(self):
        return self._preco_venda
    
    def get_preco_compra(self):
        return self._preco_compra
    
    def get_quantidade(self):
        return self._quantidade